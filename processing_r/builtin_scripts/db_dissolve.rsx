##DB-PostgreSQL=group
##admin_data=vector
##field_attribute=field admin_data
##admin_output=output vector

library(rgeos)

#dissolve
#gUnaryUnion convert the type of data from SpatialPolygonsDataFrame to SpatialPolygons
length(admin_data)
eval(parse(text=(paste("admin_data<-gUnaryUnion(admin_data, id=admin_data@data$", field_attribute, ")", sep=""))))

#get the data frame by spatial polygon IDs 
df <- data.frame(id = getSpPPolygonsIDSlots(admin_data))

#adjusting the row.names
row.names(df) <- getSpPPolygonsIDSlots(admin_data)

#add new field
seq<-1:nrow(df)
df<-cbind(seq, df)
colnames(df)[1]<-"IDADM"
colnames(df)[2]<-field_attribute

#converting the result back into a SpatialPolygonsDataFrame
length(admin_data)
admin_output <- SpatialPolygonsDataFrame(admin_data, data=df)
