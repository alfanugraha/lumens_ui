##QUES-PostgreSQL=group
##proj.file=string
##landuse_1=string
##landuse_2=string
##planning_unit=string
##lookup_c=string
##raster.nodata=number 0
#include_peat=selection Yes;No
#peatmap=string
#lookup_c_peat=string
##resultoutput=output table
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
library(jsonlite)
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

T1<-data_luc1$PERIOD
T2<-data_luc2$PERIOD

#=Set Working Directory
pu_name<-data_pu$RST_DATA 
idx_QUESC<-idx_QUESC+1
dirQUESC<-paste(dirname(proj.file), "/QUES/QUES-C/", idx_QUESC, "_QUESC_", T1, "_", T2, "_", pu_name, sep="")
dir.create(dirQUESC, mode="0777")

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
# peat
# if (include_peat == 1){
#   data_peat<-list_of_data_pu[which(list_of_data_pu$RST_NAME==peatmap),]
#   peat<-getRasterFromPG(pgconf, project, data_peat$RST_DATA, paste(data_peat$RST_DATA, '.tif', sep=''))
#   lookup_peat<-dbReadTable(DB, c("public", data_peat$LUT_NAME)) 
# }
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
# set lookup table
lookup_c<-lookup_c[which(lookup_c[1] != raster.nodata),]
lookup_lc<-lookup_c
lookup_ref<-lut_ref
colnames(lookup_lc)<-c("ID","LC","CARBON")
colnames(lookup_z)<-c("ID", "COUNT_ZONE", "ZONE")
colnames(lookup_ref)<-c("REF", "REF_NAME")

nLandCoverId<-nrow(lookup_lc)
nPlanningUnitId<-nrow(lookup_z)
nRefId<-nrow(lookup_ref)

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

#=Create land use change data dummy
#=Create cross-tabulation for reference
dummy1<-data.frame(nPU=lookup_ref$REF, divider=nLandCoverId*nLandCoverId)
dummy1<-expandRows(dummy1, 'divider')

dummy2<-data.frame(nT1=lookup_lc$ID, divider=nLandCoverId)
dummy2<-expandRows(dummy2, 'divider')
dummy2<-data.frame(nT1=rep(dummy2$nT1, nRefId))

dummy3<-data.frame(nT2=rep(rep(lookup_lc$ID, nLandCoverId), nRefId))

landUseChangeRefDummy<-cbind(dummy1, dummy2, dummy3)
colnames(landUseChangeRefDummy)<-c('REF', 'ID_LC1', 'ID_LC2')

R1<-(ref*1) + (landuse1*100^1)+ (landuse2*100^2) 
ref.db<-as.data.frame(freq(R1))
ref.db<-na.omit(ref.db)
n<-3
k<-0
ref.db$value_temp<-ref.db$value
while(k < n) {
  eval(parse(text=(paste("ref.db$Var", n-k, "<-ref.db$value_temp %% 100", sep=""))))  
  ref.db$value_temp<-floor(ref.db$value_temp/100)
  k=k+1
}
ref.db$value_temp<-NULL
colnames(ref.db) = c("ID_CHG", "COUNT", "REF", "ID_LC1", "ID_LC2")
ref.db<-merge(landUseChangeRefDummy, ref.db, by=c('REF', 'ID_LC1', 'ID_LC2'), all=TRUE)
ref.db$ID_CHG<-ref.db$REF*1 + ref.db$ID_LC1*100^1 + ref.db$ID_LC2*100^2
ref.db<-replace(ref.db, is.na(ref.db), 0)
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
  
  setwd(dirQUESC)
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
refMelt<-melt(data = ref.db, id.vars=c('REF'), measure.vars=c('COUNT'))
refArea<-dcast(data = refMelt, formula = REF ~ ., fun.aggregate = sum)

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

#=Modify carbon stock density for each time series
data_merge$ck_em<-data_merge$CARBON_t1>data_merge$CARBON_t2
data_merge$ck_sq<-data_merge$CARBON_t1<data_merge$CARBON_t2
data_merge$em<-(data_merge$CARBON_t1-data_merge$CARBON_t2)*data_merge$ck_em*data_merge$COUNT*3.67
data_merge$sq<-(data_merge$CARBON_t2-data_merge$CARBON_t1)*data_merge$ck_sq*data_merge$COUNT*3.67
data_merge$LU_CHG <- do.call(paste, c(data_merge[c("LC_t1", "LC_t2")], sep = " to "))
data_merge$null<-0
data_merge$nullCek<-data_merge$em+data_merge$sq

#=Generate area_zone lookup and calculate min area
area_zone<-melt(data = data_merge, id.vars=c('ZONE'), measure.vars=c('COUNT'))
area_zone<-dcast(data = area_zone, formula = ZONE ~ ., fun.aggregate = sum)
colnames(area_zone)[1]<-"ID"
colnames(area_zone)[2]<-"COUNT"
area_zone$ID<-as.numeric(as.character(area_zone$ID))
area_zone<-area_zone[with(area_zone, order(ID)),]
colnames(lookup_z)[1]<-"ID"
area_zone<-merge(area_zone, lookup_z, by="ID")
area<-min(sum(area_zone$COUNT), sum(data_merge$COUNT))

#=Generate administrative unit
colnames(refArea)[1]<-"ID"
colnames(refArea)[2]<-"COUNT"
colnames(lookup_ref)[1]<-"ID"
colnames(lookup_ref)[2]<-"KABKOT"
area_admin<-merge(refArea, lookup_ref, by="ID")

#=Calculate emission for each planning unit
zone_emission <- as.data.frame(zonal((Spat_res*emission),zone,'sum')) #adjust emission by actual raster area
zone_sequestration <- as.data.frame(zonal((Spat_res*sequestration),zone,'sum'))#adjust sequestration by actual raster area
colnames(zone_emission)[1] = "ID"
colnames(zone_emission)[2] = "Em_tot"
colnames(zone_sequestration)[1] = "ID"
colnames(zone_sequestration)[2]="Sq_tot"
zone_emission<-merge(area_zone,zone_emission,by="ID")
zone_carbon<-merge(zone_emission,zone_sequestration,by="ID")
zone_carbon$COUNT_ZONE<-NULL
zone_carbon$Net_em<-zone_carbon$Em_tot-zone_carbon$Sq_tot
zone_carbon$Net_em_rate<-round((zone_carbon$Net_em/zone_carbon$COUNT/period), digits=2)
zone_carbon[,4:7]<-round(zone_carbon[,4:7], digits=2)

#=Calculate emission for each administrative unit
admin_emission <- as.data.frame(zonal((Spat_res*emission),ref,'sum')) #adjust emission by actual raster area
admin_sequestration <- as.data.frame(zonal((Spat_res*sequestration),ref,'sum'))#adjust sequestration by actual raster area
colnames(admin_emission)[1] = "ID"
colnames(admin_emission)[2] = "Em_tot"
colnames(admin_sequestration)[1] = "ID"
colnames(admin_sequestration)[2]="Sq_tot"
admin_emission<-merge(area_admin,admin_emission,by="ID")
admin_carbon<-merge(admin_emission,admin_sequestration,by="ID")
admin_carbon$Net_em<-admin_carbon$Em_tot-admin_carbon$Sq_tot
admin_carbon$Net_em_rate<-round((admin_carbon$Net_em/admin_carbon$COUNT/period), digits=2)
admin_carbon[,4:7]<-round(admin_carbon[,4:7], digits=2)

