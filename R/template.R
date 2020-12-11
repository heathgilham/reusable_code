# Purpose: 
## Author: Heath Gilham
##
## To Do: logging

## Setup variables
StartTime = proc.time()
setwd("")

## Import Packages
PackagesUsed <- c("data.table", "dplyr")

# Install Missing Packages
PackagesToInstall <- PackagesUsed[!(PackagesUsed %in% installed.packages()[,"Package"])]
if(length(PackagesToInstall)>0) {install.packages(PackagesToInstall)}

# Load Packages
dummy = lapply(PackagesUsed, require, character.only = TRUE)


## Data setup


## End 
TimeTaken = proc.time() - StartTime ; TimeTaken