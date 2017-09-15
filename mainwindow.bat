set OSGEO4W_ROOT=C:\Program Files (x86)\LUMENS
set GDAL_DATA=%OSGEO4W_ROOT%\share\epsg_csv
set QGIS_PREFIX=%OSGEO4W_ROOT%\apps\qgis
set RPATH=C:\Program Files\R\R-3.3.2
set R_USE64=True
set PATH=%OSGEO4W_ROOT%\bin;%QGIS_PREFIX%\bin;%RPATH%\bin;%PATH%
set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python27
set PYTHONPATH=%QGIS_PREFIX%\python;%QGIS_PREFIX%\python\plugins;%OSGEO4W_ROOT%\apps\Python27;%PYTHONPATH%
set RLIBS=C:\Users\UsersName\Documents\R\win-library\3.3
set RSCRIPTS=C:\lumens_scripts

python mainwindow.py
PAUSE