#=Create final summary of emission calculation at landscape level
fs_id<-c(1,2,3,4,5,6,7)
fs_cat<-c("Period", "Total area", "Total Emisi (Ton CO2-eq)", "Total Sequestrasi (Ton CO2-eq)", "Emisi Bersih (Ton CO2-eq)", "Laju Emisi (Ton CO2-eq/tahun)","Laju emisi per-unit area (Ton CO2-eq/ha.tahun)")
fs_em<-sum(zone_carbon$Em_tot)
fs_sq<-sum(zone_carbon$Sq_tot)
fs_Nem<-fs_em-fs_sq
fs_Rem<-fs_Nem/period
fs_ARem<-fs_Rem/area
fs_summary<-c(proj_prop$period, area,round(fs_em, digits=2),round(fs_sq, digits=2),round(fs_Nem, digits=2),round(fs_Rem, digits=2),round(fs_ARem, digits=2))
fs_table<-data.frame(fs_id,fs_cat,fs_summary)
fs_table$fs_summary<-as.character(fs_table$fs_summary)
colnames(fs_table)<-c("ID", "Kategori", "Ringkasan")

#=Create QUES-C database
#=Zonal statistics database
lg<-length(unique(data_merge$ZONE))
zone_lookup<-area_zone
data_zone<-area_zone
data_zone$Z_CODE<-toupper(abbreviate(data_zone$Z_NAME))
data_zone$Rate_seq<-data_zone$Rate_em<-data_zone$Avg_C_t2<-data_zone$Avg_C_t1<-0
for(a in 1:lg){
  i<-unique(data_merge$ZONE)[a]
  data_z<-data_merge[which(data_merge$ZONE == i),]
  data_zone<-within(data_zone, {Avg_C_t1<-ifelse(data_zone$ID == i, sum(data_z$CARBON_t1*data_z$COUNT)/sum(data_z$COUNT),Avg_C_t1)}) 
  data_zone<-within(data_zone, {Avg_C_t2<-ifelse(data_zone$ID == i, sum(data_z$CARBON_t2*data_z$COUNT)/sum(data_z$COUNT),Avg_C_t2)}) 
  data_zone<-within(data_zone, {Rate_em<-ifelse(data_zone$ID == i, sum(data_z$em)/(sum(data_z$COUNT)*period),Rate_em)}) 
  data_zone<-within(data_zone, {Rate_seq<-ifelse(data_zone$ID == i, sum(data_z$sq)/(sum(data_z$COUNT)*period),Rate_seq)}) 
}
data_zone$COUNT_ZONE<-NULL
data_zone[,5:8]<-round(data_zone[,5:8],digits=2)

#=Emission
# calculate largest source of emission
data_merge_sel <- data_merge[ which(data_merge$nullCek > data_merge$null),]
order_sq <- as.data.frame(data_merge[order(-data_merge$sq),])
order_em <- as.data.frame(data_merge[order(-data_merge$em),])
# total emission
tb_em_total<-as.data.frame(cbind(order_em$LU_CHG, as.data.frame(round(order_em$em, digits=3))))
colnames(tb_em_total)<-c("LU_CHG", "em")
tb_em_total<-aggregate(em~LU_CHG,data=tb_em_total,FUN=sum)
tb_em_total$LU_CODE<-as.factor(toupper(abbreviate(tb_em_total$LU_CHG, minlength=5, strict=FALSE, method="both")))
tb_em_total<-tb_em_total[order(-tb_em_total$em),]
tb_em_total<-tb_em_total[c(3,1,2)]
tb_em_total$Percentage<-as.numeric(format(round((tb_em_total$em / sum(tb_em_total$em) * 100),2), nsmall=2))
tb_em_total_10<-head(tb_em_total,n=10)
# zonal emission
tb_em_zonal<-as.data.frame(NULL)
for (i in 1:length(zone_lookup$ID)){
  tryCatch({
    a<-(zone_lookup$ID)[i]
    tb_em<-as.data.frame(cbind(order_em$ZONE, order_em$LU_CHG, as.data.frame(round(order_em$em, digits=3))))
    colnames(tb_em)<-c("ZONE","LU_CHG", "em")
    tb_em_z<-as.data.frame(tb_em[which(tb_em$ZONE == a),])
    tb_em_z<-aggregate(em~ZONE+LU_CHG,data=tb_em_z,FUN=sum)
    tb_em_z$LU_CODE<-as.factor(toupper(abbreviate(tb_em_z$LU_CHG, minlength=5, strict=FALSE, method="both")))
    tb_em_z<-tb_em_z[order(-tb_em_z$em),]
    tb_em_z<-tb_em_z[c(1,4,2,3)]
    tb_em_z$Percentage<-as.numeric(format(round((tb_em_z$em / sum(tb_em_z$em) * 100),2), nsmall=2))
    tb_em_z_10<-head(tb_em_z,n=10)
    tb_em_zonal<-rbind(tb_em_zonal,tb_em_z_10)
  },error=function(e){cat("ERROR :",conditionMessage(e), "\n")})
}
# rm(tb_em, tb_em_total, tb_em_z, tb_em_z_10)

#=Sequestration
# total sequestration
tb_seq_total<-as.data.frame(cbind(order_sq$LU_CHG, as.data.frame(round(order_sq$sq, digits=3))))
colnames(tb_seq_total)<-c("LU_CHG", "seq")
tb_seq_total<-aggregate(seq~LU_CHG,data=tb_seq_total,FUN=sum)
tb_seq_total$LU_CODE<-as.factor(toupper(abbreviate(tb_seq_total$LU_CHG, minlength=5, strict=FALSE, method="both")))
tb_seq_total<-tb_seq_total[order(-tb_seq_total$seq),]
tb_seq_total<-tb_seq_total[c(3,1,2)]
tb_seq_total$Percentage<-as.numeric(format(round((tb_seq_total$seq / sum(tb_seq_total$seq) * 100),2), nsmall=2))
tb_seq_total_10<-head(tb_seq_total,n=10)
# zonal sequestration
tb_seq_zonal<-as.data.frame(NULL)
for (i in 1:length(zone_lookup$ID)){
  tryCatch({
    a<-(zone_lookup$ID)[i]
    tb_seq<-as.data.frame(cbind(order_sq$ZONE, order_sq$LU_CHG, as.data.frame(round(order_sq$sq, digits=3))))
    colnames(tb_seq)<-c("ZONE","LU_CHG", "seq")
    tb_seq_z<-as.data.frame(tb_seq[which(tb_seq$ZONE == i),])
    tb_seq_z<-aggregate(seq~ZONE+LU_CHG,data=tb_seq_z,FUN=sum)
    tb_seq_z$LU_CODE<-as.factor(toupper(abbreviate(tb_seq_z$LU_CHG, minlength=5, strict=FALSE, method="both")))
    tb_seq_z<-tb_seq_z[order(-tb_seq_z$seq),]
    tb_seq_z<-tb_seq_z[c(1,4,2,3)]
    tb_seq_z$Percentage<-as.numeric(format(round((tb_seq_z$seq / sum(tb_seq_z$seq) * 100),2), nsmall=2))
    tb_seq_z_10<-head(tb_seq_z,n=10)
    tb_seq_zonal<-rbind(tb_seq_zonal,tb_seq_z_10)
  },error=function(e){cat("ERROR :",conditionMessage(e), "\n")})
}
# rm(tb_seq, tb_seq_total, tb_seq_z, tb_seq_z_10)

#=Zonal additional statistics
if (((length(unique(data_merge$ID_LC1)))>(length(unique(data_merge$ID_LC2))))){
  dimention<-length(unique(data_merge$ID_LC1))
  name.matrix<-cbind(as.data.frame(data_merge$ID_LC1), as.data.frame(data_merge$LC_t1))
  name.matrix<-unique(name.matrix)
  colnames(name.matrix)<-c("ID","LC")
  name.matrix<-name.matrix[order(name.matrix$ID),]
  name.matrix$LC_CODE<-toupper(abbreviate(name.matrix$LC, minlength=4, method="both"))
} else{
  dimention<-length(unique(data_merge$ID_LC2))
  name.matrix<-cbind(as.data.frame(data_merge$ID_LC2), as.data.frame(data_merge$LC_t2))
  name.matrix<-unique(name.matrix)
  colnames(name.matrix)<-c("ID","LC")
  name.matrix<-name.matrix[order(name.matrix$ID),]
  name.matrix$LC_CODE<-toupper(abbreviate(name.matrix$LC, minlength=4, method="both"))
}

