##DB-PostgreSQL=group
##proj.file=string
##csv_delete_data=string
##statusoutput=output table

#=Load library
library(stringr)
library(RPostgreSQL)
library(DBI)
library(rpostgis)

#=Load active project
load(proj.file)

# set driver connection
driver <- dbDriver('PostgreSQL')
project <- as.character(proj_descr[1,2])
DB <- dbConnect(
  driver, dbname=project, host=as.character(pgconf$host), port=as.character(pgconf$port),
  user=as.character(pgconf$user), password=as.character(pgconf$pass)
)

list_of_delete<-read.table(csv_delete_data, header=FALSE, sep=",") #error
len_delete_data<-nrow(list_of_delete)

list_of_data_luc<-dbReadTable(DB, c("public", "list_of_data_luc"))
list_of_data_pu<-dbReadTable(DB, c("public", "list_of_data_pu"))
list_of_data_lut<-dbReadTable(DB, c("public", "list_of_data_lut"))
list_of_data_f<-dbReadTable(DB, c("public", "list_of_data_f"))

# bind all data
temp_luc<-data.frame(CATEGORY='list_of_data_luc', NAME=list_of_data_luc$RST_DATA)
temp_pu<-data.frame(CATEGORY='list_of_data_pu', NAME=list_of_data_pu$RST_DATA)
temp_lut<-data.frame(CATEGORY='list_of_data_lut', NAME=list_of_data_lut$TBL_DATA)
temp_f<-data.frame(CATEGORY='list_of_data_f', NAME=list_of_data_f$RST_DATA)
temp_all_data<-rbind(temp_luc, temp_pu, temp_lut, temp_f)

# loop delete data
for(i in 1:len_delete_data){
  statuscode<-0
  statusmessage<-"Something happened!"
  statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)
  
  eval(parse(text=(paste("data_name<-as.character(list_of_delete[", i, ",])")))) 
  data_temp<-temp_all_data[which(temp_all_data$NAME==data_name),]
  if(data_temp$CATEGORY == 'list_of_data_lut') {
    del_query<-paste0("DELETE FROM public.", data_temp$CATEGORY, " WHERE \"TBL_DATA\"='", data_name, "'")
  } else {
    del_query<-paste0("DELETE FROM public.", data_temp$CATEGORY, " WHERE \"RST_DATA\"='", data_name, "'")
  }
  result <- dbSendQuery(DB, del_query)
  dbRemoveTable(DB, c("public", data_name))
}

# rewrite temporary csv table
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

dbDisconnect(DB)

#=Writing final status message (code, message)
statuscode<-1
statusmessage<-"Data has been deleted!"
statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)