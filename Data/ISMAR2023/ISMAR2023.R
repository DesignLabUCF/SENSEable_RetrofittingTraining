library(ggplot2)
library(RColorBrewer)
library(reshape2)
library(dplyr)
library(pastecs) # Statistical summary table
library(car) # Levene Test
#library(forcats)
library(rcompanion)

ar_color <- "#1A85FF"
#paper_color <- "#D41159"
paper_color <- "azure3"
  
plot_outline_color <- "black"
plot_outline_size <- 1.5
plot_grid_color <- "gray85"
plot_grid_size_major <- 0.55
plot_grid_size_minor <- 0.35

output_folder <- "Outputs"
pt_filename <- "PT_stats.txt"
cuts_filename <- "cutout_stats.txt"
usability_filename <- "Usability_stats.txt"

subjects_to_remove <- c("2", "58")

print_summary <- function(df, metric){
  print(paste(metric, "AR", sep=" - "))
  ar <- df[df$Augmentation==TRUE,]
  print(summary(ar[[metric]]))
  print(stat.desc(ar[[metric]]))
  
  paper <- df[df$Augmentation==FALSE,]
  print(paste(metric, "Printed", sep=" - "))
  print(summary(paper[[metric]]))
  print(stat.desc(paper[[metric]]))
}

print_general_stats <- function(df, metric){
  print(paste(df, metric, sep=" - "))
  #print(summary(df[[metric]]))
  print(stat.desc(as.numeric(df[[metric]])))
}

##############################################
### Progress Tracker Data
##############################################

# TODO UPDATE 55 MANUALLY

progress_tracker_data <- read.csv("../Subjects/CongregatedProgressTrackers.csv",
                                  #skip=1,
                                  header=TRUE,
                                  sep=",")[,-1]
progress_tracker_data <- progress_tracker_data[!progress_tracker_data$Subject_ID %in% subjects_to_remove, ] # Remove unused subjects
progress_tracker_data$AR_Condition <- as.logical(progress_tracker_data$AR_Condition) # Cast to boolean for condition value
colnames(progress_tracker_data)[colnames(progress_tracker_data) == "AR_Condition"] <- "Augmentation" # Match column name to other

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
  condition <- subset(progress_tracker_data, Subject_ID==as.character(subject_id), select=Augmentation)[1,]
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
  group_by(Augmentation, Task_Name, Task_ID) %>%
  summarise(Mean_Duration=mean(Duration))
progress_tracker_sum <- na.omit(progress_tracker_sum) # Remove NA row that appeared. Not sure why it's there. Must investigate.

###### START WRITE FILE ###### 
sink(paste(output_folder, pt_filename, sep="/"), append=FALSE)

print("############################")
print("Summary Statistics")
print("############################")
print("======= 3 =======")
print_summary(progress_tracker_data[progress_tracker_data$Task_ID=="3",], "Duration")
print("======= 4a =======")
print_summary(progress_tracker_data[progress_tracker_data$Task_ID=="4a",], "Duration")
print("======= 4b =======")
print_summary(progress_tracker_data[progress_tracker_data$Task_ID=="4b",], "Duration")
print("======= 5/6 =======")
print_summary(progress_tracker_data[progress_tracker_data$Task_ID=="5/6",], "Duration")
print("======= 9 =======")
print_summary(progress_tracker_data[progress_tracker_data$Task_ID=="9",], "Duration")
print("======= 10 =======")
print_summary(progress_tracker_data[progress_tracker_data$Task_ID=="10",], "Duration")
print("======= 11 =======")
print_summary(progress_tracker_data[progress_tracker_data$Task_ID=="11",], "Duration")

print("############################")
print("Progress Tracker t-test's")
print("############################")

# Create empty frame to multiple t test comparisons to
progress_tracker_t_tests <- data.frame(matrix(ncol=2, nrow=0)) 
colnames(progress_tracker_t_tests) <- c("Task_ID", "p_value")

# Statistical tests - t-tests
print("ALL TASKS - T-test")
print(t.test(progress_tracker_data$Augmentation, progress_tracker_data$Duration)) 

