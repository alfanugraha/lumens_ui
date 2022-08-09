##QUES-PostgreSQL=group
##proj.file=string
##landuse_1=string
##landuse_2=string
##planning_unit=string
##raster.nodata=number 0
#include_peat=selection Yes;No
##peatmap=string
##peat_cell= string
##lookup_c_peat=string
##resultoutput=output table
##statusoutput=output table

# 14/12/2017

# attempt to calculate emission from peat decomposition

library(raster)
library(rtf)
library(data.table)
library(ggplot2)
library(RPostgreSQL)
library(rpostgis)
library(magick)
library(stringr)
library(spatial.tools)
library(rasterVis)
library(foreign)

# INPUT reading process
peat_cell <- read.csv(peat_cell, header=FALSE, sep=",")
peat_cell <- as.numeric(peat_cell[,1])

# DEFINE FUNCTIONS====
# 0. polygonize
# Define the function as written in https://johnbaumgartner.wordpress.com/2012/07/26/getting-rasters-into-shape-from-r/
gdal_polygonizeR <- function(x, outshape=NULL, gdalformat = 'ESRI Shapefile',
                             pypath= paste0(LUMENS_path,"/bin/gdal_polygonize.py"), readpoly=TRUE, quiet=TRUE) {
  if (isTRUE(readpoly)) require(rgdal)
  if (is.null(pypath)) {
    pypath <- Sys.which('gdal_polygonize.py')
  }
  if (!file.exists(pypath)) stop("Can't find gdal_polygonize.py on your system.")
  owd <- getwd()
  on.exit(setwd(owd))
  setwd(dirname(pypath))
  if (!is.null(outshape)) {
    outshape <- sub('\\.shp$', '', outshape)
    f.exists <- file.exists(paste(outshape, c('shp', 'shx', 'dbf'), sep='.'))
    if (any(f.exists))
      stop(sprintf('File already exists: %s',
                   toString(paste(outshape, c('shp', 'shx', 'dbf'),
                                  sep='.')[f.exists])), call.=FALSE)
  } else outshape <- tempfile()
  if (is(x, 'Raster')) {
    require(raster)
    writeRaster(x, {f <- tempfile(fileext='.tif')})
    rastpath <- normalizePath(f)
  } else if (is.character(x)) {
    rastpath <- normalizePath(x)
  } else stop('x must be a file path (character string), or a Raster object.')
  system2('python', args=(sprintf('"%1$s" "%2$s" -f "%3$s" "%4$s.shp"',
                                  pypath, rastpath, gdalformat, outshape)))
  if (isTRUE(readpoly)) {
    shp <- readOGR(dirname(outshape), layer = basename(outshape), verbose=!quiet)
    return(shp)
  }
  return(NULL)
}

# adding tables from inside a table list
add.lsTab <- function(x){
  pu_id <- unique(x$ZONE)
  x <- x[, c("ID_LC1", "ID_LC2", "HECT", "em_calc")]
  for(t in 1:2){
    # merging the 'x' with 'luc_lut' to get class names
    if(t == 1) p_text <- "semula" else p_text <- "setelah"
    x <- merge(x, luc_lut, by.x = paste0("ID_LC", t), by.y = "ID", all.x = TRUE)
    names(x)[names(x) == "Legend"] <- paste0("Tutupan ", p_text)
  }
  # subset columns
  x <- x[,c("Tutupan semula", "Tutupan setelah", "HECT", "em_calc")]
  # reorder the rows based on 'em_calc'
  x <- x[order(x$em_calc, decreasing = TRUE), ]
  # subset the rows when necessary
  if(nrow(x) > 10) x <- x[1:10,]
  names(x) <- c("Tutupan semula", "Tutupan setelah", "Luas*", "Emisi*")
  n.c <- ncol(x)
  al_col <- c("L", "L", replicate((n.c-2), "R"))
  text <- paste0("\\b ", lookup_z[lookup_z$ID == pu_id, "Legend"], "\\b0")
  addParagraph(rtffile, text)
  addTable(rtffile, x, font.size = 9, col.justify = al_col, header.col.justify = al_col)
  text <- paste0("\\fs16 *Luas dalam hektar; Emisi dalam ton CO2-eq\\fs16")
  addParagraph(rtffile, text)
  addNewLine(rtffile, n = 1)
}

