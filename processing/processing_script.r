options("repos"="http://cran.at.r-project.org/")
.libPaths("C:/Users/ANugraha/Documents/R/win-library/3.3")
tryCatch(find.package("rgdal"), error=function(e) install.packages("rgdal", dependencies=TRUE))
tryCatch(find.package("raster"), error=function(e) install.packages("raster", dependencies=TRUE))
library("raster")
library("rgdal")
project_file="C:/LUMENS_test/EMPAT_LAWANG/empt_lawang/empt_lawang.lpj"

load(project_file)

setwd(LUMENS_path_user)
unlink(list.files(pattern="*"))

overview<-ref
writeRaster(overview,"C:/Users/ANugraha/AppData/Local/Temp/processing/14bd01983f104ccfbdebb86551e178d6/overview.tif", overwrite=TRUE)