#=Transition matrix
# zonal emission matrix
e.m.z<-matrix(0, nrow=dimention, ncol=dimention)
em.matrix.zonal<-as.data.frame(NULL)
for (k in 1:length(zone_lookup$ID)){
  for (i in 1:nrow(e.m.z)){
    for (j in 1:ncol(e.m.z)){
      em.data<-data_merge_sel[which(data_merge_sel$ID_LC1==i & data_merge_sel$ID_LC2==j & data_merge_sel$ZONE==k),]
      e.m.z[i,j]<-as.numeric(round(sum(em.data$em), 2))
    }
  }
  e.m.z<-as.data.frame(e.m.z)
  e.m.z.c<-as.data.frame(cbind(name.matrix$LC_CODE,e.m.z))
  e.m.z.c<-cbind(rep(k,nrow(e.m.z)),e.m.z.c)
  em.matrix.zonal<-rbind(em.matrix.zonal,e.m.z.c)
}
colnames(em.matrix.zonal)<-c("ZONE","LC_CODE",as.vector(name.matrix$LC_CODE))
# rm(em.data, e.m.z, e.m.z.c)
# total emission matrix
e.m<-matrix(0, nrow=dimention, ncol=dimention)
for (i in 1:nrow(e.m)){
  for (j in 1:ncol(e.m)){
    em.data<-data_merge_sel[which(data_merge_sel$ID_LC1==i & data_merge_sel$ID_LC2==j),]
    e.m[i,j]<-round(sum(em.data$em), digits=2)
  }
}
e.m<-as.data.frame(e.m)
em.matrix.total<-as.data.frame(cbind(name.matrix$LC_CODE,e.m))
colnames(em.matrix.total)<-c("LC_CODE",as.vector(name.matrix$LC_CODE))
# rm(em.data, e.m)
# zonal sequestration matrix
s.m.z<-matrix(0, nrow=dimention, ncol=dimention)
seq.matrix.zonal<-as.data.frame(NULL)
for (k in 1:length(zone_lookup$ID)){
  for (i in 1:nrow(s.m.z)){
    for (j in 1:ncol(s.m.z)){
      seq.data<-data_merge_sel[which(data_merge_sel$ID_LC1==i & data_merge_sel$ID_LC2==j & data_merge_sel$ZONE==k),]
      s.m.z[i,j]<-round(sum(seq.data$sq), digits=2)
    }
  }
  s.m.z<-as.data.frame(s.m.z)
  s.m.z.c<-as.data.frame(cbind(name.matrix$LC_CODE,s.m.z))
  s.m.z.c<-cbind(rep(k,nrow(s.m.z)),s.m.z.c)
  seq.matrix.zonal<-rbind(seq.matrix.zonal,s.m.z.c)
}
colnames(seq.matrix.zonal)<-c("ZONE","LC_CODE",as.vector(name.matrix$LC_CODE))
# rm(seq.data, s.m.z, s.m.z.c)
# total sequestration matrix
s.m<-matrix(0, nrow=dimention, ncol=dimention)
for (i in 1:nrow(s.m)){
  for (j in 1:ncol(s.m)){
    seq.data<-data_merge_sel[which(data_merge_sel$ID_LC1==i & data_merge_sel$ID_LC2==j),]
    s.m[i,j]<-round(sum(seq.data$sq), digits=2)
  }
}
s.m<-as.data.frame(s.m)
seq.matrix.total<-as.data.frame(cbind(name.matrix$LC_CODE,s.m))
colnames(seq.matrix.total)<-c("LC_CODE",as.vector(name.matrix$LC_CODE))
# rm(seq.data, s.m, order_em, order_sq)

#=Save database
write.dbf(data_merge, paste0('QUESC_database_', T1, '-', T2, '.dbf'))

idx_lut<-idx_lut+1
eval(parse(text=(paste("in_lut", idx_lut, " <- data_merge", sep=""))))

eval(parse(text=(paste("list_of_data_lut<-data.frame(TBL_DATA='in_lut", idx_lut,"', TBL_NAME='out_hist_quesc_", tolower(pu_name), T1, T2, "', row.names=NULL)", sep=""))))
# save to PostgreSQL
InLUT_i <- paste('in_lut', idx_lut, sep="")
dbWriteTable(DB, InLUT_i, eval(parse(text=(paste(InLUT_i, sep="" )))), append=TRUE, row.names=FALSE)
dbWriteTable(DB, "list_of_data_lut", list_of_data_lut, append=TRUE, row.names=FALSE)

#=Rearrange zone carbon
zone_carbon_pub<-zone_carbon
colnames(zone_carbon_pub) <- c("ID", "Luas (Ha)", "Tutupan lahan", "Total emisi (Ton CO2-eq)", "Total sekuestrasi(Ton CO2-eq)", "Emisi bersih (Ton CO2-eq)", "Laju emisi (Ton CO2/Ha.yr)")
admin_carbon_pub<-admin_carbon
colnames(admin_carbon_pub) <- c("ID", "Luas (Ha)", "Wil. Administratif", "Total emisi (Ton CO2-eq)", "Total sekuestrasi(Ton CO2-eq)", "Emisi bersih (Ton CO2-eq)", "Laju emisi (Ton CO2/Ha.yr)")
data_zone_pub<-data_zone
data_zone_pub$Z_CODE<-NULL
colnames(data_zone_pub) <- c("ID", "Luas (Ha)", "Unit Perencanaan", "Rerata Karbon Periode 1", "Rerata Karbon Periode 2", "Emisi bersih", "Laju emisi")

#=Create QUES-C Report (.doc)
# create maps and charts for report
# arrange numerous colors with RColorBrewer
myColors1 <- brewer.pal(9,"Set1")
myColors2 <- brewer.pal(8,"Accent")
myColors3 <- brewer.pal(12,"Paired")
myColors4 <- brewer.pal(9, "Pastel1")
myColors5 <- brewer.pal(8, "Set2")
myColors6 <- brewer.pal(8, "Dark2")
myColors7 <- brewer.pal(11, "Spectral")
myColors8 <- rev(brewer.pal(11, "RdYlGn"))
myColors <- c(myColors8,myColors5,myColors1, myColors2, myColors3, myColors4, myColors7, myColors8)

# land use/cover map first period
myColors.lu <- myColors[1:length(unique(lookup_lc$ID))]
lookup_lc$Colors<-myColors.lu

lu1<-as.data.frame(unique(lu.db$ID_LC1))
colnames(lu1)<-"ID"
# lu1<-merge(lu1,lookup_lc, by="ID", all=TRUE)
# lu1<-within(lu1, {Colors<-ifelse(is.na(Colors), "#FF0000", Colors)})
lu1<-merge(lu1,lookup_lc, by="ID")
lu1$ID<-as.numeric(as.character(lu1$ID))
lu1<-lu1[order(lu1$ID),]
lu1<-rbind(lu1, c(0, NA, NA, '#FFFFFF')) # new line
ColScale.lu1<-scale_fill_manual(name="Tipe tutupan lahan t1", breaks=lu1$ID, labels=lu1$LC, values=lu1$Colors)
plot.LU1<-gplot(landuse1, maxpixels=100000) + geom_raster(aes(fill=as.factor(value))) +
  coord_equal() + ColScale.lu1 +
  theme(plot.title = element_text(lineheight= 5, face="bold")) +
  theme( axis.title.x=element_blank(),axis.title.y=element_blank(),
         panel.grid.major=element_blank(), panel.grid.minor=element_blank(),
         legend.title = element_text(size=8),
         legend.text = element_text(size = 6),
         legend.key.height = unit(0.25, "cm"),
         legend.key.width = unit(0.25, "cm"))

