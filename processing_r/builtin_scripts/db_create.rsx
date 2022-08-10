##Database=group
##project=string (enter name of the project)
##working_directory=folder
##description=string
##location=string (enter location)
##province=string (enter province name of your location) 
##country=string (enter country name)
##admin_attribute=vector
##field_attribute=field admin_attribute
##spat_res= number 50
##dissolve_table=file
##statusoutput=output table

#=Load library
library(rtf)
library(rasterVis)
library(ggplot2)
library(RColorBrewer)
library(stringr)
library(rgeos)
library(grid)
library(jsonlite)
library(RPostgreSQL)
library(DBI)
library(rpostgis)
library(rgdal)

#=Set time start
time_start<-paste(eval(parse(text=(paste("Sys.time ()")))), sep="")

# check desktop architecture
win_arch=Sys.getenv("R_ARCH")
user_doc = Sys.getenv("USERPROFILE")
LUMENS_path = paste0(Sys.getenv("ProgramFiles"), "\\LUMENS")
if (file.exists(LUMENS_path)){
  processing_path = paste0(LUMENS_path, "\\apps\\qgis\\python\\plugins\\processing\\r\\scripts")
} else{
  LUMENS_path = paste0(Sys.getenv("ProgramFiles(x86)"), "\\LUMENS")
  processing_path = paste0(LUMENS_path, "\\apps\\qgis\\python\\plugins\\processing\\r\\scripts")
}
postgre_path = paste0(Sys.getenv("ProgramFiles"), "\\PostgreSQL\\9.6")
if(!file.exists(postgre_path)){
  postgre_path = paste0(Sys.getenv("ProgramFiles(x86)"), "\\PostgreSQL\\9.6")
  if(!file.exists(postgre_path)){
    statuscode<-0
    statusmessage<-"Please install PostgreSQL database.."
    statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)
    quit()
  }
}

# set PostgreSQL driver and profile
user_appdata<-Sys.getenv("APPDATA")
pgconf_file<-paste0(user_appdata, "\\postgresql\\pgpass.conf")
if(file.exists(pgconf_file)){
  pgconf_line<-readLines(pgconf_file)
  pgconf_len<-length(pgconf_line)
  pgconf_line<-pgconf_line[pgconf_len]
  pgconf_list<-unlist(str_split(pgconf_line, ':'))
  pgconf<-data.frame(rbind(pgconf_list))
  colnames(pgconf)<-c("host", "port", "auth", "user", "pass")
} else {
  # please install PostgreSQL 
  statuscode<-0
  statusmessage<-"Please check PostgreSQL configuration.."
  statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)
  quit()
}

# check status of PostgreSQL server
pg_isready<-paste0("\"", postgre_path, "\\bin\\pg_isready\" -p ", pgconf$port)
pg_response<-system(pg_isready)
if(pg_response==2){
  # please check your connection
  statuscode<-0
  statusmessage<-"Please check PostgreSQL connection.."
  statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)
  quit()
}

#=Create structure folder for LUMENS project 
setwd(working_directory)
project<-str_replace_all(string=project, pattern=" ", repl="_")
project_path <- paste(working_directory, "/", project, sep="")
PUR_path <- paste(project_path, "/PUR", sep="")
QUES_path <- paste(project_path, "/QUES", sep="")
PreQUES_path <- paste(QUES_path, "/PreQUES", sep="")
QUESC_path <- paste(QUES_path, "/QUES-C", sep="")
QUESB_path <- paste(QUES_path, "/QUES-B", sep="")
QUESH_path <- paste(QUES_path, "/QUES-H", sep="")
TA_path <- paste(project_path, "/TA", sep="")
SCIENDO_path  <- paste(project_path, "/SCIENDO", sep="")
#help_path  <- paste(LUMENS_path, "/help", sep="")
dir.create(project_path, mode="0777")
dir.create(PUR_path, mode="0777")
dir.create(QUES_path, mode="0777")
dir.create(PreQUES_path, mode="0777")
dir.create(QUESC_path, mode="0777")
dir.create(QUESB_path, mode="0777")
dir.create(QUESH_path, mode="0777")
dir.create(TA_path, mode="0777")
dir.create(SCIENDO_path, mode="0777")
#dir.create(help_path, mode="0777")

