##SCIENDO-PostgreSQL=group
##proj.file=string
##csv_ques_c_db=string
##iteration=number 10
##statusoutput=output table

#=Load library
library(ggplot2)
library(foreign)
library(rtf)
library(reshape)
library(reshape2)
library(DBI)
library(RPostgreSQL)
library(rpostgis)
#include_peat=1

time_start<-paste(eval(parse(text=(paste("Sys.time ()")))), sep="")

#=Load active project
load(proj.file)

#=Read selected QUES-C database
QUESC_list<-read.table(csv_ques_c_db, sep=",")
colnames(QUESC_list)="Database"

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

#=Set all initial data, values, and working directory
QUESC_list_n<-nrow(QUESC_list)
dbase_all<-NULL
# periods and planning unit name
data<-as.character(QUESC_list[QUESC_list_n,1]) # get the last transition period as a central data
n_dta<-nchar(data)
t1<-as.integer(substr(data, (n_dta-7):(n_dta-4), (n_dta-4)))
t2<-as.integer(substr(data, (n_dta-3):n_dta, n_dta))
pu_name<-substr(data, 16:(n_dta-8), (n_dta-8))
# lookup table
pu_lut<-list_of_data_pu[which(tolower(list_of_data_pu$RST_NAME)==pu_name),]
lut.pu<-dbReadTable(DB, c("public", pu_lut$LUT_NAME))

lc_lut<-list_of_data_luc[which(list_of_data_luc$PERIOD==t1),]
lc_lu1<-dbReadTable(DB, c("public", lc_lut[1,]$LUT_NAME)) 

lc_lut<-list_of_data_luc[which(list_of_data_luc$PERIOD==t2),]
lc_lu2<-dbReadTable(DB, c("public", lc_lut[1,]$LUT_NAME)) 
# new directory 
idx_SCIENDO_led=idx_SCIENDO_led+1
dirAnnual<-paste(dirname(proj.file), "/SCIENDO/Annual_", pu_name, idx_SCIENDO_led, sep="")
dir.create(dirAnnual, mode="0777")
setwd(dirAnnual)
workingDirectory<-dirAnnual