# land use/cover map next period
lu2<-as.data.frame(unique(lu.db$ID_LC2))
colnames(lu2)<-"ID"
# lu2<-merge(lu2,lookup_lc, by="ID", all=TRUE)
# lu2<-within(lu2, {Colors<-ifelse(is.na(Colors), "#FFFFFF", Colors)})
lu2<-merge(lu2,lookup_lc, by="ID")
lu2$ID<-as.numeric(as.character(lu2$ID))
lu2<-lu2[order(lu2$ID),]
lu2<-rbind(lu2, c(0, NA, NA, '#FFFFFF')) # new line
ColScale.lu2<-scale_fill_manual(name="Tipe tutupan lahan t2", breaks=lu2$ID, labels=lu2$LC, values=lu2$Colors)
plot.LU2<-gplot(landuse2, maxpixels=100000) + geom_raster(aes(fill=as.factor(value))) +
  coord_equal() + ColScale.lu2 +
  theme(plot.title = element_text(lineheight= 5, face="bold")) +
  theme( axis.title.x=element_blank(),axis.title.y=element_blank(),
         panel.grid.major=element_blank(), panel.grid.minor=element_blank(),
         legend.title = element_text(size=8),
         legend.text = element_text(size = 6),
         legend.key.height = unit(0.25, "cm"),
         legend.key.width = unit(0.25, "cm"))

myColors  <-c(myColors5,myColors1, myColors2, myColors3, myColors4, myColors7, myColors6, myColors8)

# zone
myColors.Z <- myColors[1:length(unique(lookup_z$ID))]
lookup_z$Colors<-myColors.Z
pu<-as.data.frame(unique(lu.db$ZONE))
colnames(pu)<-"ID"
pu<-merge(pu,lookup_z, by="ID", all=TRUE)
pu<-within(pu, {Colors<-ifelse(is.na(Colors), "#FFFFFF", Colors)})
pu$ID<-as.numeric(as.character(pu$ID))
pu<-pu[order(pu$ID),]
# pu<-rbind(pu, c(0, NA, NA, '#FFFFFF'))
ColScale.Z<-scale_fill_manual(name="Kelas Unit Perencanaan", breaks=pu$ID, labels=pu$Z_NAME, values=pu$Colors)
plot.Z<-gplot(zone, maxpixels=100000) + geom_raster(aes(fill=as.factor(value))) +
  coord_equal() + ColScale.Z +
  theme(plot.title = element_text(lineheight= 5, face="bold")) +
  theme( axis.title.x=element_blank(),axis.title.y=element_blank(),
         panel.grid.major=element_blank(), panel.grid.minor=element_blank(),
         legend.title = element_text(size=8),
         legend.text = element_text(size = 6),
         legend.key.height = unit(0.25, "cm"),
         legend.key.width = unit(0.25, "cm"))

# administrative 
myColors.Admin <- myColors[1:(length(unique(lookup_ref$ID))+1)]
ColScale.Admin<-scale_fill_manual(name="Wilayah Administratif", breaks=lookup_ref$ID, labels=lookup_ref$KABKOT, values=myColors.Admin)
plot.Admin<-gplot(ref, maxpixels=100000) + geom_raster(aes(fill=as.factor(value))) +
  coord_equal() + ColScale.Admin +
  theme(plot.title = element_text(lineheight= 5, face="bold")) +
  theme( axis.title.x=element_blank(),axis.title.y=element_blank(),
         panel.grid.major=element_blank(), panel.grid.minor=element_blank(),
         legend.title = element_text(size=8),
         legend.text = element_text(size = 6),
         legend.key.height = unit(0.25, "cm"),
         legend.key.width = unit(0.25, "cm"))

# rm(myColors7,myColors1, myColors2, myColors3, myColors4, myColors5, myColors6,myColors8)

# save carbon, emission, and sequestration maps 
setwd(dirQUESC)

color_pallete_cat <- c("#FFCC66", "#A5C663")
color_pallete_cont <- c("#62D849", "#0000f5", "#6B54D3")

writeRastFile(carbon1, paste0('carbon_', T1, '.tif'), cat = TRUE, colorpal = color_pallete_cat, lookup = lookup_lc)
writeRastFile(carbon2, paste0('carbon_', T2, '.tif'), cat = TRUE, colorpal = color_pallete_cat, lookup = lookup_lc)
writeRastFile(emission, paste0('emission_', T1, '-', T2, '.tif'), colorpal = color_pallete_cont)
writeRastFile(sequestration, paste0('sequestration_', T1, '-', T2, '.tif'), colorpal = color_pallete_cont)
# analysis_map=c('carbon1', 'carbon2', 'emission', 'sequestration')
# for(i in 1:length(analysis_map)){
#   idx_factor<-idx_factor+1
#   eval(parse(text=(paste('factor', idx_factor, '<-', analysis_map[i], sep=''))))  
#   eval(parse(text=(paste("list_of_data_f<-data.frame(RST_DATA='factor", idx_factor,"', RST_NAME='", analysis_map[i], "_", T1, T2,  "', row.names=NULL)", sep=""))))  
#   InFactor_i <- paste("factor", idx_factor, sep="")  
#   dbWriteTable(DB, "list_of_data_f", list_of_data_f, append=TRUE, row.names=FALSE)
#   #write to csv
#   list_of_data_f<-dbReadTable(DB, c("public", "list_of_data_f"))
#   csv_file<-paste(dirname(proj.file),"/csv_factor_data.csv", sep="")
#   write.table(list_of_data_f, csv_file, quote=FALSE, row.names=FALSE, sep=",")  
#   eval(parse(text=(paste("addRasterToPG(project, '", analysis_map[i], ".tif', InFactor_i, srid)", sep=''))))
# }
# unlink(list.files(pattern = ".tif"))
resave(idx_QUESC, idx_lut, idx_factor, file=proj.file)

# carbon t1 map
y<-ceiling( maxValue(carbon1)/100)
y<-y*100
plot.C1  <- gplot(carbon1, maxpixels=100000) + geom_raster(aes(fill=value)) + coord_equal() +
  scale_fill_gradient(name="Kerapatan karbon",low = "#FFCC66", high="#003300",limits=c(0,y), breaks=c(0,10,20,50,100,200,300), guide="colourbar") +
  theme(plot.title = element_text(lineheight= 5, face="bold")) +
  theme( axis.title.x=element_blank(),axis.title.y=element_blank(),
         panel.grid.major=element_blank(), panel.grid.minor=element_blank(),
         legend.title = element_text(size=8),
         legend.text = element_text(size = 7),
         legend.key.height = unit(1.5, "cm"),
         legend.key.width = unit(0.375, "cm"))
# carbon t2 map
plot.C2  <- gplot(carbon2, maxpixels=100000) + geom_raster(aes(fill=value)) + coord_equal() +
  scale_fill_gradient(name="Kerapatan karbon",low = "#FFCC66", high="#003300",limits=c(0,y), breaks=c(0,10,20,50,100,200,300), guide="colourbar") +
  theme(plot.title = element_text(lineheight= 5, face="bold")) +
  theme( axis.title.x=element_blank(),axis.title.y=element_blank(),
         panel.grid.major=element_blank(), panel.grid.minor=element_blank(),
         legend.title = element_text(size=8),
         legend.text = element_text(size = 7),
         legend.key.height = unit(1.5, "cm"),
         legend.key.width = unit(0.375, "cm"))
