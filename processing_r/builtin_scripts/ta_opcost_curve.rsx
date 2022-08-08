ta##TA-PostgreSQL=group
##proj.file=string
##NPV=file
##ques_c_db=string
##cost_threshold=number 2
##statusoutput=output table

# library(pander)
# library(knitr)
# library(markdown)
library(rasterVis)
library(reshape2)
library(plyr)
library(lattice)
library(latticeExtra)
library(RColorBrewer)
library(hexbin)
library(grid)
library(ggplot2)
library(foreign)
library(scales)
library(DBI)



time_start<-paste(eval(parse(text=(paste("Sys.time ()")))), sep="")

#=Load active project
load(proj.file)

# set driver connection
driver <- dbDriver('PostgreSQL')
project <- as.character(proj_descr[1,2])
DB <- dbConnect(
  driver, dbname=project, host=as.character(pgconf$host), port=as.character(pgconf$port),
  user=as.character(pgconf$user), password=as.character(pgconf$pass)
)

list_of_data_lut<-dbReadTable(DB, c("public", "list_of_data_lut"))
# return the selected data from the list
data_lut<-list_of_data_lut[which(list_of_data_lut$TBL_NAME==ques_c_db),]
data_npv<-list_of_data_lut[which(list_of_data_lut$TBL_NAME==NPV),]

quesc_db<-as.character(data_lut[1,2])
n_dta<-nchar(as.character(factor(data_lut[1,2])))
T1<-as.integer(substr(data_lut[1,2], (n_dta-7):(n_dta-4), (n_dta-4)))
T2<-as.integer(substr(data_lut[1,2], (n_dta-3):n_dta, n_dta))
pu_name<-substr(as.character(factor(data_lut[1,2])), 16:(n_dta-8), (n_dta-8))

#====CREATE FOLDER AND WORKING DIRECTORY====
idx_TA_opcost=idx_TA_opcost+1
wd<-paste(dirname(proj.file), "/TA/", idx_TA_opcost, "_OpCostCurve_", T1, "_", T2, "_", pu_name, sep="")
dir.create(wd)
setwd(wd)

# load datasets
data<-dbReadTable(DB, c("public", data_lut$TBL_DATA))
lookup_npv<-dbReadTable(DB, c("public", data_npv$TBL_DATA))
t1=T1
t2=T2
period<-t2-t1
#iteration=5

#prepare NPV look up table
lookup_n<-lookup_npv
lookup_n[,2]<-NULL
colnames(lookup_n)[1] ="ID_LC1"
colnames(lookup_n)[2] ="NPV1"
data<-merge(data,lookup_n,by="ID_LC1")
colnames(lookup_n)[1] ="ID_LC2"
colnames(lookup_n)[2] ="NPV2"
data<-merge(data,lookup_n,by="ID_LC2")
tot_area<-sum(data$COUNT)

#Select data where emission happened and count>0
data_em_sel <- data[ which(data$ck_em == "TRUE"),]
data_em_sel <- data_em_sel[ which(data_em_sel$em > 0),]
data_em_sel<-within(data_em_sel, {
  em_rate<-((CARBON_t1-CARBON_t2)*(COUNT*3.67))/(tot_area*period)
  em_tot<- (CARBON_t1-CARBON_t2)*3.67
  sq_rate<-((CARBON_t2-CARBON_t1)*(COUNT*3.67))/(tot_area*period)
  sq_tot<- (CARBON_t2-CARBON_t1)*3.67
  opcost<-(NPV1-NPV2)/em_tot
  opcost_sq<-(NPV1-NPV2)/sq_tot
  cumsum_em<-cumsum(em_rate)
  cumsum_sq<-cumsum(sq_rate)
})

#Build opcost table
lcc_col<-as.data.frame(data_em_sel$LU_CHG)
zone_col<-as.data.frame(data_em_sel$Z_NAME)
opcost_col<-as.data.frame(data_em_sel$opcost)
em_col<-as.data.frame(data_em_sel$em_rate)
opcost_tab<-cbind(lcc_col,zone_col)
opcost_tab<-cbind(opcost_tab,opcost_col)
opcost_tab<-cbind(opcost_tab,em_col)
names(opcost_tab)[1] <- "luchg"
names(opcost_tab)[2] <- "zone"
names(opcost_tab)[3] <- "opcost"
names(opcost_tab)[4] <- "emrate"