# INPUTS=====
# proj.file="D:/LUMENS/trial/coarse_SS/coarse_SS.lpj"
# landuse_1="lu10_48s_100m"
# landuse_2="lu14_48s_100m"
# planning_unit="pu_IDH_48s_100m"
# raster.nodata= 0
# include_peat= 1
# peatmap= "dummy_peat"
# peat_cell=1
# lookup_c_peat= "lc_peat_em"

# blanko for resultoutput
resultoutput <- character()

# Parameterization and pre-processings====
load(proj.file) # loading the project file
# Static parameters and variables
time_start <- format(Sys.time())
# Static parameters and variables
time_start <- format(Sys.time())
# setting up the connection with the PostGre database system
driver <- dbDriver('PostgreSQL')
project <- as.character(proj_descr[1,2])
DB <- dbConnect(
  driver, dbname=project, host=as.character(pgconf$host), port=as.character(pgconf$port),
  user=as.character(pgconf$user), password=as.character(pgconf$pass)
)
# Setting up the working directory
setwd(paste0(dirname(proj.file), "/QUES"))
# derive the list of available data----
list_of_data_luc<-dbReadTable(DB, c("public", "list_of_data_luc"))
list_of_data_pu<-dbReadTable(DB, c("public", "list_of_data_pu"))
list_of_data_lut<-dbReadTable(DB, c("public", "list_of_data_lut"))
list_of_data_f<-dbReadTable(DB, c("public", "list_of_data_f"))
# reference map
ref.obj<-exists('ref')
ref.path<-paste(dirname(proj.file), '/reference.tif', sep='')
if(!ref.obj){
  if(file.exists(ref.path)){
    ref<-raster(ref.path)
  } else {
    ref<-getRasterFromPG(pgconf, project, 'ref_map', 'reference.tif')
  }
}
# planning unit
data_pu<-list_of_data_pu[which(list_of_data_pu$RST_NAME==planning_unit),]
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

# peat map====
peatmap <- list_of_data_pu[which(list_of_data_pu$RST_NAME==peatmap),]
# peat att.tble
pt_table <- dbReadTable(DB, c("public", peatmap$LUT_NAME))
peatmap <- getRasterFromPG(pgconf, project, peatmap$RST_DATA, paste0(peatmap$RST_DATA, ".tif"))

# lookup table carbon peat
lookup_c.pt <- list_of_data_lut[list_of_data_lut$TBL_NAME==lookup_c_peat,"TBL_DATA"]
lookup_c.pt <- dbReadTable(DB, c("public", lookup_c.pt))
# standardize the column names
names(lookup_c.pt)[1] <- "ID"
names(lookup_c.pt)[ncol(lookup_c.pt)] <- "Peat" # the table may contain only two columns or three

# identification of time dimension====
T_1 <- list_of_data_luc[list_of_data_luc$RST_NAME == landuse_1, "PERIOD"]
T_2 <- list_of_data_luc[list_of_data_luc$RST_NAME == landuse_2, "PERIOD"]

# summarize the lookup table for land use/cover classes
luc_1 <- dbReadTable(DB, c("public", list_of_data_luc[list_of_data_luc$RST_NAME == landuse_1, "LUT_NAME"]))
luc_2 <- dbReadTable(DB, c("public", list_of_data_luc[list_of_data_luc$RST_NAME == landuse_2, "LUT_NAME"]))
luc_lut <- unique(rbind(luc_1, luc_2)[, c("ID", "Legend")])
# load chg map
# define chg_db
# conditional testing for assessing the impact of the land use change in habitat conditions
# checking the availability of the change analysis in the database