# carbon emission map
plot.E  <- gplot(emission, maxpixels=100000) + geom_raster(aes(fill=value)) + coord_equal() +
  scale_fill_gradient(name="Emisi (ton CO2-eq)",low = "#FFCC66", high="#FF0000", guide="colourbar") +
  theme(plot.title = element_text(lineheight= 5, face="bold")) +
  theme( axis.title.x=element_blank(),axis.title.y=element_blank(),
         panel.grid.major=element_blank(), panel.grid.minor=element_blank(),
         legend.title = element_text(size=8),
         legend.text = element_text(size = 8),
         legend.key.height = unit(0.375, "cm"),
         legend.key.width = unit(0.375, "cm"))
# carbon sequestration map
plot.S  <- gplot(sequestration, maxpixels=100000) + geom_raster(aes(fill=value)) + coord_equal() +
  scale_fill_gradient(name="Sequestrasi (ton CO2-eq)",low = "#FFCC66", high="#000033", guide="colourbar") +
  theme(plot.title = element_text(lineheight= 5, face="bold")) +
  theme( axis.title.x=element_blank(),axis.title.y=element_blank(),
         panel.grid.major=element_blank(), panel.grid.minor=element_blank(),
         legend.title = element_text(size=8),
         legend.text = element_text(size = 8),
         legend.key.height = unit(0.375, "cm"),
         legend.key.width = unit(0.375, "cm"))

# average zonal carbon rate t1
rcl.m.c1<-as.matrix(data_zone[,1])
rcl.m.c2<-as.matrix(data_zone[,5])
rcl.m<-cbind(rcl.m.c1,rcl.m.c2)
rcl.m<-rbind(rcl.m, c(0, NA))
Z.Avg.C.t1<-reclassify(zone, rcl.m)
plot.Z.Avg.C.t1<-gplot(Z.Avg.C.t1, maxpixels=100000) + geom_raster(aes(fill=value)) +
  coord_equal() + scale_fill_gradient(name="Carbon Density Level",low = "#FFCC66", high="#003300", guide="colourbar") +
  ggtitle(paste("Rerata Kerapatan Karbon", location, period1 )) +
  theme(plot.title = element_text(lineheight= 5, face="bold")) +
  theme( axis.title.x=element_blank(),axis.title.y=element_blank(),
         panel.grid.major=element_blank(), panel.grid.minor=element_blank(),
         legend.title = element_text(size=8),
         legend.text = element_text(size = 8),
         legend.key.height = unit(0.375, "cm"),
         legend.key.width = unit(0.375, "cm"))
# average zonal carbon rate t2
rcl.m.c1<-as.matrix(data_zone[,1])
rcl.m.c2<-as.matrix(data_zone[,6])
rcl.m<-cbind(rcl.m.c1,rcl.m.c2)
rcl.m<-rbind(rcl.m, c(0, NA))
Z.Avg.C.t2<-reclassify(zone, rcl.m)
plot.Z.Avg.C.t2<-gplot(Z.Avg.C.t2, maxpixels=100000) + geom_raster(aes(fill=value)) +
  coord_equal() + scale_fill_gradient(name="Carbon Density Level",low = "#FFCC66", high="#003300", guide="colourbar") +
  ggtitle(paste("Rerata Kerapatan Karbon", location, period2 )) +
  theme(plot.title = element_text(lineheight= 5, face="bold")) +
  theme( axis.title.x=element_blank(),axis.title.y=element_blank(),
         panel.grid.major=element_blank(), panel.grid.minor=element_blank(),
         legend.title = element_text(size=8),
         legend.text = element_text(size = 8),
         legend.key.height = unit(0.375, "cm"),
         legend.key.width = unit(0.375, "cm"))
# average zonal emission rate
rcl.m.c1<-as.matrix(data_zone[,1])
rcl.m.c2<-as.matrix(data_zone[,7])
rcl.m<-cbind(rcl.m.c1,rcl.m.c2)
rcl.m<-rbind(rcl.m, c(0, NA))
Z.Avg.em<-reclassify(zone, rcl.m)
plot.Z.Avg.em<-gplot(Z.Avg.em, maxpixels=100000) + geom_raster(aes(fill=value)) +
  coord_equal() + scale_fill_gradient(name="Tingkat Emisi",low = "#fff5f0", high="#67000d", guide="colourbar") +
  ggtitle(paste(" Rerata laju emisi", location, period1, "-", period2 )) +
  theme(plot.title = element_text(lineheight= 5, face="bold")) +
  theme( axis.title.x=element_blank(),axis.title.y=element_blank(),
         panel.grid.major=element_blank(), panel.grid.minor=element_blank(),
         legend.title = element_text(size=8),
         legend.text = element_text(size = 8),
         legend.key.height = unit(0.375, "cm"),
         legend.key.width = unit(0.375, "cm"))
# average zonal sequestration rate
rcl.m.c1<-as.matrix(data_zone[,1])
rcl.m.c2<-as.matrix(data_zone[,8])
rcl.m<-cbind(rcl.m.c1,rcl.m.c2)
rcl.m<-rbind(rcl.m, c(0, NA))
Z.Avg.sq<-reclassify(zone,rcl.m)
plot.Z.Avg.sq<-gplot(Z.Avg.sq, maxpixels=100000) + geom_raster(aes(fill=value)) +
  coord_equal() + scale_fill_gradient(name="Tingkat Sequestrasi",low = "#fff5f0", high="#67000d", guide="colourbar") +
  ggtitle(paste("Rerata laju sequestrasi", location, period1, "-", period2 )) +
  theme(plot.title = element_text(lineheight= 5, face="bold")) +
  theme( axis.title.x=element_blank(),axis.title.y=element_blank(),
         panel.grid.major=element_blank(), panel.grid.minor=element_blank(),
         legend.title = element_text(size=8),
         legend.text = element_text(size = 8),
         legend.key.height = unit(0.375, "cm"),
         legend.key.width = unit(0.375, "cm"))

# emission rate
emissionRate<-ggplot(data=zone_carbon, aes(x=reorder(Z_NAME, -Net_em_rate), y=(zone_carbon$Net_em_rate))) + geom_bar(stat="identity", fill="Red") +
  geom_text(data=zone_carbon, aes(label=round(Net_em_rate, 1)),size=4) +
  ggtitle(paste("Rerata laju emisi bersih", location, period1,"-", period2 )) + guides(fill=FALSE) + ylab("CO2-eq/ha.yr") +
  theme(plot.title = element_text(lineheight= 5, face="bold")) +
  theme(axis.title.x=element_blank(), axis.text.x = element_text(angle=20),
        panel.grid.major=element_blank(), panel.grid.minor=element_blank())
# largest emission
largestEmission<-ggplot(data=tb_em_total_10, aes(x=reorder(LU_CODE, -em), y=(em))) + geom_bar(stat="identity", fill="blue") +
  geom_text(data=tb_em_total_10, aes(x=LU_CODE, y=em, label=round(em, 1)),size=3, vjust=0.1) +
  ggtitle(paste("Sumber emisi terbesar", location )) + guides(fill=FALSE) + ylab("CO2-eq") +
  theme(plot.title = element_text(lineheight= 5, face="bold")) + scale_y_continuous() +
  theme(axis.title.x=element_blank(), axis.text.x = element_text(size=8),
        panel.grid.major=element_blank(), panel.grid.minor=element_blank())
