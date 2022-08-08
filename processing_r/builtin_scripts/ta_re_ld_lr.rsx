#Regional Economy Land Distribution and Requirement Analysis
##TA-PostgreSQL=group
##proj.file=string
##land_use=string
##land.distribution_file=string
##desc_output=string
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
load(desc_output)

# set driver connection
driver <- dbDriver('PostgreSQL')
project <- as.character(proj_descr[1,2])
DB <- dbConnect(
  driver, dbname=project, host=as.character(pgconf$host), port=as.character(pgconf$port),
  user=as.character(pgconf$user), password=as.character(pgconf$pass)
)

#=Set Working Directory
work_dir<-paste(dirname(proj.file), "/TA/Land_Requirement", idx_TA_regeco, sep="")
dir.create(work_dir, mode="0777")
setwd(work_dir)

#READ INPUT FILE
load(desc_output)
list_of_data_lut<-dbReadTable(DB, c("public", "list_of_data_lut"))
list_of_data_luc<-dbReadTable(DB, c("public", "list_of_data_luc"))

nodata_val<-0 # still hardcode (!)
row_land_dist <- list_of_data_lut[which(list_of_data_lut$TBL_NAME==land.distribution_file),]
land.distribution <- list_of_data_lut<-dbReadTable(DB, c("public", row_land_dist$TBL_DATA))
# lc.list<-read.table(lc.list_file, header=FALSE, sep=",")
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
GDP[is.na(GDP)]<-0
order_GDP <- as.data.frame(GDP[order(-GDP$GDP),])
order_GDP10<-head(order_GDP,n=20)
GDP_tot<-as.matrix(GDP$GDP)
GDP_tot<-colSums(GDP_tot)

#LINK LAND SISTRIBUTION FILE WITH LAND USE MAP
#Read land use map and calculate area of land use distribution matrix
data_luc<-list_of_data_luc[which(list_of_data_luc$RST_NAME==land_use),]
# landuse<-getRasterFromPG(pgconf, project, data_luc$RST_DATA, paste(data_luc$RST_DATA, '.tif', sep=''))
landuse_lut<-dbReadTable(DB, c("public", data_luc$LUT_NAME))

landuse_area<-subset(landuse_lut,ID !=nodata_val)
landuse_area<-as.matrix(landuse_area$COUNT)
land.distribution_t<-as.matrix(land.distribution)
landuse_area_diag<-diag(as.numeric(as.matrix(landuse_area)))
land.distribution.val<-land.distribution_t %*% landuse_area_diag

#CALCULATE LAND DISTRIBUTION COEFFICIENT MATRIX
land.distribution.ctot<-colSums(land.distribution.val)
land.distribution.rtot<-rowSums(land.distribution.val)
land.distribution.prop<-land.distribution.val %*% diag(1/land.distribution.ctot)
land.distribution.prop[is.na(land.distribution.prop)]<-0
land.distribution.prop.r<-t(land.distribution.val) %*% diag(1/land.distribution.rtot)
land.distribution.prop.r[is.na(land.distribution.prop.r)]<-0
land.requirement<-rowSums(land.distribution.val)
fin_dem.rtot<-rowSums(fin_dem)
int_con.rtot<-rowSums(int_con)
demand<-fin_dem.rtot+int_con.rtot
land.requirement.coeff<-land.requirement/demand
land.requirement.coeff[is.infinite(land.requirement.coeff)]<-0
land.productivity.coeff<-land.requirement/fin_dem.rtot
land.productivity.coeff[is.infinite(land.productivity.coeff)]<-0

