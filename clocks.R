library(ggplot2)
infile <- read.csv(file="mhs.csv", header=TRUE,sep=",")
out <- ggplot(data=infile, aes(x=mem, y=core, fill=mhs)) + geom_tile() + scale_colour_gradientn(colours = rainbow(7))

ggsave(out,filename='clocks.png')
