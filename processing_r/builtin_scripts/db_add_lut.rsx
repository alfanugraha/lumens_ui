##DB-PostgreSQL=group
##proj.file=string
##description=string
##attribute_table=string
##statusoutput=output table

#=Load library
library(stringr)
library(DBI)
library(RPostgreSQL)
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

description<-str_replace_all(string=description, pattern=" ", repl=".")

idx_lut<-idx_lut+1
eval(parse(text=(paste("in_lut", idx_lut, "<-read.table(attribute_table, header=TRUE, sep=',')", sep=""))))

eval(parse(text=(paste("list_of_data_lut<-data.frame(TBL_DATA='in_lut", idx_lut,"', TBL_NAME='", description, "', row.names=NULL)", sep=""))))

InLUT_i <- paste('in_lut', idx_lut, sep="")

dbWriteTable(DB, "list_of_data_lut", list_of_data_lut, append=TRUE, row.names=FALSE)
dbWriteTable(DB, InLUT_i, eval(parse(text=(paste(InLUT_i, sep="" )))), append=TRUE, row.names=FALSE)

#write to csv # rudimentary, removed
list_of_data_lut<-dbReadTable(DB, c("public", "list_of_data_lut"))
csv_file<-paste(LUMENS_path_user,"/csv_lookup_table.csv", sep="")
write.table(list_of_data_lut, csv_file, quote=FALSE, row.names=FALSE, sep=",")

resave(idx_lut, file=proj.file)

dbDisconnect(DB)

#=Writing final status message (code, message)
statuscode<-1
statusmessage<-"Lookup table has been added"
statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)


