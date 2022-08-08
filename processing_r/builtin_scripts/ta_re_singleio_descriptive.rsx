#Regional Economy Single I-O Descriptive Analysis
##TA-PostgreSQL=group
##proj.file=string
##int_con_file=string
##add_val_file=string
##fin_dem_file=string
##add_val_struc_file=string
##fin_dem_struc_file=string
##sector_file=string
##labour_file=string
##unit=string
##location=string
##I_O_period= number 2000
##statusoutput=output table

library(reshape2)
library(ggplot2)
library(foreign)
library(rtf)
library(DBI)
library(RPostgreSQL)
library(rpostgis)
library(magick)

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

#=Set Working Directory
idx_TA_regeco<-idx_TA_regeco+1
working_dir<-paste(dirname(proj.file), "/TA/Descriptive_Analysis", idx_TA_regeco, sep="")
dir.create(working_dir, mode="0777")
setwd(working_dir)

#READ INPUT FILE
list_of_data_lut<-dbReadTable(DB, c("public", "list_of_data_lut"))
row_int_con <- list_of_data_lut[which(list_of_data_lut$TBL_NAME==int_con_file),]
row_add_val <- list_of_data_lut[which(list_of_data_lut$TBL_NAME==add_val_file),]
row_fin_dem <- list_of_data_lut[which(list_of_data_lut$TBL_NAME==fin_dem_file),]
row_fin_dem_struc <- list_of_data_lut[which(list_of_data_lut$TBL_NAME==fin_dem_struc_file),]
row_add_val_struc <- list_of_data_lut[which(list_of_data_lut$TBL_NAME==add_val_struc_file),]
row_sector <- list_of_data_lut[which(list_of_data_lut$TBL_NAME==sector_file),]
row_labour <- list_of_data_lut[which(list_of_data_lut$TBL_NAME==labour_file),]

int_con <- list_of_data_lut<-dbReadTable(DB, c("public", row_int_con$TBL_DATA))
add_val <- list_of_data_lut<-dbReadTable(DB, c("public", row_add_val$TBL_DATA))
fin_dem <- list_of_data_lut<-dbReadTable(DB, c("public", row_fin_dem$TBL_DATA))
fin_dem_struc <- list_of_data_lut<-dbReadTable(DB, c("public", row_fin_dem_struc$TBL_DATA))
add_val_struc <- list_of_data_lut<-dbReadTable(DB, c("public", row_add_val_struc$TBL_DATA))
sector <- list_of_data_lut<-dbReadTable(DB, c("public", row_sector$TBL_DATA))
labour <- list_of_data_lut<-dbReadTable(DB, c("public", row_labour$TBL_DATA))

int_con.m<-as.matrix(int_con)
add_val.m<-as.matrix(add_val)
dim<-ncol(int_con.m)

#CALCULATE INVERS LEONTIEF
int_con.ctot<-colSums(int_con.m)
add_val.ctot<-colSums(add_val.m)
fin_con<- 1/(int_con.ctot+add_val.ctot)
fin_con[is.infinite(fin_con)]<-0
t.input.invers<-diag(fin_con)
A<-int_con.m %*% t.input.invers
I<-as.matrix(diag(dim))
I_A<-I-A
Leontief<-solve(I_A)

#DIRECT BACKWARD LINKAGES
DBL<-colSums(Leontief)
DBL<-DBL/(mean(DBL))
DBL<-cbind(sector,DBL)
colnames(DBL)[3] <- "DBL"
order_DBL <- as.data.frame(DBL[order(-DBL$DBL),])
order_DBL10<-head(order_DBL,n=20)
colnames(order_DBL10)[1] <- "SECTOR"
colnames(order_DBL10)[2] <- "CATEGORY"
BPD_graph<-ggplot(data=order_DBL10, aes(x=SECTOR, y=DBL, fill=CATEGORY)) + 
  geom_bar(colour="black", stat="identity")+ coord_flip() +  
  guides(fill=FALSE) + xlab("Sectors") + ylab("Value") 

#DIRECT FORWARD LINKAGES
DFL<-rowSums(Leontief)
DFL<-DFL/(mean(DFL))
DFL<-cbind(sector,DFL)
colnames(DFL)[3] <- "DFL"
order_DFL <- as.data.frame(DFL[order(-DFL$DFL),])
order_DFL10<-head(order_DFL,n=20)
colnames(order_DFL10)[1] <- "SECTOR"
colnames(order_DFL10)[2] <- "CATEGORY"
FPD_graph<-ggplot(data=order_DFL10, aes(x=SECTOR, y=DFL, fill=CATEGORY)) + 
  geom_bar(colour="black", stat="identity")+ coord_flip() +  
  guides(fill=FALSE) + xlab("Sectors") + ylab("Value") 