#=Combine all database, calculate TPM and predicted area
get_central_data<-list_of_data_lut[which(tolower(list_of_data_lut$TBL_NAME)==data),]$TBL_DATA
central_data<-dbReadTable(DB, c("public", get_central_data))
# create key(LU_chg, Zone)
central_data$key<- do.call(paste, c(central_data[c("LU_CHG", "Z_NAME")], sep = " in "))
for(i in 1:QUESC_list_n) {
  data<-as.character(QUESC_list[i,1])
  get_data<-list_of_data_lut[which(tolower(list_of_data_lut$TBL_NAME)==data),]$TBL_DATA[1] # get the first if it has duplicates
  dbase<-dbReadTable(DB, c("public", get_data))
  n_dta<-nchar(data)
  t1<-as.integer(substr(data, (n_dta-7):(n_dta-4), (n_dta-4)))
  t2<-as.integer(substr(data, (n_dta-3):n_dta, n_dta))
  dbase$Start_year<-t1
  dbase$End_year<-t2
  dbase$nYear<-dbase$End_year-dbase$Start_year
  data2<-dbase
  
  data2$ID_LC1<-as.character(data2$ID_LC1)
  data2$ID_LC2<-as.character(data2$ID_LC2)
  # select unchanged areas 
  data2.1<-subset(data2, ID_LC1==ID_LC2)
  data2.1$ID_LC1<-as.factor(data2.1$ID_LC1)
  data2.1$ID_LC2<-as.factor(data2.1$ID_LC2) 
  # select changed areas
  data2.2<-subset(data2, ID_LC1!=ID_LC2)
  data2.2$ID_LC1<-as.factor(data2.2$ID_LC1)
  data2.2$ID_LC2<-as.factor(data2.2$ID_LC2)  
  
  # reckon how much changed areas per year 
  data2.2$COUNTx<-data2.2$COUNT/data2.2$nYear
  # find the total difference in N year
  data2.2$COUNTy<-data2.2$COUNT-data2.2$COUNTx
  # replace existing changed area with area per year 
  data2.2$COUNT<-data2.2$COUNTx
  data2.2$COUNTx<-NULL
  
  # aggregate the total difference on first period 
  data2.2melt <- melt(data = data2.2, id.vars=c('LC_t1','Z_NAME'), measure.vars=c('COUNTy'))
  data2.2cast <- dcast(data = data2.2melt, formula = LC_t1 + Z_NAME ~ ., fun.aggregate = sum,fill = 0, drop = FALSE)
  # add new key(LC_t1, Zone) to changed area
  data2.2cast$key<- do.call(paste, c(data2.2cast[c("LC_t1", "Z_NAME")], sep = " in "))
  data2.2cast$LC_t1<-NULL
  data2.2cast$Z_NAME<-NULL
  data2.2$COUNTy<-NULL
  
  # add also new key(LC_t1, Zone) to unchanged area
  data2.1$key<- do.call(paste, c(data2.1[c("LC_t1", "Z_NAME")], sep = " in "))
  # merge unchanged with changed area by key
  data2.1<-merge(data2.1, data2.2cast, by="key", all=TRUE)
  data2.1<-replace(data2.1, is.na(data2.1), 0)
  # sum unchanged area with aggregate value
  data2.1$COUNT<-data2.1$COUNT+data2.1$.
  data2.1$key<-NULL
  data2.1$.<-NULL
  # bind all of them to get the database which is changing in annual 
  data2ann<-rbind(data2.1,data2.2)
  
  # Calculate Tansition Probability Matrix
  n.zone<-nrow(as.data.frame(unique(data2ann$Z_NAME)))
  data2.melt <- melt(data = data2ann, id.vars=c('LC_t2','Z_NAME'), measure.vars=c('COUNT'))
  lu.count.zone.t2<- dcast(data = data2.melt, formula = LC_t2 + Z_NAME ~ ., fun.aggregate = sum,fill = 0, drop = FALSE)
  data2.melt <- melt(data = data2ann, id.vars=c('LC_t1','Z_NAME'), measure.vars=c('COUNT'))
  lu.count.zone.t1<- dcast(data = data2.melt, formula = LC_t1 + Z_NAME ~ ., fun.aggregate = sum, fill = 0, drop = FALSE)
  colnames(lu.count.zone.t1)[3]<-"COUNT.LU.ZONE.t1"
  colnames(lu.count.zone.t2)[3]<-"COUNT.LU.ZONE.t2"
  
  data2ann<-merge(data2ann,lu.count.zone.t1, by=c("LC_t1", "Z_NAME"), all=TRUE)
  data2ann<-replace(data2ann, is.na(data2ann), 0)
  data2ann<-merge(data2ann,lu.count.zone.t2, by.x=c("LC_t1", "Z_NAME"), by.y=c("LC_t2", "Z_NAME"), all=TRUE)
  data2ann<-replace(data2ann, is.na(data2ann), 0)
  eval(parse(text=(paste("data2ann$TPM", i, "<-data2ann$COUNT/data2ann$COUNT.LU.ZONE.t1", sep=""))))
  
  # Handling new emerging land use type in TPM
  # replace NA value, which is obtained from divided-by-zero, with zero
  data2ann <- replace(data2ann, is.na(data2ann), 0)
  # Get the total of TPM i-th according to first landcover period and zone
  data2.cek<- melt(data = data2ann, id.vars=c('ID_LC1','ZONE'), measure.vars=c(paste("TPM", i, sep="")))
  data2.cek<- dcast(data = data2.cek, formula = ID_LC1 + ZONE ~ ., fun.aggregate = sum, fill = 0, drop = FALSE)
  # Check if the TPM value is... 
  colnames(data2.cek)[3]<-"CEK"
  # equal to zero, then rename the column with 'Fix'
  # it means the specific record-with-zero have to be revalued  
  data2.cek1<-subset(data2.cek, CEK==0)
  if(nrow(data2.cek1)!=0){
    data2.cek1$ACT<-"Fix"
  }
  # more than zero, then rename the column with 'Ignore'
  # it means the specific record must keep the value 
  data2.cek2<-subset(data2.cek, CEK>0)
  if(nrow(data2.cek2)!=0){
    data2.cek2$ACT<-"Ignore"
  }
  # bind both the fixed and ignored table
  data2.cek<-rbind(data2.cek1,data2.cek2)
  data2.cek$CEK<-NULL
  # merge data2ann with data-bound table
  data3<-merge(data2ann, data2.cek, by=c("ID_LC1", "ZONE"), all=TRUE)
  data3<-replace(data3, is.na(data3), 0)
  data3.cek2<-subset(data3, ACT=="Ignore")
  data3.cek2<-data3.cek2[which(data3.cek2$LU_CHG!=0),]
  data3.cek1<-subset(data3, ACT=="Fix")
  data3.cek1$ID_LC1<-as.character(data3.cek1$ID_LC1)
  data3.cek1$ID_LC2<-as.character(data3.cek1$ID_LC2)
  # find unchanged land use/cover in fix-checked table
  # and set TPM1 value as 1 
  data3.cek1a<-subset(data3.cek1, ID_LC1==ID_LC2) 
  data3.cek1b<-subset(data3.cek1, ID_LC1!=ID_LC2) 
  if(nrow(data3.cek1a)!=0){
    data3.cek1a$ID_LC1<-as.factor(data3.cek1a$ID_LC1)
    data3.cek1a$ID_LC2<-as.factor(data3.cek1a$ID_LC2) 
    data3.cek1b$ID_LC1<-as.factor(data3.cek1b$ID_LC1)
    data3.cek1b$ID_LC2<-as.factor(data3.cek1b$ID_LC2)  
    eval(parse(text=(paste("data3.cek1a$TPM", i, "<-1", sep="")))) 
    data4<-rbind(data3.cek1a,data3.cek1b,data3.cek2)
  } else {
    data4<-data3.cek2
  }
  # finally, merge with central data by key(LU_chg, Zone)
  data4$key<- do.call(paste, c(data4[c("LU_CHG", "Z_NAME")], sep = " in "))
  eval(parse(text=(paste("data4<-subset(data4,select=c(key, TPM", i, "))", sep=""))))
  central_data<-merge(central_data, data4, by="key", all=TRUE)
}
# save the original data, the last period
data2ori<-data2
data2<-replace(central_data, is.na(central_data), 0)

