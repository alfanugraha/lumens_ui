##Database=group
##project_file=string
##overview=output raster
##passfilenames

library(RPostgreSQL)
library(rpostgis)

load(project_file)

# clear temporary folder first
if(!dir.exists(LUMENS_path_user)) dir.create(LUMENS_path_user)
setwd(LUMENS_path_user)
unlink(list.files(pattern="*"))

# Establishing connection to postgreSQL database
driver <- dbDriver('PostgreSQL')
project <- as.character(proj_descr[1,2])
DB <- dbConnect(
  driver, dbname=project, host=as.character(pgconf$host), port=as.character(pgconf$port),
  user=as.character(pgconf$user), password=as.character(pgconf$pass)
)

# identification of data which have been input: check idx_ es: factor, landuse, lut, pu
data_types <- c("factor", "landuse", "lut", "pu")
abbrvs <- c("f", "luc", "lut", "pu")
categories <- c("factor_data", "land_use_cover","lookup_table","planning_unit")

for(d in 1:length(data_types)){
  # check whether the value of 'idx_'data_types[d] is bigger than 0
  logic <- eval(parse(text=paste0("idx_", data_types[d], " > 0")))
  if(logic){
    list_of_data_lut<-dbReadTable(DB, c("public", paste0("list_of_data_",abbrvs[d])))
    csv_file<-paste0(LUMENS_path_user,"/csv_",categories[d],".csv")
    write.table(list_of_data_lut, csv_file, quote=FALSE, row.names=FALSE, sep=",")
  }
}

overview<-ref
dbDisconnect(DB)