pt_t_test <- function(pt_df, task_id)
{
  print(paste0("###### ", task_id, " ######"))
  pt_subset <- pt_df[pt_df$Task_ID==task_id,]
  # Assumptions
  ar_shapiro <- shapiro.test(pt_subset[pt_subset$Augmentation=="TRUE",]$Duration)
  print(ar_shapiro)
  paper_shapiro <- shapiro.test(pt_subset[pt_subset$Augmentation=="FALSE",]$Duration)
  print(paper_shapiro)
  if(ar_shapiro$p.value < 0.05 | paper_shapiro$p.value < 0.05)
  {
    print("Assumption of normailty: FAILED")
  } else
  {
    print("Assumption of normailty: PASSED")
  }
  # T-test
  print(t.test(pt_subset$Augmentation, pt_subset$Duration)) 
  p_val <- t.test(pt_subset$Augmentation, pt_subset$Duration)$p.value
  return(c(task_id, p_val))
}

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
  wilcoxin <- wilcox.test(pt_subset$Duration ~ pt_subset$Augmentation,
                          #data = pt_subset,
                          paired = FALSE,
                          alternative = "two.sided",
                          conf.level = 0.95,
                          exact = FALSE)
  print(wilcoxin)
  print(wilcoxonR(x = pt_subset$Duration, g = pt_subset$Augmentation))
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

##############################################
### Plot - Progress Tracker Mean Times
##############################################

# Plot
pt_duration <- ggplot(progress_tracker_sum, aes(x=Task_ID, y=Mean_Duration, fill=Augmentation)) +
  geom_bar(stat="identity",
           position="dodge",
           alpha=0.7,
           color="black") +
  #scale_fill_brewer(palette = "Spectral") +
  scale_fill_manual(values=c(paper_color, ar_color),
                    labels=c("Paper", "AR")) +
  labs(
    title="Mean Task Duration",
    x="Task ID",
    y="Duration (s)") +
  #theme_classic() +
  theme_bw() +
  theme(
    # Text
    text = element_text(family="serif"), # Times New Roman
    plot.title = element_text(size=18, face="bold", hjust=0.5), 
    axis.title = element_text(size=18, face="italic", hjust=0.5),
    axis.text = element_text(size=14),
    # Axis Ticks
    axis.ticks = element_blank(),
    # Legend
    legend.background = element_rect(color="black", size=0.5, linetype="dashed"),
    legend.position = c(0.23, 0.91),
    legend.title = element_text(size=14, face="italic", hjust=0.5),
    legend.text = element_text(size=12),
    legend.direction = "horizontal",
    # Borders
    panel.border = element_rect(color=plot_outline_color, fill=NA, size=plot_outline_size),
    panel.grid.major = element_line(color=plot_grid_color, size=plot_grid_size_major),
    panel.grid.minor = element_line(color=plot_grid_color, size=plot_grid_size_minor)
  )
print(pt_duration)

##############################################
### Plot - Identification-based task Mean Times
##############################################

plot_df_identification <- progress_tracker_sum[progress_tracker_sum$Task_ID == "5/6" |
                                                 progress_tracker_sum$Task_ID == "4a" | 
                                                 progress_tracker_sum$Task_ID == "4b" | 
                                                 progress_tracker_sum$Task_ID == "10", ] %>%
  mutate(Task_ID = factor(Task_ID, levels=c("4a", "4b", "5/6", "10")))
levels(plot_df_identification$Task_ID) <- c("Locate ideal\nvertical stud", "Select optimal\nheight", "Mark cutout\narea", "Mark outlet-stud\nscrew holes")

# Plot
pt_id_duration <- ggplot(plot_df_identification,
                         aes(x=Task_ID,
                             y=Mean_Duration,
                             fill=Augmentation)) +
  geom_bar(stat="identity",
           position="dodge",
           width=0.9,
           size=1.25,
           alpha=0.7,
           color="black") +
  #scale_fill_brewer(palette = "Spectral") +
  scale_fill_manual(values=c(paper_color, ar_color),
                    labels=c("Paper", "AR")) +
  labs(
    title="Identication-based Task Durations",
    x="Task",
    y="Duration (seconds)") +
  #theme_classic() +
  theme_bw() +
  theme(
    # Text
    text = element_text(family="serif"), # Times New Roman
    plot.title = element_text(size=18, face="bold", hjust=0.5), 
    axis.title = element_text(size=18, face="italic", hjust=0.5),
    axis.text = element_text(size=14),
    # Axis Ticks
    axis.ticks = element_blank(),
    # Legend
    legend.background = element_rect(color="black", size=0.5, linetype="dashed"),
    legend.position = c(0.77, 0.91),
    legend.title = element_text(size=14, face="italic", hjust=0.5),
    legend.text = element_text(size=12),
    legend.direction = "horizontal",
    # Borders
    panel.border = element_rect(color=plot_outline_color, fill=NA, size=plot_outline_size),
    panel.grid.major = element_line(color=plot_grid_color, size=plot_grid_size_major),
    panel.grid.minor = element_line(color=plot_grid_color, size=plot_grid_size_minor)
  )