#This variables only to find out the identity of user who create database for the first time 
user_temp_folder<-Sys.getenv("TEMP")
if(user_temp_folder=="") {
  user_temp_folder<-Sys.getenv("TMP")
}
LUMENS_path_user <- paste(user_temp_folder,"/LUMENS", sep="") 
dir.create(LUMENS_path_user, mode="0777")

# clear temp first
setwd(LUMENS_path_user)
unlink(list.files(pattern="*"))

#=Set reference data
# save as temporary data 
setwd(project_path)
writeOGR(admin_attribute, dsn=project_path, "reference", overwrite_layer=TRUE, driver="ESRI Shapefile")
# rasterizing the polygon data of reference (e.g administrative, such as district or province boundary map) using gdal_rasterize
shp_dir<-paste(project_path,"/", "reference.shp", sep="")
file_out<-paste(project_path, "/", "reference.tif", sep="")
res<-spat_res
gdalraster<-paste0("\"", LUMENS_path, "\\bin\\gdal_rasterize.exe\"")
osgeo_comm<-paste(gdalraster, shp_dir, file_out,"-a IDADM -tr", res, res, "-a_nodata 255 -ot Byte", sep=" ")
system(osgeo_comm)

# create an initial coverage reference for LUMENS project
ref<-raster(file_out)
# ref<-ref*1
names(ref)<-"Administrative maps"
Ref.name<-names(ref)
Ref.type<-class(ref)
Ref.coord<-as.character(crs(ref))
Ref.res<-res(ref)
Ref.xmin<-xmin(ref)
Ref.xmax<-xmax(ref)
Ref.ymin<-ymin(ref)
Ref.ymax<-ymax(ref)
cov.desc1<-c("Reference name","Reference class", "Reference CRS", "Reference Resolution", "Xmin", "Xmax", "Ymin", "Ymax")
cov.desc2<-as.data.frame(rbind(Ref.name, Ref.type, Ref.coord, Ref.res, Ref.xmin, Ref.xmax, Ref.ymin, Ref.ymax))
cov.desc2<-cov.desc2[1]
cov_desc<-cbind(cov.desc1,cov.desc2)
colnames(cov_desc)[1]<-"Coverage"
colnames(cov_desc)[2]<-"Description"
# load reference attribute from csv dissolve table 
lut_ref<-read.table(dissolve_table, header=TRUE, sep=",")
lut_ref$fid<-NULL
colnames(lut_ref)[2]="ADMIN_UNIT"

# set batch parameter 
pgEnvBatch <- paste(LUMENS_path_user, "/pg_env.bat", sep="")
pathEnv = ""
pathEnv[1] = paste0("@SET PATH=", postgre_path, "\\bin;%PATH%")
pathEnv[2] = paste0("@SET PGDATA=", postgre_path, "\\data")
pathEnv[3] = paste0("@SET PGUSER=", pgconf$user)
pathEnv[4] = paste0("@SET PGPORT=", pgconf$port)
pathEnv[5] = paste0("@SET PGLOCALEDIR=", postgre_path, "\\share\\locale\n")

createNewPGTbl = pathEnv
# project as a new pg_db name
createNewPGTbl[6] = paste("createdb ", project, sep="")
createNewPGTbl[7] = paste('psql -d ', project, ' -c "CREATE EXTENSION postgis;"', sep="")
createNewPGTbl[8] = paste('psql -d ', project, ' -c "CREATE EXTENSION postgis_topology;"', sep="")
createNewPGTbl[9] = paste('psql -d ', project, ' -c "CREATE EXTENSION postgis_raster;"\n', sep="")

newBatchFile <- file(pgEnvBatch)
writeLines(createNewPGTbl, newBatchFile)
close(newBatchFile)
# execute batch file
pgEnvBatchFile<-str_replace_all(string=pgEnvBatch, pattern="/", repl='\\\\')
system(pgEnvBatchFile)

# set driver connection
driver <- dbDriver('PostgreSQL')
DB <- dbConnect(
  driver, dbname=project, host=as.character(pgconf$host), port=as.character(pgconf$port),
  user=as.character(pgconf$user), password=as.character(pgconf$pass)
)
# add reference map to database
# xxBUI = bit unsigned integer
# xxBSI = bit signed integer
# xxBF  = bit float
# pgWriteRast(DB, c("public", "ref_map"), raster=ref)

