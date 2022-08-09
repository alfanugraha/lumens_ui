##DB-PostgreSQL=group
##proj.file=string
##type=selection Land Use/Cover; Planning Unit; Factor
##data=raster
##period=number 0
##description=string
##attribute_table=string
##statusoutput=output table
##passfilenames

#=Load library
library(spatial.tools) #Package 'spatial.tools' was removed from the CRAN repository
library(DBI)
library(RPostgreSQL)
library(rpostgis)
library(stringr)

#=Load active project 
load(proj.file)

#=Create raster_category function
# to synchronize all of the data spatial input
command="raster"
raster_category<-function(category, name, desc) {
  eval(parse(text=(paste(name, "<<-", command,'("', data, '")', sep=""))))
  eval(parse(text=(paste(name, "<<-spatial_sync_raster(", name, ',', 'ref, method = "ngb")', sep=""))))
  eval(parse(text=(paste(name, "<<-", name, "*1",  sep=""))))
  eval(parse(text=(paste("names(", name, ")<<-desc", sep=""))))
  eval(parse(text=(paste(name, "@title<<-category", sep=""))))
}

# set driver connection
driver <- dbDriver('PostgreSQL')
project <- as.character(proj_descr[1,2])
DB <- dbConnect(
  driver, dbname=project, host=as.character(pgconf$host), port=as.character(pgconf$port),
  user=as.character(pgconf$user), password=as.character(pgconf$pass)
)