# average the TPM
command<-NULL
for(j in 1:QUESC_list_n){
  if (j!=QUESC_list_n) {
    command<-paste(command,"data2$TPM", j, "+", sep="")
  } else {
    command<-paste(command,"data2$TPM", j, sep="")
  }
}
eval(parse(text=(paste("data2$TPM1<-(", command, ")/QUESC_list_n", sep="" ))))

# get annual count in first and second period 
n.zone<-nrow(as.data.frame(unique(data2$Z_NAME)))
data2.melt <- melt(data = data2, id.vars=c('LC_t2','Z_NAME'), measure.vars=c('COUNT'))
lu.count.zone.t2<- dcast(data = data2.melt, formula = LC_t2 + Z_NAME ~ ., fun.aggregate = sum, fill = 0, drop = FALSE)
data2.melt <- melt(data = data2, id.vars=c('LC_t1','Z_NAME'), measure.vars=c('COUNT'))
lu.count.zone.t1<- dcast(data = data2.melt, formula = LC_t1 + Z_NAME ~ ., fun.aggregate = sum, fill = 0, drop = FALSE)
colnames(lu.count.zone.t1)[3]<-"COUNT.LU.ZONE.t1"
colnames(lu.count.zone.t2)[3]<-"COUNT.LU.ZONE.t2"
data2<-merge(data2,lu.count.zone.t1, by=c("LC_t1", "Z_NAME"), all=TRUE)
data2<-merge(data2,lu.count.zone.t2, by.x=c("LC_t1", "Z_NAME"), by.y=c("LC_t2", "Z_NAME"), all=TRUE)
data2<-replace(data2, is.na(data2), 0)

#=Calculate predicted area at iteration 1
data4<-data2
data4$COUNT.it0<-data4$COUNT
data4$COUNT.it1<-data4$TPM1*data4$COUNT.LU.ZONE.t2