srid<-tryCatch({pgSRID(DB, crs(ref), create.srid = TRUE)}, error=function(e){ })
# ADDRASTERTOPG function
addRasterToPG<-function(project, raster.path, raster.name, raster.srid) {
  createNewPGTbl = pathEnv
  createNewPGTbl[6] = paste('raster2pgsql -s ', raster.srid, ' -I -C -t auto ', str_replace_all(string=raster.path, pattern="/", repl='\\\\'), ' public.', raster.name, ' | psql -d ', project, sep="")
  
  newBatchFile <- file(pgEnvBatch)
  writeLines(createNewPGTbl, newBatchFile)
  close(newBatchFile)
  # execute batch file
  pgEnvBatchFile<-str_replace_all(string=pgEnvBatch, pattern="/", repl='\\\\')
  system(pgEnvBatchFile)
}
addRasterToPG(project, 'reference.tif', 'ref_map', srid)

# unlink shapefile and raster
file.rename("reference.tif", "base.tif")
unlink(list.files(pattern = "reference"))
file.rename("base.tif", "reference.tif")

# write project properties into table
proj_descr <- as.data.frame(rbind(project, description, working_directory, location, province, country))
test<-c(rownames(proj_descr))
proj_descr<-cbind(test, proj_descr)
colnames(proj_descr)[1]<-"Type"
colnames(proj_descr)[2]<-"Description"
proj_descr<-as.data.frame(proj_descr)
proj.file<-paste(project_path, "/",project,".lpj", sep="")

