library(ggplot2)
library(RColorBrewer)
library(reshape2)

subject_folders <- list.files(path="Subjects")
for(i in 1:length(subject_folders)){
  filenames_pt <- list.files(path=paste0("Subjects/",subject_folders[i]),
                             pattern="ProgressTracker_MANUAL*.csv", full.names=TRUE)
  print(filenames_pt)
}