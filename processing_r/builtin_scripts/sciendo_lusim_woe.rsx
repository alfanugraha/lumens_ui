##SCIENDO-PostgreSQL=group
##proj.file=string
##SCIENDO_LUCM_index=string
##lc_lut=string
##statusoutput=output table

library(spatial.tools)
library(splitstackshape)
library(DBI)
library(RPostgreSQL)
library(rpostgis)
library(XML)

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
list_of_data_lut<-dbReadTable(DB, c("public", "list_of_data_lut"))
data_lut<-list_of_data_lut[which(list_of_data_lut$TBL_NAME==lc_lut),]
lusim_lc<-dbReadTable(DB, c("public", data_lut$TBL_DATA)) 

#=Set working directory
SCIENDO_folder<-SCIENDO_LUCM_index
result_dir<-paste(dirname(proj.file),"/SCIENDO/", SCIENDO_folder, sep="")
setwd(result_dir)
factor_dir <- (paste(result_dir,"/factor/", sep=""))
DINAMICA_exe<-paste0(Sys.getenv("ProgramFiles"), "\\Dinamica EGO\\DinamicaConsole.exe")
if (file.exists(DINAMICA_exe)){
  urlDINAMICAConsole = DINAMICA_exe
} else{
  DINAMICA_exe<-paste0(Sys.getenv("ProgramFiles(x86)"), "\\Dinamica EGO\\DinamicaConsole.exe")
  urlDINAMICAConsole = DINAMICA_exe
}

########################################################################################################################
# CALCULATE WEIGHT OF EVIDENCE                                                                                         #
########################################################################################################################

static_var<-data.frame(aliasFactor)
static_var$identifier<-paste('&quot;static_var/', static_var$aliasFactor, '&quot; 10 500000 1 5,&#x0A;', sep='')

identifier<-do.call(paste, c(as.list(static_var$identifier), sep="        "))

start <- as.numeric(lusim_lc[1,1])
lenght <- as.numeric(nrow(lusim_lc))
end <- as.numeric(lusim_lc[lenght,1])

skeleton1<-data.frame(nT1=c(start:end), divider=lenght)
skeleton1<-expandRows(skeleton1, 'divider')
skeleton2<-data.frame(nT2=rep(rep(c(start:end), lenght)))

skeleton<-cbind(skeleton1, skeleton2)
skeleton$key<-do.call(paste, c(skeleton[c("nT1", "nT2")], sep = "-&gt;"))

skeleton$transition<-paste("&#x0A;    ", skeleton$key, " [&#x0A;        ", identifier, "    ]", sep='')

skeletonFinal<-do.call(paste, c(as.list(skeleton$transition), sep=","))
skeletonFinal<-paste('[', skeletonFinal, "&#x0A;]", sep='')

# begin writing tag
con <- xmlOutputDOM(tag="script")
# add property
con$addTag("property", attrs=c(key="dff.date", value="2016-Oct-18 12:59:40"))
con$addTag("property", attrs=c(key="dff.version", value="3.0.17.20160922"))

# begin.
# add functor = LoadCategoricalMap
con$addTag("functor", attrs=c(name="LoadCategoricalMap"), close=FALSE)
con$addTag("property", attrs=c(key="dff.functor.alias", value="Final Landscape"))
con$addTag("inputport", attrs=c(name="filename"), paste('"', result_dir, '/landuse_2.tif"', sep=''))
con$addTag("inputport", attrs=c(name="nullValue"), ".none")
con$addTag("inputport", attrs=c(name="loadAsSparse"), ".no")
con$addTag("inputport", attrs=c(name="suffixDigits"), 0)
con$addTag("inputport", attrs=c(name="step"), "0")
con$addTag("inputport", attrs=c(name="workdir"), ".none")
con$addTag("outputport", attrs=c(name="map", id="v1"))
con$closeTag("functor")
# end.

# begin.
# add functor = LoadCategoricalMap
con$addTag("functor", attrs=c(name="LoadCategoricalMap"), close=FALSE)
con$addTag("property", attrs=c(key="dff.functor.alias", value="Initial Landscape"))
con$addTag("inputport", attrs=c(name="filename"), paste('"', result_dir, '/landuse_1.tif"', sep=''))
con$addTag("inputport", attrs=c(name="nullValue"), ".none")
con$addTag("inputport", attrs=c(name="loadAsSparse"), ".no")
con$addTag("inputport", attrs=c(name="suffixDigits"), 0)
con$addTag("inputport", attrs=c(name="step"), "0")
con$addTag("inputport", attrs=c(name="workdir"), ".none")
con$addTag("outputport", attrs=c(name="map", id="v2"))
con$closeTag("functor")
# end.

