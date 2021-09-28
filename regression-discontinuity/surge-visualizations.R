library(plotly)
library(ggplot2)
library(tidyverse)

## Visualizations ##

rides = data.table::fread('/Volumes/GabeTB/Data/chicago/ride-hailing-preprocessed.csv') %>%
  as_tibble()

# ------------------

# Proportion clean vs non-clean
ggplot(data=rides,
       aes(x=trip_miles, y=has_clean_fare_info)) +
  geom_point()

# ------------------

# We expect a linear relationship - except for some non-linearity as a result of latent variables (due to 2d plotting)
rides %>% 
  filter(has_clean_fare_info == TRUE) %>%
  ggplot(aes(x = trip_miles, y=fare)) +
  geom_point()

# We expect a linear relationship - except for some non-linearity as a result of latent variables (due to 2d plotting)
rides %>% 
  filter(has_clean_fare_info == TRUE) %>%
  ggplot(aes(x = trip_minutes, y=fare)) +
  geom_point()

# ------------------

# Geographic Density Plot - THIS DOES NOT WORK
fig <- rides
fig <- fig %>% 
  layout(
    type = 'densitymapbox',
    lat = ~pickup_centroid_latitude,
    lon = ~pickup_centroid_longitude,
    coloraxis = 'coloraxis',
    radius = 10
  )

# ------------------

# Surge multiplier - not rounded
rides %>% 
  filter(has_clean_fare_info == TRUE &
           (fare_ratio >= 1.15 & fare_ratio <= 2.0)) %>%
  ggplot(aes(x = fare_ratio, y=fare)) +
  geom_point(position = position_jitter()) +
  geom_smooth() +
  geom_vline(xintercept = c(1.25, 1.35, 1.45, 1.55, 1.65, 1.75, 1.85, 1.95), color='red', size=0.5)

# Surge multiplier - not rounded and plotted by range
rides %>% 
  filter(has_clean_fare_info == TRUE &
           (fare_ratio >= 1.15 & fare_ratio <= 1.35)) %>%
  ggplot(aes(x = fare_ratio, y=fare)) +
  geom_point(position = position_jitter()) +
  geom_smooth() +
  geom_vline(xintercept = 1.25, color='red', size=0.5)

# ------------------

# Surge multiplier - rounded all multpliers
rides %>% 
  filter(has_clean_fare_info == TRUE) %>%
  ggplot(aes(x = fare_rounded, y=fare)) +
  geom_point(position = position_jitter()) +
  geom_smooth() +
  geom_vline(xintercept = 1.25, color='red', size=0.5)

# Surge multiplier - rounded multipler and plotted by range
rides %>% 
  filter(has_clean_fare_info == TRUE &
           (fare_rounded >= 1.15 & fare_rounded <= 1.35)) %>%
  ggplot(aes(x = fare_rounded, y=fare)) +
  geom_point(position = position_jitter()) +
  geom_smooth() +
  geom_vline(xintercept = 1.25, color='red', size=0.5)

# ------------------

# New metric - surge surplus experienced by ride hailers
rides = rides %>%
  mutate(
    surge_surplus = fare_ratio - fare_rounded
  )

# ------------------

# Consumer Surge Surplus
rides %>% 
  filter(has_clean_fare_info == TRUE &
           (fare_rounded >= 1.15 & fare_rounded <= 1.35)) %>%
  ggplot(aes(x = fare_rounded, y=surge_surplus)) +
  geom_point(position = position_jitter()) +
  geom_vline(xintercept = 1.25, color='red', size=0.5)

# ------------------

# Plotly interactive plotting - to zoom in on areas around rounding discontinuity
fig <- plot_ly(data = rides, x = ~fare_rounded, y = ~fare, type='scatter', mode='markers') %>%
  layout(title='Surge Multplier Rounding Discontinuity')
fig