print(pt_id_duration)

rm(plot_df_identification) # Clean RStudio env

##############################################
### Log/Cutout Area data
##############################################

log_data <- read.csv("../Subjects/Log.csv",
                     skip=1,
                     header=TRUE,
                     sep=",")
log_data$Condition <- as.factor(log_data$Condition)
#log_data$Augmentation <- as.factor(log_data$Augmentation)
log_data$Augmentation <- (log_data$Augmentation == "AR")
colnames(log_data)[colnames(log_data) == "Participant_ID"] ="Participant.ID"
log_data <- log_data[!log_data$Participant.ID %in% subjects_to_remove, ] # Remove unused subjects


# Add in cutout area data
cutout_data <- read.csv("../Subjects/CutoutAreas.csv",
                        #skip=1,
                        header=TRUE,
                        sep=",")
colnames(cutout_data)[colnames(cutout_data) == "Participant_ID"] ="Participant.ID"
cutout_data <- cutout_data[!cutout_data$Participant.ID %in% subjects_to_remove, ] # Remove unused subjects
log_data <- merge(log_data, cutout_data, by="Participant.ID")

# Add column for wall stud positions
# Objective measures:
#   wall-x-min: 45
#   wall-xx-max: 777
#   wall-x-average: 560 => 560 / 732 => ~76.5% across wall from left side
log_data$Stud_Percentage = log_data$Stud_X_Coordinate / (log_data$Wall_Max_X - log_data$Wall_Min_X)

# Ideal Cutout area (inches)
ideal_cutout_width <- 9.1890 # 0.2334 m
ideal_cutout_height <- 8.9685 # 0.2278 m
ideal_cutout_area <- ideal_cutout_width * ideal_cutout_height
# TODO 

###### START WRITE FILE ###### 
sink(paste(output_folder, cuts_filename, sep="/"), append=FALSE)

print("############################")
print("Summary Statistics")
print("############################")
print_summary(log_data, "Cutout_Area_Inches")

print("############################")
print("Cutout area t-test")
print("############################")

# Assumptions
ar_shapiro <- shapiro.test(log_data[log_data$Augmentation==TRUE,]$Cutout_Area_Inches)
print(ar_shapiro)
paper_shapiro <- shapiro.test(log_data[log_data$Augmentation==FALSE,]$Cutout_Area_Inches)
print(paper_shapiro)
if(ar_shapiro$p.value < 0.05 | paper_shapiro$p.value < 0.05)
{
  print("Assumption of normailty: FAILED")
} else
{
  print("Assumption of normailty: PASSED")
}
# T-test
t <- t.test(log_data$Cutout_Area_Inches~log_data$Augmentation,
            paired=FALSE,
            alternative="two.sided",
            conf.level=0.95)
print(t) 

print("############################")
print("Cutout Area Wilcoxin test")
print("############################")

wilcoxin <- wilcox.test(log_data$Cutout_Area_Inches ~ log_data$Augmentation,
                        paired = FALSE,
                        alternative = "two.sided",
                        #conf.level = 0.95,
                        exact = FALSE)
print(wilcoxin)
print(wilcoxonR(x = log_data$Cutout_Area_Inches, g = log_data$Augmentation))

print("############################")
print("Levene Test for variance")
print("############################")

# Can't use F-test since data is not normally distributed.
print(leveneTest(data=log_data,
                 Cutout_Area_Inches ~ Augmentation))


###### STOP WRITE FILE ###### 
sink()

##############################################
### Plot - Mistakes count (bar plot)
##############################################