t_mult <- abs((T_2-T_1))/2 # multiplier, in year
chg_db_name <- tolower(paste0("xtab_", planning_unit, T_1, T_2))
if(chg_db_name  %in% list_of_data_lut$TBL_NAME){
  # loading the lulc change cross table from postgre database as 'lu_db' dataframe
  chg_db <- list_of_data_lut[list_of_data_lut$TBL_NAME == chg_db_name, "TBL_DATA"]
  chg_db <- dbReadTable(DB, c("public", chg_db))
  # loading the associated raster file as 'lu_chg' raster
  lu_chg <- getRasterFromPG(pgconf, project, list_of_data_f[list_of_data_f$RST_NAME == gsub("xtab", "chgmap", chg_db_name), "RST_DATA"], paste0(gsub("xtab", "chgmap", chg_db_name), ".tif"))
} else{
  statuscode<-0
  statusmessage<-"Change analysis result of the selected period coudn't be found. Please run Pre-QUES before continuing"
  statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)
  quit()
}



# generate the subset====
# peat reclassification
rec_value <- pt_table$ID
rep_value <- replicate(length(rec_value), NA)
rep_value[which(rec_value %in% peat_cell)] <- 1
peatmap <- reclassify(peatmap, matrix(c(rec_value, rep_value), ncol = 2))
# FROM NOW ON, PEATMAP IS BOOLEAN 1=PEAT; NA= NONPEAT
# subset the lu_chg
chg_ptmap <- lu_chg * peatmap

# generate summary table which indicate the emission associated with the change occurring on the peat area====
chg_ptable <- freq(chg_ptmap)
chg_ptable <- as.data.frame(chg_ptable)
names(chg_ptable) <- c("ID", "COUNT")
chg_ptable$HECT <- chg_ptable$COUNT * res(ref)[1] ^ 2/10000 # area in hectare, only valid for maps with meter unit
chg_ptable <- chg_ptable[,c("ID", "HECT")]
# subset the chg_db based on the values exist in the newly created raster
sub.chg_db <- chg_db[chg_db$ID_CHG %in% chg_ptable$ID, ! names(chg_db) %in% "COUNT"]
# merge with the chg_ptable
chg_ptable <- merge(chg_ptable, sub.chg_db, by.x = "ID", by.y = "ID_CHG", all.x = TRUE)

# merge with the 'lookup_c.pt'
for(p in 1:2){ # 
  chg_ptable <- merge(chg_ptable, lookup_c.pt, by.x = paste0("ID_LC", p), by.y = "ID", all.x = TRUE)
  names(chg_ptable)[names(chg_ptable) == "Peat"] <- paste0("Cp_", eval(parse(text= paste0("T_", p))))
}

# calculate the total emission of each row
chg_ptable$raw_em <- t_mult*eval(parse(text= paste0("chg_ptable$Cp_", T_1, "+ chg_ptable$Cp_", T_2)))

chg_ptable$em_calc <- chg_ptable$raw_em * chg_ptable$HECT

# merge as data.table
chg_pdtable <- data.table(chg_ptable[, c("ZONE", "em_calc", "HECT")])
chg_pdtable <- chg_pdtable[, lapply(.SD, sum), by = list(ZONE)][!is.na(ZONE)]

# emission map: peat area either with emission or not
em_map <- reclassify(chg_ptmap, as.matrix(chg_ptable[,c("ID", "raw_em")]))