#=Calculate predicted area at next iteration
for (w in 2:iteration) {
  eval(parse(text=(paste("data4.melt <- melt(data = data4, id.vars=c('LC_t2','ZONE'), measure.vars=c('COUNT.it",w-1,"'))", sep=""))))
  eval(parse(text=(paste("lu.count.zone.t", w+1, "<- dcast(data = data4.melt, formula = LC_t2 + ZONE ~ ., fun.aggregate = sum, fill = 0, drop = FALSE)", sep=""))))
  eval(parse(text=(paste("colnames(lu.count.zone.t", w+1,')[3]<-"COUNT.LU.ZONE.t', w+1, '"', sep=""))))
  eval(parse(text=(paste('data4<-merge(data4,lu.count.zone.t', w+1, ', by.x=c("LC_t1", "ZONE"), by.y=c("LC_t2", "ZONE"), all=TRUE)', sep=""))))
  data4<-replace(data4, is.na(data4), 0)
  eval(parse(text=(paste("data4$COUNT.it", w, "<-data4$TPM1*data4$COUNT.LU.ZONE.t", w+1, sep=""))))
}

# calculate annual emission
annual_emission<-NULL
for (y in 1:iteration) {
  eval(parse(text=(paste("data4$em_t", y,"<-data4$COUNT.it", y, "*(data4$CARBON_t1-data4$CARBON_t2)*data4$ck_em*3.67", sep=""))))
  eval(parse(text=(paste("emtot<-sum(data4$em_t", y,")", sep=""))))
  annual_emission<-c(annual_emission, emtot)
}
# calculate annual sequestration
annual_sequestration<-NULL
for (x in 1:iteration) {
  eval(parse(text=(paste("data4$sq_t", x,"<-data4$COUNT.it", x, "*(data4$CARBON_t2-data4$CARBON_t1)*data4$ck_sq*3.67", sep=""))))
  eval(parse(text=(paste("sqtot<-sum(data4$sq_t", x,")", sep=""))))
  annual_sequestration<-c(annual_sequestration, sqtot)
}
# cumulative
cum_em<-cumsum(annual_emission)
cum_sq<-cumsum(annual_sequestration)
em<-as.data.frame(cbind(annual_emission, cum_em, annual_sequestration, cum_sq))
em$netem<-em$annual_emission-em$annual_sequestration
em$cum_netem<-cumsum(em$netem)

idx_lut<-idx_lut+1
eval(parse(text=(paste("in_lut", idx_lut, " <- data4", sep=""))))

eval(parse(text=(paste("list_of_data_lut<-data.frame(TBL_DATA='in_lut", idx_lut,"', TBL_NAME='AnnualDB_", pu_name, "', row.names=NULL)", sep=""))))
# save to PostgreSQL
InLUT_i <- paste('in_lut', idx_lut, sep="")
dbWriteTable(DB, InLUT_i, eval(parse(text=(paste(InLUT_i, sep="" )))), append=TRUE, row.names=FALSE)
dbWriteTable(DB, "list_of_data_lut", list_of_data_lut, append=TRUE, row.names=FALSE)

year<-as.character(QUESC_list [QUESC_list_n,1])
t0<-t2
t1<-t0+1
year_len<-iteration-1
yearsim<-c(paste(t0:(t0+year_len), t1:(t1+year_len), sep="-"))
# generate plot
em<-as.data.frame(cbind(yearsim,em))
em$yearsim<-factor(em$yearsim)
plot1<-ggplot(em,aes(yearsim,cum_em,group=1))+ geom_line(colour="red")+geom_point(colour="red", size=4, shape=21, fill="white")
plot2<-ggplot(em,aes(yearsim,annual_emission,group=1))+ geom_line(colour="red")+geom_point(colour="red", size=4, shape=21, fill="white")
plot3<-ggplot(em,aes(yearsim,annual_sequestration,group=1))+ geom_line(colour="red")+geom_point(colour="red", size=4, shape=21, fill="white")
plot4<-ggplot(em,aes(yearsim,cum_netem,group=1))+ geom_line(colour="red")+geom_point(colour="red", size=4, shape=21, fill="white")

#=Create .CAR file for new version of REDD Abacus
# check existing land use/cover from two period of time
if(pu_lut$LUT_NAME != "lut_Ref"){
  pu<-as.data.frame(lut.pu[,1])
  pu<-cbind(pu, lut.pu[,3])
} else {
  pu<-lut.pu
}
colnames(pu)[1] <- "ZONE"
colnames(pu)[2] <- "Z_NAME"