#CREATE LINKAGES TABLE
DBL_temp<-colSums(Leontief)
BPD_temp<-DBL_temp/(mean(as.matrix(DBL_temp)))
DFL_temp<-rowSums(Leontief)
FPD_temp<-DFL_temp/(mean(as.matrix(DFL_temp)))
DBL_temp<-as.data.frame(round(DBL_temp, digits=2))
BPD_temp<-as.data.frame(round(BPD_temp, digits=2))
DFL_temp<-as.data.frame(round(DFL_temp, digits=2))
FPD_temp<-as.data.frame(round(FPD_temp, digits=2))
Linkages_table<-cbind(sector,DBL_temp,DFL_temp,BPD_temp,FPD_temp)
colnames(Linkages_table)[1] <- "SECTOR"
colnames(Linkages_table)[2] <- "CATEGORY"
colnames(Linkages_table)[3] <- "DBL"
colnames(Linkages_table)[4] <- "DFL"
colnames(Linkages_table)[5] <- "BPD"
colnames(Linkages_table)[6] <- "FPD"
PRS_graph<-ggplot(Linkages_table, aes(x=BPD, y=FPD, color=CATEGORY)) + geom_point(shape=19, size=5) + geom_hline(aes(yintercept=1), colour="#BB0000", linetype="dashed") + geom_vline(aes(xintercept=1), colour="#BB0000", linetype="dashed")


#SELECTION OF PRIMARY SECTOR
P.sector<-cbind(DBL,DFL)
colnames (P.sector) [1]<-"Sectors"
P.sector[4]<-NULL
P.sector[4]<-NULL
P.sector.selected <- P.sector[ which(P.sector$DBL >= 1),]
P.sector.selected <- P.sector.selected[ which(P.sector.selected$DFL >= 1),]
colnames(P.sector.selected)[1] <- "SECTOR"
colnames(P.sector.selected)[2] <- "CATEGORY"


#GDP
GDP.val<-as.data.frame(add_val.m[2,]+add_val.m[3,])
GDP.val.m<-as.matrix(GDP.val)
GDP.val.m<-as.numeric(GDP.val.m)
OUTPUT.val<-as.data.frame(add_val.m[2,]+add_val.m[3,]+add_val.m[1,]+int_con.ctot)
OUTPUT.val.m<-as.matrix(OUTPUT.val)
OUTPUT.val.m<-as.numeric(OUTPUT.val.m)
GDP<-cbind(sector,GDP.val,OUTPUT.val)
colnames(GDP)[1] <- "SECTOR"
colnames(GDP)[2] <- "CATEGORY"
colnames(GDP)[3] <- "GDP"
colnames(GDP)[4] <- "OUTPUT"
GDP$GDP_PROP<-GDP$GDP/GDP$OUTPUT
GDP[is.na(GDP)]<-0
colnames(GDP)[5] <- "P_OUTPUT"
GDP_tot<-as.matrix(GDP$GDP)
GDP_tot<-colSums(GDP_tot)
GDP$P_GDP<-round((GDP$GDP/GDP_tot), digits=2)
order_GDP <- as.data.frame(GDP[order(-GDP$GDP),])
order_GDP10<-head(order_GDP,n=20)
GDP_graph<-ggplot(data=order_GDP10, aes(x=SECTOR, y=GDP, fill=SECTOR)) + 
  geom_bar(colour="black", stat="identity")+ coord_flip() +  
  guides(fill=FALSE) + xlab("Sectors") + ylab("GDP") 
GDP$GDP<-round(GDP$GDP, digits=1)
GDP$OUTPUT<-round(GDP$OUTPUT, digits=1)
GDP$P_OUTPUT<-round(GDP$P_OUTPUT, digits=2)
GDP$P_GDP<-round(GDP$P_GDP, digits=2)


#OUTPUT MULTIPLIER 
Out.multiplier<-colSums(Leontief)
Out.multiplier<-cbind(sector,Out.multiplier)
order_Out.multiplier <- as.data.frame(Out.multiplier[order(-Out.multiplier$Out.multiplier),])
order_Out.multiplier <-head(order_Out.multiplier,n=20)
OMPL_graph<-ggplot(data=order_Out.multiplier, aes(x=V1, y=Out.multiplier, fill=V2)) + 
  geom_bar(colour="black", stat="identity")+ coord_flip() +  
  guides(fill=FALSE) + xlab("Sectors") + ylab("Output multiplier")