# largest sequestration
largestSeq<-ggplot(data=tb_seq_total_10, aes(x=reorder(LU_CODE, -seq), y=(seq))) + geom_bar(stat="identity", fill="green") +
  geom_text(data=tb_seq_total_10, aes(x=LU_CODE, y=seq, label=round(seq, 1)),size=3, vjust=0.1) +
  ggtitle(paste("Sumber sequestrasi terbesar", location )) + guides(fill=FALSE) + ylab("CO2-eq") +
  theme(plot.title = element_text(lineheight= 5, face="bold")) + scale_y_continuous() +
  theme(axis.title.x=element_blank(), axis.text.x = element_text(size=8),
        panel.grid.major=element_blank(), panel.grid.minor=element_blank())

printArea <- function(x){
  format(x, digits=15, big.mark=",")
}
printRate <- function(x){
  format(x, digits=15, nsmall=2, decimal.mark=".", big.mark=",")
}

tabel_ket<-proj_descr
row.names(tabel_ket)<-NULL
tabel_ket$Type<-as.character(tabel_ket$Type)
colnames(tabel_ket)<-c("Tipe", "Keterangan")
tabel_ket[1,1]<-"Proyek"
tabel_ket[2,1]<-"Deskripsi"
tabel_ket[3,1]<-"Direktori"
tabel_ket[4,1]<-"Wilayah Analisis"
tabel_ket[5,1]<-"Provinsi"
tabel_ket[6,1]<-"Negara"

# write report
title1<-"{\\colortbl;\\red0\\green0\\blue0;\\red255\\green0\\blue0;\\red146\\green208\\blue80;\\red0\\green176\\blue240;\\red140\\green175\\blue71;\\red0\\green112\\blue192;\\red79\\green98\\blue40;} \\pard\\qr\\b\\fs70\\cf2 L\\cf3U\\cf4M\\cf5E\\cf6N\\cf7S \\cf1HASIL ANALISIS \\par\\b0\\fs20\\ql\\cf1"
title2<-paste("\\pard\\qr\\b\\fs40\\cf1 Modul QUES-C - Analisis Dinamika Cadangan Karbon \\par\\b0\\fs20\\ql\\cf1", sep="")
sub_title<-"\\cf2\\b\\fs32 ANALISIS DINAMIKA CADANGAN KARBON\\cf1\\b0\\fs20"
#rad_grk<-"\\pard\\qr\\b\\fs40\\cf1 Dokumen RAD GRK - Bab 2.3. Permasalahan Emisi GRK \\par\\b0\\fs20\\ql\\cf1"
test<-as.character(Sys.Date())
date<-paste("Date : ", test, sep="")
time_start<-paste("Proses dimulai : ", time_start, sep="")
time_end<-paste("Proses selesai : ", eval(parse(text=(paste("Sys.time ()")))), sep="")
line<-paste("------------------------------------------------------------------------------------------------------------------------------------------------")
area_name_rep<-paste("\\b", "\\fs20", location, "\\b0","\\fs20")
I_O_period_1_rep<-paste("\\b","\\fs20", period1)
I_O_period_2_rep<-paste("\\b","\\fs20", period2)
chapter1<-"\\b\\fs32 DATA YANG DIGUNAKAN \\b0\\fs20"
chapter2<-"\\b\\fs32 ANALISIS PADA TINGKAT BENTANG LAHAN \\b0\\fs20"
chapter3<-"\\b\\fs32 ANALISIS PADA TINGKAT UNIT PERENCANAAN \\b0\\fs20"

# ==== Report 0. Cover=====
rtffile <- RTF("QUES-C_report.doc", font.size=11, width = 8.267, height = 11.692, omi = c(0,0,0,0))
# INPUT
file.copy(paste0(LUMENS_path, "/ques_cover.png"), dirQUESC, recursive = FALSE)
img_location<-paste0(dirQUESC, "/ques_cover.png")
# loading the .png image to be edited
cover <- image_read(img_location)
# to display, only requires to execute the variable name, e.g.: "> cover"
# adding text at the desired location
text_submodule <- paste("Sub-Modul Karbon\n\nAnalisis Dinamika Cadangan Karbon\n", location, ", ", "Periode ", T1, "-", T2, sep="")
cover_image <- image_annotate(cover, text_submodule, size = 23, gravity = "southwest", color = "white", location = "+46+220", font = "Arial")
cover_image <- image_write(cover_image)
# 'gravity' defines the 'baseline' anchor of annotation. "southwest" defines the text shoul be anchored on bottom left of the image
# 'location' defines the relative location of the text to the anchor defined in 'gravity'
# configure font type
addPng(rtffile, cover_image, width = 8.267, height = 11.692)
addPageBreak(rtffile, width = 8.267, height = 11.692, omi = c(1,1,1,1))

addNewLine(rtffile)
addNewLine(rtffile)
addNewLine(rtffile)
addNewLine(rtffile)
addNewLine(rtffile)
addNewLine(rtffile)
addNewLine(rtffile)
addNewLine(rtffile)
addNewLine(rtffile)
addNewLine(rtffile)
addNewLine(rtffile)
addNewLine(rtffile)
addNewLine(rtffile)
addNewLine(rtffile)
addNewLine(rtffile)
addNewLine(rtffile)
addNewLine(rtffile)
addNewLine(rtffile)
addNewLine(rtffile)
addNewLine(rtffile)
addParagraph(rtffile, title1)
addParagraph(rtffile, title2)
#addNewLine(rtffile)
#addParagraph(rtffile, rad_grk)
addNewLine(rtffile)
addParagraph(rtffile, line)
addParagraph(rtffile, time_start)
addParagraph(rtffile, time_end)
addParagraph(rtffile, line)
addNewLine(rtffile)
width<-as.vector(c(1.34,3.1))
addTable(rtffile,tabel_ket,font.size=8,col.widths=width)
addPageBreak(rtffile)
addParagraph(rtffile, sub_title)
addNewLine(rtffile)
addParagraph(rtffile, line)
addParagraph(rtffile, date)
addParagraph(rtffile, time_start)
addParagraph(rtffile, time_end)
addParagraph(rtffile, line)
addNewLine(rtffile)
addParagraph(rtffile, "Analisis dinamika cadangan karbon dilakukan untuk perubahan cadangan karbon di suatu daerah pada satu kurun waktu. Metode yang digunakan adalah metode Stock Difference. Emisi dihitung sebagai jumlah penurunan cadangan karbon akibat perubahan tutupan lahan terjadi apabila cadangan karbon awal lebih tinggi dari cadangan karbon setelah terjadinya perubahan penggunaan lahan. Sebaliknya, sequestrasi dihitung sebagai jumlah penambahan cadangan karbon akibat perubahan tutupan lahan (cadangan karbon pada penggunaan lahan awal lebih rendah dari cadangan karbon setelah terjadinya perubahan penggunaan lahan).. Analisis ini dilakukan dengan menggunakan data peta tutupan lahan pada dua periode waktu yang berbeda dan tabel acuan kerapatan karbon untuk masing-masing tipe tutupan lahan. Selain itu, dengan memasukkan data unit perencanaan kedalam  analisis, dapat diketahui tingkat perubahan cadangan karbon pada masing-masing kelas unit perencanaan yang ada. Informasi yang dihasilkan melalui analisis ini dapat digunakan dalam proses perencanaan untuk berbagai hal, diantaranya menentukan prioritas aksi mitigasi perubahan iklim, mengetahui faktor pemicu terjadinya emisi, dan merencanakan skenario pembangunan di masa yang akan datang.")
addNewLine(rtffile)
addParagraph(rtffile, chapter1)
addParagraph(rtffile, line)
addNewLine(rtffile)
addParagraph(rtffile, "Data yang digunakan dalam analisis ini adalah data peta penggunaan lahan dan data peta unit perencanaan daerah. Data pendukung yang digunakan adalah peta acuan tipe penggunaan lahan, data acuan kerapatan karbon masing-masing tipe tutupan lahan dan data acuan kelas unit perencanaan.")
addNewLine(rtffile)