# plotting planning unit map====
myColors1 <- brewer.pal(9,"Set1")
myColors2 <- brewer.pal(8,"Accent")
myColors3 <- brewer.pal(12,"Paired")
myColors4 <- brewer.pal(9, "Pastel1")
myColors5 <- brewer.pal(8, "Set2")
myColors6 <- brewer.pal(8, "Dark2")
myColors7 <- rev(brewer.pal(11, "RdYlGn"))
myColors  <-c(myColors5,myColors1, myColors2, myColors3, myColors4, myColors7, myColors6)
area_zone<-lookup_z
colnames(area_zone)[1]<-'ID'
colnames(area_zone)[3]<-'ZONE'
myColors.Z <- myColors[1:length(unique(area_zone$ID))]
ColScale.Z<-scale_fill_manual(name="Unit Perencanaan", breaks=area_zone$ID, labels=area_zone$ZONE, values=myColors.Z)
plot.Z<-gplot(zone, maxpixels=100000) + geom_raster(aes(fill=as.factor(value))) +
  coord_equal() + ColScale.Z +
  theme(plot.title = element_text(lineheight= 5, face="bold")) + guides( fill = guide_legend(title.position = "top", ncol = 2)) +
  theme( legend.position = "bottom", axis.title.x=element_blank(), axis.title.y=element_blank(),
         panel.grid.major=element_blank(), panel.grid.minor=element_blank(),
         legend.title = element_text(size=8),
         legend.text = element_text(size = 6),
         legend.key.height = unit(0.25, "cm"),
         legend.key.width = unit(0.25, "cm"))

# plotting emission map====
# generate bg_poly
background <- ref/ref
bg_poly <- gdal_polygonizeR(background)
# maximum range of value
maxval <- ceiling(max(values(em_map), na.rm = TRUE))
# plotting functions
p.em_map <- gplot(em_map)
p.em_map <- p.em_map + geom_polygon(data = bg_poly, aes(x = long, y = lat, group = group), fill="#FFCC66", show.legend = FALSE) +
  geom_raster(aes(fill=value)) + scale_fill_gradient2(low = "#223BF8", mid = "#A0FD01", high="#FF6001", midpoint = maxval/2, guide="colourbar", na.value = NA)
p.em_map <- p.em_map + labs(fill = "Emisi Gambut") + coord_equal() + theme( axis.title.x=element_blank(),axis.title.y=element_blank(),
                                                                            panel.grid.major=element_blank(), panel.grid.minor=element_blank(),
                                                                            legend.title = element_text(size=8, face = "bold"),
                                                                            legend.text = element_text(size = 8),
                                                                            legend.key.height = unit(0.375, "cm"),
                                                                            legend.key.width = unit(0.375, "cm"))

# plotting the emission at the landscape level====
# generate the table as the basis
lsc_em_table <- chg_ptable[, c("ID_LC1", "ID_LC2", "em_calc")]
for(t in 1:2){
  # merging the 'lsc_em_table' with 'luc_lut' to get class names
  lsc_em_table <- merge(lsc_em_table, luc_lut, by.x = paste0("ID_LC", t), by.y = "ID", all.x = TRUE)
  names(lsc_em_table)[names(lsc_em_table) == "Legend"] <- paste0("LC_", t)
}
lsc_em_table <- data.table(lsc_em_table)
lsc_em_table <- lsc_em_table[, lapply(.SD, sum), by = list(ID_LC1, ID_LC2, LC_1, LC_2)][!is.na(em_calc)]
lsc_em_table <- as.data.frame(lsc_em_table)
lsc_em_table$abbr <- paste0(abbreviate(lsc_em_table$LC_1), "->", (abbreviate(lsc_em_table$LC_2)))
lsc_em_table <- lsc_em_table[order(lsc_em_table$em_calc, decreasing = TRUE), ]
lsc_em_table <- lsc_em_table[1:10, ]
# plotting functions----
lsc_em.plot <- ggplot(lsc_em_table, aes(x = reorder(abbr, -em_calc), y = em_calc)) + geom_bar(stat = "identity")
# rotate the axis text
lsc_em.plot <- lsc_em.plot + theme(axis.text.x = element_text(angle = 45, hjust = 1, vjust = 1)) + labs(x = "", y = "Emisi (ton CO2 eq)")
# legend table: list of abbreviation
abbr_leg <- lsc_em_table[, c("abbr", "LC_1", "LC_2")]
names(abbr_leg) <- c("Singkatan", paste0("Kelas tutupan ", T_1), paste0("Kelas tutupan ", T_2))
# table for each planning unit with peat====
pu.chg_ptable <- split(chg_ptable, f = chg_ptable$ZONE)
# sort records in each table in the list based on the amount of peat emission
pu.chg_ptable <- lapply(pu.chg_ptable, function(x) x[order(x$em_calc, decreasing = TRUE),])
# sort the table according to the total emission
pu.chg_ptable <- pu.chg_ptable[eval(parse(text=paste0("as.character(", as.character(chg_pdtable[order(chg_pdtable$em_calc, decreasing = TRUE), "ZONE"]), ")")))]

