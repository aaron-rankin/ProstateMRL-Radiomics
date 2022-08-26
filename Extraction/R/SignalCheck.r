library(dplyr) # for `rename` & `select`
library(tidyr) # for `gather`
library(ggplot2)

setwd("C:/Users/b01297ar/Documents/ProstateMRL-local/ProstateMRL-Radiomics/Data/")

data <- read.csv("All_signal_changes_pyRad.csv")

PatIDs <- unique(data$PatID)
Norms <- unique(data$Normalisation)
Regions <- unique(data$Region)

pat_df <- filter()
