# Weather-To-Eat-Or-Not-Dataset
### -- Uncover the nation’s appetite – a decision support dataset for would-be restauranteurs

## Introduction - Abeer
Scope, motivation and purpose.



## Data Dictionary - Devanshi

Explanation of each attribute in Yelp and OpenWeatherMap and why certain attributes were eliminated in dataset.

Data Dictionary - Restaurant Review Dataset

Name | Data Type | Description
------- | -------- | ---------
date_id | string | Unique ID to map the restaurant review and weather information dataset
id | string | Unique Yelp ID of this business. Example: '4kMBvIEWPxWkWKFN__8SxQ'
name | string | Name of this business
is_closed | bool | Whether business has been (permanently) closed
url | string | URL for business page on Yelp
review_count | int | Number of reviews for this business
categories | string | Title of a category for display purpose. Example: Japanese, Italian, Juicebars vegan
rating | decimal | Rating for this business (value ranges from 1, 1.5, ... 4.5, 5)
latitude | decimal | Latitude coordinates of this business
longitude | decimal | Longitude coordinates of this business
transactions | string[] | List of Yelp transactions that the business is registered for. Current supported values are pickup, delivery and restaurant_reservation.
price | string | Price level of the business. Value is one of $, $$, $$$ and $$$$.
display_phone | string | Array of strings that if organized vertically give an address that is in the standard address format for the business's country
display_phone | string | Phone number of the business formatted nicely to be displayed to users. The format is the standard phone number format for the business's country
distance | decimal | Distance in meters from the search location. This returns meters regardless of the locale

Data Dictionary - Weather Information Dataset

Name | Data Type | Description
------- | -------- | ---------
date_id | string | Unique ID to map the restaurant review and weather information dataset
weather_main | string | Group of weather parameters (Example: Clouds, Rain, Snow, Extreme etc.)
weather_description | string | Weather condition within the group mentioned above (Example: Broken clouds, Few clouds, Light rain etc.)
main_temp | decimal | The temperature of that day. The default unit considered here is Kelvin
main_pressure | decimal | Atmospheric pressure of that day in hPa (hectopascals)
main_humidity | int | Relative air humidity of that day in %
main_temp_min | decimal | Minimum temperature on that day. The default unit considered here is Kelvin
main_temp_max | decimal | Maximum temperature on that day. The default unit considered here is Kelvin
visibility | decimal | Visibility on that day in meters
wind_speed | decimal | Speed of the wind in mps (meters per second)
wind_deg | decimal | Direction of the wind that day in degrees (meteorogical) (Example: 270 degrees means the wind is blowing from the west
clouds_all | int | The % of cloudiness/cloud cover for that day
dt | int | Date & time of receiving data in the unix timestamp format, UTC (Example: Unix timestamp 1541696160 is equivalent to 11/08/2018 @ 4:56pm (UTC))
sys_sunrise | int | Date & time of sunrise in the unix timestamp format, UTC
sys_sunset | int | Date & time of sunrise in the unix timestamp format, UTC
id | int | City ID
name | string | City name


## Working with the APIs - Stella
This program allows users to obtain restaurant review and weather information based on customized location and business type.

The Yelp Fusion APIs offer several endpoints including search, business details, etc. Each endpoint returns a specific facet about the businesses in Yelp's database. Its construct is similar to many database APIs in that one first needs to identify a unique ID of the desired entity by certain parameters in order to obtain more attributes of it, hence the separate end points search and business details.

In reviewing the API documentations, we summarized the following limits of the service.
  1. A client is limited to 5,000 APIs per 24 hours resetting every midnight UTC.
  2. If queries against the API are deemed too frequent, the service will return a HTTP 429 error (too many requests). However, the documentation does not specify the maximum allowed frequency. We set our requests to be one second apart.
  3. A client can get up to 1,000 businesses from the search endpoint.
  4. Each call can have a maximum of 50 return results. (paging)

Due to the aforementioned limits, our data scope is to query the top 1000 restaurants for one city. We had to use the `offset` parameter, so that we obtain 1,000 in 20 calls. All results from the same day were stored in a list and JSON file. We also found out that Yelp's limits were enforced in a funny way. On day 1, a total of 86 calls were accepted before the server gave an out of limit message. On day 3, only 20 calls were accepted.

Another interesting quirk about the API is its sort_by function in that it is not strictly enforced by the sort criteria. Yelp will weigh multiple input parameters to return the most relevant results. Therefore, our calls to request the best rated restaurants are determined by Yelp.

    *"For example, the rating sort is not strictly sorted by the rating value, but by an adjusted rating value that takes into account the number of ratings, similar to a Bayesian average. This is to prevent skewing results to businesses with a single review."*

We wanted to generate a "pulse" for each restaurant to measure a business's daily activities. Because Yelp does not provide historical view, we resolved to make queries on the number of comments for the same set of restaurants every day to generate our own trends, providing important intelligence on the business. This also enables us to associate the volume of comments with any other measures of interest for a particular day to understand the factors impact restaurant businesses. For example, we queried the weather of each day in an attempt to understand whether weather impacts people's dinning behaviors.

In storing the results of our queries, we made the decision to store our daily results in separate files so that historical files are preserved and the JSON format cannot be corrupted by errors.

## Data aggregation/processing - Akshay
Explanation of how JSON files were manipulated and CSV files are created.
Talk about how OpenWeatherMap some times gives funny results and how you processed it.

## Challenges/Discussions/Future Work - All
Everyone gives her/his two cents. This WILL take a while.