# merge chg_pdtable with lookup_Z to obtain the planning unit names
chg_pdtable <- merge(chg_pdtable, lookup_z[,c("ID", "Legend")], by.x = "ZONE", by.y = "ID", all.x =TRUE)
chg_pdtable <- chg_pdtable[ order(chg_pdtable$em_calc, decreasing = TRUE), c("Legend", "HECT", "em_calc")]
# adding total summary
chg_pdtable <- rbind(chg_pdtable, data.frame(Legend = "TOTAL", HECT = sum(chg_pdtable$HECT), em_calc = sum(chg_pdtable$em_calc), stringsAsFactors = FALSE))
names(chg_pdtable)[names(chg_pdtable) == "Legend"] <- "Unit Perencanaan"
names(chg_pdtable)[2:3] <- c("Luas*", "Emisi*")
# redirect into the dirQUESC to save reports and other data====
dirQUESC<-paste(dirname(proj.file), "/QUES/QUES-C/", idx_QUESC, "_QUESC_", T_1, "_", T_2, "_", planning_unit, sep="")
dir.create(dirQUESC, mode="0777")
setwd(dirQUESC)

# Reporting system
#====Create RTF Report File====
# title<-"\\b\\fs32 LUMENS-QUES Project Report\\b0\\fs20"
title<-"\\b\\fs32 Laporan Proyek LUMENS-\\i QUES\\b0\\fs32"
# sub_title<-"\\b\\fs28 Sub-modules: Biodiversity Analysis\\b0\\fs20"
sub_title<-"\\b\\fs28 Sub-modul: Karbon-Gambut\\b0\\fs28"
test<-as.character(Sys.Date())
date<-paste("Tanggal : ", test, sep="")
t_start<-paste("Proses dimulai : ", time_start, sep="")
time_end<-paste("Proses selesai : ", eval(parse(text=(paste("Sys.time ()")))), sep="")
line<-paste("------------------------------------------------------------------------------------------------------------------------------------------")
area_name_rep<-paste0("\\b", "\\fs22 ", location, "\\b0","\\fs22")
I_O_period_1_rep<-paste0("\\b","\\fs22 ", as.character(T_1), "\\b0","\\fs22")
I_O_period_2_rep<-paste0("\\b","\\fs22 ", as.character(T_2), "\\b0","\\fs22")
chapter1<-"\\b\\fs28 1. EMISI AKIBAT DEKOMPOSISI GAMBUT DI TINGKAT BENTANG LAHAN\\b0\\fs28"
chapter2<-"\\b\\fs28 2. ANALISIS UNIT PERENCANAAN \\b0\\fs28"


# ==== Report 0. Cover=====
rtffile <- RTF("QUES-Cpeat_report.doc", font.size=11, width = 8.267, height = 11.692, omi = c(0,0,0,0))
# INPUT
img_location <- paste0(LUMENS_path, "/ques_cover.png")
# loading the .png image to be edited
cover <- image_read(img_location)
# to display, only requires to execute the variable name, e.g.: "> cover"
# adding text at the desired location
text_submodule <- paste("Sub-Modul Karbon\n\nAnalisis Emisi akibat Dekomposisi Gambut\ndan Keterkaitannya dengan\nPerubahan Penggunaan Lahan\n\n", location, ", ", "Periode ", T_1, "-", T_2, sep="")
cover_image <- image_annotate(cover, text_submodule, size = 23, gravity = "southwest", color = "white", location = "+46+220", font = "Arial")
cover_image <- image_write(cover_image)
# 'gravity' defines the 'baseline' anchor of annotation. "southwest" defines the text shoul be anchored on bottom left of the image
# 'location' defines the relative location of the text to the anchor defined in 'gravity'
# configure font type
addPng(rtffile, cover_image, width = 8.267, height = 11.692)
addPageBreak(rtffile, width = 8.267, height = 11.692, omi = c(1,1,1,1))