#=Set all values, functions, and initial indices to zero, for each index serves as a counter
# e.g landuse.index serve as a counter of landuse numbers
#setwd(DATA_path)
db_name<-paste(project, ".lpj", sep="")
idx_landuse=0
idx_pu=1
idx_rec_pu=0
idx_factor=0
idx_lut=0
idx_lut_carbon=0
idx_lut_landuse=0
idx_lut_pu=0
idx_period=0
idx_PUR=0
idx_PreQUES=0
idx_QUESC=0
idx_QUESB=0
idx_QUESH=0
idx_SCIENDO_led=0
idx_SCIENDO_lucm=0
idx_TA_opcost=0
idx_TA_regeco=0
# getting an information of windows architecture through the path of LUMENS installation 
gdaltranslate<-paste0("\"",LUMENS_path, "\\bin\\gdal_translate.exe\"")
# prepare some functions and store it to LUMENS project file, so it can be used later
# RESAVE function
resave <- function(..., list = character(), file) {
  previous  <- load(file)
  var.names <- c(list, as.character(substitute(list(...)))[-1L])
  for (var in var.names) assign(var, get(var, envir = parent.frame()))
  save(list = unique(c(previous, var.names)), file = file)
}
# GET_FROM_RDB function
# get_from_rdb <- function(symbol, filebase, envir =parent.frame()){
#   lazyLoad(filebase = filebase, envir = envir, filter = function(x) x == symbol)
# }
# GETRASTERFROMPG function
getRasterFromPG<-function(pg_conf, pg_database, pg_table, pg_rasterfile) { 
  if(!file.exists(pg_rasterfile)){
    postgres_connection<-paste('PG:\"host=', as.character(pg_conf$host), ' port=', as.character(pg_conf$port), ' dbname=\'', pg_database, '\' user=\'', as.character(pg_conf$user), '\' password=\'', as.character(pg_conf$pass), '\' schema=\'public\'', sep="")
    gdaltranslate_cmd<-paste(gdaltranslate, postgres_connection, sep=" ")
    
    postgres_table<-paste('table=\'', pg_table, '\' mode=2\"', sep="")
    # postgres_output<-paste('-a_nodata', pg_nodata, pg_rasterfile, sep=" ")
    gdaltranslate_cmd_pu<-paste(gdaltranslate_cmd, postgres_table, pg_rasterfile, sep=" ") 
    system(gdaltranslate_cmd_pu)
  }
  loadRaster<-raster(pg_rasterfile)
  loadRaster<-reclassify(loadRaster, cbind(255, NA))
  
  # define projection
  crs(loadRaster)<-as.character(cov_desc[3,2])
  
  # sync spatial data
  if(pg_table!='ref_map'){
    compareData<-tryCatch({ compareRaster(ref, loadRaster) }, error=function(e){})
    if(is.null(compareData)){ loadRaster<-spatial_sync_raster(loadRaster, ref, method="ngb") }  
  }
  return(loadRaster)
}
# writeRastFile function
writeRastFile <- function(raster_in, raster_ou_path = character(), cat = FALSE, colorpal, lookup){
  # the function is to replace 'writeRaster' usage in the LUMENS scripts so that not only the raster file will be written as '.tif' but also the '.qml' file will be automatically created
  writeRaster(raster_in, raster_ou_path, format = "GTiff", overwrite = TRUE)
  # assessing the values in 'raster_in'
  if(cat){
    u_values <- unique(values(raster_in))
    u_values <- u_values[!is.na(u_values)]
  } else{
    u_values <- numeric()
    u_values[1] <- min(values(raster_in), na.rm = TRUE)
    u_values[2] <- 0
    u_values[3] <- max(values(raster_in), na.rm = TRUE)
    u_values[2] <- u_values[1] + (u_values[3] - u_values[1])/2# the average of the min and max
  }
  u_values <- u_values[order(u_values)]
  # the only difference between the continuous and discrete style is in the number of <item> under <colorrampshader>
  # writing the qml file
  if(grepl(".tif$", raster_ou_path)){
  qml_file_conn <- file(gsub(pattern = ".tif", replacement = ".qml", x = raster_ou_path))
  } else qml_file_conn <- file(paste0(raster_ou_path, ".qml"))
  qml_texts <- character()
  # standardized lines
  qml_texts[1] <- paste0('<!DOCTYPE qgis PUBLIC \'http://mrcc.com/qgis.dtd\' \'SYSTEM\'>')
  qml_texts[2] <- paste0('<qgis version="2.0.0-Taoge" minimumScale="0" maximumScale="1e+08" hasScaleBasedVisibilityFlag="0">')
  qml_texts[3] <- paste0('  <pipe>')
  qml_texts[4] <- paste0('    <rasterrenderer opacity="1" alphaBand="-1" classificationMax="', max(u_values), '" classificationMinMaxOrigin="MinMaxFullExtentEstimated" band="1" classificationMin="', min(u_values), '" type="singlebandpseudocolor">')
  qml_texts[5] <- paste0('      <rasterTransparency/>')
  qml_texts[6] <- paste0('      <rastershader>')
  qml_texts[7] <- paste0('        <colorrampshader colorRampTye="INTERPOLATED" clip="0">')
  # generating the right number of colors according to the colorpal (using 'colorRampPalette')
  my_col <- colorRampPalette(colorpal)
  my_col <- my_col(length(u_values))# number of classes as the basis of color interpolation
  # define labels for each values
  if(cat){
    names(lookup) <- c("values", "labels")
    lbls <- data.frame(values = u_values, orr = seq(length(u_values)), stringsAsFactors = FALSE)
    lookup$values <- as.numeric(lookup$values)
    lbls <- merge(lbls, lookup, by = "values", all.x = TRUE)
    lbls <- lbls[order(lbls$orr),"labels"]
  } else {
    lbls <- round(u_values,digits = 2)
  }
  # looping to generate the qml lines
  for(ql in 8: (7+length(u_values))){
    qml_texts[ql] <- paste0('          <item alpha="255" value="', u_values[ql-7], '" label="', lbls[ql-7], '" color="', my_col[ql-7], '"/>')
  }
  qml_texts <- c(qml_texts, paste0('        </colorrampshader>'))
  qml_texts <- c(qml_texts, paste0('      </rastershader>'))
  qml_texts <- c(qml_texts, paste0('    </rasterrenderer>'))
  qml_texts <- c(qml_texts, paste0('    <brightnesscontrast brightness="0" contrast="0"/>'))
  qml_texts <- c(qml_texts, paste0('    <huesaturation colorizeGreen="128" colorizeOn="0" colorizeRed="255" colorizeBlue="128" grayscaleMode="0" saturation="0" colorizeStrength="100"/>'))
  qml_texts <- c(qml_texts, paste0('    <rasterresampler maxOversampling="2"/>'))
  qml_texts <- c(qml_texts, paste0('  </pipe>'))
  qml_texts <- c(qml_texts, paste0('  <blendMode>0</blendMode>'))
  qml_texts <- c(qml_texts, paste0('</qgis>'))
  # writing down the qml lines into the path specified at qml_file_conn
  writeLines(qml_texts, qml_file_conn)
  close(qml_file_conn)
  # writing the .csv containing the paths of the output rasters
  if(file.exists(paste0(LUMENS_path_user,"/ou_raster.csv"))){
    ou_raster_paths <- read.csv(paste0(LUMENS_path_user,"/ou_raster.csv"), stringsAsFactors = FALSE)
    ou_raster_paths <- rbind(ou_raster_paths, raster_ou_path)
  } else {
    ou_raster_paths <- data.frame(raster_ou_path = raster_ou_path, stringsAsFactors = FALSE)
  }
  write.csv(ou_raster_paths, paste0(LUMENS_path_user,"/ou_raster.csv"), row.names = FALSE)
}

