##TA-PostgreSQL=group
##proj.file=string
##landuse_1=string
##landuse_2=string
##planning_unit=string
##lookup_c=string
##lookup_npv=string
##raster.nodata=number 0
#resultoutput=output table
##statusoutput=output table

#=Load library
library(tiff)
library(foreign)
library(rasterVis)
library(reshape2)
library(plyr)
library(lattice)
library(latticeExtra)
library(RColorBrewer)
library(grid)
library(ggplot2)
library(spatial.tools)
library(rtf)
library(splitstackshape)
library(stringr)
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

#=Retrieve all list of data that are going to be used
# list_of_data_luc ==> list of data land use/cover 
# list_of_data_pu ==> list of data planning unit
# list_of_data_f ==> list of data factor
# list_of_data_lut ==> list of data lookup table
list_of_data_luc<-dbReadTable(DB, c("public", "list_of_data_luc"))
list_of_data_pu<-dbReadTable(DB, c("public", "list_of_data_pu"))
list_of_data_lut<-dbReadTable(DB, c("public", "list_of_data_lut"))
# return the selected data from the list
data_luc1<-list_of_data_luc[which(list_of_data_luc$RST_NAME==landuse_1),]
data_luc2<-list_of_data_luc[which(list_of_data_luc$RST_NAME==landuse_2),]
data_pu<-list_of_data_pu[which(list_of_data_pu$RST_NAME==planning_unit),]
data_lut<-list_of_data_lut[which(list_of_data_lut$TBL_NAME==lookup_c),]
data_npv<-list_of_data_lut[which(list_of_data_lut$TBL_NAME==lookup_npv),]

T1<-data_luc1$PERIOD
T2<-data_luc2$PERIOD

#=Set Working Directory
pu_name<-data_pu$RST_DATA 
idx_TA_opcost<-idx_TA_opcost+1
working_directory<-paste(dirname(proj.file), "/TA/", idx_TA_opcost, "_OpCost_", T1, "_", T2, "_", pu_name, sep="")
dir.create(working_directory, mode="0777")

# create temp directory
dir.create(LUMENS_path_user, mode="0777")
setwd(LUMENS_path_user)

#=Set initial variables
# reference map
ref.obj<-exists('ref')
ref.path<-paste(dirname(proj.file), '/ref.tif', sep='')
if(!ref.obj){
  if(file.exists(ref.path)){
    ref<-raster(ref.path)
  } else {
    ref<-getRasterFromPG(pgconf, project, 'ref_map', 'ref.tif')
  }
}

# planning unit
if (data_pu$RST_DATA=="ref") {
  zone<-ref
  count_ref<-as.data.frame(freq(ref))
  count_ref<-na.omit(count_ref)
  colnames(count_ref)<-c("IDADM", "COUNT")
  ref_table<-dbReadTable(DB, c("public", data_pu$LUT_NAME)) 
  lookup_z<-merge(count_ref, ref_table, by="IDADM")
} else {
  zone<-getRasterFromPG(pgconf, project, data_pu$RST_DATA, paste(data_pu$RST_DATA, '.tif', sep=''))
  lookup_z<-dbReadTable(DB, c("public", data_pu$LUT_NAME)) 
}
# landuse first time period
landuse1<-getRasterFromPG(pgconf, project, data_luc1$RST_DATA, paste(data_luc1$RST_DATA, '.tif', sep=''))
# landuse second time period
landuse2<-getRasterFromPG(pgconf, project, data_luc2$RST_DATA, paste(data_luc2$RST_DATA, '.tif', sep=''))
# landcover lookup table
lookup_c<-dbReadTable(DB, c("public", data_lut$TBL_DATA)) 
lookup_npv<-dbReadTable(DB, c("public", data_npv$TBL_DATA))
# set lookup table
lookup_c<-lookup_c[which(lookup_c[1] != raster.nodata),]
lookup_npv<-lookup_npv[which(lookup_npv[1] != raster.nodata),]
lookup_lc<-lookup_c
lookup_ref<-lut_ref
colnames(lookup_lc)<-c("ID","LC","CARBON")
colnames(lookup_z)<-c("ID", "COUNT_ZONE", "ZONE")
colnames(lookup_npv)<-c("ID", "LC", "NPV")