# rtffile <- RTF("LUMENS_QUES-B_report.lpr", font.size=10, width = 8.267, height = 11.692, omi = c(1,1,1,1))
addParagraph(rtffile, title)
addParagraph(rtffile, sub_title)
addNewLine(rtffile)
addParagraph(rtffile, line)
addParagraph(rtffile, date)
addParagraph(rtffile, t_start)
addParagraph(rtffile, time_end)
# addParagraph(rtffile, time_end)
addParagraph(rtffile, line)
# ==== Report 0.1 Table of Contents page====
addPageBreak(rtffile, width = 8.267, height = 11.692, omi = c(1,1,1,1))
addHeader(rtffile, title = "\\qc\\b\\fs28 DAFTAR ISI\\b0\\fs28", TOC.level = 1)
addNewLine(rtffile, n = 1.5)
addTOC(rtffile)
addPageBreak(rtffile, width = 8.267, height = 11.692, omi = c(1,1,1,1))
#==== Report I. EMISI AKIBAT DEKOMPOSISI GAMBUT DI TINGKAT BENTANG LAHAN ====
addHeader(rtffile, chapter1, TOC.level = 1)
addNewLine(rtffile, n = 1.5)
addNewLine(rtffile)
# planning unit map
text <- paste("\\b Peta Unit Perencanaan \\b0", area_name_rep)
addParagraph(rtffile, text)
addPlot.RTF(rtffile, plot.fun=print, width=6.27, height = (4 + 0.24 + round(nrow(lookup_z)/2, digits = 0)*0.14), res=150, plot.Z)
addNewLine(rtffile, n=1)
# emission map
text <- paste("\\b Peta Emisi akibat Dekomposisi Gambut \\b0 ",area_name_rep, " \\b  tahun \\b0", I_O_period_1_rep, "\\b  - \\b0", I_O_period_2_rep, sep="")
addParagraph(rtffile, text)
addPlot.RTF(rtffile, plot.fun=print, width=6.27, height=4, res=150, p.em_map)
# bar chart to visualize the 
text <- paste("\\b Kontribusi Tipologi Perubahan Penggunaan Lahan terhadap Emisi Gambut \\b0 ",area_name_rep, " \\b  tahun \\b0", I_O_period_1_rep, "\\b  - \\b0", I_O_period_2_rep, sep="")
addParagraph(rtffile, text)
addPlot.RTF(rtffile, plot.fun=print, width=4.3, height=5, res=150, lsc_em.plot)
addNewLine(rtffile, n=1)
text <- paste0("\\b Keterangan\\b0")
addParagraph(rtffile, text)
addTable(rtffile, abbr_leg, font.size = 9, col.justify = c("L", "R", "R"), header.col.justify = c("L", "R", "R"))
addNewLine(rtffile, n=1)
# summary table for each planning unit
text <- paste("\\b Kontribusi Unit Perencanaan terhadap Emisi Gambut \\b0 ",area_name_rep, " \\b  tahun \\b0", I_O_period_1_rep, "\\b  - \\b0", I_O_period_2_rep, sep="")
addParagraph(rtffile, text)
addTable(rtffile, chg_pdtable, font.size = 9, col.justify = c("L", "R", "R"), header.col.justify = c("L", "R", "R"))
text <- paste0("*Luas dalam hektar; Emisi dalam Ton CO2-eq")
addNewLine(rtffile, n=1)
#==== Report II. ANALISIS UNIT PERENCANAAN ====
addHeader(rtffile, chapter2, TOC.level = 1)
addNewLine(rtffile, n=1.5)
# plot the tables
lapply(pu.chg_ptable, add.lsTab)
# lsc_em.plot abbr_leg
done(rtffile)
# resaving indices and rtffile====
eval(parse(text=paste0("QUESCp", "_", planning_unit, "_", T_1, "_", T_2, " <- rtffile")))
eval(parse(text = paste0("resave(QUESCp", "_", planning_unit, "_", T_1, "_", T_2, ", file = proj.file)")))
# saving tables and maps as hard files and into postgis
# 1. chg_ptable into postgis
# save table into postgre
idx_lut <- idx_lut+1
dbWriteTable(DB, paste0("in_lut", idx_lut), chg_ptable, append=TRUE, row.names=FALSE)
# update the list_of_data_lut both in LUMENS_path_user as well as in postgre
list_of_data_lut <- data.frame(TBL_DATA = paste0("in_lut", idx_lut), TBL_NAME = paste0("Cpeat_",planning_unit, "_", T_1, T_2), stringsAsFactors = FALSE)
dbWriteTable(DB, "list_of_data_lut", list_of_data_lut, append=TRUE, row.names=FALSE)
# update the list_of_data_lut in 'LUMENS_path_user'
list_of_data_lut <- dbReadTable(DB, c("public", "list_of_data_lut"))
write.csv(list_of_data_lut, paste0(LUMENS_path_user, "/list_of_data_lut.csv"), row.names = FALSE)
# 2. chg_pdtable as .dbf (resultoutput)
# save table into postgre
idx_lut <- idx_lut+1
dbWriteTable(DB, paste0("in_lut", idx_lut), chg_pdtable, append=TRUE, row.names=FALSE)
# update the list_of_data_lut both in LUMENS_path_user as well as in postgre
list_of_data_lut <- data.frame(TBL_DATA = paste0("in_lut", idx_lut), TBL_NAME = paste0("Cpeat_sum_",planning_unit, "_", T_1, T_2), stringsAsFactors = FALSE)
dbWriteTable(DB, "list_of_data_lut", list_of_data_lut, append=TRUE, row.names=FALSE)
# update the list_of_data_lut in 'LUMENS_path_user'
list_of_data_lut <- dbReadTable(DB, c("public", "list_of_data_lut"))
write.csv(list_of_data_lut, paste0(LUMENS_path_user, "/list_of_data_lut.csv"), row.names = FALSE)
# generate dbf version of the 'sumtab1' table
write.dbf(chg_pdtable, paste0("Cpeat_sum_",planning_unit, "_", T_1, T_2, ".dbf"))

