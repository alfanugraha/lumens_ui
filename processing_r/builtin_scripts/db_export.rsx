##Database=group
##proj.file=string

#=Load library
library(stringr)

#=Load active project that will be exported
load(proj.file)

#set zip name
LZIP<-dirname(proj.file)
setwd(LZIP)

#extract database name from proj.file
db_name <- as.character(proj_descr[1,2])
sql_file <- paste0(LZIP, '/', db_name, '.sql')

createNewPGTbl = pathEnv
# db_name as a new db_name.sql
createNewPGTbl[6] = paste("pg_dump -d ", db_name, " > ", sql_file, sep="")
# replacement pgEnvBatch
newBatchFile <- file(pgEnvBatch)
writeLines(createNewPGTbl, newBatchFile)
close(newBatchFile)
# execute batch file
pgEnvBatchFile<-str_replace_all(string=pgEnvBatch, pattern="/", repl='\\\\')
system(pgEnvBatchFile)

#=Zipping process
zipexe<-paste0("\"", LUMENS_path, "\\bin\\zip.exe\" ")
zip_comm<-paste0(zipexe, "-r ", paste0(db_name, ".lpa"), " .")
system(zip_comm)
unlink(sql_file)