# Plot
mistakes_plot <- ggplot(log_data, aes(x=Augmentation, y=Mistakes, fill=Augmentation)) +
  geom_boxplot(alpha=0.7,
               size=1.25,
               color="black") +
  scale_fill_manual(values=c(paper_color, ar_color),
                    labels=c("Paper", "AR")) +
  scale_x_discrete(labels=c("Paper", "AR")) + 
  labs(
    title="Critical Mistakes Made",
    x="Augmentation",
    y="Mistakes") +
  #theme_classic() +
  theme_bw() +
  theme(
    # Text
    text = element_text(family="serif"), # Times New Roman
    plot.title = element_text(size=18, face="bold", hjust=0.5), 
    axis.title = element_text(size=18, face="italic", hjust=0.5),
    axis.text = element_text(size=14),
    # Axis Ticks
    axis.ticks = element_blank(),
    # Legend
    legend.position = "none",
    # Borders
    panel.border = element_rect(color=plot_outline_color, fill=NA, size=plot_outline_size),
    panel.grid.major = element_line(color=plot_grid_color, size=plot_grid_size_major),
    panel.grid.minor = element_line(color=plot_grid_color, size=plot_grid_size_minor),
    panel.grid.major.x = element_blank()
  )
print(mistakes_plot)

##############################################
### Plot - Cutout Area
##############################################

# Plot
cutout_plot <- ggplot(log_data, aes(x=Augmentation, y=Cutout_Area_Inches, fill=Augmentation)) +
  geom_boxplot(alpha=0.7,
               size=1.15,
               color="black") +
  geom_jitter(color="black",
              size=0.5,
              alpha=0.9) +
  scale_fill_manual(values=c(paper_color, ar_color)) +
  scale_x_discrete(labels=c("Paper", "AR")) + 
  #ylim(25, 150) +
  labs(
    title="Final Cutout Area",
    x="Augmentation",
    y="Cutout Area (Square Inch)") +
    #y=bquote('Cutout Area '(inch^2))) +
  theme_bw() + 
  #coord_flip()
  theme(
    # Text
    text = element_text(family="serif"), # Times New Roman
    plot.title = element_text(size=18, face="bold", hjust=0.5), 
    axis.title = element_text(size=18, face="italic", hjust=0.5),
    axis.text = element_text(size=14),
    # Axis Ticks
    axis.ticks = element_blank(),
    # Legend
    legend.position = "none",
    # Borders
    panel.border = element_rect(color=plot_outline_color, fill=NA, size=plot_outline_size),
    panel.grid.major = element_line(color=plot_grid_color, size=plot_grid_size_major),
    panel.grid.minor = element_line(color=plot_grid_color, size=plot_grid_size_minor),
    panel.grid.major.x = element_blank()
  )
print(cutout_plot)

##############################################
### Plot - Stud Location
##############################################

stud_location_plot <- ggplot(log_data, aes(fill=Augmentation, color=Augmentation)) +
  geom_vline(aes(xintercept=Stud_Percentage,
                 color=Augmentation),
             size=0.5) +
  geom_vline(xintercept=0.765,
             color='black',
             size=1.5) +
  # geom_boxplot(aes(x=Stud_Percentage),
  #              alpha=0.2,
  #              color="darkgreen") +
  #scale_fill_manual(values=c(paper_color, ar_color)) +
  scale_color_manual(values=c(paper_color, ar_color)) +
  ##xlim(0.7, 0.95) +
  xlim(0, 1.0) + 
  labs(
    title="Stud Location",
    x="Marked Stud Position"
  ) +
  facet_grid(Augmentation ~ .,
             labeller=labeller(Augmentation=c("TRUE" = "AR", "FALSE" = "Paper"))) + 
  theme_bw() +
    theme(
      # Text
      text = element_text(family="serif"), # Times New Roman
      plot.title = element_text(size=18, face="bold", hjust=0.5), 
      axis.title = element_text(size=18, face="italic", hjust=0.5),
      axis.text = element_text(size=14),
      # Axis Ticks
      axis.ticks = element_blank(),
      # Legend
      legend.position = "none",
      # Facet
      strip.text = element_text(size=14, hjust=0.5, vjust=0.5),
      strip.background = element_rect(color="black", fill="gray85"),
      # Borders
      panel.border = element_rect(color=plot_outline_color, fill=NA, size=plot_outline_size),
      panel.grid.major = element_line(color=plot_grid_color, size=plot_grid_size_major),
      panel.grid.minor = element_line(color=plot_grid_color, size=plot_grid_size_minor)
    )
print(stud_location_plot)

##############################################
### Qualtrics data
##############################################

qualtrics_data <- read.csv("../Subjects/Qualtrics.csv",
                           #skip=1,
                           header=TRUE,
                           sep=",")
qualtrics_data <- qualtrics_data[-1:-2,] # Drop junk data

