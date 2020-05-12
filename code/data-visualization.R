#----------------------------------#
# Paper XXX                        #
#                                  #
# @claudioalvesmonteiro            #
# May/2020                         #
#----------------------------------#

# load packages
library(ggplot2)
library(wordcloud)
library(ggpubr)

# list files
files <- list.files('results/tables')

# Tema para Graficos
tema_massa <- function (base_size = 12, base_family = "") {
  theme_minimal(base_size = base_size, base_family = base_family) %+replace% 
    theme(axis.text.x = element_text(size=12,hjust=.5,vjust=.5,face="plain"),
          axis.text.y = element_text(size=12,angle=0,hjust=1,vjust=0,face="plain"), 
          axis.title.x = element_text(colour="black",size=12,angle=0,hjust=.5,vjust=0,face="plain"),
          axis.title.y = element_text(colour="black",size=12,angle=90,hjust=0.5,vjust=0.6,face="plain"),
          title = element_text(colour="black",size=14,angle=0,hjust=.5,vjust=.5,face="plain"))
}

#==============================================
# read files and generate WORDCLOUDS for each
#==============================================

for (file in files){

  # read data
  data <- read.csv(paste0('results/tables/', file))
    
  # test if data is empty
  if (dim(data)[1] == 0){
 
     print(paste0(file, ' EMPTY!'))
  
    } else {

      # remove csv from filename
      file = gsub('.{4}$', '', file)
      # create png file
      png(file=paste0('results/plots/', file, '.png'), width=500, height=500)
      
      # generate wordcloud
      wordcloud(words = data[,1], 
                freq = data[,2], 
                min.freq = 2,
                random.order=FALSE, 
                rot.per=0.2, 
                use.r.layout=T,
                colors=brewer.pal(8, "Dark2"))
      
      # save wordcloud as png  
      dev.off()
  }
}

#=======================
# WORDCOUNT barplots
#=======================

# funtion to plot wordcount
plotWordCount <- function(data, title){
  # select most freq
  data = data[1:15,]
  # order factors to plot
  data[,1] = factor(data[,1], levels = data[,1][order(data$freq)])
  # plot
  plot = ggplot(data, aes(x=data[,1], y=data$freq))+
    geom_bar(stat='identity', fill='#696969')+
    geom_label(aes(label=data$freq), size=3)+
    labs(y='Freq', x='', title=title)+
    coord_flip()+
    tema_massa()
  return(plot)
}

# load data
d1 = read.csv('results/tables/academia.csv')
d2 = read.csv('results/tables/setor_empresarial.csv')
d3 = read.csv('results/tables/terceiro_setor.csv')
d4 = read.csv('results/tables/setor_publico.csv')

# wordcount plots
p1 = plotWordCount(d1, 'Academia')
p2 = plotWordCount(d2, 'Companies')
p3 = plotWordCount(d3, 'Third Sector')
p4 = plotWordCount(d4, 'Public Sector')

# arrange plots into one and save
jovProp  <- ggarrange(p1, p2, p3, p4, ncol = 4, nrow = 1)
ggsave('wordcount_total.png', jovProp, path = "results/plots", width = 14, height = 4, units = "in")