text <- paste("\\b \\fs20 Peta penutupan lahan \\b0 \\fs20 ", area_name_rep, "\\b \\fs20 tahun \\b0 \\fs20 ", I_O_period_1_rep, sep="")
addParagraph(rtffile, text)
addNewLine(rtffile, n=1)
addPlot.RTF(rtffile, plot.fun=plot, width=6.4, height=4, res=150, plot.LU1 )
#rm(plot.LU1)
text <- paste("\\b \\fs20 Peta penutupan lahan \\b0 \\fs20 ", area_name_rep, "\\b \\fs20 tahun \\b0 \\fs20 ", I_O_period_2_rep, sep="")
addParagraph(rtffile, text)
addNewLine(rtffile, n=1)
addPlot.RTF(rtffile, plot.fun=plot, width=6.7, height=4, res=150, plot.LU2 )
#rm(plot.LU2)
text <- paste("\\b \\fs20 Peta unit perencanaan \\b0 \\fs20 ", area_name_rep, sep="")
addParagraph(rtffile, text)
addNewLine(rtffile, n=1)
addPlot.RTF(rtffile, plot.fun=plot, width=6.7, height=4, res=150, plot.Z )
#rm(plot.Z)
text <- paste("\\b \\fs20 Peta wilayah administratif \\b0 \\fs20 ", area_name_rep, sep="")
addParagraph(rtffile, text)
addNewLine(rtffile, n=1)
addPlot.RTF(rtffile, plot.fun=plot, width=6.7, height=4, res=150, plot.Admin )
#rm(plot.Admin)
addNewLine(rtffile, n=1)
addNewLine(rtffile, n=1)
addNewLine(rtffile, n=1)
addNewLine(rtffile, n=1)
addParagraph(rtffile, chapter2)
addParagraph(rtffile, line)
addNewLine(rtffile)
addParagraph(rtffile, "Pada bagian ini disajikan hasil analisis dinamika cadangan karbon untuk keseluruhan bentang lahan yang dianalisis. Beberapa bentuk analisis yang dilakukan antara lain: tingkat emisi, tingkat sequestrasi, laju emisi dan tipe perubahan penggunaan lahan yang paling banyak menyebabkan emisi/sequestrasi.")

addNewLine(rtffile)
text <- paste("\\b \\fs20 Peta kerapatan karbon \\b0 \\fs20 ", area_name_rep, "\\b \\fs20 tahun \\b0 \\fs20 ", I_O_period_1_rep, " \\b \\fs20 (dalam Ton C/Ha)\\b0 \\fs20", sep="")
addParagraph(rtffile, text)
addPlot.RTF(rtffile, plot.fun=plot, width=6.7, height=4, res=150, plot.C1 )
#rm(plot.C1)
text <- paste("\\b \\fs20 Peta kerapatan karbon \\b0 \\fs20 ", area_name_rep, "\\b \\fs20 tahun \\b0 \\fs20 ", I_O_period_2_rep, " \\b \\fs20 (dalam Ton C/Ha)\\b0 \\fs20", sep="")
addParagraph(rtffile, text)
addNewLine(rtffile, n=1)
addPlot.RTF(rtffile, plot.fun=plot, width=6.7, height=4, res=150, plot.C2 )
addNewLine(rtffile, n=1)
#rm(plot.C2)
text <- paste("\\b \\fs20 Peta emisi karbon \\b0 \\fs20 ", area_name_rep, "\\b \\fs20 tahun \\b0 \\fs20 ", I_O_period_1_rep, "\\b \\fs20 - \\b0 \\fs20 ", I_O_period_2_rep, sep="")
addParagraph(rtffile, text)
addNewLine(rtffile, n=1)
addPlot.RTF(rtffile, plot.fun=plot, width=6.7, height=4, res=150, plot.E )
addNewLine(rtffile, n=1)
#rm(plot.E)
text <- paste("\\b \\fs20 Peta penyerapan karbon \\b0 \\fs20 ", area_name_rep, "\\b \\fs20 tahun \\b0 \\fs20 ", I_O_period_1_rep, "\\b \\fs20 - \\b0 \\fs20 ", I_O_period_2_rep, sep="")
addParagraph(rtffile, text)

addPlot.RTF(rtffile, plot.fun=plot, width=6.7, height=4, res=150, plot.S )
#rm(plot.S)
addNewLine(rtffile, n=1)
addNewLine(rtffile, n=1)
addParagraph(rtffile, "\\b \\fs20 Intisari perhitungan emisi\\b0 \\fs20")
addNewLine(rtffile, n=1)
fs_table[2,3]<-printArea(as.numeric(as.character(fs_table[2,3])))
fs_table[3,3]<-printRate(as.numeric(as.character(fs_table[3,3])))
fs_table[4,3]<-printRate(as.numeric(as.character(fs_table[4,3])))
fs_table[5,3]<-printRate(as.numeric(as.character(fs_table[5,3])))
fs_table[6,3]<-printRate(as.numeric(as.character(fs_table[6,3])))
fs_table[7,3]<-printRate(as.numeric(as.character(fs_table[7,3])))
addTable(rtffile, fs_table)
addNewLine(rtffile, n=1)

addParagraph(rtffile, "\\b \\fs20 Intisari perhitungan emisi per unit perencanaan\\b0 \\fs20")
addNewLine(rtffile, n=1)
data_zone_pub[2]<-printArea(data_zone_pub[2])
addTable(rtffile, data_zone_pub)
addNewLine(rtffile, n=1)

addNewLine(rtffile, n=1)
zone_carbon_pub[2]<-printArea(zone_carbon_pub[2])
zone_carbon_pub[4]<-printRate(zone_carbon_pub[4])
zone_carbon_pub[5]<-printRate(zone_carbon_pub[5])
zone_carbon_pub[6]<-printRate(zone_carbon_pub[6])
addTable(rtffile, zone_carbon_pub)
addNewLine(rtffile, n=1)
addParagraph(rtffile, "\\b \\fs20 Intisari perhitungan emisi per wilayah administrasi\\b0 \\fs20")
addNewLine(rtffile, n=1)
admin_carbon_pub[2]<-printArea(admin_carbon_pub[2])
admin_carbon_pub[4]<-printRate(admin_carbon_pub[4])
admin_carbon_pub[5]<-printRate(admin_carbon_pub[5])
admin_carbon_pub[6]<-printRate(admin_carbon_pub[6])
addTable(rtffile, admin_carbon_pub)
addParagraph(rtffile, "Keterangan : ")
addParagraph(rtffile, "Emisi bersih = Total emisi - Total sequestrasi ")
addParagraph(rtffile, "Laju emisi = (Total Emisi - Total Sequestrasi) / (luas * periode waktu) ")
addNewLine(rtffile, n=1)
addPlot.RTF(rtffile, plot.fun=plot, width=6.7, height=3, res=150, emissionRate )
addNewLine(rtffile, n=1)
# rm(emissionRate)
addPlot.RTF(rtffile, plot.fun=plot, width=6.7, height=4, res=150, plot.Z.Avg.C.t1 )
addNewLine(rtffile, n=1)
#rm(plot.Z.Avg.C.t1)
addPlot.RTF(rtffile, plot.fun=plot, width=6.7, height=4, res=150, plot.Z.Avg.C.t2 )
addNewLine(rtffile, n=1)
#rm(plot.Z.Avg.C.t2)
addPlot.RTF(rtffile, plot.fun=plot, width=6.7, height=4, res=150, plot.Z.Avg.em  )
addNewLine(rtffile, n=1)
#rm(plot.Z.Avg.em)
addPlot.RTF(rtffile, plot.fun=plot, width=6.7, height=4, res=150, plot.Z.Avg.sq )
#rm(plot.Z.Avg.sq)
addNewLine(rtffile, n=1)
addNewLine(rtffile, n=1)
addNewLine(rtffile, n=1)
addNewLine(rtffile, n=1)
addNewLine(rtffile, n=1)
addParagraph(rtffile, "\\b \\fs20 Sumber Emisi Terbesar\\b0 \\fs20")
addNewLine(rtffile, n=1)
tb_em_total_10[3]<-printRate(tb_em_total_10[3])
addTable(rtffile, tb_em_total_10)
addNewLine(rtffile, n=1)
addPlot.RTF(rtffile, plot.fun=plot, width=6.7, height=3, res=150, largestEmission )
addNewLine(rtffile, n=1)
# rm(largestEmission)
addParagraph(rtffile, "\\b \\fs20 Sumber sequestrasi terbesar\\b0 \\fs20")
addNewLine(rtffile, n=1)
tb_seq_total_10[3]<-printRate(tb_seq_total_10[3])
addTable(rtffile, tb_seq_total_10)
addNewLine(rtffile, n=1)