# Rename essential columns in data and drop unused subjects
colnames(qualtrics_data)[colnames(qualtrics_data) == "X1"] ="Participant.ID"
colnames(qualtrics_data)[colnames(qualtrics_data) == "X4"] ="Augmentation"  
colnames(qualtrics_data)[colnames(qualtrics_data) == "X5"] ="Condition"
colnames(qualtrics_data)[colnames(qualtrics_data) == "X2.5"] ="Construction.Familiarity"
colnames(qualtrics_data)[colnames(qualtrics_data) == "X4.4"] ="Construction.Experience"

qualtrics_data <- qualtrics_data[!qualtrics_data$Participant.ID %in% subjects_to_remove, ] # Remove unused subjects

# Factor/Unify data names with other data frames
qualtrics_data$Augmentation[qualtrics_data$Augmentation == "Augmented Reality"] <- "AR"
#qualtrics_data$Augmentation <- as.logical(qualtrics_data$Augmentation) # Cast to boolean for condition value

# SUS (1 (Strongly disagree) to 5 (Strongly agree))
sus_cols <- 71:80
sus_data <- qualtrics_data[,sus_cols]
colnames(sus_data) <- 1:10 # Update column names to match answer key
sus_data[1:10] <- sapply(sus_data[1:10],as.numeric) # Cast to numeric for scoring
sus_data$Participant.ID <- qualtrics_data$Participant.ID # Re-add participant ID
# Score the SUS (https://www.measuringux.com/sus/index.htm)
# FORMULA: = ((B2-1)+(5-C2)+(D2-1)+(5-E2)+(F2-1)+(5-G2)+(H2-1)+(5-I2)+(J2-1)+(5-K2))*2.5
sus_data$SUS_Score <- (
  (sus_data$'1' - 1) +
  (5 - sus_data$'2') +
  (sus_data$'3' - 1) +
  (5 - sus_data$'4') +
  (sus_data$'5' - 1) +
  (5 - sus_data$'6') +
  (sus_data$'7' - 1) +
  (5 - sus_data$'8') +
  (sus_data$'9' - 1) +
  (5 - sus_data$'10')) * 2.5
# Add SUS back into overall subject log
log_data <- merge(x = log_data, y = sus_data[ , c("Participant.ID", "SUS_Score")], by = "Participant.ID", all.x=TRUE)
  
# Score the TLX (https://measuringu.com/nasa-tlx/#:~:text=To%20score%2C%20you%20count%20the,to%20a%20hundred%2Dpoint%20scale.)
tlx_cols <- 81:85
tlx_data <- qualtrics_data[,tlx_cols]
tlx_data <- mutate_all(tlx_data, function(x) as.numeric(as.character(x)))
tlx_data$Participant.ID <- qualtrics_data$Participant.ID # Re-add participant ID
# Rename columns
colnames(tlx_data)[1] <- "Mental_Demand_Raw"
colnames(tlx_data)[2] <- "Physical_Demand_Raw"
colnames(tlx_data)[3] <- "Temporal_Demand_Raw"
colnames(tlx_data)[4] <- "Performance_Demand_Raw"
colnames(tlx_data)[5] <- "Effort_Demand_Raw"
# Score them
tlx_data$Mental_Demand_Score <- (tlx_data$Mental_Demand_Raw - 1) * 5
tlx_data$Physical_Demand_Score <- (tlx_data$Physical_Demand_Raw - 1) * 5
tlx_data$Temporal_Demand_Score <- (tlx_data$Temporal_Demand_Raw - 1) * 5
tlx_data$Performance_Demand_Score <- (tlx_data$Performance_Demand_Raw - 1) * 5
tlx_data$Effort_Demand_Score <- (tlx_data$Effort_Demand_Raw - 1) * 5
# Frustration missing...
# Add TLX back into overall subject log
log_data <- merge(x = log_data, y = tlx_data[ , c("Participant.ID", "Mental_Demand_Score", "Physical_Demand_Score", "Temporal_Demand_Score", "Performance_Demand_Score", "Effort_Demand_Score")], by = "Participant.ID", all.x=TRUE)

# Paper folding answer key
### TODO

###### START WRITE FILE ###### 
sink(paste(output_folder, usability_filename, sep="/"), append=FALSE)

