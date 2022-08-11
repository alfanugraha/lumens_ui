##Database=group
##proj.file=string
##database_status=output table

load(proj.file)

numberOfObject<-length(ls(all.names=T))

#=Create function for list all objects in project file
.ls.objects <- function (pos = 1, pattern, order.by,
  decreasing=FALSE, head=FALSE, n=5) {
  napply <- function(names, fn) sapply(names, function(x)
  fn(get(x, pos = pos)))
  names <- ls(pos = pos, pattern = pattern)
  obj.class <- napply(names, function(x) as.character(class(x))[1])
  obj.mode <- napply(names, mode)
  obj.type <- ifelse(is.na(obj.class), obj.mode, obj.class)
  obj.size <- napply(names, object.size)
  obj.dim <- t(napply(names, function(x)
  as.numeric(dim(x))[1:2]))
  vec <- is.na(obj.dim)[, 1] & (obj.type != "function")
  obj.dim[vec, 1] <- napply(names, length)[vec]
  out <- data.frame(obj.type, obj.size, obj.dim)
  names(out) <- c("Type", "Size", "Rows", "Columns")
  if (!missing(order.by))
  out <- out[order(out[[order.by]], decreasing=decreasing), ]
  if (head)
  out <- head(out, n)
  out
}
lsos <- function(..., n=10) {
  .ls.objects(..., order.by="Size", decreasing=TRUE, head=TRUE, n=n)
}
listOfData<-lsos(pos = environment(), n=numberOfObject)
listOfData$var_name<-row.names(listOfData)
row.names(listOfData)<-NULL
setwd(dirname(proj.file))

#description
status_country<-c("Country", eval(parse(text=(paste("country")))) )
status_province<-c("Province", eval(parse(text=(paste("province")))) )
status_location<-c("Location", eval(parse(text=(paste("location")))) )
database_status<-as.data.frame(rbind(status_country, status_location, status_province))
database_status$V1<-as.character(factor(database_status$V1))
database_status$V2<-as.character(factor(database_status$V2))

#check inputted data on the temporary folder
setwd(LUMENS_path_user)
abbrvs <- c("luc", "pu", "f", "lut")
categories <- c("land_use_cover", "planning_unit", "factor_data", "lookup_table")
for(d in 1:length(categories)){
  # check whether csv is exist
  logic <- eval(parse(text=paste0("file.exists('csv_", categories[d], ".csv')")))
  if(logic){
    eval(parse(text=paste0("list_of_data_", abbrvs[d], "<-read.table('csv_", categories[d], ".csv', header=T, sep=',')")))
    if(abbrvs[d]!="lut"){
      eval(parse(text=(paste0("V1<-as.character(list_of_data_", abbrvs[d], "$RST_DATA)"))))
      eval(parse(text=(paste0("V2<-as.character(list_of_data_", abbrvs[d], "$RST_NAME)"))))
      status_landuse<-cbind(V1, V2)
      database_status<-rbind(database_status, status_landuse)
      if(abbrvs[d]=="luc"){
        eval(parse(text=(paste0("V1<-paste0('period', substr(list_of_data_", abbrvs[d], "$RST_DATA, 13, 15))"))))
        eval(parse(text=(paste0("V2<-as.character(list_of_data_", abbrvs[d], "$PERIOD)"))))  
        status_period<-cbind(V1, V2)
        database_status<-rbind(database_status, status_period)
      }
    }
  }
}

#index
status_PUR.index<-c("PUR", eval(parse(text=(paste("idx_PUR")))) )
status_PreQUES.index<-c("PreQUES", eval(parse(text=(paste("idx_PreQUES")))) )
status_QUESB.index<-c("QUES-B", eval(parse(text=(paste("idx_QUESB")))) )
status_QUESC.index<-c("QUES-C", eval(parse(text=(paste("idx_QUESC")))) )
status_QUESH.index<-c("QUES-H", eval(parse(text=(paste("idx_QUESH")))) )
status_SCIENDO1.index<-c("SCIENDO Historical baseline", eval(parse(text=(paste("idx_SCIENDO_led")))) )
status_SCIENDO2.index<-c("SCIENDO Land use simulation", eval(parse(text=(paste("idx_SCIENDO_lucm")))) )
status_TA1.index<-c("TA Opportunity cost", eval(parse(text=(paste("idx_TA_opcost")))) )
status_TA2.index<-c("TA Regional economy", eval(parse(text=(paste("idx_TA_regeco")))) )
status_landuse.index<-c("Land-use/cover map", eval(parse(text=(paste("idx_landuse")))) )
status_pu.index<-c("Planning unit map", eval(parse(text=(paste("idx_pu")))) )
status_factor.index<-c("Factor map", eval(parse(text=(paste("idx_factor")))) )
status_lut.index<-c("Lookup table", eval(parse(text=(paste("idx_lut")))) )
database_status<-rbind(database_status, status_PUR.index, status_PreQUES.index,
status_QUESB.index, status_QUESC.index, status_QUESH.index,
status_SCIENDO1.index, status_SCIENDO2.index, status_TA1.index, status_TA2.index,
status_landuse.index, status_pu.index, status_factor.index, status_lut.index)

