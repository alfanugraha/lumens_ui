##QUES-PostgreSQL=group
##proj.file=string
##csv_ques_c_db=string
#include_peat=selection Yes;No
##statusoutput=output table

library(ggplot2)
library(foreign)
library(rtf)
library(reshape2)
library(RPostgreSQL)
library(DBI)
library(rpostgis)

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
# list_of_data_lut ==> list of data lookup table
list_of_data_lut<-dbReadTable(DB, c("public", "list_of_data_lut"))

QUESC_list_n<-nrow(QUESC_list)
dbase_all<-NULL

for(i in 1:QUESC_list_n) {
  data<-as.character(QUESC_list[i,1])
  n_dta<-nchar(data)
  t1<-as.integer(substr(data, (n_dta-7):(n_dta-4), (n_dta-4)))
  t2<-as.integer(substr(data, (n_dta-3):n_dta, n_dta))
  pu_name<-substr(data, 16:(n_dta-8), (n_dta-8))
  get_data<-list_of_data_lut[which(tolower(list_of_data_lut$TBL_NAME)==data),]$TBL_DATA[1] 
  dbase<-dbReadTable(DB, c("public", get_data))
  dbase<-subset(dbase, select=c(LC_t1,LC_t2,Z_NAME, COUNT, em, sq))
  dbase$Start_year<-t1
  dbase$End_year<-t2
  dbase$nYear<-dbase$End_year-dbase$Start_year
  dbase$em.rate<-dbase$em/dbase$nYear
  dbase$sq.rate<-dbase$sq/dbase$nYear
  dbase$COUNT.rate<-dbase$COUNT/dbase$nYear
  dbase$Z_CODE<-toupper(abbreviate(dbase$Z_NAME, minlength=3))
  dbase_all<-rbind(dbase_all, dbase)
}

dbase_all$period <- do.call(paste, c(dbase_all[c("Start_year", "End_year")], sep = "-"))
Comb_em.graph<-ggplot(dbase_all, aes(x = period, y = em, fill=factor(Z_CODE))) +
  geom_bar(stat='identity') + labs(y = "Emission (ton CO2)", x = "Period", fill = "Zone")
comb_em.graph.fac<-ggplot(dbase_all, aes(x = Z_CODE, y = em, fill=factor(Z_CODE))) +
  geom_bar(stat='identity') + coord_flip() + facet_wrap(~ period) + labs(y = "Emission (ton CO2)", x = "Zone", fill = "Period")
Comb_sq.graph<-ggplot(dbase_all, aes(x = period, y = sq,fill=factor(Z_CODE))) +
  geom_bar(stat='identity') + labs(y = "Sequestration (ton CO2)", x = "Period", fill = "Zone")
comb_sq.graph.fac<-ggplot(dbase_all, aes(x = Z_CODE, y = sq,fill=period)) +
  geom_bar(stat='identity') + coord_flip() + facet_wrap(~ period) + labs(y = "Sequestration (ton CO2)", x = "Zone", fill = "Period")

tb_em_total<-aggregate(em~period,data=dbase_all,FUN=sum)
tb_sq_total<-aggregate(sq~period,data=dbase_all,FUN=sum)
tb_em<-merge(tb_em_total, tb_sq_total, by="period")
tb_em_rate<-aggregate(em.rate~period,data=dbase_all,FUN=sum)
tb_sq_rate<-aggregate(sq.rate~period,data=dbase_all,FUN=sum)
tb_em<-merge(tb_em, tb_em_rate, by="period")
tb_em<-merge(tb_em, tb_sq_rate, by="period")
tb_em$net.em.rate<-tb_em$em.rate-tb_em$sq.rate

n.period<-nrow(tb_em)

ztb_em_melt <- melt(data = dbase_all, id.vars=c('Z_NAME','period'), measure.vars=c('em'))
ztb_em_melt_cast <- dcast(data = ztb_em_melt, formula = Z_NAME ~ period, fun.aggregate = sum)

ztb_em_rate<-aggregate(em.rate~Z_NAME,data=dbase_all,FUN=sum)
ztb_sq_rate<-aggregate(sq.rate~Z_NAME,data=dbase_all,FUN=sum)
ztb_em_rate$em.rate<-ztb_em_rate$em.rate/n.period
ztb_sq_rate$sq.rate<-ztb_sq_rate$sq.rate/n.period
ztb_em_melt_cast<-merge(ztb_em_melt_cast, ztb_em_rate, by="Z_NAME")
ztb_em_melt_cast<-merge(ztb_em_melt_cast, ztb_sq_rate, by="Z_NAME")

ztb_em_melt_cast$Z_CODE<-toupper(abbreviate(ztb_em_melt_cast$Z_NAME, minlength=3))

