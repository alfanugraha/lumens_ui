##SCIENDO-PostgreSQL=group
##Drivers_data=file
##LUC_type=string

require(igraph)
require(rtf)
require(ggplot2)
require(Cairo)


#CREATE RESAVE FUNCTION
resave <- function(..., list = character(), file) {
previous  <- load(file)
var.names <- c(list, as.character(substitute(list(...)))[-1L])
for (var in var.names) assign(var, get(var, envir = parent.frame()))
save(list = unique(c(previous, var.names)), file = file)
}

#READ LUMENS LOG FILE
user_temp_folder<-Sys.getenv("TEMP")
if(user_temp_folder=="") {
  user_temp_folder<-Sys.getenv("TMP")
}
LUMENS_path_user <- paste(user_temp_folder,"/LUMENS/LUMENS.log", sep="")
log.file<-read.table(LUMENS_path_user, header=FALSE, sep=",")
proj.file<-paste(log.file[1,1], "/", log.file[1,2],"/",log.file[1,2], ".lpj", sep="")
load(proj.file)
wd<-dirname(proj.file)
wd<-paste(wd,"/SCIENDO", sep="")
dirnew<-paste(wd,"/Drivers_Analysis", sep="")
dir.create(dirnew)
setwd(dirnew)
# Load the igraph package (install if needed)

bsk<-read.table(Drivers_data, sep='\t', dec=',', header=T)#specify the path, separator(tab, comma, ...), decimal point symbol, etc.
judul<-paste("Faktor Pemicu Untuk ", LUC_type, sep="")
bsk<-edit(bsk)
bsk$grade<-0
bsk$spec<-"unknown"

# Transform the table into the required graph format:
bsk.network<-graph.data.frame(bsk, directed=T) #the 'directed' attribute specifies whether the edges are directed

# Inspect the data:

Daftar_faktor<-V(bsk.network) #prints the list of vertices
Daftar_hubungan<-E(bsk.network) #prints the list of edges
Daftar_derajat<-as.data.frame(degree(bsk.network,normalized=TRUE)) #print the number of edges per vertex (relationships per people)
test<-as.data.frame(c(Daftar_derajat[1]))
colnames(test)[1]<-"Derajat"
test2<-as.data.frame(rownames(Daftar_derajat))
colnames(test2)[1]<-"Faktor"
Daftar_derajat<-cbind(test2,test)

bad.vs<-V(bsk.network)[degree(bsk.network)<1] #identify those vertices part of less than three edges
bsk.network<-delete.vertices(bsk.network, bad.vs) #exclude them from the graph


V(bsk.network)$color<-ifelse(V(bsk.network)$name=='Less poverty', 'blue', 'red') #useful for highlighting


#E(bsk.network)$color<-ifelse(E(bsk.network)$grade==9, "red", "grey")

# or depending on the different specialization ('spec'):

E(bsk.network)$color<-ifelse(E(bsk.network)$spec!='X', "grey", ifelse(E(bsk.network)$spec=='Y', "grey", "red"))


V(bsk.network)$size<-degree(bsk.network)#here the size of the vertices is specified by the degree of the vertex

par(mai=c(0,0,1,0))
png(filename="org_network.png", height=800, width=1000, units="px",pointsize=10, res=120) #call the png writer
plot(bsk.network,				#the graph to be plotted
layout=layout.fruchterman.reingold,	# the layout method.
main=LUC_type,	#the title
vertex.label.dist=0.5,			# the name labels
vertex.frame.color='gray',
vertex.label.color='purple',
vertex.label.font=0.15,
vertex.label=V(bsk.network)$name,
vertex.label.cex=1,
edge.arrow.size=0.35
)

#run the plot
dev.off() #dont forget to close the device

Faktor_graph<-ggplot(data=Daftar_derajat, aes(x=Faktor, y=Derajat, fill=Faktor)) +
geom_bar(colour="black", stat="identity")+ coord_flip() +
guides(fill=FALSE) + xlab("Factors") + ylab("Eigenvalue")

#====WRITE REPORT====
title1<-"{\\colortbl;\\red0\\green0\\blue0;\\red255\\green0\\blue0;\\red146\\green208\\blue80;\\red0\\green176\\blue240;\\red140\\green175\\blue71;\\red0\\green112\\blue192;\\red79\\green98\\blue40;} \\pard\\qr\\b\\fs70\\cf2 L\\cf3U\\cf4M\\cf5E\\cf6N\\cf7S \\cf1REPORT \\par\\b0\\fs20\\ql\\cf1"
title2<-paste("\\pard\\qr\\b\\fs40\\cf1 SCIENDO-Drivers Analysis ", "for ", location, ", ", province, ", ", country, "\\par\\b0\\fs20\\ql\\cf1", sep="")
sub_title<-"\\cf2\\b\\fs32 ANALISA FAKTOR PEMICU PERUBAHAN PENGGUNAAN LAHAN\\cf1\\b0\\fs20"
#date<-paste("Date : ", date, sep="")
time_end<-paste("Proses selesai : ", eval(parse(text=(paste("Sys.time ()")))), sep="")
line<-paste("------------------------------------------------------------------------------------------------------------------------------------------------")
area_name_rep<-paste("\\b", "\\fs20", location, "\\b0","\\fs20")
chapter1<-"\\cf2\\b\\fs28 JEJARING FAKTOR PEMICU \\cf1\\b0\\fs20"
chapter2<-"\\cf2\\b\\fs28 FAKTOR KUNCI \\cf1\\b0\\fs20"
rtffile <- RTF("LUMENS_Pre-QUES_change_report.lpr", font.size=9)
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
addParagraph(rtffile, time_end)
addParagraph(rtffile, line)
addNewLine(rtffile)
width<-as.vector(c(1.34,3.1))
addTable(rtffile,proj_descr,font.size=8,col.widths=width)
addPageBreak(rtffile)
addParagraph(rtffile, sub_title)
addNewLine(rtffile)
addParagraph(rtffile, line)
#addParagraph(rtffile, date)
addParagraph(rtffile, time_end)
addParagraph(rtffile, line)
addNewLine(rtffile)
addParagraph(rtffile, "Analisa perubahan tutupan lahan dilakukan untuk mengetahui kecenderungan perubahan tutupan lahan di suatu daerah pada satu kurun waktu. Analisa ini dilakukan dengan menggunakan data peta tutupan lahan pada dua periode waktu yang berbeda. Selain itu, dengan memasukkan data unit perencanaan kedalam proses analisa, dapat diketahui kecenderungan perubahan tutupan lahan pada masing-masing kelas unit perencanaan yang ada. Informasi yang dihasilkan melalui analisa ini dapat digunakan dalam proses perencanaan untuk berbagai hal. Diantaranya adalah: menentukan prioritas pembangunan, mengetahui faktor pemicu perubahan penggunaan lahan, merencanakan skenario pembangunan di masa yang akan datang, dan lain sebagainya.")
addNewLine(rtffile)
addParagraph(rtffile, chapter1)
addParagraph(rtffile, line)
gambar<-paste(dirnew,"/org_network.png", sep="")
addPng(rtffile, gambar, width=6.7, height=5, res=150)
addParagraph(rtffile, line)
addParagraph(rtffile, chapter1)
addPlot(rtffile,plot.fun=print, width=5,height=5,res=200, Faktor_graph)
done(rtffile)
