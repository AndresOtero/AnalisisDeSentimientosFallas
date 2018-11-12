library(RWeka)

mydata=read.csv("reviewsSentimientos.csv",header=TRUE)
library("foreign")
write.arff(x =mydata ,file= "reviewsSentimientos.arff")