print("############################")
print("Summary Statistics")
print("############################")
print_summary(log_data, "SUS_Score")
print_summary(log_data, "Mental_Demand_Score")
print_summary(log_data, "Physical_Demand_Score")
print_summary(log_data, "Temporal_Demand_Score")
print_summary(log_data, "Performance_Demand_Score")
print_summary(log_data, "Effort_Demand_Score")

print("############################")
print("Usability t-test's")
print("############################")

# Create empty frame to multiple t test comparisons to
usability_t_tests <- data.frame(matrix(ncol=2, nrow=0)) 
colnames(usability_t_tests) <- c("Metric", "p_value")

usability_t_test <- function(usability_df, metric)
{
  print(paste0("###### ", metric, " ######"))
  usability_subset <- usability_df[,c("Augmentation", metric)]
  # Assumptions
  ar_shapiro <- shapiro.test(usability_subset[usability_subset$Augmentation==TRUE,][[metric]])
  print(ar_shapiro)
  paper_shapiro <- shapiro.test(usability_subset[usability_subset$Augmentation==FALSE,][[metric]])
  print(paper_shapiro)
  if(ar_shapiro$p.value < 0.05 | paper_shapiro$p.value < 0.05)
  {
    print("Assumption of normailty: FAILED")
  } else
  {
    print("Assumption of normailty: PASSED")
  }
  # T-test
  t <- t.test(usability_subset[[metric]]~usability_subset$Augmentation,
              #x=usability_subset$Augmentation, 
              #y=usability_subset[metric],
              paired=FALSE,
              alternative="two.sided",
              conf.level=0.95)
  print(t) 
  p_val <- t$p.value
  return(c(metric, p_val))
}

# Run t-tests
usability_t_tests[nrow(usability_t_tests) + 1,] <- usability_t_test(log_data, "SUS_Score")
usability_t_tests[nrow(usability_t_tests) + 1,] <- usability_t_test(log_data, "Mental_Demand_Score")
usability_t_tests[nrow(usability_t_tests) + 1,] <- usability_t_test(log_data, "Physical_Demand_Score")
usability_t_tests[nrow(usability_t_tests) + 1,] <- usability_t_test(log_data, "Temporal_Demand_Score")
usability_t_tests[nrow(usability_t_tests) + 1,] <- usability_t_test(log_data, "Performance_Demand_Score")
usability_t_tests[nrow(usability_t_tests) + 1,] <- usability_t_test(log_data, "Effort_Demand_Score")

# Adjust for multiple comparisons using Bonferroni (https://rcompanion.org/rcompanion/f_01.html)
usability_t_tests$Bonferroni <- p.adjust(usability_t_tests$p_value, method="bonferroni")
print("Bonferroni Adjusted p-Values")
print(usability_t_tests)

# Statistical tests - Wilcoxin
usability_wilcoxin <- function(usability_df, metric)
{
  print(paste0("###### ", metric, " ######"))
  x <- usability_df$Augmentation
  y <- usability_df[[metric]]
  print(x)
  print(y)
  wilcoxin <- wilcox.test(y ~ x,
                          paired = FALSE,
                          alternative = "two.sided",
                          conf.level = 0.95,
                          exact = FALSE)
  print(wilcoxin)
  print(wilcoxonR(x = usability_df[[metric]], g = usability_df$Augmentation))
}

print("############################")
print("Usability Wilcoxin tests")
print("############################")
usability_wilcoxin(log_data, "SUS_Score")
usability_wilcoxin(log_data, "Mental_Demand_Score")
usability_wilcoxin(log_data, "Physical_Demand_Score")
usability_wilcoxin(log_data, "Temporal_Demand_Score")
usability_wilcoxin(log_data, "Performance_Demand_Score")
usability_wilcoxin(log_data, "Effort_Demand_Score")

print("############################")
print("Prev. AR/VR experience and SUS")
print("############################")
# 2.4 <- Prev. AR Experience (1 - 7)
# 5.1 <- Prev AR or VR Experience (1 - 10)
cor_col <-"X5.1"
print(shapiro.test(as.integer(qualtrics_data[qualtrics_data$Augmentation=="AR",][[cor_col]])))
print(shapiro.test(log_data[log_data$Augmentation==TRUE,]$SUS_Score))
# Cant use Pearson beacuse not normally distributed, so use Spearman (https://www.geeksforgeeks.org/spearman-correlation-testing-in-r-programming/)
sus_cor <- cor.test(as.integer(qualtrics_data[qualtrics_data$Augmentation=="AR",][[cor_col]]), 
                    log_data[log_data$Augmentation==TRUE,]$SUS_Score,
                    method="spearman",
                    exact=FALSE)
