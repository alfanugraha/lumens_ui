##SCIENDO-PostgreSQL=group
##Historical_Baseline_Car = file

user_temp_folder<-Sys.getenv("TEMP")
if(user_temp_folder=="") {
  user_temp_folder<-Sys.getenv("TMP")
}
LUMENS_log_dir <- paste(user_temp_folder,"/LUMENS", sep="")

if (file.exists("C:/Program Files (x86)/LUMENS/Abacus2")){
abacusExecutable = "C:/Progra~2/LUMENS/Abacus2/abacus2 "
} else{
abacusExecutable = "C:/Progra~1/LUMENS/Abacus2/abacus2 "
}

systemCommand <- paste(abacusExecutable, Historical_Baseline_Car, "-ref LUMENS -wd", LUMENS_log_dir)

system(systemCommand)