nLandCoverId<-nrow(lookup_lc)
nPlanningUnitId<-nrow(lookup_z)

#=Projection handling
if (grepl("+units=m", as.character(ref@crs))){
  print("Raster maps have projection in meter unit")
  Spat_res<-res(ref)[1]*res(ref)[2]/10000
  paste("Raster maps have ", Spat_res, " Ha spatial resolution, QuES-C will automatically generate data in Ha unit")
} else if (grepl("+proj=longlat", as.character(ref@crs))){
  print("Raster maps have projection in degree unit")
  Spat_res<-res(ref)[1]*res(ref)[2]*(111319.9^2)/10000
  paste("Raster maps have ", Spat_res, " Ha spatial resolution, QuES-C will automatically generate data in Ha unit")
} else{
  statuscode<-0
  statusmessage<-"Raster map projection is unknown"
  statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)
  quit()
}

#=Set project properties
title=location
tab_title<-as.data.frame(title)
period1=T1
period2=T2
period=period2-period1
proj_prop<-as.data.frame(title)
proj_prop$period1<-period1
proj_prop$period2<-period2
proj_prop$period <- do.call(paste, c(proj_prop[c("period1", "period2")], sep = " - "))

#=Create cross-tabulation for zone
xtab<-tolower(paste('xtab_', pu_name, T1, T2, sep=''))
data_xtab<-list_of_data_lut[which(list_of_data_lut$TBL_NAME==xtab),]
if(nrow(data_xtab)==0){
  dummy1<-data.frame(nPU=lookup_z$ID, divider=nLandCoverId*nLandCoverId)
  dummy1<-expandRows(dummy1, 'divider')
  
  dummy2<-data.frame(nT1=lookup_lc$ID, divider=nLandCoverId)
  dummy2<-expandRows(dummy2, 'divider')
  dummy2<-data.frame(nT1=rep(dummy2$nT1, nPlanningUnitId))
  
  dummy3<-data.frame(nT2=rep(rep(lookup_lc$ID, nLandCoverId), nPlanningUnitId))
  
  landUseChangeMapDummy<-cbind(dummy1, dummy2, dummy3)
  colnames(landUseChangeMapDummy)<-c('ZONE', 'ID_LC1', 'ID_LC2')
  
  R2<-(zone*1) + (landuse1*100^1)+ (landuse2*100^2) 
  lu.db<-as.data.frame(freq(R2))
  lu.db<-na.omit(lu.db)
  n<-3
  k<-0
  lu.db$value_temp<-lu.db$value
  while(k < n) {
    eval(parse(text=(paste("lu.db$Var", n-k, "<-lu.db$value_temp %% 100", sep=""))))  
    lu.db$value_temp<-floor(lu.db$value_temp/100)
    k=k+1
  }
  lu.db$value_temp<-NULL
  colnames(lu.db) = c("ID_CHG", "COUNT", "ZONE", "ID_LC1", "ID_LC2")
  lu.db<-merge(landUseChangeMapDummy, lu.db, by=c('ZONE', 'ID_LC1', 'ID_LC2'), all=TRUE)
  lu.db$ID_CHG<-lu.db$ZONE*1 + lu.db$ID_LC1*100^1 + lu.db$ID_LC2*100^2
  lu.db<-replace(lu.db, is.na(lu.db), 0)
  
  idx_lut<-idx_lut+1
  eval(parse(text=(paste("in_lut", idx_lut, " <- lu.db", sep=""))))
  
  eval(parse(text=(paste("list_of_data_lut<-data.frame(TBL_DATA='in_lut", idx_lut,"', TBL_NAME='", xtab, "', row.names=NULL)", sep=""))))
  # save to PostgreSQL
  InLUT_i <- paste('in_lut', idx_lut, sep="")
  dbWriteTable(DB, InLUT_i, eval(parse(text=(paste(InLUT_i, sep="" )))), append=TRUE, row.names=FALSE)
  dbWriteTable(DB, "list_of_data_lut", list_of_data_lut, append=TRUE, row.names=FALSE)
  
  setwd(working_directory)
  idx_factor<-idx_factor+1
  chg_map<-tolower(paste('chgmap_', pu_name, T1, T2, sep=''))
  eval(parse(text=(paste("writeRaster(R2, filename='", chg_map, ".tif', format='GTiff', overwrite=TRUE)", sep=""))))
  eval(parse(text=(paste("factor", idx_factor, "<-'", chg_map, "'", sep=''))))  
  eval(parse(text=(paste("list_of_data_f<-data.frame(RST_DATA='factor", idx_factor,"', RST_NAME='", chg_map, "', row.names=NULL)", sep=""))))  
  InFactor_i <- paste("factor", idx_factor, sep="")  
  dbWriteTable(DB, "list_of_data_f", list_of_data_f, append=TRUE, row.names=FALSE)
  #write to csv
  list_of_data_f<-dbReadTable(DB, c("public", "list_of_data_f"))
  csv_file<-paste(dirname(proj.file),"/csv_factor_data.csv", sep="")
  write.table(list_of_data_f, csv_file, quote=FALSE, row.names=FALSE, sep=",")  
  addRasterToPG(project, paste0(chg_map, '.tif'), InFactor_i, srid)
  unlink(paste0(chg_map, '.tif'))
} else {
  lu.db<-dbReadTable(DB, c("public", data_xtab$TBL_DATA))
}
# rename column
colnames(lookup_c) = c("ID_LC1", "LC_t1", "CARBON_t1")
data_merge <- merge(lu.db,lookup_c,by="ID_LC1")
colnames(lookup_c) = c("ID_LC2", "LC_t2", "CARBON_t2")
data_merge <- as.data.frame(merge(data_merge,lookup_c,by="ID_LC2"))
colnames(lookup_z)[1]="ZONE"
colnames(lookup_z)[3]="Z_NAME"
data_merge <- as.data.frame(merge(data_merge,lookup_z,by="ZONE"))
#data_merge <- as.data.frame(merge(data_merge,lookup_ref,by="REF"))
data_merge$COUNT<-data_merge$COUNT*Spat_res
data_merge$COUNT_ZONE<-data_merge$COUNT_ZONE*Spat_res
#save crosstab
# original_data<-subset(data_merge, select=-c(CARBON_t1, CARBON_t2))
# eval(parse(text=(paste("write.dbf(original_data, 'lu.db_", pu_name ,"_", T1, "_", T2, ".dbf')", sep="")))) 
# rm(lu.db, original_data)
#calculate area based on reference/administrative data
# refMelt<-melt(data = ref.db, id.vars=c('REF'), measure.vars=c('COUNT'))
# refArea<-dcast(data = refMelt, formula = REF ~ ., fun.aggregate = sum)