print(sus_cor)

###### STOP WRITE FILE ###### 
sink()

print("############################")
print("Prev. Construction Experience and Condition")
print("############################")
wilcoxin <- wilcox.test(as.numeric(qualtrics_data$Construction.Experience) ~ qualtrics_data$Augmentation,
                        paired = FALSE,
                        alternative = "two.sided",
                        conf.level = 0.95,
                        exact = FALSE)
print(wilcoxin)
print(wilcoxonR(x = as.numeric(qualtrics_data$Construction.Experience), g = qualtrics_data$Augmentation))

print("############################")
print("General pre-questionnaire stats")
print("############################")

# X1.3 = Age
# X4.2 = Physical activity (1 - 10)
# X3.4 = Gaming freq (1 - 10)
# X1.4 = VR frq (1 - 7)
# X2.4 = AR frq (1 - 7)
# X4.3 = 3D modeling (1 - 7)
# X5.2 = Computer use freq (1 - 7)
# Construction.Experience

print_general_stats(subset(qualtrics_data, Augmentation=="AR"), "X1.3") # AGE
print_general_stats(subset(qualtrics_data, Augmentation=="Paper"), "X1.3") # AGE
print_general_stats(subset(qualtrics_data, Augmentation=="AR"), "X4.2") # TODO

##############################################
### Plot - SUS and TLX
##############################################

usability_melted <- melt(select(log_data, c("Augmentation", "SUS_Score", "Mental_Demand_Score", "Physical_Demand_Score", "Temporal_Demand_Score", "Performance_Demand_Score", "Effort_Demand_Score")), 
                         id = ("Augmentation"),
                         variable.name = "Metric",
                         value.name = "Score")
# Re-order and refactor
usability_melted <- usability_melted %>%
  mutate(Metric = factor(Metric, levels=c("SUS_Score", "Mental_Demand_Score", "Physical_Demand_Score", "Temporal_Demand_Score", "Performance_Demand_Score", "Effort_Demand_Score")))
levels(usability_melted$Metric) <- c("SUS", "TLX - Mental", "TLX - Physical", "TLX - Temporal", "TLX - Performance", "TLX - Effort")

# Plot
usability_plot <- ggplot(usability_melted, aes(x=Metric, y=Score, fill=Augmentation)) +
  geom_boxplot(alpha=0.7,
               width=0.6,
               size=1,
               color="black",
               outlier.shape=NA) +
  # geom_jitter(color="black",
  #             size=0.4,
  #             alpha=0.9) +
  scale_fill_manual(values=c(paper_color, ar_color),
                    labels=c("Paper", "AR")) +
  scale_x_discrete(limits = rev(levels(usability_melted$Metric))) +
  #scale_x_discrete(labels=rev(c("TLX - Effort",
  #                          "TLX - Performance",
  #                          "TLX - Temporal",
  #                          "TLX - Physical",
  #                          "TLX - Mental",
  #                          "SUS"))) +
  labs(
    title="Post-Questionnaire Metrics",
    x="Test",
    y="Normalized Score") +
  #theme_classic() +
  theme_bw() +
  coord_flip() + 
  theme(
    # Text
    text = element_text(family="serif"), # Times New Roman
    plot.title = element_text(size=18, face="bold", hjust=0.5), 
    axis.title = element_text(size=18, face="italic", hjust=0.5),
    axis.title.y = element_blank(),
    axis.text = element_text(size=14),
    # Axis Ticks
    axis.ticks = element_blank(),
    # Legend
    legend.background = element_rect(color="black", size=0.5, linetype="dashed"),
    legend.position = "bottom",
    legend.title = element_text(size=14, face="italic", hjust=0.5),
    legend.text = element_text(size=12),
    legend.direction = "horizontal",
    # Borders
    panel.border = element_rect(color=plot_outline_color, fill=NA, size=plot_outline_size),
    panel.grid.major = element_line(color=plot_grid_color, size=plot_grid_size_major),
    panel.grid.minor = element_line(color=plot_grid_color, size=plot_grid_size_minor),
    panel.grid.major.y = element_blank()
  )# + 
  #scale_x_discrete(limits = rev(levels(usability_melted$Metric)))
print(usability_plot)

##############################################
### Watch data
##############################################

# TODO