# if (include_peat==0) {
#   #SELECTING AVAILABLE QUES-C ANALYSIS
#   QUESC_peat_list<-as.data.frame(ls(pattern="QUESC_peat_emission_database"))
#   if(nrow(QUESC_peat_list)==0){
#     msgBox <- tkmessageBox(title = "QUES",
#                            message = "No peat list found",
#                            icon = "info",
#                            type = "ok")
#     quit()
#   }
#   colnames (QUESC_peat_list) [1]<-"Data"
#   QUESC_peat_list$Usage<-0
#   
#   repeat{
#     QUESC_peat_list<-edit(QUESC_peat_list)
#     if(sum(QUESC_peat_list$Usage)>2){
#       break
#     }
#   }
#   
#   QUESC_peat_list <- QUESC_peat_list[which(QUESC_peat_list$Usage==1),]
#   QUESC_peat_list$Usage<-NULL
#   QUESC_peat_list_n<-nrow(QUESC_peat_list)
#   dbase_peat_all<-NULL
#   
#   for(i in 1:QUESC_peat_list_n) {
#     data<-as.character(QUESC_peat_list [i,1])
#     t1<-as.integer(substr(data, 30:33, 33))
#     t2<-as.integer(substr(data, 35:38, 38))
#     eval(parse(text=(paste("dbase<-subset(QUESC_peat_emission_database_", t1,"_", t2, ", select=c(LC_t1,LC_t2,Z_NAME, COUNT, em_peat))", sep=""))))
#     dbase$Start_year<-t1
#     dbase$End_year<-t2
#     dbase$nYear<-dbase$End_year-dbase$Start_year
#     dbase$em_peat.rate<-dbase$em_peat/dbase$nYear
#     dbase$COUNT.rate<-dbase$COUNT/dbase$nYear
#     dbase$Z_CODE<-toupper(abbreviate(dbase$Z_NAME, minlength=3))
#     dbase_peat_all<-rbind(dbase_peat_all, dbase)
#   }
#   
#   dbase_peat_all$period <- do.call(paste, c(dbase_peat_all[c("Start_year", "End_year")], sep = "-"))
#   Comb_em_peat.graph<-ggplot(dbase_peat_all, aes(x = period, y = em_peat, fill=factor(Z_CODE))) +
#     geom_bar(stat='identity') + labs(y = "Peat Emission (ton CO2)", x = "Period", fill = "Zone")
#   comb_em_peat.graph.fac<-ggplot(dbase_peat_all, aes(x = Z_CODE, y = em_peat, fill=factor(Z_CODE))) +
#     geom_bar(stat='identity') + coord_flip() + facet_wrap(~ period) + labs(y = "Peat Emission (ton CO2)", x = "Zone", fill = "Period")
#   
#   tb_em_peat_total<-aggregate(em_peat~period,data=dbase_peat_all,FUN=sum)
#   tb_em_peat_rate<-aggregate(em_peat.rate~period,data=dbase_peat_all,FUN=sum)
#   
#   tb_em_peat_total<-merge(tb_em_peat_total, tb_em_peat_rate, by="period")
#   
#   n.period<-nrow(tb_em_peat_total)
#   
#   ztb_em_peat_melt <- melt(data = dbase_peat_all, id.vars=c('Z_NAME','period'), measure.vars=c('em_peat'))
#   ztb_em_peat_melt_cast <- dcast(data = ztb_em_peat_melt, formula = Z_NAME ~ period, fun.aggregate = sum)
#   
#   ztb_em_peat_rate<-aggregate(em_peat.rate~Z_NAME,data=dbase_peat_all,FUN=sum)
#   ztb_em_peat_rate$em_peat.rate<-ztb_em_peat_rate$em_peat.rate/n.period
#   ztb_em_peat_melt_cast<-merge(ztb_em_peat_melt_cast, ztb_em_peat_rate, by="Z_NAME")
#   
#   ztb_em_peat_melt_cast$Z_CODE<-toupper(abbreviate(ztb_em_peat_melt_cast$Z_NAME, minlength=3))
# } 

dirSummaryCarbon<-paste(dirname(proj.file), "/QUES/QUES-C/Summary", sep="")
dir.create(dirSummaryCarbon, mode="0777")
setwd(dirSummaryCarbon)

