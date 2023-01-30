library(tidyverse)
library(ggplot2)
library(dplyr)
library(ggpubr)

setwd("C:/Users/b01297ar/Documents/ProstateMRL-local/ProstateMRL-Radiomics/Data/")
df_all <- read.csv("All_Features_2.csv")

treatment = "SABR"

## Input Feature Data
### Want to carry out feature reduction by correlating feature values with volume at given timepoints. 
df_all <- select(df_all, -c("X", "Unnamed..0", "Unnamed..0.1"))
df_all$Treatment <- gsub("_new", "", as.character(df_all$Treatment))
df_all <- df_all[,-c(6:27, 130:131)]

print(head(df_all))#, 10))
df_all = subset(df_all, Normalisation!= "Norm-Pros"& Normalisation != "Norm-Glute" & Normalisation != "Norm-Psoas")
df_all <- filter(df_all, Treatment==treatment)

### Pivot to long format.
df_long <- pivot_longer(df_all, cols = c(6:107), names_to = "FeatureName", values_to = "FeatureValue")
df_long$FeatureName <-  gsub('original_', "", as.character(df_long$FeatureName))


### Create a second dataframe containing only volume values and remove from total dataframe along with Minimum and shape fts (offers nothing).
### Leaves 87 features.
df_vol <- df_long %>% 
  filter(FeatureName == "shape_MeshVolume")%>% 
  filter(Normalisation == "Raw") %>% 
  subset(select = -c(Normalisation, FeatureName)) %>% 
  rename(Volume = FeatureValue)

df_long <- df_long[!grepl("shape", df_long$FeatureName),]
df_long <- df_long[!(df_long$FeatureName == "firstorder_Minimum"),]

patIDs <- as.character(unique(df_long$PatID))
Features <- unique(df_long$FeatureName)
Norms <- unique(df_long$Normalisation)

df_volcorr <- data.frame()

# Loop through each normalisation to determine vol correlation from first timepoint
for (n in Norms){
  print(n)
  df_n <- filter(df_long, Normalisation == n)
  df_d <- filter(df_n, DaysDiff == 0)
  
  # Loop through each feature
  for (f in Features){
    
    df_temp1 <- data.frame()
    df_f <- filter(df_d, FeatureName == f)
    
    # Check for empty rows
    df_na1 <- df_vol_d[is.na(df_vol_d$Volume),]
    if(nrow(df_na1) > 0){
      cat(n,f,d, "\n", df_na1, "\n")
    }
    sp_corr <- cor(df_f$FeatureValue, df_vol_d$Volume, "everything", "spearman")
    df_temp1 <- data.frame(n, f, sp_corr)
    df_volcorr <- rbind(df_volcorr, df_temp1)
  }
}

colnames(df_volcorr) <- c("Normalisation", "Feature", "SPCorr")

ls_vol_ind <- split(df_long, df_long$Normalisation)
# remove fts correlated with volume
for(n in Norms){
  print(n)
  df_n <- df_volcorr %>% 
    filter(Normalisation == n) %>% 
    filter(abs(SPCorr) < 0.6)
  
  fts_ind <- df_n$Feature
  
  ls_vol_ind[[n]] <- filter(ls_vol_ind[[n]], FeatureName %in% fts_ind)
}

# calc feature change variable
for(n in Norms){
  df_n <- ls_vol_ind[[n]]
  df_newp <- data.frame()
  for(p in patIDs){
    df_p <- filter(df_n, PatID == p)
    fts <- unique(df_p$FeatureName)
    
    for(f in fts){
      df_f <- filter(df_p, FeatureName == f)
      df_f$FeatureChange <- (df_f$FeatureValue - df_f$FeatureValue[1]) / df_f$FeatureValue[1]
      df_newp <- rbind(df_newp,df_f)
    }
  }
  ls_vol_ind[[n]] <- df_newp
}


lapply(1:length(ls_vol_ind), function(x) write.csv(ls_vol_ind[[x]],file = paste("./VolIndFts/", names(ls_vol_ind[x]), ".csv", sep=""), row.names = FALSE ))

       