setwd("D:/Aaron/ProstateMRL/code/extraction/")
library(tidyverse)
library(irr)
library(data.table)
library(splitstackshape)

# import files
data_files <- list.files("D:/Aaron/ProstateMRL/data/extraction/patientDatainfo/")

# read in files + clean names
scans <- lapply(data_files, read.csv)
names(scans) <- str_remove_all(data_files, "[BladderMR, .csv]")

# clean column names and get patient + timepoint
scans <- lapply(scans,function(x) {
  colnames(x) <- gsub("\\_.*","", colnames(x)) 
  x })

# bind all rows of list of dfs together
long_format_df <- dplyr::bind_rows(scans,.id='Patient_Timepoint')

# pivot to allow for change in region + observer
long_format_df <- long_format_df %>% 
  pivot_longer(cols = 3:6, names_to = "Obs_region" ) %>% 
  relocate(Obs_region, .before = X)

# convert to wide format and split in to identifying cols with features along top
wide_format_df <- pivot_wider(long_format_df, id_cols = c(1,2), names_from = X, values_from = c(4))
wide_format_df <- wide_format_df %>% 
  separate(col=Patient_Timepoint, sep = "_", into=c("Patient", "Timepoint")) %>% 
  separate(col=Obs_region, sep = 2:3, into=c("Observer", "Region"))

# Gwt unique variables just in case need them
#Patient_IDs <- unique(wide_format_df$Patient)
#Time_points <- unique(wide_format_df$Timepoint)
#Observers <- unique(wide_format_df$Observer)
#Regions <-  unique(wide_format_df$Region)
Feature_names <- colnames(select(wide_format_df, 27:114))

#working with baseline scans for now
baseline_scans_t <- wide_format_df %>% 
  filter(Timepoint == "1", Region == "t") %>%
  # get rid of non-useful columns, just features
  select(-c(2,4:26)) 

# define empty results DF for holding ICCs
results <- data.frame(array(NA, dim = c(length(Feature_names),4)))
colnames(results) <- c("Feature", "ICC", "ICC_lb", "ICC_ub")

tumour_list <- filter(wide_format_df, Region == "t")
tumour_list <- split(tumour_list, f=tumour_list$Timepoint)
tumour_list <- lapply(tumour_list, function(x){
  x <- select(x,-c(2,4:26))
}
)

Tumour_ICCs <-  as.list(1:4)
lapply(tumour_list, function(x){
  for (f in 1:88){
    testcase <- pivot_wider(x,id_cols=Patient,names_from = c(Observer),values_from=c(f+2))
    testcase <- mutate_all(testcase,as.numeric)
    #print(testcase)
    hold2 <- icc(testcase[-1], model = c("twoway"), type = c("agreement"), unit = c("single"))
    #print(Feature_names[f])
    #print(hold2$value)
    results[f,1] <- Feature_names[f]
    results[f,2] <- hold2$value
    results[f,3] <- hold2$lbound
    results[f,4] <- hold2$ubound
  }
  print(results)
  c(list(results), Tumour_ICCs) 
})