#PRODUCE OUTPUT
land.requirement_table<-as.data.frame(land.requirement)
land.requirement.tot<-sum(land.requirement)
land.requirement_table_prop<-as.data.frame(land.requirement/land.requirement.tot)
land.requirement_table<-cbind(sector,land.requirement_table,land.requirement_table_prop,demand,fin_dem.rtot,land.requirement.coeff, land.productivity.coeff)
colnames(land.requirement_table)[1] <- "SECTOR"
colnames(land.requirement_table)[2] <- "CATEGORY"
colnames(land.requirement_table)[3] <- "LR"
colnames(land.requirement_table)[4] <- "LR_PROP"
colnames(land.requirement_table)[5] <- "OUTPUT"
colnames(land.requirement_table)[6] <- "DEMAND"
colnames(land.requirement_table)[7] <- "LRC"
colnames(land.requirement_table)[8] <- "LPC"
land.requirement_table$LR<-round(land.requirement_table$LR)
land.requirement_table$LR_PROP<-round(land.requirement_table$LR_PROP, digits=2)
land.requirement_table$OUTPUT<-round(land.requirement_table$OUTPUT)
land.requirement_table$DEMAND<-round(land.requirement_table$DEMAND)
land.requirement_table$LRC<-round(land.requirement_table$LRC, digits=2)
land.requirement_table$LPC<-round(land.requirement_table$LPC, digits=2)

#land.requirement_table$LRC<-round(land.requirement_table$LRC, digits=2)-->catasthropic error !!!!
#land.requirement_table$LPC<-round(land.requirement_table$LPC, digits=2)-->catasthropic error !!!!
order_land.requirement <- as.data.frame(land.requirement_table[order(-land.requirement_table$LRC),])
order_land.requirement <-head(order_land.requirement,n=20)
LRC_graph<-ggplot(data=order_land.requirement, aes(x=SECTOR, y=LRC, fill=CATEGORY)) +
  geom_bar(stat="identity")+ coord_flip() + xlab("Sectors") + ylab("Land requirement coefficient") +
  theme( legend.title = element_text(size=8),legend.text = element_text(size = 6),
         axis.text.x = element_text(size = 8))

#EXPORT OUTPUT
land_distribution_file<-"Land_distribution_matrix.dbf"
# write.dbf(land.distribution.prop, land_distribution_file,  factor2char = TRUE, max_nchar = 254)
land_requirement_file<-"Land_requirement_coefficient.dbf"
# write.dbf(land.requirement_table, land_requirement_file, factor2char = TRUE, max_nchar = 254)

#WRITE REPORT
title<-"\\b\\fs32 LUMENS-Trade-off Analysis (TA) Project Report\\b0\\fs20"
sub_title<-"\\b\\fs28 Sub-modules 2: Regional economic-Land Requirement Coefficient\\b0\\fs20"
test<-as.character(Sys.Date())
date<-paste("Date : ", test, sep="")
time_start<-paste("Processing started : ", time_start, sep="")
time_end<-paste("Processing ended : ", eval(parse(text=(paste("Sys.time ()")))), sep="")
line<-paste("------------------------------------------------------------------------------------------------------------------------------------------------")
chapter1<-"\\b\\fs24 Land Requirement Coefficient \\b0\\fs20"

# ==== Report 0. Cover=====
rtffile <- RTF("TA-Land_Requirement_report.doc", font.size=11, width = 8.267, height = 11.692, omi = c(0,0,0,0))
# INPUT
file.copy(paste0(LUMENS_path, "/ta_cover.png"), work_dir, recursive = FALSE)
img_location<-paste0(work_dir, "/ta_cover.png")
# loading the .png image to be edited
cover <- image_read(img_location)
# to display, only requires to execute the variable name, e.g.: "> cover"
# adding text at the desired location
text_submodule <- paste("Sub-Modul Ekonomi Regional\n\nAnalisis Kebutuhan dan Produktifitas Lahan\n", location, ", ", "Tahun ", I_O_period, sep="")
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
addParagraph(rtffile, "\\b\\fs20 Table 1. Land requirement\\b0\\fs20.")
addTable(rtffile,land.requirement_table,font.size=7.5)
addNewLine(rtffile)
addPlot(rtffile,plot.fun=print, width=6.7,height=3,res=300,LRC_graph)
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
     land.distribution.prop,
     land.requirement_table,
     # landuse,
     landuse_lut,
     file=paste0('LandRequirement', I_O_period, '.ldbase'))

unlink(img_location)
dbDisconnect(DB)

#=Writing final status message (code, message)
statuscode<-1
statusmessage<-"TA regional economy analysis successfully completed!"
statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)
