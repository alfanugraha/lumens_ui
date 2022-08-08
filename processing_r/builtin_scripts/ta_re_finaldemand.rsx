#Regional Economy Final Demand Change Multiplier Analysis
##TA-PostgreSQL=group
##proj.file=string
##land_req=string
##fin_demand_scenario_file=string
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
work_dir<-paste(dirname(proj.file), "/TA/FinalDemandScenario", idx_TA_regeco, sep="")
dir.create(work_dir, mode="0777")
setwd(work_dir)

#READ INPUT FILE
list_of_data_lut<-dbReadTable(DB, c("public", "list_of_data_lut"))
row_fin_demand <- list_of_data_lut[which(list_of_data_lut$TBL_NAME==fin_demand_scenario_file),]
fin_demand_scenario<- list_of_data_lut<-dbReadTable(DB, c("public", row_fin_demand$TBL_DATA))
land.requirement.db<-land.requirement_table
lc.list<-subset(landuse_lut, select=c(ID, Legend))

int_con.m<-as.matrix(int_con)
add_val.m<-as.matrix(add_val)
dim<-ncol(int_con.m)

#CALCULATE INVERS LEONTIEF
int_con.ctot<-colSums(int_con.m)
add_val.ctot<-colSums(add_val.m)
fin_con<- 1/(int_con.ctot+add_val.ctot)
t.input.invers<-diag(fin_con)
A<-int_con.m %*% t.input.invers
I<-as.matrix(diag(dim))
I_A<-I-A
Leontief<-solve(I_A)

#GDP
GDP.val<-as.data.frame(add_val.m[2,]+add_val.m[3,])
GDP.val.m<-as.matrix(GDP.val)
GDP.val.m<-as.numeric(GDP.val.m)
OUTPUT.val<-as.data.frame(add_val.m[2,]+add_val.m[3,]+add_val.m[1,]+int_con.ctot)
OUTPUT.val.m<-as.matrix(OUTPUT.val)
OUTPUT.val.m<-as.numeric(OUTPUT.val.m)
GDP<-cbind(sector,GDP.val,OUTPUT.val)
colnames(GDP)[1] <- "SECTOR"
colnames(GDP)[2] <- "SECTOR CLASS"
colnames(GDP)[3] <- "GDP"
colnames(GDP)[4] <- "OUTPUT"
GDP$GDP_PROP<-GDP$GDP/GDP$OUTPUT
order_GDP <- as.data.frame(GDP[order(-GDP$GDP),])
order_GDP10<-head(order_GDP,n=20)
GDP_tot<-as.matrix(GDP$GDP)
GDP_tot<-colSums(GDP_tot)

#MODEL FINAL DEMAND
fin_dem.rtot<-rowSums(fin_dem)
int_con.rtot<-rowSums(int_con)
demand<-fin_dem.rtot+int_con.rtot
land.requirement.coeff<-land.requirement.db$LRC
land.productivity.coeff<-land.requirement.db$LPC
# land.distribution.prop<-as.matrix(land.distribution)
land.distribution.prop.r<-t(land.distribution.prop)

#CALCULATE LAND USE REQUIREMENT FROM CHANGE IN FINAL DEMAND SCENARIO

#base on absolute number in financial unit
temp_output0<-as.matrix(fin_demand_scenario)
temp_output0<-as.numeric(temp_output0)
temp_output0<-Leontief %*% temp_output0
temp_output<-cbind(OUTPUT.val,temp_output0)
colnames(temp_output)[1] <- "OUTPUT"
colnames(temp_output)[2] <- "SCEN_OUTPUT"
temp_output$delt_output<-temp_output$SCEN_OUTPUT-temp_output$OUTPUT
delt_output<-as.numeric(as.matrix(temp_output$delt_output))
R_C<-land.distribution.prop.r %*% diag(land.requirement.coeff)
delta_L<-R_C  %*% delt_output
delta_L2<-round(delta_L, digits=3)
delta_L2<-cbind(lc.list,delta_L2)

#PRODUCE OUTPUT
GDP_base<-GDP$GDP
GDP_table<-cbind(sector, temp_output$OUTPUT, temp_output$SCEN_OUTPUT, GDP_base)
colnames(GDP_table)[1] <- "SECTOR"
colnames(GDP_table)[2] <- "CATEGORY"
colnames(GDP_table)[3] <- "OUT_base"
colnames(GDP_table)[4] <- "OUT_scen"
GDP_table$GDP_scen<-(GDP_table$GDP_base/GDP_table$OUT_base)*GDP_table$OUT_scen
GDP_table$GDP_change<-GDP_table$GDP_scen-GDP_table$GDP_base
GDP_table$GDP_base<-round(GDP_table$GDP_base, digits=2)
GDP_table$GDP_scen<-round(GDP_table$GDP_scen, digits=2)
GDP_table$GDP_change<-round(GDP_table$GDP_change, digits=2)
GDP_table$OUT_base<-round(GDP_table$OUT_base, digits=2)
GDP_table$OUT_scen<-round(GDP_table$OUT_scen, digits=2)

#EXPORT OUTPUT
LUC_scen_file<-"LUC_scenario_summary.dbf"
write.dbf(delta_L2, LUC_scen_file,  factor2char = TRUE, max_nchar = 254)
GDP_scen_file<-"GDP_scenario_summary.dbf"
write.dbf(GDP_table, GDP_scen_file,  factor2char = TRUE, max_nchar = 254)

#WRITE REPORT
title<-"\\b\\fs32 LUMENS-Trade-off Analysis (TA) Project Report\\b0\\fs20"
sub_title<-"\\b\\fs28 Sub-modules 2: Regional economic-Impact of GDP change\\b0\\fs20"
test<-as.character(Sys.Date())
date<-paste("Date : ", test, sep="")
time_start<-paste("Processing started : ", time_start, sep="")
time_end<-paste("Processing ended : ", eval(parse(text=(paste("Sys.time ()")))), sep="")
line<-paste("------------------------------------------------------------------------------------------------------------------------------------------------")
chapter1<-"\\b\\fs24 Impact of GDP change to land use requirement \\b0\\fs20"

# ==== Report 0. Cover=====
rtffile <- RTF("TA-Final_Demand_report.doc", font.size=11, width = 8.267, height = 11.692, omi = c(0,0,0,0))
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
addParagraph(rtffile, "\\b\\fs20 Table 1. GDP change\\b0\\fs20.")
addTable(rtffile,GDP_table,font.size=6)
addNewLine(rtffile)
addParagraph(rtffile, "\\b\\fs20 Table 2. Impact of GDP change to land use requirement\\b0\\fs20.")
addTable(rtffile,delta_L2,font.size=7)
done(rtffile)

unlink(img_location)
dbDisconnect(DB)

#=Writing final status message (code, message)
statuscode<-1
statusmessage<-"TA regional economy analysis successfully completed!"
statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)




