library(ggplot2)
library(RColorBrewer)
library(reshape2)
library(dplyr)

ar_color <- "#1A85FF"
paper_color <- "#D41159"

output_filename <- "StatisticalAnalyses.txt"


##############################################
### Progress Tracker Data
##############################################
progress_tracker_data <- read.csv("Outputs/CongregatedProgressTrackers.csv",
                                  #skip=1,
                                  header=TRUE,
                                  sep=",")[,-1]
progress_tracker_data$AR_Condition <- as.logical(progress_tracker_data$AR_Condition) # Cast to boolean for condition value

# Keep only desired columns
progress_tracker_data <- progress_tracker_data[progress_tracker_data$Task_ID=="2c" |
                                                 progress_tracker_data$Task_ID=="3" |
                                                 progress_tracker_data$Task_ID=="4a" |
                                                 progress_tracker_data$Task_ID=="4b" |
                                                 progress_tracker_data$Task_ID=="5" |
                                                 progress_tracker_data$Task_ID=="6" |
                                                 progress_tracker_data$Task_ID=="9" |
                                                 progress_tracker_data$Task_ID=="10" |
                                                 progress_tracker_data$Task_ID=="11"
                                             ,]

# Combine steps 5 and 6
for (subject_id in 1:length(unique(progress_tracker_data$Subject_ID))) {
  tasks_duration <- sum(subset(progress_tracker_data, ((Task_ID=="5" | Task_ID=="6") & Subject_ID==as.character(subject_id)), select=Duration))
  condition <- subset(progress_tracker_data, Subject_ID==as.character(subject_id), select=AR_Condition)[1,]
  progress_tracker_data[nrow(progress_tracker_data) + 1,] = list(
    "Corners",
    "5/6", 
    tasks_duration,
    subject_id,
    condition)
  rm(tasks_duration) # Clean up R Studio
  rm(condition) # Clean up R Studio
}
progress_tracker_data<-progress_tracker_data[!(progress_tracker_data$Task_ID=="5" | progress_tracker_data$Task_ID=="6"),] # Drop 5 and 6 individuals

# Summarize
progress_tracker_sum <- progress_tracker_data %>%
  group_by(AR_Condition, Task_Name, Task_ID) %>%
  summarise(Mean_Duration=mean(Duration))

###### START WRITE FILE ###### 
sink(output_filename, append=FALSE)
print("Progress Tracker t-test's")
print("############################")

# Create empty frame to multiple t test comparisons to
progress_tracker_t_tests <- data.frame(matrix(ncol=2, nrow=0)) 
colnames(progress_tracker_t_tests) <- c("Task_ID", "p_value")

# Statistical tests - t-tests
print("ALL TASKS - T-test")
print(t.test(progress_tracker_data$AR_Condition, progress_tracker_data$Duration)) 

pt_t_test <- function(pt_df, task_id)
{
  print(paste0("###### ", task_id, " ######"))
  pt_subset <- pt_df[pt_df$Task_ID==task_id,]
  # Assumptions
  ar_shapiro <- shapiro.test(pt_subset[pt_subset$AR_Condition=="TRUE",]$Duration)
  print(ar_shapiro)
  paper_shapiro <- shapiro.test(pt_subset[pt_subset$AR_Condition=="FALSE",]$Duration)
  print(ar_shapiro)
  if(ar_shapiro$p.value < 0.05 | paper_shapiro$p.value < 0.05)
  {
    print("Assumption of normailty: FAILED")
  }
  else
  {
    print("Assumption of normailty: PASSED")
  }
  # T-test
  print(t.test(pt_subset$AR_Condition, pt_subset$Duration)) 
  p_val <- t.test(pt_subset$AR_Condition, pt_subset$Duration)$p.value
  return(c(task_id, p_val))
  #progress_tracker_t_tests[nrow(progress_tracker_t_tests) + 1,] <- c(task_id, p_val) 
}

# print("2C")
# task_id <- "2c"
# pt_subset <- progress_tracker_data[progress_tracker_data$Task_ID==task_id,]
# # Assumptions
# print(shapiro.test(pt_subset[pt_subset$AR_Condition=="TRUE",]$Duration))
# print(shapiro.test(pt_subset[pt_subset$AR_Condition=="FALSE",]$Duration))
# # T-testA
# print(t.test(pt_subset$AR_Condition, pt_subset$Duration))
# p_val <- t.test(pt_subset$AR_Condition, pt_subset$Duration)$p.value
# progress_tracker_t_tests[nrow(progress_tracker_t_tests) + 1,] <- c(task_id, p_val)

