library(dplyr) # for `rename` & `select`
library(tidyr) # for `gather`
library(ggplot2)
library(patchwork)

setwd("C:/Users/b01297ar/Documents/ProstateMRL-local/ProstateMRL-Radiomics/Data/")

data <- read.csv("All_signal_changes_pyRad.csv")

PatIDs <- unique(data$PatID)
Norms <- unique(data$Normalisation)
Regions <- unique(data$Region)
pat_df <- data %>%
  filter(PatID == PatIDs[1])
         #Normalisation == Norms[1])
pros_df <- filter(pat_df, Region == Regions[1])
glute_df <- filter(pat_df, Region == Regions[2])
psoas_df <- filter(pat_df, Region == Regions[3])

pros_mean <- ggplot(data = pros_df, mapping = aes(x = DaysDiff, y = Mean)) +
  geom_point(aes(color = Normalisation)) + 
  geom_line(aes(color = Normalisation)) +
  labs(title = "Prostate") 

pros_med <- ggplot(data = pros_df, mapping = aes(x = DaysDiff, y = Median)) +
  geom_point(aes(color = Normalisation)) + 
  geom_line(aes(color = Normalisation)) 
  

glute_mean <- ggplot(data = glute_df, mapping = aes(x = DaysDiff, y = Mean)) +
  geom_point(aes(color = Normalisation)) + 
  geom_line(aes(color = Normalisation)) +
  labs(title = "Glute") 

glute_med <- ggplot(data = glute_df, mapping = aes(x = DaysDiff, y = Median)) +
  geom_point(aes(color = Normalisation)) + 
  geom_line(aes(color = Normalisation))

psoas_mean <-  ggplot(data = psoas_df, mapping = aes(x = DaysDiff, y = Mean)) +
  geom_point(aes(color = Normalisation)) + 
  geom_line(aes(color = Normalisation)) + 
  labs(title = "Psoas") 

psoas_med <- ggplot(data = psoas_df, mapping = aes(x = DaysDiff, y = Median)) +
  geom_point(aes(color = Normalisation)) + 
  geom_line(aes(color = Normalisation))

plot_combined <- ((pros_mean / pros_med) | (glute_mean / glute_med) | (psoas_mean / psoas_med)) & theme(legend.position = "bottom")
plot_combined + plot_layout(guides = "collect")


