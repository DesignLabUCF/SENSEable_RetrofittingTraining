library(ggplot2)
library(RColorBrewer)
library(reshape2)


##############################################
### Read in subject data
##############################################
progress_tracker_data <- read.csv("Outputs/CongregatedProgressTrackers.csv",
                                  #skip=1,
                                  header=TRUE,
                                  sep=",")[,-1]