#=Classify raster into three types of input
# type 0: land_use_cover
# type 1: planning_unit
# type 2: factor
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
  
  #create raster data & reclass the value of nodata 
  # tryCatch({
  #   raster_category(category=category, name=paste("in_hist_", data_name, index1, sep=""), desc=description) 
  # }, error=function(e){ 
  #   statuscode<-0
  #   statusmessage<-e    
  # })
  raster_temp<-raster(data)
  raster_temp<-reclassify(raster_temp, cbind(NA, 255)) # need to set as a dynamic variable
  raster_temp_name<-paste0(LUMENS_path_user, "/raster_temp.tif")
  writeRaster(raster_temp, filename=raster_temp_name, format="GTiff", overwrite=TRUE)
  
  #create attribute table
  attribute_table<-read.table(attribute_table, sep=",")
  colnames(attribute_table)<-c("ID", "COUNT", "Legend", "Classified")
  eval(parse(text=(paste("in_hist_", data_name, "_lut", idx_landuse, "<-attribute_table",  sep=""))))
  
  #write raster detail to PostgreSQL
  eval(parse(text=(paste("list_of_data_luc<-data.frame(RST_DATA='in_hist_", data_name, idx_landuse,"', RST_NAME='", description, "', PERIOD=", period, ", LUT_NAME='in_hist_", data_name,"_lut", idx_landuse, "', row.names=NULL)", sep=""))))
  
  InHistLanduseLUT_i <- paste('in_hist_', data_name, "_lut", idx_landuse, sep="")
  InHistLanduse_i <- paste('in_hist_', data_name, idx_landuse, sep="")
  
  #append list
  dbWriteTable(DB, "list_of_data_luc", list_of_data_luc, append=TRUE, row.names=FALSE)
  dbWriteTable(DB, InHistLanduseLUT_i, eval(parse(text=(paste(InHistLanduseLUT_i, sep="" )))), append=TRUE, row.names=FALSE)
  # pgWriteRast(DB, c("public", InHistLanduse_i), raster=eval(parse(text=(paste(InHistLanduse_i, sep="" )))))
  
  #write to csv
  list_of_data_luc<-dbReadTable(DB, c("public", "list_of_data_luc"))
  csv_file<-paste(LUMENS_path_user,"/csv_", category, ".csv", sep="")
  write.table(list_of_data_luc, csv_file, quote=FALSE, row.names=FALSE, sep=",")
  
  addRasterToPG(project, raster_temp_name, InHistLanduse_i, srid)

  # resave index
  eval(parse(text=(paste("resave(idx_landuse, idx_period, ", period_i, ", file=proj.file)", sep=""))))
  
  statuscode<-1
  statusmessage<-"land use/cover data has been added"
} else if(type==1){
  category<-"planning_unit"
  data_name<-"in_pu"
  
  #write index
  idx_pu<-idx_pu+1
  index1<-idx_pu
  
  # tryCatch({
  #   raster_category(category=category, name=paste(data_name, index1, sep=""), desc=description) 
  # }, error=function(e){ 
  #   statuscode<-0
  #   statusmessage<-e    
  # })
  raster_temp<-raster(data)
  raster_temp<-reclassify(raster_temp, cbind(NA, 255)) # need to set as a dynamic variable
  raster_temp_name<-paste0(LUMENS_path_user, "/raster_temp.tif")
  writeRaster(raster_temp, filename=raster_temp_name, format="GTiff", overwrite=TRUE)
  
  attribute_table<-read.table(attribute_table, sep=",")
  colnames(attribute_table)<-c("ID", "COUNT", "Legend")
  eval(parse(text=(paste(data_name, "_lut", idx_pu, "<-attribute_table",  sep=""))))
  
  eval(parse(text=(paste("list_of_data_pu<-data.frame(RST_DATA='", data_name, idx_pu,"', RST_NAME='", description, "', LUT_NAME='", data_name, "_lut", idx_pu, "', row.names=NULL)", sep=""))))

  InPuLUT_i <- paste(data_name, "_lut", idx_pu, sep="")
  InPu_i <- paste(data_name, idx_pu, sep="")
  
  #append list
  dbWriteTable(DB, "list_of_data_pu", list_of_data_pu, append=TRUE, row.names=FALSE)
  dbWriteTable(DB, InPuLUT_i, eval(parse(text=(paste(InPuLUT_i, sep="" )))), append=TRUE, row.names=FALSE)
  # pgWriteRast(DB, c("public", InPu_i), raster=eval(parse(text=(paste(InPu_i, sep="" )))))
  
  #write to csv
  list_of_data_pu<-dbReadTable(DB, c("public", "list_of_data_pu"))
  csv_file<-paste(LUMENS_path_user,"/csv_", category, ".csv", sep="")
  write.table(list_of_data_pu, csv_file, quote=FALSE, row.names=FALSE, sep=",")

  addRasterToPG(project, raster_temp_name, InPu_i, srid)
  
  resave(idx_pu, file=proj.file)
  
  statuscode<-1
  statusmessage<-"planning unit has been added"
} else if(type==2){
  category<-"factor_data"
  data_name<-"in_factor"
  
  #Defining the function to handle large raster data
  large_rst_handler <- function(dir){
    if(class(dir)=="character") rst.file <- raster(dir) else if (class(dir)=="RasterLayer") rst.file <- dir
    int.m <- as.matrix(rst.file)
    xn <- extent(rst.file)@xmin
    xx <- extent(rst.file)@xmax
    yn <- extent(rst.file)@ymin
    yx <- extent(rst.file)@ymax
    rst.obj <- raster(int.m, xmn =xn, xmx = xx, ymn = yn, ymx = yx)
    projection(rst.obj) <- projection(rst.file)
    return(rst.obj)
  }
  
  #write index
  idx_factor<-idx_factor+1
  index1<-idx_factor
  
  # tryCatch({
  #   raster_category(category=category, name=paste(data_name, index1, sep=""), desc=description) 
  # }, error=function(e){ 
  #   statuscode<-0
  #   statusmessage<-e    
  # })
  
  #run the function to add large raster data here
  # eval(parse(text=paste0(data_name, index1, "<- large_rst_handler(dir =", data_name, index1,")")))
  # eval(parse(text=(paste("names(", data_name, index1, ")<-description", sep=""))))
  
  eval(parse(text=(paste("list_of_data_f<-data.frame(RST_DATA='", data_name, idx_factor,"', RST_NAME='", description, "', row.names=NULL)", sep=""))))

  InFactor_i <- paste(data_name, idx_factor, sep="")
  # pgWriteRast(DB, c("public", InFactor_i), raster=eval(parse(text=(paste(InFactor_i, sep="" )))))
  dbWriteTable(DB, "list_of_data_f", list_of_data_f, append=TRUE, row.names=FALSE)
  
  #write to csv
  list_of_data_f<-dbReadTable(DB, c("public", "list_of_data_f"))
  csv_file<-paste(LUMENS_path_user,"/csv_", category, ".csv", sep="")
  write.table(list_of_data_f, csv_file, quote=FALSE, row.names=FALSE, sep=",")  
  
  addRasterToPG(project, data, InFactor_i, srid)
  
  resave(idx_factor, file=proj.file)

  statuscode<-1
  statusmessage<-"factor data has been added!"
}

dbDisconnect(DB)

#=Writing final status message (code, message)
statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)