addPlot.RTF(rtffile, plot.fun=plot, width=6.7, height=3, res=150, largestSeq )
addNewLine(rtffile, n=1)
# rm(largestSeq)
addNewLine(rtffile, n=1)
addNewLine(rtffile, n=1)
addParagraph(rtffile, chapter3)
addParagraph(rtffile, line)
addNewLine(rtffile)
addParagraph(rtffile, "Pada bagian ini disajikan hasil analisis dinamika cadangan karbon untuk masing-masing kelas unit perencanaan yang dianalisis. Beberapa bentuk analisis yang dilakukan antara lain: tingkat emisi, tingkat sequestrasi, laju emisi dan tipe perubahan penggunaan lahan yang paling banyak menyebabkan emisi/sequestrasi.")
addNewLine(rtffile)

#z.emission.name<-as.vector(NULL)
#z.seq.name<-as.vector(NULL)
for(i in 1:length(zone_lookup$ID)){
  tryCatch({
    a<-zone_lookup$ID[i]
    zona<-paste("\\b", "\\fs20", i, "\\b0","\\fs20")
    zona_nm<-paste("\\b", "\\fs20", data_zone$Z_NAME[i], "\\b0","\\fs20")
    zona_ab<-paste("\\b", "\\fs20", data_zone$Z_CODE[i], "\\b0","\\fs20")
    addParagraph(rtffile, "\\b \\fs20 Sumber Emisi terbesar pada \\b0 \\fs20", zona,"\\b \\fs20 - \\b0 \\fs20", zona_nm, "\\b \\fs20 (\\b0 \\fs20", zona_ab, "\\b \\fs20)\\b0 \\fs20" )
    addNewLine(rtffile, n=1)
    
    tb_em_zon<-tb_em_zonal[which(tb_em_zonal$ZONE == a),]
    tb_em_zon$ZONE<-NULL
    tabel_em_zon<-tb_em_zon
    tabel_em_zon[3]<-printRate(tabel_em_zon[3])
    addTable(rtffile, tabel_em_zon)
    addNewLine(rtffile, n=1)
    
    #largest emission
    largestE.Z<-ggplot(data=tb_em_zon, aes(x=reorder(LU_CODE, -em), y=(em))) + geom_bar(stat="identity", fill="blue") +
      geom_text(data=tb_em_zon, aes(x=LU_CODE, y=em, label=round(em, 1)),size=3, vjust=0.1) +
      ggtitle(paste("Sumber Emisi Terbesar Pada",i, "-", data_zone$Z_CODE[i] )) + guides(fill=FALSE) + ylab("CO2-eq") +
      theme(plot.title = element_text(lineheight= 5, face="bold")) + scale_y_continuous() +
      theme(axis.title.x=element_blank(), axis.text.x = element_text(size=8),
            panel.grid.major=element_blank(), panel.grid.minor=element_blank())
    
    #png(filename=paste("Largest_Emission_Z_",a,".png", sep=""),type="cairo",units="in",width=6.7,height=4,res=125)
    #print(largestE.Z)
    #dev.off()
    
    #z.emission.name<-c(z.emission.name, paste("Largest_Emission_Z_",a,".png", sep=""))
    
    addPlot.RTF(rtffile, plot.fun=plot, width=6.7, height=3, res=150, largestE.Z )
    addNewLine(rtffile, n=1)
    
    addParagraph(rtffile, "\\b \\fs20 Sumber Sequestrasi Terbesar Pada \\b0 \\fs20", zona,"\\b \\fs20 - \\b0 \\fs20", zona_nm, "\\b \\fs20 (\\b0 \\fs20", zona_ab, "\\b \\fs20)\\b0 \\fs20" )
    addNewLine(rtffile, n=1)
    
    tb_seq_zon<-tb_seq_zonal[which(tb_seq_zonal$ZONE == a),]
    tb_seq_zon$ZONE<-NULL
    tabel_seq_zon<-tb_seq_zon
    tabel_seq_zon[3]<-printRate(tabel_seq_zon[3])    
    addTable(rtffile, tabel_seq_zon)
    addNewLine(rtffile, n=1)
    
    #largest sequestration
    largestS.Z<-ggplot(data=tb_seq_zon, aes(x=reorder(LU_CODE, -seq), y=(seq))) + geom_bar(stat="identity", fill="green") +
      geom_text(data=tb_seq_zon, aes(x=LU_CODE, y=seq, label=round(seq, 1)),size=3, vjust=0.1) +
      ggtitle(paste("Sumber Sequestrasi Terbesar Pada",i, "-", data_zone$Z_CODE[i] )) + guides(fill=FALSE) + ylab("CO2-eq") +
      theme(plot.title = element_text(lineheight= 5, face="bold")) + scale_y_continuous() +
      theme(axis.title.x=element_blank(), axis.text.x = element_text(size=8),
            panel.grid.major=element_blank(), panel.grid.minor=element_blank())
    
    #png(filename=paste("Largest_Seq_Z_",a,".png", sep=""),type="cairo",units="in",width=6.7,height=4,res=125)
    #print(largestS.Z)
    #dev.off()
    
    #z.seq.name<-c(z.seq.name, paste("Largest_Seq_Z_",a,".png", sep=""))
    
    addPlot.RTF(rtffile, plot.fun=plot, width=6.7, height=3, res=150, largestS.Z )
    addNewLine(rtffile, n=1)
    
  },error=function(e){cat("Nice try pal! ~ please re-check your input data :",conditionMessage(e), "\n"); addParagraph(rtffile, "no data");addNewLine(rtffile)})
}
# rm(largestE.Z, largestS.Z)
addNewLine(rtffile)
done(rtffile)

unlink(img_location)

eval(parse(text=(paste('rtf_QUESC_', T1, '_', T2, '_', pu_name, '<-rtffile', sep=''))))
eval(parse(text=(paste('resave(rtf_QUESC_', T1, '_', T2, '_', pu_name, ', file=proj.file)', sep=''))))

# command<-paste("start ", "winword ", dirQUESC, "/LUMENS_QUES-C_report.doc", sep="" )
# shell(command)

resultoutput<-data.frame(PATH=c(paste0(dirQUESC, '/carbon_', T1, '.tif'),
                                paste0(dirQUESC, '/carbon_', T2, '.tif'),
                                paste0(dirQUESC, '/emission_', T1, '-', T2, '.tif'),
                                paste0(dirQUESC, '/sequestration_', T1, '-', T2, '.tif'),
                                paste0(dirQUESC, '/QUESC_database_', T1, '-', T2, '.dbf')))

dbDisconnect(DB)

#=Writing final status message (code, message)
statuscode<-1
statusmessage<-"QUES-C analysis successfully completed!"
statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)