#=Save all params into .RData objects
save(LUMENS_path_user,
     LUMENS_path,
     pgEnvBatch,
     pathEnv,
     idx_landuse,
     proj_descr,
     ref,
     srid,
     lut_ref,
     location,
     province,
     country,
     cov_desc,
     idx_pu,
     idx_rec_pu,
     idx_factor,
     idx_lut,
     idx_lut_carbon,
     idx_lut_landuse,
     idx_lut_pu,
     idx_period,
     idx_PUR,
     idx_PreQUES,
     idx_QUESC,
     idx_QUESB,
     idx_QUESH,
     idx_SCIENDO_led,
     idx_SCIENDO_lucm,
     idx_TA_opcost,
     idx_TA_regeco,
     win_arch,
     processing_path,
     gdalraster,
     gdaltranslate,
     addRasterToPG,
     getRasterFromPG,
     postgre_path,
     pgconf,
     user_doc,
     resave,
     writeRastFile,
     file=proj.file)
# write the properties of reference data to PostgreSQL
eval(parse(text=(paste("list_of_data_pu<-data.frame(RST_DATA='ref', RST_NAME=names(ref), LUT_NAME='lut_ref', row.names=NULL)", sep=""))))
csv_file<-paste(LUMENS_path_user,"/csv_planning_unit.csv", sep="")
write.table(list_of_data_pu, csv_file, quote=FALSE, row.names=FALSE, sep=",")

dbWriteTable(DB, "list_of_data_pu", list_of_data_pu, append=TRUE, row.names=FALSE)
dbWriteTable(DB, "lut_ref", lut_ref, row.names=FALSE)
dbDisconnect(DB)

#=Create LUMENS Project Report (.doc)
# arrange numerous colors with RColorBrewer
myColors1 <- brewer.pal(9,"Set1")
myColors2 <- brewer.pal(8,"Accent")
myColors3 <- brewer.pal(12,"Paired")
myColors4 <- brewer.pal(9, "Pastel1")
myColors5 <- brewer.pal(8, "Set2")
myColors6 <- brewer.pal(8, "Dark2")
myColors7 <- rev(brewer.pal(11, "RdYlGn"))
myColors8 <- "#000000"
myColors9 <- brewer.pal(12, "Set3")
if (0 %in% lut_ref$IDADM){
  myColors  <-c(myColors8, myColors7,myColors1, myColors2, myColors3, myColors4, myColors5, myColors6)
} else {
  myColors  <-c(myColors7,myColors1, myColors2, myColors3, myColors4, myColors5, myColors6)
}
# create an Rplot for reference map
myColors.lu <- myColors[1:(length(unique(lut_ref$IDADM))+1)]
ColScale.lu<-scale_fill_manual(name=field_attribute, breaks=c(0, lut_ref$IDADM), labels=c("NoData", as.character(lut_ref$ADMIN_UNIT)), values=myColors.lu)
plot.admin<-gplot(ref, maxpixels=100000) + geom_raster(aes(fill=as.factor(value))) +
  coord_equal() + ColScale.lu + theme(plot.title = element_text(lineheight= 5, face="bold")) +
  theme( axis.title.x=element_blank(),axis.title.y=element_blank(),
         panel.grid.major=element_blank(), panel.grid.minor=element_blank(),
         legend.title = element_text(size=10),
         legend.text = element_text(size=10),
         legend.key.height = unit(0.35, "cm"),
         legend.key.width = unit(0.35, "cm"))