#BUILD POSITIVE OPCOST TABLE
opcost_tab_p<- opcost_tab[ which(opcost_tab$opcost >= 0),]
opcost_tab_p<- opcost_tab_p[order(opcost_tab_p$opcost),]
opcost_tab_p$cum_emrate<-cumsum(opcost_tab_p$emrate)
TA_opcost_database<-opcost_tab_p
write.dbf(TA_opcost_database,"TA_opcost_database.dbf")
opcost_tab_p$opcost_log<-log10(opcost_tab_p$opcost)
is.na(opcost_tab_p) <- sapply(opcost_tab_p, is.infinite)
opcost_tab_p[is.na(opcost_tab_p)] <- 0

#BUILD NEGATIVE OPCOST TABLE
opcost_tab_n<- opcost_tab[ which(opcost_tab$opcost < 0),]
opcost_tab_n<- opcost_tab_n[order(opcost_tab_n$opcost),]
opcost_tab_n$cum_emrate<-cumsum(opcost_tab_n$emrate)
opcost_tab_n$opcost_log<-opcost_tab_n$opcost*-1
opcost_tab_n$opcost_log<-log10(opcost_tab_n$opcost_log)*-1

#-----MODIFIED UP TO THIS LINE------------------------------------------

#COMBINE POS && NEG OPCOST
opcost_all<-rbind(opcost_tab_n, opcost_tab_p)

#opcost_tab_p$cum_emrate2<-as.factor(opcost_tab_p$cum_emrate)
#opcost_tab_n$cum_emrate2<-as.factor(opcost_tab_n$cum_emrate)
opcost_all$cum_emrate2<-as.factor(opcost_all$cum_emrate)

#find cost threshold
opcost_all2<- opcost_all
opcost_all2$order<-c(1:nrow(opcost_all2))
find_x_val<-subset(opcost_all2, opcost_log>=log10(cost_threshold))
x_val<-find_x_val$order[1]

#opcost_all
#x<-qplot(x=cum_emrate2, y=opcost_log, fill=zone,data=opcost_all, geom="bar", xlab="Emission Per-Ha Area (ton CO2-eq/ha.year)", ylab="Opportunity Cost ($/ton CO2-eq)" )
#x<-x+geom_hline(aes(yintercept=cost_threshold), linetype="dashed")
#x<-x+geom_vline(aes(xintercept=x_val))
#x<-x+theme(axis.text.x = element_text(angle=90, hjust=1, vjust=0))
#x<-x+scale_y_continuous(breaks=c(-5,-4,-3,-2,-1,0,1,2,3,4,5))

#emission
#x<-qplot(x=cum_emrate2, y=opcost_log, fill=zone, data=opcost_tab_p, geom="bar", xlab="Emission Per-Ha Area (ton CO2-eq/ha.year)", ylab="Opportunity Cost ($/ton CO2-eq)")
#x<-x+theme(axis.text.x = element_text(angle=90, hjust=1, vjust=0))

#sequestration
#y<-qplot(x=cum_emrate2, y=opcost_log, fill=zone, data=opcost_tab_n, geom="bar", xlab="Emission Per-Ha Area (ton CO2-eq/ha.year)", ylab="Opportunity Cost ($/ton CO2-eq)" )
#y<-y+theme(axis.text.x = element_text(angle=90, hjust=1, vjust=0))


