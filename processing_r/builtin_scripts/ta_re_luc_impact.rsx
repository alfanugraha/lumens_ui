#Impact of Land Using to Regional Economy Indicator Analysis
##TA-PostgreSQL=group
##proj.file=string
##land_req=string
##projected_land_use=string
##statusoutput=output table

library(reshape2)
library(ggplot2)
library(raster)
library(foreign)
library(rtf)
library(DBI)
library(RPostgreSQL)
library(rpostgis)
library(magick)

time_start<-paste(eval(parse(text=(paste("Sys.time ()")))), sep="")

load(proj.file)
load(land_req)

# set driver connection
driver <- dbDriver('PostgreSQL')
project <- as.character(proj_descr[1,2])
DB <- dbConnect(
  driver, dbname=project, host=as.character(pgconf$host), port=as.character(pgconf$port),
  user=as.character(pgconf$user), password=as.character(pgconf$pass)
)

#=Set Working Directory
work_dir<-paste(dirname(proj.file), "/TA/LandUseScenario", idx_TA_regeco, sep="")
dir.create(work_dir, mode="0777")
setwd(work_dir)

#READ INPUT FILE
list_of_data_luc<-dbReadTable(DB, c("public", "list_of_data_luc"))

nodata_val<-0
land.requirement.db<-land.requirement_table
lc.list<-subset(landuse_lut, select=c(ID, Legend))

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

#Read land use map and calculate area of land use
next_data_luc<-list_of_data_luc[which(list_of_data_luc$RST_NAME==projected_land_use),]
# next_landuse<-getRasterFromPG(pgconf, project, next_data_luc$RST_DATA, paste(next_data_luc$RST_DATA, '.tif', sep=''))
next_landuse_lut<-dbReadTable(DB, c("public", next_data_luc$LUT_NAME))

# landuse_area0<-as.data.frame(levels(landuse0))
landuse_area<-subset(next_landuse_lut, ID != nodata_val)
landuse_area0<-subset(landuse_lut, ID != nodata_val)
# landuse_area<-subset(landuse_area,ID !=15)
landuse_area<-as.matrix(landuse_area$COUNT)
landuse_area0<-as.matrix(landuse_area0$COUNT)
landuse_table<-cbind(lc.list,landuse_area0, landuse_area)
landuse_area_diag<-diag(as.numeric(as.matrix(landuse_area)))
colnames(landuse_table)[1] <- "LAND_USE"
colnames(landuse_table)[2] <- "T1_HA"
colnames(landuse_table)[3] <- "T2_HA"
landuse_table<-edit(landuse_table)
landuse_table$CHANGE<-landuse_table$T2_HA-landuse_table$T1_HA

#MODEL FINAL DEMAND
land.distribution.scen<-land.distribution.prop %*% landuse_area_diag
land.requirement.scen<-rowSums(land.distribution.scen)
fin_dem.rtot<-rowSums(fin_dem)
int_con.rtot<-rowSums(int_con)
demand<-fin_dem.rtot+int_con.rtot
land.requirement.coeff<-land.requirement.db$LRC
land.productivity.coeff<-land.requirement.db$LPC
fin_dem.scen<-land.requirement.scen/land.productivity.coeff
fin_dem.scen[is.infinite(fin_dem.scen)]<-0
fin_dem.scen[is.na(fin_dem.scen)]<-0

#CALCULATE FINAL DEMAND AND GDP FROM SCENARIO OF LAND USE CHANGE
fin.output.scen<-Leontief %*% fin_dem.scen
fin.output.scen<-round(fin.output.scen, digits=1)
colnames(fin.output.scen)[1]<-"OUTPUT_Scen"
GDP.prop.from.output<-GDP.val/demand
GDP.prop.from.output[is.na(GDP.prop.from.output)]<-0
GDP.scen<-GDP.prop.from.output*fin.output.scen
GDP.scen<-round(GDP.scen, digits=1)
GDP.scen[is.na(GDP.scen)]<-0
colnames(GDP.scen)[1] <- "GDP_scen"
GDP.diff<-GDP.scen-GDP$GDP
GDP.diff<-round(GDP.diff, digits=1)
colnames(GDP.diff)[1] <- "GDP_diff"
GDP.rate<-GDP.diff/GDP.val
GDP.rate[is.na(GDP.rate)]<-0
GDP.rate<-round(GDP.rate, digits=2)
colnames(GDP.rate)[1] <- "GDP_rate"
GDP_summary<-cbind(GDP,GDP.scen,fin.output.scen,GDP.diff, GDP.rate)
GDP_summary$P_OUTPUT<-NULL
GDP_summary$P_GDP<-NULL

#calculate total GDP
GDP_tot_scen<-as.matrix(GDP_summary$GDP_scen)
GDP_tot_scen<-colSums(GDP_tot_scen)
GDP_tot_diff<-GDP_tot_scen-GDP_tot
GDP_tot_rate<-GDP_tot_diff/GDP_tot
text1<-"Total GDP"
text2<-"Scenario GDP"
text3<-"GDP difference"
text4<-"Rate of difference"
GDP_overall1<-rbind(text1,text2,text3,text4)
GDP_overall2<-rbind(GDP_tot, GDP_tot_scen,GDP_tot_diff,GDP_tot_rate)
GDP_overall<-cbind(GDP_overall1,GDP_overall2)