# begin.
# add functor = LoadMap
con$addTag("functor", attrs=c(name="LoadMap"), close=FALSE)
con$addTag("property", attrs=c(key="dff.functor.alias", value="Static Variables"))
con$addTag("inputport", attrs=c(name="filename"), paste('"', factor_dir, 'sciendo_factor.ers"', sep=''))
con$addTag("inputport", attrs=c(name="nullValue"), ".none")
con$addTag("inputport", attrs=c(name="loadAsSparse"), ".no")
con$addTag("inputport", attrs=c(name="suffixDigits"), 0)
con$addTag("inputport", attrs=c(name="step"), "0")
con$addTag("inputport", attrs=c(name="workdir"), ".none")
con$addTag("outputport", attrs=c(name="map", id="v3"))
con$closeTag("functor") 
# end.

# begin.
# add functor = LoadCategoricalMap
con$addTag("functor", attrs=c(name="LoadCategoricalMap"), close=FALSE)
con$addTag("property", attrs=c(key="dff.functor.alias", value="Regions"))
con$addTag("inputport", attrs=c(name="filename"), paste('"', result_dir, '/zone.tif"', sep=''))
con$addTag("inputport", attrs=c(name="nullValue"), ".none")
con$addTag("inputport", attrs=c(name="loadAsSparse"), ".no")
con$addTag("inputport", attrs=c(name="suffixDigits"), 0)
con$addTag("inputport", attrs=c(name="step"), "0")
con$addTag("inputport", attrs=c(name="workdir"), ".none")
con$addTag("outputport", attrs=c(name="map", id="v4"))
con$closeTag("functor")
# end.
# begin.

# begin.
# add containerfunctor = ForEachRegion
con$addTag("containerfunctor", attrs=c(name="ForEachRegion"), close=FALSE)
con$addTag("property", attrs=c(key="dff.functor.alias", value="forEachRegion"))
con$addTag("inputport", attrs=c(name="regions", peerid="v4"))
con$addTag("inputport", attrs=c(name="borderCells"), 0)
con$addTag("internaloutputport", attrs=c(name="regionManager", id="v5"))
con$addTag("internaloutputport", attrs=c(name="step", id="v6"))

# add subtag functor for SaveWeights
con$addTag("functor", attrs=c(name="SaveWeights"), close=FALSE)
con$addTag("property", attrs=c(key="dff.functor.alias", value="saveWeights"))
con$addTag("inputport", attrs=c(name="weights", peerid="v10"))
con$addTag("inputport", attrs=c(name="filename"), paste('"', factor_dir, '/woe.dcf"', sep=''))
con$addTag("inputport", attrs=c(name="suffixDigits"), 6)
con$addTag("inputport", attrs=c(name="step", peerid="v6"))
con$addTag("inputport", attrs=c(name="workdir"), ".none")
con$closeTag("functor")

# add subtag functor for RegionalizeCategoricalMap
con$addTag("functor", attrs=c(name="RegionalizeCategoricalMap"), close=FALSE)
con$addTag("property", attrs=c(key="dff.functor.alias", value="Final Landscape (Region)"))
con$addTag("inputport", attrs=c(name="globalMap", peerid="v1"))
con$addTag("inputport", attrs=c(name="regionId", peerid="v6"))
con$addTag("inputport", attrs=c(name="keepNonRegionCells"), ".no")
con$addTag("inputport", attrs=c(name="regionManager", peerid="v5"))
con$addTag("outputport", attrs=c(name="regionalMap", id="v7"))
con$closeTag("functor")

# add subtag functor for RegionalizeCategoricalMap
con$addTag("functor", attrs=c(name="RegionalizeCategoricalMap"), close=FALSE)
con$addTag("property", attrs=c(key="dff.functor.alias", value="Initial Landscape (Region)"))
con$addTag("inputport", attrs=c(name="globalMap", peerid="v2"))
con$addTag("inputport", attrs=c(name="regionId", peerid="v6"))
con$addTag("inputport", attrs=c(name="keepNonRegionCells"), ".no")
con$addTag("inputport", attrs=c(name="regionManager", peerid="v5"))
con$addTag("outputport", attrs=c(name="regionalMap", id="v8"))
con$closeTag("functor")

