##DB-PostgreSQL=group
##proj.file=string
##type=selection Land Use/Cover; Planning Unit
##data=vector
##attribute_field_id=field data
##period=number 0 (tahun)
##description=string
##attribute_table=string
##statusoutput=output table

#=Load library
library(stringr)
library(spatial.tools)
library(DBI)
library(RPostgreSQL)
library(rpostgis)

#=Load active project 
load(proj.file)

#=Set temporary folder
user_temp_folder<-Sys.getenv("TEMP")
if(user_temp_folder=="") {
  user_temp_folder<-Sys.getenv("TMP")
}

#=Write temporary vector to temporary folder
setwd(user_temp_folder)
description<-str_replace_all(string=description, pattern=" ", repl=".")
writeOGR(data, dsn=user_temp_folder, description, overwrite_layer=TRUE, driver="ESRI Shapefile")

shp_dir<-paste(user_temp_folder,"/", description, ".shp", sep="")
file_out<-paste(user_temp_folder, "/", description,  ".tif", sep="")
res<-res(ref)[1]
osgeo_comm<-paste(gdalraster, shp_dir, file_out,"-a IDADM -tr", res, res, "-a_nodata 255 -ot Byte", sep=" ")
system(osgeo_comm)

raster_category<-function(category, raster_data, name, desc) {
  eval(parse(text=(paste(name, "<<-spatial_sync_raster(raster_data, ref, method = 'ngb')", sep=""))))
  eval(parse(text=(paste(name, "<<-", name, "*1",  sep=""))))
  eval(parse(text=(paste("names(",name, ")<<-desc", sep=""))))
  eval(parse(text=(paste(name, "@title<<-category", sep=""))))
}

# set driver connection
driver <- dbDriver('PostgreSQL')
project <- as.character(proj_descr[1,2])
DB <- dbConnect(
  driver, dbname=project, host=as.character(pgconf$host), port=as.character(pgconf$port),
  user=as.character(pgconf$user), password=as.character(pgconf$pass)
)

#=Classify raster into two types of input
# type 0: land_use_cover
# type 1: planning_unit
tif_file<-raster(file_out)
if(type==0){
  category<-"land_use_cover"
  data_name<-"lulc"
  
  #write index
  idx_landuse<-idx_landuse+1
  idx_period<-idx_period+1
  eval(parse(text=(paste("period", idx_period, "<-period", sep=""))))
  period_i<-paste("period", idx_period, sep="")
  eval(parse(text=(paste(period_i, "<-period", sep="" ))))
  index1<-idx_landuse
  
  raster_temp<-reclassify(tif_file, cbind(NA, 255)) # need to set as a dynamic variable
  raster_temp_name<-paste0(LUMENS_path_user, "/raster_temp.tif")
  writeRaster(raster_temp, filename=raster_temp_name, format="GTiff", overwrite=TRUE)
  
  attribute_table<-read.table(attribute_table, sep=",")
  colnames(attribute_table)<-c("ID", "Old_Legend", "Legend", "Classified")
  eval(parse(text=(paste("freqR<-na.omit(as.data.frame(freq(", data_name, "_", idx_landuse, ")))", sep=""))))
  colnames(freqR)<-c("ID", "COUNT")
  attribute_table<-merge(attribute_table, freqR, by="ID")
  attribute_table<-subset(attribute_table, select=c('ID', 'COUNT', 'Legend', 'Classified'))
  eval(parse(text=(paste("in_hist_", data_name, "_lut", idx_landuse, "<-attribute_table",  sep=""))))

  #write raster detail to PostgreSQL
  eval(parse(text=(paste("list_of_data_luc<-data.frame(RST_DATA='in_hist_", data_name, idx_landuse,"', RST_NAME='", description, "', PERIOD=", period, ", LUT_NAME='in_hist_", data_name,"_lut", idx_landuse, "', row.names=NULL)", sep=""))))
  
  InHistLanduseLUT_i <- paste('in_hist_', data_name, "_lut", idx_landuse, sep="")
  InHistLanduse_i <- paste('in_hist_', data_name, idx_landuse, sep="")
  
  dbWriteTable(DB, "list_of_data_luc", list_of_data_luc, append=TRUE, row.names=FALSE)
  dbWriteTable(DB, InHistLanduseLUT_i, eval(parse(text=(paste(InHistLanduseLUT_i, sep="" )))), append=TRUE, row.names=FALSE)
  
  #write to csv 
  list_of_data_luc<-dbReadTable(DB, c("public", "list_of_data_luc"))
  csv_file<-paste(LUMENS_path_user,"/csv_", category, ".csv", sep="")
  write.table(list_of_data_luc, csv_file, quote=FALSE, row.names=FALSE, sep=",")
  
  addRasterToPG(project, raster_temp_name, InHistLanduse_i, srid)
  
  # resave index
  eval(parse(text=(paste("resave(idx_landuse, idx_period, ", period_i, ", file=proj.file)", sep=""))))
    
  statuscode<-1
  statusmessage<-"land use/cover data has been added"
} else {
  category<-"planning_unit"
  data_name<-"in_pu"
  
  #write index
  idx_pu<-idx_pu+1
  index1<-idx_pu
  
  raster_temp<-reclassify(tif_file, cbind(NA, 255)) # need to set as a dynamic variable
  raster_temp_name<-paste0(LUMENS_path_user, "/raster_temp.tif")
  writeRaster(raster_temp, filename=raster_temp_name, format="GTiff", overwrite=TRUE)

  attribute_table<-read.table(attribute_table, sep=",")
  colnames(attribute_table)<-c("ID", attribute_field_id)
  
  eval(parse(text=(paste(data_name, "_lut", idx_pu, "<-attribute_table",  sep=""))))
  
  eval(parse(text=(paste("list_of_data_pu<-data.frame(RST_DATA='", data_name, idx_pu,"', RST_NAME='", description, "',", "LUT_NAME='", data_name, "_lut", idx_pu, "', row.names=NULL)", sep=""))))
  
  InPuLUT_i <- paste(data_name, "_lut", idx_pu, sep="")
  InPu_i <- paste(data_name, idx_pu, sep="")
  
  dbWriteTable(DB, "list_of_data_pu", list_of_data_pu, append=TRUE, row.names=FALSE)
  dbWriteTable(DB, InPuLUT_i, eval(parse(text=(paste(InPuLUT_i, sep="" )))), append=TRUE, row.names=FALSE)
  
  #write to csv
  list_of_data_pu<-dbReadTable(DB, c("public", "list_of_data_pu"))
  csv_file<-paste(LUMENS_path_user,"/csv_", category, ".csv", sep="")
  write.table(list_of_data_pu, csv_file, quote=FALSE, row.names=FALSE, sep=",")    
  
  addRasterToPG(project, raster_temp_name, InPu_i, srid)
  
  resave(idx_pu, file=proj.file)
  
  statuscode<-1
  statusmessage<-"planning unit has been added"
}

dbDisconnect(DB)
 
#=Writing final status message (code, message)
statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)