#=Carbon accounting process
NAvalue(landuse1)<-raster.nodata
NAvalue(landuse2)<-raster.nodata
rcl.m.c1<-as.matrix(lookup_lc[,1])
rcl.m.c2<-as.matrix(lookup_lc[,3])
rcl.m<-cbind(rcl.m.c1,rcl.m.c2)
rcl.m<-rbind(rcl.m, c(0, NA))
carbon1<-reclassify(landuse1, rcl.m)
carbon2<-reclassify(landuse2, rcl.m)
chk_em<-carbon1>carbon2
chk_sq<-carbon1<carbon2
emission<-((carbon1-carbon2)*3.67)*chk_em
sequestration<-((carbon2-carbon1)*3.67)*chk_sq

#====NPV Accounting Process====
rcl.m.npv1<-as.matrix(lookup_npv[,1])
rcl.m.npv2<-as.matrix(lookup_npv[,3])
rcl.m.npv<-cbind(rcl.m.npv1,rcl.m.npv2)
npv1<-reclassify(landuse1, rcl.m.npv)
npv2<-reclassify(landuse2, rcl.m.npv)

npv_chg<-npv2-npv1
opcost<-npv_chg/emission

#export analysis result
carbontiff1<-carbon1
carbontiff2<-carbon2
npvtiff1<-npv1
npvtiff2<-npv2
npvchgtiff<-npv_chg
opcosttiff<-opcost