# add subtag functor for RegionalizeMap
con$addTag("functor", attrs=c(name="RegionalizeMap"), close=FALSE)
con$addTag("property", attrs=c(key="dff.functor.alias", value="Static Variables (Region)"))
con$addTag("inputport", attrs=c(name="globalMap", peerid="v3"))
con$addTag("inputport", attrs=c(name="regionId", peerid="v6"))
con$addTag("inputport", attrs=c(name="keepNonRegionCells"), ".no")
con$addTag("inputport", attrs=c(name="regionManager", peerid="v5"))
con$addTag("outputport", attrs=c(name="regionalMap", id="v9"))
con$closeTag("functor")

# add subtag functor for SaveTable
con$addTag("functor", attrs=c(name="SaveTable"), close=FALSE)
con$addTag("property", attrs=c(key="dff.functor.alias", value="saveTable"))
con$addTag("inputport", attrs=c(name="table", peerid="v11"))
con$addTag("inputport", attrs=c(name="filename"), paste('"', factor_dir, '/weight_report.csv"', sep=''))
con$addTag("inputport", attrs=c(name="suffixDigits"), 2)
con$addTag("inputport", attrs=c(name="step", peerid="v6"))
con$addTag("inputport", attrs=c(name="workdir"), ".none")
con$closeTag("functor")

# add subtag functor for DetermineWeightsOfEvidenceCoefficients
con$addTag("containerfunctor", attrs=c(name="DetermineWeightsOfEvidenceCoefficients"), close=FALSE)
con$addTag("property", attrs=c(key="dff.functor.alias", value="Weight of Evidence Coefficients"))
con$addTag("inputport", attrs=c(name="initialLandscape", peerid="v8"))
con$addTag("inputport", attrs=c(name="finalLandscape", peerid="v7"))
con$addTag("inputport", attrs=c(name="ranges", peerid="v12"))
con$addTag("inputport", attrs=c(name="fixAbnormalWeights"), ".no")
con$addTag("outputport", attrs=c(name="weights", id="v10"))
con$addTag("outputport", attrs=c(name="report", id="v11"))

con$addTag("functor", attrs=c(name="NameMap"), close=FALSE)
con$addTag("property", attrs=c(key="dff.functor.alias", value="nameMapCoeff"))
con$addTag("inputport", attrs=c(name="map", peerid="v9"))
con$addTag("inputport", attrs=c(name="mapName"), '"static_var"')
con$closeTag("functor")

con$closeTag("containerfunctor")  

# add subtag functor for DetermineWeightsOfEvidenceRanges
con$addTag("containerfunctor", attrs=c(name="DetermineWeightsOfEvidenceRanges"), close=FALSE)
con$addTag("property", attrs=c(key="dff.functor.alias", value="Weight of Evidence Ranges"))
con$addTag("inputport", attrs=c(name="initialLandscape", peerid="v8"))
con$addTag("inputport", attrs=c(name="finalLandscape", peerid="v7"))
con$addTag("inputport", attrs=c(name="skeleton"), skeletonFinal)
con$addTag("inputport", attrs=c(name="fixAbnormalWeights"), ".no")
con$addTag("outputport", attrs=c(name="ranges", id="v12"))

con$addTag("functor", attrs=c(name="NameMap"), close=FALSE)
con$addTag("property", attrs=c(key="dff.functor.alias", value="nameMapRanges"))
con$addTag("inputport", attrs=c(name="map", peerid="v9"))
con$addTag("inputport", attrs=c(name="mapName"), '"static_var"')
con$closeTag("functor")

con$closeTag("containerfunctor")
con$closeTag("containerfunctor")
# end.

# print(con$value())
# write egoml
egoml_file=paste(result_dir, "/3_Weight_of_Evidence_per_Region.egoml", sep='')
saveXML(con$value(), file=egoml_file)

# replace ampersand code character
egoml_text  <- readLines(egoml_file)
egoml_text_new  <- gsub(pattern="amp;", replace="", x=egoml_text)
writeLines(egoml_text_new, con=egoml_file)

command<-paste('"', urlDINAMICAConsole, '" -processors 0 -log-level 4 "', result_dir, '/3_Weight_of_Evidence_per_Region.egoml"', sep="")

system(command)

resave(lusim_lc, file=proj.file)
dbDisconnect(DB)

statuscode<-1
statusmessage<-"SCIENDO has completed successfully"
statusoutput<-data.frame(statuscode=statuscode, statusmessage=statusmessage)