# 3. peat emission map 'p.em_map' (resultoutput)====
idx_factor <- idx_factor+1
data_ptmap <- paste0('Cpeat', '_',planning_unit, '_',T_1, T_2)
add_row_f <- data.frame(RST_DATA = paste0("factor", idx_factor), RST_NAME = data_ptmap, stringsAsFactors = FALSE)
dbWriteTable(DB, "list_of_data_f", add_row_f, append=TRUE, row.names=FALSE)
# update the list_of_data_f in 'LUMENS_path_user'
list_of_data_f <- dbReadTable(DB, c("public", "list_of_data_f"))
write.csv(list_of_data_f, paste0(LUMENS_path_user, "/list_of_data_f.csv"), row.names = FALSE)
# write the raster file in targeted directory as well as the .qml for value visualization
pt_pal <- c("#223BF8","#A0FD01","#FF6001")
writeRastFile(em_map, data_ptmap, colorpal = pt_pal)
# add teci map into the postgre database
addRasterToPG(project, paste0(data_ptmap, ".tif"), paste0("factor", idx_factor), srid)

# 4. saving idx
resave(idx_factor, file = proj.file)
resave(idx_lut, file = proj.file)

# 5. define resultoutput
resultoutput <- c(paste0(dirQUESC, "/Cpeat_sum_",planning_unit, "_", T_1, T_2, ".dbf"), paste0(dirQUESC, "/", data_ptmap, ".dbf"))
resultoutput <- data.frame(PATH= resultoutput)
# 5. Pass statusoutput
statuscode<-1
statusmessage<-"QUES-C peat analysis successfully completed!"
statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)