d1<-lc_lu1[which(lc_lu1$ID!=0),]
d2<-lc_lu2[which(lc_lu2$ID!=0),]
d1<-subset(d1, select=c(ID, Legend))
d2<-subset(d2, select=c(ID, Legend))
colnames(d1)[1] <- "ID_LC1"
colnames(d1)[2] <- "LC_t1"
colnames(d2)[1] <- "ID_LC2"
colnames(d2)[2] <- "LC_t2"

lu1.lost<-unique(data2$ID_LC2)[is.na(match(unique(data2$ID_LC2),unique(data2$ID_LC1)))]
lu2.lost<-unique(data2$ID_LC1)[is.na(match(unique(data2$ID_LC1),unique(data2$ID_LC2)))]
lu.lost<-c(as.integer(as.matrix(lu1.lost)),as.integer(as.matrix(lu2.lost)))
while(length(lu1.lost)!=0 || length(lu2.lost)!=0){
  if(length(lu1.lost)!=0){
    new.lu<-d2[d2$ID_LC2 %in% lu1.lost, 1:2]
    colnames(new.lu)[1]<-'ID_LC1'
    colnames(new.lu)[2]<-'LC_t1'
    d1<-rbind(d1,new.lu)
    lu1.lost<-unique(d2$ID_LC2)[is.na(match(unique(d2$ID_LC2),unique(d1$ID_LC1)))]
  } else if(length(lu2.lost)!=0){
    new.lu<-d1[d1$ID_LC1 %in% lu2.lost, 1:2]
    colnames(new.lu)[1]<-'ID_LC2'
    colnames(new.lu)[2]<-'LC_t2'
    d2<-rbind(d2,new.lu)
    lu2.lost<-unique(d1$ID_LC1)[is.na(match(unique(d1$ID_LC1),unique(d2$ID_LC2)))]
  }
}
colnames(d2)<-c("ID","CLASS")

name.matrix<-d2
name.matrix$order<-name.matrix$ID
name.matrix$order<-as.numeric(levels(name.matrix$order))[name.matrix$order]
name.matrix<- as.data.frame(name.matrix[order(name.matrix$order, decreasing=FALSE),])
name.matrix$order<-NULL

options(scipen=999)
Scenario_name<-gsub(" ","","Annual projection")

#=Create .CAR file for new version of REDD Abacus
# General and Project information
Gnrl.info.1<-c("file_version")
Gnrl.info.2<-c("1.2.0")
Gnrl.info<-paste(Gnrl.info.1,Gnrl.info.2,sep="=")
#fileConn<-file(paste(result_dir,"/",Scenario_name,".txt",sep=""))
text0<-"#GENERAL"
write(text0, paste(dirAnnual, "/",Scenario_name,".car",sep=""),append=TRUE, sep="\t")
write.table(Gnrl.info, paste(dirAnnual,"/",Scenario_name,".car",sep=""),append=TRUE,quote=FALSE,col.names=FALSE,row.names=FALSE,sep="\t")

Project.info.1<-c("title","description", "baseyear0", "baseyear1", "n_iteration")
Project.info.2<-c("SCIENDO", "Project description", t0, t1, iteration)
Project.info<-paste(Project.info.1,Project.info.2,sep="=")
text<-"\n#PROJECT"
write(text, paste(dirAnnual, "/",Scenario_name,".car",sep=""),append=TRUE, sep="\t")
write.table(Project.info, paste(dirAnnual,"/",Scenario_name,".car",sep=""),append=TRUE,quote=FALSE,col.names=FALSE,row.names=FALSE,sep="\t")

# Landcover information
text<-"\n#LANDCOVER"
write(text, paste(dirAnnual, "/",Scenario_name,".car",sep=""),append=TRUE, sep="\t")
name.matrix$lc_id<-0:(nrow(name.matrix)-1)
name.lc<-as.data.frame(name.matrix$lc_id)
name.lc$label<-name.matrix$CLASS
name.lc$description<-''
colnames(name.lc)[1]='//lc_id'
name.lc.temp<-name.lc
write.table(name.lc, paste(dirAnnual, "/",Scenario_name,".car",sep=""),append=TRUE,quote=FALSE,col.names=TRUE,row.names=FALSE,sep="\t")