#====Create RTF Report File====
title1<-"{\\colortbl;\\red0\\green0\\blue0;\\red255\\green0\\blue0;\\red146\\green208\\blue80;\\red0\\green176\\blue240;\\red140\\green175\\blue71;\\red0\\green112\\blue192;\\red79\\green98\\blue40;} \\pard\\qr\\b\\fs70\\cf2 L\\cf3U\\cf4M\\cf5E\\cf6N\\cf7S \\cf1REPORT \\par\\b0\\fs20\\ql\\cf1"
title2<-paste("\\pard\\qr\\b\\fs40\\cf1 QUES-C Carbon Dynamics Analysis ", "for ", location, ", ", province, ", ", country, "\\par\\b0\\fs20\\ql\\cf1", sep="")
sub_title<-"\\cf2\\b\\fs32 ANALISA DINAMIKA CADANGAN KARBON\\cf1\\b0\\fs20"
line<-paste("------------------------------------------------------------------------------------------------------------------------------------------------")
area_name_rep<-paste("\\b", "\\fs20", location, "\\b0","\\fs20")
I_O_period_1_rep<-paste("\\b","\\fs20", period1)
I_O_period_2_rep<-paste("\\b","\\fs20", period2)
chapter1<-"\\b\\fs32 DATA YANG DIGUNAKAN \\b0\\fs20"
chapter2<-"\\b\\fs32 ANALISA PADA TINGKAT BENTANG LAHAN \\b0\\fs20"
chapter3<-"\\b\\fs32 ANALISA PADA TINGKAT UNIT PERENCANAAN \\b0\\fs20"
rtffile <- RTF("QUESC_multiple_period_report.doc", font.size=9)
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
addNewLine(rtffile)
addParagraph(rtffile, line)
addNewLine(rtffile)
width<-as.vector(c(1.34,3.1))
addTable(rtffile,proj_descr,font.size=8,col.widths=width)
addPageBreak(rtffile)
addParagraph(rtffile, sub_title)
addNewLine(rtffile)
addParagraph(rtffile, line)
#addParagraph(rtffile, date)
addParagraph(rtffile, line)
addNewLine(rtffile)
addParagraph(rtffile, "Analisa dinamika cadangan karbon dilakukan untuk perubahan cadangan karbon di suatu daerah pada satu kurun waktu. Metode yang digunakan adalah metode Stock Difference. Emisi dihitung sebagai jumlah penurunan cadangan karbon akibat perubahan tutupan lahan. Sebaliknya, sequestrasi dihitung sebagai jumlah penambahan cadangan karbon akibat perubahan tutupan lahan. Analisa ini dilakukan dengan menggunakan data peta tutupan lahan pada dua periode waktu yang berbeda dan tabel acuan kerapatan karbon untuk masing-masing tipe tutupan lahan. Selain itu, dengan memasukkan data unit perencanaan kedalam proses analisa, dapat diketahui tingkat perubahan cadangan karbon pada masing-masing kelas unit perencanaan yang ada. Informasi yang dihasilkan melalui analisa ini dapat digunakan dalam proses perencanaan untuk berbagai hal. Diantaranya adalah: menentukan prioritas aksi mitigasi perubahan iklim, mengetahui faktor pemicu pterjadinya emisi, merencanakan skenario pembangunan di masa yang akan datang, dan lain sebagainya.")
addNewLine(rtffile)
addTable(rtffile,tb_em,font.size=8)
addNewLine(rtffile)
addPlot.RTF(rtffile, plot.fun=plot, width=6.4, height=4, res=150, Comb_em.graph )
addNewLine(rtffile)
addPlot.RTF(rtffile, plot.fun=plot, width=6.4, height=4, res=150, Comb_sq.graph )
addNewLine(rtffile)
addTable(rtffile,ztb_em_melt_cast,font.size=8)
addNewLine(rtffile)
addPlot.RTF(rtffile, plot.fun=plot, width=6.4, height=4, res=150, comb_em.graph.fac )
addNewLine(rtffile)
addPlot.RTF(rtffile, plot.fun=plot, width=6.4, height=4, res=150, comb_sq.graph.fac )
addNewLine(rtffile)

# INCLUSION OF QUESC_Peat calculation
# if (include_peat==0) {
#   addParagraph(rtffile, "\\b\\fs32 Hasil analisis emisi karbon pada lahan gambut\\b0\\fs20")
#   addNewLine(rtffile)
#   addTable(rtffile,tb_em_peat_total,font.size=8)
#   addNewLine(rtffile)
#   addPlot.RTF(rtffile, plot.fun=plot, width=6.4, height=4, res=150, Comb_em_peat.graph )
#   addNewLine(rtffile)
#   addTable(rtffile,ztb_em_peat_melt_cast,font.size=8)
#   addNewLine(rtffile)
#   addPlot.RTF(rtffile, plot.fun=plot, width=6.4, height=4, res=150, comb_em_peat.graph.fac )
#   write.dbf(dbase_peat_all, "dbase_peat_all.dbf")
# } 

done(rtffile)

# write.dbf(dbase_all, "dbase_all.dbf")
statuscode<-1
statusmessage<-"Summarize multiple period successfully completed!"
statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)