#WRITE REPORT
title<-"\\b\\fs32 LUMENS-Trade-off Analysis (TA) Project Report\\b0\\fs20"
sub_title<-"\\b\\fs28 Sub modul 1: Opportunity Cost Map \\b0\\fs20"
line<-paste("------------------------------------------------------------------------------------------------------------------------------------------------")
chapter1<-"\\b\\fs24 1.Carbon stock maps \\b0\\fs20"
chapter2<-"\\b\\fs24 2.NPV maps \\b0\\fs20"
chapter3<-"\\b\\fs24 3.Opportunity cost maps \\b0\\fs20"
rtffile <- RTF("TA-Opportunity_cost_report.doc", font.size=11, width = 8.267, height = 11.692, omi = c(0,0,0,0))
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
C1 <- levelplot(carbon1, col.regions= function(x)rev(terrain.colors(x)))
addPlot(rtffile, plot.fun=print, width=6, height=5, res=300, C1 )
addParagraph(rtffile, "\\b\\fs20 Figure 1. Carbon density maps t1\\b0\\fs20.")
addNewLine(rtffile)
C2 <- levelplot(carbon2, col.regions= function(x)rev(terrain.colors(x)))
addPlot(rtffile, plot.fun=print, width=6, height=5, res=300, C2 )
addParagraph(rtffile, "\\b\\fs20 Figure 2. Carbon density maps t2\\b0\\fs20.")
addNewLine(rtffile)
C3 <- levelplot(emission, col.regions= function(x)rev(terrain.colors(x)))
addPlot(rtffile, plot.fun=print, width=6, height=5, res=300, C3 )
addParagraph(rtffile, "\\b\\fs20 Figure 3. Emission maps t1-t2\\b0\\fs20.")
addNewLine(rtffile)
C4 <- levelplot(emission, col.regions= function(x)rev(terrain.colors(x)))
addPlot(rtffile, plot.fun=print, width=6, height=5, res=300, C4 )
addParagraph(rtffile, "\\b\\fs20 Figure 4. Emission maps t1-t2\\b0\\fs20.")
addNewLine(rtffile)
C5 <- levelplot(sequestration, col.regions= function(x)rev(terrain.colors(x)))
addPlot(rtffile, plot.fun=print, width=6, height=5, res=300, C5 )
addParagraph(rtffile, "\\b\\fs20 Figure 5. Sequestration maps t1-t2\\b0\\fs20.")
addNewLine(rtffile)
C6 <- levelplot(sequestration, col.regions= function(x)rev(terrain.colors(x)))
addPlot(rtffile, plot.fun=print, width=6, height=5, res=300, C6 )
addParagraph(rtffile, "\\b\\fs20 Figure 6. Sequestration maps t1-t2\\b0\\fs20.")
addNewLine(rtffile)
addParagraph(rtffile, chapter2)
addNewLine(rtffile)
C7 <- levelplot(npv1, col.regions= function(x)rev(terrain.colors(x)))
addPlot(rtffile, plot.fun=print, width=6, height=5, res=300, C7 )
addParagraph(rtffile, "\\b\\fs20 Figure 7. NPV map t1\\b0\\fs20.")
addNewLine(rtffile)
C8<- levelplot(npv2, col.regions= function(x)rev(terrain.colors(x)))
addPlot(rtffile, plot.fun=print, width=6, height=5, res=300, C8 )
addParagraph(rtffile, "\\b\\fs20 Figure 8. NPV map t2\\b0\\fs20.")
addNewLine(rtffile)
C9 <- levelplot(npv_chg, col.regions= function(x)rev(terrain.colors(x)))
addPlot(rtffile, plot.fun=print, width=6, height=5, res=300, C9 )
addParagraph(rtffile, "\\b\\fs20 Figure 9. NPV change map t1-t2\\b0\\fs20.")
addNewLine(rtffile)
addParagraph(rtffile, chapter3)
addNewLine(rtffile)
C10 <-gplot(opcost) + geom_tile(aes(fill = value)) + scale_fill_gradient(low = 'white', high = 'blue') + coord_equal()
addPlot(rtffile, plot.fun=print, width=6, height=5, res=300, C10 )
addParagraph(rtffile, "\\b\\fs20 Figure 10. Opcost map t1-t2\\b0\\fs20.")
addNewLine(rtffile)

done(rtffile)

resave(idx_TA_opcost, file=proj.file)

dbDisconnect(DB)

#=Writing final status message (code, message)
statuscode<-1
statusmessage<-"QUES-C analysis successfully completed!"
statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)