# Zone information
text<-"\n#ZONE"
write(text, paste(dirAnnual, "/",Scenario_name,".car",sep=""),append=TRUE, sep="\t")
pu$order<-pu$ZONE
#pu$order<-as.numeric(levels(pu$order))[pu$order]
pu<-as.data.frame(pu[order(pu$order, decreasing=FALSE),])
pu$zone_id<-0:(nrow(pu)-1)
name.pu<-as.data.frame(pu$zone_id)
name.pu$label<-pu$Z_NAME
name.pu$description<-''
colnames(name.pu)[1]='//zone_id'
name.pu.temp<-name.pu
colnames(name.pu.temp)[2]='Z_NAME'
write.table(name.pu, paste(dirAnnual, "/",Scenario_name,".car",sep=""),append=TRUE,quote=FALSE,col.names=TRUE,row.names=FALSE,sep="\t")

# Landcover change
text<-"\n#LANDCOVER_CHANGE"
write(text, paste(dirAnnual, "/",Scenario_name,".car",sep=""),append=TRUE, sep="\t")
name.lcc<-data4
name.lcc$iteration_id<-name.lcc$'//scenario_id'<-0
name.lcc<-merge(name.lcc, name.pu.temp, by="Z_NAME")
colnames(name.lc.temp)[2]='LC_t1'
name.lcc<-merge(name.lcc, name.lc.temp, by="LC_t1")
name.lcc$lc1_id<-name.lcc$'//lc_id'
name.lcc$'//lc_id'<-NULL
colnames(name.lc.temp)[2]='LC_t2'
name.lcc<-merge(name.lcc, name.lc.temp, by="LC_t2")
name.lcc$lc2_id<-name.lcc$'//lc_id'
name.lcc<-name.lcc[c('//scenario_id','iteration_id','//zone_id','lc1_id','lc2_id','COUNT.it1')]
colnames(name.lcc)[3]='zone_id'
colnames(name.lcc)[4]='lc1_id'
colnames(name.lcc)[5]='lc2_id'
colnames(name.lcc)[6]='area'
name.lcc<-name.lcc[which(name.lcc$area != 0),]
write.table(name.lcc, paste(dirAnnual, "/",Scenario_name,".car",sep=""),append=TRUE,quote=FALSE,col.names=TRUE,row.names=FALSE,sep="\t")

# Carbon Stock
c1<-melt(data=data4, id.vars=c('LC_t1','CARBON_t1')) # it takes too long, need improvement
c1$variable<-c1$value<-NULL
c1<-unique(c1)
c2<-melt(data=data4, id.vars=c('LC_t2','CARBON_t2')) # it takes too long, need improvement
c2$variable<-c2$value<-NULL
c2<-unique(c2)
c1.lost<-unique(data4$CARBON_t2)[is.na(match(unique(data4$CARBON_t2),unique(data4$CARBON_t1)))]
c2.lost<-unique(data4$CARBON_t1)[is.na(match(unique(data4$CARBON_t1),unique(data4$CARBON_t2)))]
c.lost<-c(as.integer(as.matrix(c1.lost)),as.integer(as.matrix(c2.lost)))
while(length(c1.lost)!=0 || length(c2.lost)!=0){
  if(length(c1.lost)!=0){
    new.lu<-c2[c2$CARBON_t2 %in% c1.lost, 1:2]
    colnames(new.lu)[1]<-'LC_t1'
    colnames(new.lu)[2]<-'CARBON_t1'
    c1<-rbind(c1,new.lu)
    c1.lost<-unique(c2$CARBON_t2)[is.na(match(unique(c2$CARBON_t2),unique(c1$CARBON_t1)))]
  } else if(length(c2.lost)!=0){
    new.lu<-c1[c1$CARBON_t1 %in% c2.lost, 1:2]
    colnames(new.lu)[1]<-'LC_t2'
    colnames(new.lu)[2]<-'CARBON_t2'
    c2<-rbind(c2,new.lu)
    c2.lost<-unique(c1$CARBON_t1)[is.na(match(unique(c1$CARBON_t1),unique(c2$CARBON_t2)))]
  }
}
row.names(c2)<-NULL
c2<-na.omit(c2)
text<-"\n#CARBONSTOCK"
write(text, paste(dirAnnual, "/",Scenario_name,".car",sep=""),append=TRUE, sep="\t")
colnames(name.lc.temp)[2]<-"LC"
colnames(c2)[1]<-"LC"
colnames(c2)[2]<-"CARBON"
name.carbon.temp<-merge(name.lc.temp, c2, by="LC")
name.carbon.temp<-name.carbon.temp[c('//lc_id','CARBON')]
name.carbon<-data.frame()
for(i in 0:(nrow(name.pu)-1)){
  for(j in 1:nrow(name.lc)){
    name.carbon<-rbind(name.carbon, c(0, 0, i, name.carbon.temp$'//lc_id'[j], name.carbon.temp$CARBON[j]))
  }
}
colnames(name.carbon)=c('//scenario_id','iteration_id','zone_id','lc_id','area')
write.table(name.carbon, paste(dirAnnual, "/",Scenario_name,".car",sep=""),append=TRUE,quote=FALSE, col.names=TRUE,row.names=FALSE, sep="\t")

