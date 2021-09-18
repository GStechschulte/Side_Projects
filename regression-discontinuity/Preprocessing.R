source("/Users/gabestechschulte/Documents/git-repos/Side_Projects/Difference-in-Difference/helpers.R")

library(ggplot2)
library(fasttime)
library(MASS)
library(lubridate)
library(tidyverse)
library(dplyr)
library(plotly)

# -----------------

tnp_trips = data.table::fread('/Volumes/GabeTB/Data/chicago/chicago-ride-hailing-2M.csv') %>%
  as_tibble() %>%
  filter(
    !is.na(pickup_community_area)
  )

# -----------------

## New dataframe with new features engineered and features with criteria filtering ##

tnp_trips = tnp_trips %>%
  mutate(
    trip_minutes = trip_seconds / 60,
    trip_start = fastPOSIXct(trip_start_timestamp, tz = "UTC"),
    pickup_census_tract = as.character(pickup_census_tract),
    dropoff_census_tract = as.character(dropoff_census_tract),
    trip_id = row_number(),
    #share_requested = shared_trip_authorized %in% c("true", "false"),
    calendar_month = as.Date(floor_date(trip_start, unit = "month")),
    mph = 60 * trip_miles / trip_minutes,
    has_clean_fare_info = (
      !is.na(fare) & !is.na(trip_miles) & !is.na(trip_minutes) &
        (trip_miles >= 1.5 | trip_minutes >= 8) &
        trip_miles >= 0.5 & trip_miles < 100 &
        trip_minutes >= 2 & trip_minutes < 180 &
        mph >= 0.5 & mph < 80 &
        fare > 2 & fare < 1000 &
        fare / trip_miles < 25
    )
  ) %>%
  #select(-trip_seconds) %>%
  left_join(area_sides, by = c("pickup_community_area" = "community_area")) %>%
  rename(pickup_side = side)

# -----------------

## Visualizations ##

ggplot(data=tnp_trips,
       aes(x=trip_miles, y=has_clean_fare_info)) +
  geom_point()

ggplot(data=tnp_trips,
       aes(x=trip_seconds, y=fare)) +
  geom_point()

fig <- tnp_trips
fig <- fig %>% 
  layout(
    type = 'densitymapbox',
    lat = ~pickup_centroid_latitude,
    lon = ~pickup_centroid_longitude,
    coloraxis = 'coloraxis',
    radius = 10
  )

# -----------------