title1<-"{\\colortbl;\\red0\\green0\\blue0;\\red255\\green0\\blue0;\\red146\\green208\\blue80;\\red0\\green176\\blue240;\\red140\\green175\\blue71;\\red0\\green112\\blue192;\\red79\\green98\\blue40;} \\pard\\qr\\b\\fs70\\cf2 L\\cf3U\\cf4M\\cf5E\\cf6N\\cf7S \\cf1REPORT \\par\\b0\\fs20\\ql\\cf1"
title2<-paste("\\pard\\qr\\b\\fs40\\cf1 Create LUMENS Project ", "for ", location, ", ", province, ", ", country, "\\par\\b0\\fs20\\ql\\cf1", sep="")
sub_title<-"\\cf2\\b\\fs32 Ringkasan Deskripsi Projek\\cf1\\b0\\fs20"
chapter1<-"\\cf2\\b\\fs28 Deskripsi Projek \\cf1\\b0\\fs20"
chapter2<-"\\cf2\\b\\fs28 Cakupan Geografis Projek \\cf1\\b0\\fs20"
chapter3<-"\\cf2\\b\\fs28 Data-data Acuan Dalam Projek \\cf1\\b0\\fs20"
time_start<-paste("Proses LUMENS dimulai : ", time_start, sep="")
time_end<-paste("Proses LUMENS selesai : ", eval(parse(text=(paste("Sys.time ()")))), sep="")
line<-paste("-------------------------------------------------------------------------------------------------------------------------------------------------------")
area_name_rep<-paste("\\b", "\\fs20", location, "\\b0","\\fs20")
rtffile <- RTF(paste0(project, "_", gsub(" ", "_", location), ".doc"), font.size=9)
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
addParagraph(rtffile, time_start)
#addParagraph(rtffile, time_end)
addParagraph(rtffile, line)
addNewLine(rtffile)
width<-as.vector(c(1.34,3.1))
addTable(rtffile,proj_descr,font.size=8,col.widths=width)
addPageBreak(rtffile)
addParagraph(rtffile, sub_title)
addNewLine(rtffile)
addParagraph(rtffile, line)
#addParagraph(rtffile, time_start)
addParagraph(rtffile, time_end)
addParagraph(rtffile, line)
addNewLine(rtffile)
addParagraph(rtffile, paste("Selamat datang di LUMENS!!. Anda telah berhasil menyusun konfigurasi data-data awal yang akan digunakan dalam perencanaan penggunaan lahan yang mempertimbangkan berbagai fungsi lingkungan. LUMENS project file terdiri dari dua file utama dengan akhiran .lpj dan lpd. Project file yang telah anda buat bernama ", project, ".lpj."))
addNewLine(rtffile)
addParagraph(rtffile, chapter1)
addParagraph(rtffile, line)
addNewLine(rtffile)
addParagraph(rtffile, "Deskripsi projek menyimpan informasi umum yang anda masukkan mengenai projek ini")
addNewLine(rtffile)
width<-as.vector(c(1.34,3.1))
addTable(rtffile,proj_descr,font.size=8,col.widths=width)
addNewLine(rtffile)
addParagraph(rtffile, chapter2)
addParagraph(rtffile, line)
addNewLine(rtffile)
addParagraph(rtffile, "Cakupan geografis projek menyimpan informasi mengenai cakupan area yang akan digunakan di dalam project, batas-batas koordinat, sistem projeksi serta resolusi spasial yang akan digunakan dalam projek")
addNewLine(rtffile)
addTable(rtffile,cov_desc,font.size=8,col.widths=width)
addNewLine(rtffile)
addPageBreak(rtffile)
addParagraph(rtffile, chapter3)
addParagraph(rtffile, line)
addNewLine(rtffile)
addParagraph(rtffile, "Berikut ini adalah beberapa data yang akan dijadikan data acuan dalam projek ini")
addNewLine(rtffile)
addParagraph(rtffile, paste("\\cf4\\b \\fs20 Peta batas administrasi\\b \\fs20\\cf1", sep=" "))
addPlot(rtffile,plot.fun=print, width=6,height=4.5,res=150,  plot.admin)
addNewLine(rtffile)
done(rtffile)
# show result via shell command 

# detect winword
# rtf viewer

#command<-paste("start ", "winword ", project_path, "/LUMENS_Create-Project_report.doc", sep="" )
#shell(command)

#=Writing final status message (code, message)
statuscode<-1
statusmessage<-"LUMENS database has been created!"
statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)