# Run t-tests
progress_tracker_t_tests[nrow(progress_tracker_t_tests) + 1,] <- pt_t_test(progress_tracker_data, "2c")
progress_tracker_t_tests[nrow(progress_tracker_t_tests) + 1,] <- pt_t_test(progress_tracker_data, "3")
progress_tracker_t_tests[nrow(progress_tracker_t_tests) + 1,] <- pt_t_test(progress_tracker_data, "4a")
progress_tracker_t_tests[nrow(progress_tracker_t_tests) + 1,] <- pt_t_test(progress_tracker_data, "4b")
progress_tracker_t_tests[nrow(progress_tracker_t_tests) + 1,] <- pt_t_test(progress_tracker_data, "5/6")
progress_tracker_t_tests[nrow(progress_tracker_t_tests) + 1,] <- pt_t_test(progress_tracker_data, "9")
progress_tracker_t_tests[nrow(progress_tracker_t_tests) + 1,] <- pt_t_test(progress_tracker_data, "10")
progress_tracker_t_tests[nrow(progress_tracker_t_tests) + 1,] <- pt_t_test(progress_tracker_data, "11")

# Adjust for multiple comparisons using Bonferroni (https://rcompanion.org/rcompanion/f_01.html)
progress_tracker_t_tests$Bonferroni <- p.adjust(progress_tracker_t_tests$p_value, method="bonferroni")
print("Bonferroni Adjusted p-Values")
print(progress_tracker_t_tests)

# Statistical tests - Wilcoxin
pt_wilcoxin <- function(pt_df, task_id)
{
  print(paste0("###### ", task_id, " ######"))
  pt_subset <- pt_df[pt_df$Task_ID==task_id,]
  wilcoxin <- wilcox.test(Duration ~ AR_Condition,
                          data = pt_subset,
                          paired = FALSE,
                          alternative = "two.sided",
                          conf.level = 0.95,
                          exact = FALSE)
  print(wilcoxin)
}

# Run wilcoxin tests
print("WILCOXIN TESTS")
pt_wilcoxin(progress_tracker_data, "2c")
pt_wilcoxin(progress_tracker_data, "3")
pt_wilcoxin(progress_tracker_data, "4a")
pt_wilcoxin(progress_tracker_data, "4b")
pt_wilcoxin(progress_tracker_data, "5/6")
pt_wilcoxin(progress_tracker_data, "9")
pt_wilcoxin(progress_tracker_data, "10")
pt_wilcoxin(progress_tracker_data, "11")
###### STOP WRITE FILE ###### 
sink()

# TODO SPLIT INTO INDIVIDUAL TASKS

##############################################
### Plot - Progress Tracker Mean Times
##############################################

# Plot
pt_duration <- ggplot(progress_tracker_sum, aes(x=Task_ID, y=Mean_Duration, fill=AR_Condition)) +
  geom_bar(stat="identity",
           position="dodge",
           alpha=0.7,
           color="black") +
  #scale_fill_brewer(palette = "Spectral") +
  scale_fill_manual(values=c(paper_color, ar_color)) +
  labs(
    title="Mean Task Duration",
    x="Task ID",
    y="Duration (s)") +
  #theme_classic() +
  theme_bw() #+
print(pt_duration)

##############################################
### Log/'Mistakes' data
##############################################

log_data <- read.csv("../Subjects/Log.csv",
                     skip=1,
                     header=TRUE,
                     sep=",")
log_data$Condition <- as.factor(log_data$Condition)
log_data$Augmentation <- as.factor(log_data$Augmentation)

# Get only columns related to mistakes made
mistakes_data <- select(log_data, c("Condition", "Augmentation", "Mistakes"))

##############################################
### Plot - Mistakes count (bar plot)
##############################################

# Plot
mistakes_plot <- ggplot(mistakes_data, aes(x=Augmentation, y=Mistakes, fill=Augmentation)) +
  geom_boxplot(alpha=0.7,
               color="black") +
  scale_fill_manual(values=c(ar_color, paper_color)) +
  labs(
    title="Mistakes Made",
    x="Augmentation",
    y="Mistakes Count") +
  #theme_classic() +
  theme_bw() #+
print(mistakes_plot)

##############################################
### Qualtrics data
##############################################

qualtrics_data <- read.csv("../Subjects/Qualtrics.csv",
                           #skip=1,
                           header=TRUE,
                           sep=",")
qualtrics_data <- qualtrics_data[-1:-2,] # Drop junk data

# Rename essential columns in data
colnames(qualtrics_data)[colnames(qualtrics_data) == "X1"] ="Participant.ID"
colnames(qualtrics_data)[colnames(qualtrics_data) == "X4"] ="Augmentation"  
colnames(qualtrics_data)[colnames(qualtrics_data) == "X5"] ="Condition"

# Factor/Unify data names with other data frames
qualtrics_data$Augmentation[qualtrics_data$Augmentation == "Augmented Reality"] <- "AR"
qualtrics_data$Augmentation <- as.logical(qualtrics_data$Augmentation) # Cast to boolean for condition value



# TODO REST




# Paper folding answer key
### TODO

##############################################
### Cutout area data
##############################################

# TODO

##############################################
### Watch data
##############################################

# TODO