#WRITE REPORT
title<-"\\b\\fs32 LUMENS-Trade-off Analysis (TA) Project Report\\b0\\fs20"
sub_title<-"\\b\\fs28 Sub modul 1: Opportunity Cost Curve \\b0\\fs20"
line<-paste("------------------------------------------------------------------------------------------------------------------------------------------------")
chapter1<-"\\b\\fs24 1.Opportunity curve \\b0\\fs20"
rtffile <- RTF("TA-Opportunity_cost_curve_report.doc", font.size=11, width = 8.267, height = 11.692, omi = c(0,0,0,0))
img_location <- paste0(LUMENS_path, "/ta_cover.png")
# loading the .png image to be edited
cover <- image_read(img_location)
# to display, only requires to execute the variable name, e.g.: "> cover"
# adding text at the desired location
text_submodule <- paste("Sub-Modul TA\n\n", location, ", ", "Periode ", T1, "-", T2, sep="")
cover_image <- image_annotate(cover, text_submodule, size = 23, gravity = "southwest", color = "white", location = "+46+220", font = "Arial")
cover_image <- image_write(cover_image)
# 'gravity' defines the 'baseline' anchor of annotation. "southwest" defines the text shoul be anchored on bottom left of the image
# 'location' defines the relative location of the text to the anchor defined in 'gravity'
# configure font type
addPng(rtffile, cover_image, width = 8.267, height = 11.692)
addPageBreak(rtffile, width = 8.267, height = 11.692, omi = c(1,1,1,1))

addParagraph(rtffile, title)
addParagraph(rtffile, sub_title)
addNewLine(rtffile)
addParagraph(rtffile, line)
addNewLine(rtffile)
addParagraph(rtffile, chapter1)
addNewLine(rtffile)

addPlot(rtffile, plot.fun=print, width=6, height=5, res=300, 
        barplot(opcost_all$opcost_log, axes=F, xlab='Emission Per-Ha Area (ton CO2-eq/ha.year)', ylab='Opportunity Cost ($/ton CO2-eq)', col=rainbow(20), space=0.01)+
        box()+
        axis(1)+
        axis(2,at=log10(c(-10000, -1000, -100, -10, -1, -0.1, -0.01, -0.001, -0.0001, 0.0001, 0.001, 0.01, 0.1, 1, cost_threshold, 10, 100, 1000, 10000)),
             label=c(-10000, -1000, -100, -10, -1, -0.1, -0.01, -0.001, -0.0001, 0.0001, 0.001, 0.01, 0.1, 1, cost_threshold, 10, 100, 1000, 10000))+
        abline(h=log10(1), col='black')+
        abline(h=log10(cost_threshold), lty=3)+abline(v=x_val+4)
)
addParagraph(rtffile, "\\b\\fs20 Figure 1. Opportunity cost curve t1\\b0\\fs20.")
addNewLine(rtffile)

done(rtffile)

resave(idx_TA_opcost, file=proj.file)

dbDisconnect(DB)

#=Writing final status message (code, message)
statuscode<-1
statusmessage<-"SCIENDO period projection successfully completed!"
statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)

#-----------------------------------------------------------------------

# reports<-paste("
# Land Use Planning for Multiple Environmental Services
# ========================================================
# ***
# 
# # Lembar hasil analisis TA-Opportunity Cost:
# # Perhitungan opportunity cost berdasarkan data profitabilitas
# 
# ***
# 
# # Opportunity cost oleh masing-masing unit perencanaan
# ```{r fig.width=12, fig.height=10, echo=FALSE}
# barplot(opcost_all$opcost_log, axes=F, xlab='Emission Per-Ha Area (ton CO2-eq/ha.year)', ylab='Opportunity Cost ($/ton CO2-eq)', col=rainbow(20), space=0.01)
# box()
# axis(1)
# axis(2,at=log10(c(-10000, -1000, -100, -10, -1, -0.1, -0.01, -0.001, -0.0001, 0.0001, 0.001, 0.01, 0.1, 1, cost_threshold, 10, 100, 1000, 10000)),
# label=c(-10000, -1000, -100, -10, -1, -0.1, -0.01, -0.001, -0.0001, 0.0001, 0.001, 0.01, 0.1, 1, cost_threshold, 10, 100, 1000, 10000))
# abline(h=log10(1), col='black')
# abline(h=log10(cost_threshold), lty=3)
# abline(v=x_val+4)
# ```
# ***
# # Intisari opportunity cost
# ```{r fig.width=10, fig.height=9, echo=FALSE}
# pandoc.table(TA_opcost_database)
# 
# ```
# ***
# ")


#WRITE REPORT
# write(reports,file="reporthtml.Rmd")
# knit2html("reporthtml.Rmd", options=c("use_xhml"))