#INCOME MULTIPLIER
V.income<-as.matrix(GDP.val*fin_con)
Inc.multiplier<-Leontief%*%V.income
multiplier<-cbind(Out.multiplier,Inc.multiplier)
Inc.multiplier<-cbind(sector,Inc.multiplier)
colnames(Inc.multiplier)[3]<-"Inc.multiplier"
order_Inc.multiplier <- as.data.frame(Inc.multiplier[order(-Inc.multiplier$Inc.multiplier),])
order_Inc.multiplier <-head(order_Inc.multiplier,n=20)
IMPL_graph<-ggplot(data=order_Inc.multiplier, aes(x=V1, y=Inc.multiplier, fill=V2)) + 
  geom_bar(colour="black", stat="identity")+ coord_flip() +  
  guides(fill=FALSE) + xlab("Sectors") + ylab("Income multiplier") 

#LABOUR MULTIPLIER
labour.m<-as.matrix(labour*fin_con)
labour.m<-labour.m/1000000
Lab.multiplier<-Leontief%*%labour.m
multiplier<-cbind(multiplier,Lab.multiplier)
colnames(multiplier)[1] <- "SECTOR"
colnames(multiplier)[2] <- "CATEGORY"
colnames(multiplier)[5] <- "Lab.multiplier"
multiplier$Out.multiplier<-round(multiplier$Out.multiplier, digits=3)
Lab.multiplier<-cbind(sector,Lab.multiplier)
colnames(Lab.multiplier)[3]<-"Lab.multiplier"
order_Lab.multiplier <- as.data.frame(Lab.multiplier[order(-Lab.multiplier$Lab.multiplier),])
order_Lab.multiplier <-head(order_Lab.multiplier,n=20)
LMPL_graph<-ggplot(data=order_Lab.multiplier, aes(x=V1, y=Lab.multiplier, fill=V2)) + 
  geom_bar(colour="black", stat="identity")+ coord_flip() +  
  guides(fill=FALSE) + xlab("Sectors") + ylab("Labour multiplier")
colnames(multiplier)[4]<-"Inc.multiplier"
multiplier$Inc.multiplier<-round(multiplier$Inc.multiplier, digits=3)


#COMBINE MULTIPLIER
sel.multiplier<-multiplier[ which(multiplier$Out.multiplier > 1),]
sel.multiplier<-sel.multiplier[ which(sel.multiplier$Inc.multiplier > 1),]


#EXPORT OUTPUT
Leontief_df<-as.data.frame(Leontief)
Leontief_matrix<-"Leontief_matrix.dbf"
# write.dbf(Leontief_df, Leontief_matrix, factor2char = TRUE, max_nchar = 254)
Linkages<-"Sectoral_linkages.dbf"
# write.dbf(Linkages_table, Linkages, factor2char = TRUE, max_nchar = 254)
PDRB<-"Sectoral_GDP"
# write.dbf(GDP, PDRB,factor2char = TRUE, max_nchar = 254)
PENGGANDA<-"Sectoral_multiplier"
# write.dbf(multiplier, PENGGANDA,factor2char = TRUE, max_nchar = 254)

#WRITE REPORT
title<-"\\b\\fs32 LUMENS-Trade-off Analysis (TA) Project Report\\b0\\fs20"
sub_title<-"\\b\\fs28 Sub-modules 2: Regional economic-Descriptive analysis (Single I-O)\\b0\\fs20"
test<-as.character(Sys.Date())
date<-paste("Date : ", test, sep="")
time_start<-paste("Processing started : ", time_start, sep="")
time_end<-paste("Processing ended : ", eval(parse(text=(paste("Sys.time ()")))), sep="")
line<-paste("------------------------------------------------------------------------------------------------------------------------------------------------")
chapter1<-"\\b\\fs24 1.Analysis of Sectoral Linkages \\b0\\fs20"
chapter2<-"\\b\\fs24 2.Analysis of GDP \\b0\\fs20"
chapter2_1<-"\\b\\i\\fs20 Total GDP \\b0\\i0\\fs20"
chapter3<-"\\b\\fs24 2.Analysis of multiplier \\b0\\fs20"