Abacus_Project_File = paste(dirAnnual, "/",Scenario_name,".car",sep="") #work with car file and also supported text file with abacus project format

# run REDD Abacus
abacusExecutable<-paste0("\"", LUMENS_path, "\\Abacus2\\abacus2\"")
systemCommand <- paste(abacusExecutable, Abacus_Project_File, "-ref LUMENS -wd", dirAnnual)
system(systemCommand)

#====summary area of projection from all iteration====
#====values were taken from text file in: /specified working directory/output/output.txt 
output_file<-readLines(paste(dirAnnual,"/output/output.txt",sep=""))
baris_summary<-as.numeric(pmatch('#MODEL_SUMMARY', output_file))
baris_summary<-baris_summary+11

all_summary<-as.data.frame(output_file[baris_summary:length(output_file)])
write.table(all_summary, paste(dirAnnual, "/output/all_summary.txt",sep=""), append=TRUE, quote=FALSE, col.names=FALSE, row.names=FALSE, sep=" ")
all_summary<-read.table(paste(dirAnnual, "/output/all_summary.txt",sep=""), sep="\t", header = T)
file.remove(paste(dirAnnual,  "/output/all_summary.txt",sep=""))

all_summary_melt<-melt(all_summary, id.vars=c('iteration','zone','landuse1','landuse2'), measure.vars=c('area'))
all_summary_cast<-cast(all_summary_melt, zone+landuse1+landuse2~iteration)
eval(parse(text=(paste("SCIENDO_AnnualDB_", pu_name, idx_SCIENDO_led, "<-all_summary_cast", sep=""))))

# eval(parse(text=(paste("resave(idx_SCIENDO_led, SCIENDO_AnnualDB_", pu_name, idx_SCIENDO_led, ", file=proj.file)", sep=""))))
resave(idx_SCIENDO_led, idx_lut, file=proj.file)

#====WRITE REPORT====
title<-"\\b\\fs32 LUMENS-SCIENDO - HISTORICAL BASELINE ANNUAL PROJECTION \\b0\\fs20"
date<-paste("Date : ", as.character(Sys.Date()), sep="")
time_start<-paste("Processing started : ", time_start, sep="")
time_end<-paste("Processing ended : ", eval(parse(text=(paste("Sys.time ()")))), sep="")
line<-paste("------------------------------------------------------------------------------------------------------------------------------------------------")
I_O_period_1_rep<-paste("\\b","\\fs20", period1)
I_O_period_2_rep<-paste("\\b","\\fs20", period2)
rtffile <- RTF("LUMENS_SCIENDO-Annual_Projection_report.doc", font.size=9)
addParagraph(rtffile, "\\b\\fs32 Hasil Analisis\\b0\\fs20")
addNewLine(rtffile)
addNewLine(rtffile)
addParagraph(rtffile, title)
addNewLine(rtffile)
addNewLine(rtffile)
addParagraph(rtffile, line)
addParagraph(rtffile, date)
addParagraph(rtffile, time_start)
addParagraph(rtffile, time_end)
addParagraph(rtffile, line)
addNewLine(rtffile)
addTable(rtffile,em, font.size=8) 
addNewLine(rtffile)
addPlot(rtffile,plot.fun=print, width=6.7,height=3,res=300, plot1)
addNewLine(rtffile)
addPlot(rtffile,plot.fun=print, width=6.7,height=3,res=300, plot2)
done(rtffile)

#=Writing final status message (code, message)
statuscode<-1
statusmessage<-"SCIENDO annual projection successfully completed!"
statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)
