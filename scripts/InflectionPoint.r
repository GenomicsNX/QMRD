

args <- commandArgs(TRUE)

infile <- args[1]
outfile <- args[2]
outpdf <- args[3]


library(dplyr)


# read in ABL unique UMI counts (each row corresponds to a unique UMI and its count)
umi <-read.table(infile, header=F) #study/sample
colnames(umi) <- c('count','UMI')


# order UMI counts (n)
umi <- umi[with(umi, order(-(count))), ]
umi$id <- rep(1:nrow(umi),1)

# calculate 2.5% right tail as outliers (n > mean+2sd)
outliner <- 2*sd(umi$count) + mean(umi$count)


# calculate m= frequency of (n)
umi.count.freq <- table(umi$count)
data <- as.data.frame(umi.count.freq)
data$logFreq <- log10(data$Freq)
data$Var1<-as.numeric(as.character(data$Var1))
data <- data[data$Var1 <= outliner,]
data <- data[with(data, order(-(Var1))), ]
data$id <- rep(1:nrow(data),1)
rownames(data)= data$id
head(data)

# plot ABL1 UMI frequency
pdf(outpdf, width = 7.4, height = 6.3)

plot(data$Var1,data$logFreq,type="l",xlim=rev(range(data$Var1)), xlab="UMI Count (n)" ,ylab="UMI Freq (log10)",main="Distribution of ABL1 UMI")

# fit umi frequency data
lo <- loess(data$logFreq~data$Var1)


xl <- seq(min(data$Var1),max(data$Var1), (max(data$Var1) - min(data$Var1))/1000)
out = predict(lo,xl,se = F)

#plot fitted data
lines(xl, out, col='red', lwd=1)

# calculate inflection point for fitted data
infl <- c(FALSE, diff(diff(out)>0)!=0)

# label inflection point on plot
points(xl[infl ], out[infl ], col="blue",pch=16)
abline(v=xl[infl ], col="darkblue", lwd=1 ,lty=2)
axis(1 , at=xl[infl],labels=round(xl[infl]),las=2 ,adj=1, cex.axis=0.9, col.axis="red")
dev.off()

# cut-off is the smallest inflection point
cutoff <- xl[infl]

cat (cutoff , "\t " ,"\n", file=outfile,append=TRUE)
q()