# ==== Report 0. Cover=====
rtffile <- RTF("TA-Descriptive_analysis_report.doc", font.size=11, width = 8.267, height = 11.692, omi = c(0,0,0,0))
# INPUT
file.copy(paste0(LUMENS_path, "/ta_cover.png"), working_dir, recursive = FALSE)
img_location<-paste0(working_dir, "/ta_cover.png")
# loading the .png image to be edited
cover <- image_read(img_location)
# to display, only requires to execute the variable name, e.g.: "> cover"
# adding text at the desired location
text_submodule <- paste("Sub-Modul Ekonomi Regional\n\nAnalisis Deskriptif Sektor Ekonomi\n", location, ", ", "Tahun ", I_O_period, sep="")
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
addParagraph(rtffile, date)
addParagraph(rtffile, time_start)
addParagraph(rtffile, time_end)
addParagraph(rtffile, line)
addNewLine(rtffile)
addParagraph(rtffile, chapter1)
addNewLine(rtffile)
addParagraph(rtffile, "\\b\\fs20 Table 1. Sectoral linkages\\b0\\fs20.")
addTable(rtffile,Linkages_table,font.size=8)
addNewLine(rtffile)
addPlot(rtffile,plot.fun=print, width=5,height=3,res=300,BPD_graph)
addParagraph(rtffile, "\\b\\fs20 Figure 1. Ten sectors with highest Backward power of dispersion\\b0\\fs20.")
addNewLine(rtffile)
addPlot(rtffile,plot.fun=print, width=5,height=3,res=300,FPD_graph)
addParagraph(rtffile, "\\b\\fs20 Figure 2. Ten sectors with highest Forward power of dispersion\\b0\\fs20.")
addNewLine(rtffile)
addPlot(rtffile,plot.fun=print, width=6,height=4,res=300,PRS_graph)
addParagraph(rtffile, "\\b\\fs20 Figure 3. Sectoral typology based on linkages analysis\\b0\\fs20.")
addNewLine(rtffile)
addParagraph(rtffile, "\\b\\fs20 Table 2. Primary sectors based on potential linkage\\b0\\fs20.")
addTable(rtffile,P.sector.selected,font.size=8)
addNewLine(rtffile)
addPageBreak(rtffile)
addParagraph(rtffile, chapter2)
addNewLine(rtffile)
addParagraph(rtffile, chapter2_1)
addParagraph(rtffile, GDP_tot)
addNewLine(rtffile)
addParagraph(rtffile, "\\b\\fs20 Table 3. Sectoral GDP\\b0\\fs20.")
addTable(rtffile,GDP,font.size=8)
addNewLine(rtffile)
addPlot(rtffile,plot.fun=print, width=5,height=3,res=300,GDP_graph)
addParagraph(rtffile, "\\b\\fs20 Figure 4. Twenty sectors with highest GDP\\b0\\fs20.")
addPageBreak(rtffile)
addParagraph(rtffile, chapter3)
addNewLine(rtffile)
addParagraph(rtffile, "\\b\\fs20 Table 4. Sectoral multiplier\\b0\\fs20.")
addTable(rtffile,multiplier,font.size=8)
addNewLine(rtffile)
addPlot(rtffile,plot.fun=print, width=5,height=3,res=300,OMPL_graph)
addParagraph(rtffile, "\\b\\fs20 Figure 5. Twenty sectors with highest Output multiplier\\b0\\fs20.")
addNewLine(rtffile)
addPlot(rtffile,plot.fun=print, width=5,height=3,res=300,IMPL_graph)
addParagraph(rtffile, "\\b\\fs20 Figure 6. Twenty sectors with highest Income multiplier\\b0\\fs20.")
addNewLine(rtffile)
addPlot(rtffile,plot.fun=print, width=5,height=3,res=300,LMPL_graph)
addParagraph(rtffile, "\\b\\fs20 Figure 5. Twenty sectors with highest Labour multiplier\\b0\\fs20.")
done(rtffile)

#=Save all params into .ldbase objects
save(int_con,
     add_val,
     fin_dem,
     fin_dem_struc,
     add_val_struc,
     sector,
     labour,
     unit,
     location,
     I_O_period,
     Leontief_df,
     GDP,
     Linkages_table,
     multiplier,
     file=paste0('Descriptive', I_O_period, '.ldbase'))
resave(idx_TA_regeco, file=proj.file)

unlink(img_location)
dbDisconnect(DB)

#=Writing final status message (code, message)
statuscode<-1
statusmessage<-"TA regional economy analysis successfully completed!"
statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)
