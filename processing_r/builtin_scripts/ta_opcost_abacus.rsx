##SCIENDO-PostgreSQL=group
##Abacus_Project_File = file

if (file.exists("C:/Program Files (x86)/LUMENS/AbacusCurve")){
abacusExecutable = "C:/Progra~2/LUMENS/AbacusCurve/abacus "
} else{
abacusExecutable = "C:/Progra~1/LUMENS/AbacusCurve/abacus "
}

systemCommand <- paste(abacusExecutable, Abacus_Project_File)

system(systemCommand)