row.names(database_status)<-NULL
colnames(database_status)[1]="Variable"
colnames(database_status)[2]="Value"

#=Create HTML file (.html)
setwd(dirname(proj.file))
htmlproject<-paste("project_status.html", sep="")
sink(htmlproject)
cat("<!DOCTYPE html>")
cat("<html><head><meta name='qrichtext' content='1' />")
cat("<style>
table a:link {color: #666;font-weight: bold;text-decoration:none;}
table a:visited {color: #999999;font-weight:bold;text-decoration:none;}
table a:active, table a:hover { color: #bd5a35;text-decoration:underline;}
table {font-family:Arial, Arial, sans-serif;color:#666;font-size:12px;text-shadow: 1px 1px 0px #fff;background:#eaebec;margin:20px;border:#ccc 1px solid;-moz-border-radius:3px;-webkit-border-radius:3px;border-radius:3px;-moz-box-shadow: 0 1px 2px #d1d1d1;-webkit-box-shadow: 0 1px 2px #d1d1d1;box-shadow: 0 1px 2px #d1d1d1;}
table th {
    padding:10px 25px 11px 25px;
    border-top:1px solid #fafafa;
    border-bottom:1px solid #e0e0e0;

    background: #ededed;
    background: -webkit-gradient(linear, left top, left bottom, from(#ededed), to(#ebebeb));
    background: -moz-linear-gradient(top,  #ededed,  #ebebeb);
}
table th:first-child { text-align: left; padding-left:20px; }
table tr:first-child th:first-child {-moz-border-radius-topleft:3px;-webkit-border-top-left-radius:3px;border-top-left-radius:3px;}
table tr:first-child th:last-child {-moz-border-radius-topright:3px;-webkit-border-top-right-radius:3px;border-top-right-radius:3px;}
table tr {text-align: center;padding-left:20px;}
table td:first-child {text-align: left;padding-left:20px;border-left: 0;}
table td {padding:5px;border-top: 1px solid #ffffff;border-bottom:1px solid #e0e0e0;border-left: 1px solid #e0e0e0;

    background: #fafafa;
    background: -webkit-gradient(linear, left top, left bottom, from(#fbfbfb), to(#fafafa));
    background: -moz-linear-gradient(top,  #fbfbfb,  #fafafa);
}
table tr.even td {background: #f6f6f6;background: -webkit-gradient(linear, left top, left bottom, from(#f8f8f8), to(#f6f6f6));background: -moz-linear-gradient(top,  #f8f8f8,  #f6f6f6);}
table tr:last-child td {border-bottom:0;}
table tr:last-child td:first-child {-moz-border-radius-bottomleft:3px;-webkit-border-bottom-left-radius:3px;border-bottom-left-radius:3px;}
table tr:last-child td:last-child {-moz-border-radius-bottomright:3px;-webkit-border-bottom-right-radius:3px;border-bottom-right-radius:3px;}
table tr:hover td {background: #f2f2f2;background: -webkit-gradient(linear, left top, left bottom, from(#f2f2f2), to(#f0f0f0));background: -moz-linear-gradient(top,  #f2f2f2,  #f0f0f0);}")
cat("</style></head><body><table>")
n_status<-nrow(database_status)
for(row in 0:n_status){
  if (row == 0) { 
    cat(paste("<tr><th>",colnames(database_status)[1],"</th> <th>",colnames(database_status)[2],"</th></tr>"))
  } else {
    cat(paste("<tr><td>",database_status$Variable[row],"</td> <td>",database_status$Value[row],"</td></tr>"))
  }
}
cat("</table></body></html>")
sink()

resave(database_status, file=proj.file)

gc()