order_GDP_scen <- as.data.frame(GDP_summary[order(-GDP_summary$GDP_scen),])
order_GDP_scen10<-head(order_GDP_scen,n=20)
GDP_summary.melt <- melt(data = order_GDP_scen10, id.vars=c('SECTOR'), measure.vars=c('GDP','GDP_scen'))
GDP_graph<-ggplot(data=GDP_summary.melt, aes(x=SECTOR, y=value, fill=variable)) +
  geom_bar(colour="black", stat="identity", position="dodge")+
  guides(fill=FALSE) + xlab("Sectors") + ylab("GDP") +ggtitle("Comparison of GDP Baseline and Scenario")+ theme(axis.text.x  = element_text(angle=90, size=6))

LC_graph<-ggplot(data=landuse_table, aes(x=LAND_USE, y=CHANGE)) +
  geom_bar(colour="black", stat="identity", position="dodge")+
  guides(fill=FALSE) + xlab("Land use") + ylab("Change") +ggtitle("Land Use Change")+ theme(axis.text.x  = element_text(angle=90, size=6))

#CALCULATE TOTAL LABOUR
Labour_table<-Lab.multiplier
Labour_table$Lab.multiplier<-as.numeric(format(Labour_table$Lab.multiplier, digits=3, width=5))
Labour_table<-cbind(Labour_table,fin.output.scen)
Labour_table<-cbind(Labour_table,labour)
colnames(Labour_table)[1] <- "SECTOR"
colnames(Labour_table)[2] <- "CATEGORY"
colnames(Labour_table)[4] <- "OUT_scen"
colnames(Labour_table)[5] <- "Lab_base"
test<-Labour_table$Lab.multiplier*Labour_table$OUT_scen*1000000
test<-round(test, digits=0)
Labour_table$Lab_scen<-test
Labour_table$Lab_req<-Labour_table$Lab_scen-Labour_table$Lab_base
test2<-Labour_table$Lab_req
test2<-cbind(sector, test2)
LAB_graph<-ggplot(data=test2, aes(x=V1, y=test2, fill=V2)) +
  geom_bar(colour="black", stat="identity", position="dodge")+
  guides(fill=FALSE) + xlab("Sector") + ylab("Labour requirement") +ggtitle("Impact of LU Change to Labour")+ theme(axis.text.x  = element_text(angle=90, size=6))


#EXPORT OUTPUT
GDP_scen_file<-"GDP_scenario_summary.dbf"
write.dbf(GDP_summary, GDP_scen_file,  factor2char = TRUE, max_nchar = 254)
Labour_scen_file<-"LAB_scenario_summary.dbf"
write.dbf(Labour_table, Labour_scen_file,  factor2char = TRUE, max_nchar = 254)

#WRITE REPORT
title<-"\\b\\fs32 LUMENS-Trade-off Analysis (TA) Project Report\\b0\\fs20"
sub_title<-"\\b\\fs28 Sub-modules 2: Regional economic-Impact of land use change\\b0\\fs20"
test<-as.character(Sys.Date())
date<-paste("Date : ", test, sep="")
time_start<-paste("Processing started : ", time_start, sep="")
time_end<-paste("Processing ended : ", eval(parse(text=(paste("Sys.time ()")))), sep="")
line<-paste("------------------------------------------------------------------------------------------------------------------------------------------------")
chapter1<-"\\b\\fs24 Impact of land use change to GDP \\b0\\fs20"

# ==== Report 0. Cover=====
rtffile <- RTF("TA-Landuse_scenario_report.doc", font.size=11, width = 8.267, height = 11.692, omi = c(0,0,0,0))
# INPUT
file.copy(paste0(LUMENS_path, "/ta_cover.png"), work_dir, recursive = FALSE)
img_location<-paste0(work_dir, "/ta_cover.png")
# loading the .png image to be edited
cover <- image_read(img_location)
# to display, only requires to execute the variable name, e.g.: "> cover"
# adding text at the desired location
text_submodule <- paste("Sub-Modul Ekonomi Regional\n\nSimulasi PDRB dari Perubahan Penggunaan Lahan\n", location, ", ", "Tahun ", I_O_period, sep="")
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
addParagraph(rtffile, "\\b\\fs20 Table 1. Land use change\\b0\\fs20.")
addTable(rtffile,landuse_table,font.size=8)
addNewLine(rtffile)
addPlot(rtffile,plot.fun=print, width=6.7,height=4,res=300,LC_graph)
addNewLine(rtffile)
addParagraph(rtffile, "\\b\\fs20 Table 2. Impact of land use change to GDP\\b0\\fs20.")
addTable(rtffile,GDP_summary,font.size=6)
addNewLine(rtffile)
addPlot(rtffile,plot.fun=print, width=6.7,height=4,res=300,GDP_graph)
addNewLine(rtffile)
addParagraph(rtffile, "\\b\\fs20 Table 3. Impact of land use change to labour requirement\\b0\\fs20.")
addTable(rtffile,Labour_table,font.size=6)
addNewLine(rtffile)
addPlot(rtffile,plot.fun=print, width=6.7,height=4,res=300,LAB_graph)
done(rtffile)

unlink(img_location)
dbDisconnect(DB)

#=Writing final status message (code, message)
statuscode<-1
statusmessage<-"TA regional economy analysis successfully completed!"
statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)


