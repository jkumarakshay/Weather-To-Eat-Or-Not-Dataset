# Weather-To-Eat-Or-Not-Dataset
### -- Uncover the nation’s appetite – a decision support dataset for would-be restauranteurs

## Introduction - Abeer
Scope, motivation and purpose.



## Data Dictionary - Devanshi

Translating our business idea into code, we extracted and created two datasets – Restaurant Reviews and Weather Information using Yelp Fusion and OpenWeatherMap APIs respectively. As mentioned above, our dataset will, potentially, be used by various entities. The end goal can be to, either merge these two datasets to get further insights from correlating cuisines suitable for certain weather types or analyze whether weather impacts reviewer’s rating or any such analysis or to use each dataset on a stand-alone basis.

In order to carry out any of the above, access to the data type is made available to users through the following data dictionaries. This section describes each attribute in both, the Restaurant Reviews and Weather Information datasets.

In an attempt to produce refined datasets, there were certain attributes we did not include in the final processed datasets. These eliminated attributes and reasons due to which they were not considered are presented towards the end of this section.


#### *Data Dictionary - Restaurant Review Dataset*

*Name* | *Data Type* | *Description*
------- | -------- | ---------
date_id | string | Unique ID to map the restaurant reviews and weather information dataset
id | string | Unique Yelp ID of this business. Example: '4kMBvIEWPxWkWKFN__8SxQ'
name | string | Name of this business
is_closed | bool | Whether business has been (permanently) closed
url | string | URL for business page on Yelp
review_count | int | Number of reviews for this business
categories | string | Title of a category for display purpose. Example: Japanese, Italian, Juicebars vegan
rating | decimal | Rating for this business (value ranges from 1, 1.5, ... 4.5, 5)
latitude | decimal | City geo location - latitude coordinates of this business
longitude | decimal | City geo location - longitude coordinates of this business
transactions | string[] | List of transactions that the business is registered for. Current supported values are pickup, delivery and restaurant_reservation
price | string | Price level of the business. Value is one of $, $$, $$$ and $$$$.
display_address | string | Array of strings that if organized vertically give an address that is in the standard address format for the business's country
display_phone | string | Phone number of the business formatted nicely to be displayed to users. The format is the standard phone number format for the business's country
distance | decimal | Distance in meters from the search location. This returns meters regardless of the locale

#### *Data Dictionary - Weather Information Dataset*

*Name* | *Data Type* | *Description*
------- | -------- | ---------
date_id | string | Unique ID to map the restaurant reviews and weather information dataset
weather_main | string | Group of weather parameters (Example: Clouds, Rain, Snow, Extreme etc.)
weather_description | string | Weather condition within the group mentioned above (Example: Broken clouds, Few clouds, Light rain etc.)
main_temp | decimal | The temperature of that day. The default unit considered here is Kelvin
main_pressure | decimal | Atmospheric pressure of that day in hPa (hectopascals)
main_humidity | int | Relative air humidity of that day in %
main_temp_min | decimal | Minimum temperature on that day. The default unit considered here is Kelvin
main_temp_max | decimal | Maximum temperature on that day. The default unit considered here is Kelvin
visibility | decimal | Visibility on that day in meters
wind_speed | decimal | Speed of the wind in mps (meters per second)
wind_deg | decimal | Direction of the wind on that day in degrees (meteorogical). As an example, 270 degrees means the wind is blowing from the west
clouds_all | int | The % of cloudiness/cloud cover for that day
dt | int | Date & time of receiving data in the unix timestamp format, UTC (Example: Unix timestamp 1541696160 is equivalent to 11/08/2018 @ 4:56pm (UTC))
sys_sunrise | int | Date & time of sunrise in the unix timestamp format, UTC
sys_sunset | int | Date & time of sunrise in the unix timestamp format, UTC
id | int | City ID
name | string | City name

#### *Eliminated Attributes from each dataset*
##### Restaurant Reviews
*Name* | *Data Type* | *Reason not considered*
------- | -------- | ---------
business.alias | string | Every Yelp business has both a unique ID as well as a unique alias (eg: "name-of-business-separated-by-hyphen"). These can be used interchangeably. However, the business alias cotains unicode characters and hence we thought using the business id is ideal and also we have the business name captured in column 'name'
business.image_url | string | Since our output presents the data in a csv format, decision to use just the URL of the business page on Yelp and not the the URL of the image was taken
business.location | object | The location object includes address1, address2, address3, city, state, zip and country. The attribute display_address, instead, merges all these elements as an array of strings which gives the address of the business in the standard address
business.phone | string | This attribute displays the phone number of the business in a simple format like - +17864520068 whereas the attribute we have used is the display_phone which displays the same number in a better standard format - (786) 452-0068

##### Weather Information
*Name* | *Data Type* | *Reason not considered*
------- | -------- | ---------
coord.lon, coord.lat | decimal | Taken into consideration in Restaurant Reviews dataset
weather.id | int | Displays the weather condition ID. Since the weather parameters and condition attributes are considered, this column was eliminated
weather.icon | string | Since our output presents the data in a csv format, use of the description of weather parameter and not related icon seemed fit
base.stations | string | This is an internal parameter for OpenWeatherMap to source weather data from meteorological broadcast services, raw data from airport weather stations, radar stations and other official weather stations
sys.type, sys.id, sys.message | number | These are internal parameters of the Sys structure that contain general infromation about the request and the surrounding area for where the request was made
cod | int | An internal parameter indicating the structure defined for JSON to be unmarshaled into



**Our 'Search' Parameters**

*Name* | *Data Type* | *Description*
------- | -------- | ---------
term | string | Search term, for example "food" or "restaurants". The term may also be business names, such as "Starbucks". If term is not included the endpoint will default to searching across businesses from a small number of popular categories
location | string | Required if either latitude or longitude is not provided. This string indicates the geographic area to be used when searching for businesses. Examples: "New York City", "NYC", "350 5th Ave, New York, NY 10118". Businesses returned in the response may not be strictly within the specified location.
limit | int | Number of business results to return. By default, it will return 20. Maximum is 50.
sort by | string | Suggestion to the search algorithm that the results be sorted by one of the these modes: best_match, rating, review_count or distance. The default is best_match. Note that specifying the sort_by is a suggestion (not strictly enforced) to Yelp's search, which considers multiple input parameters to return the most relevant results. For example, the rating sort is not strictly sorted by the rating value, but by an adjusted rating value that takes into account the number of ratings, similar to a Bayesian average. This is to prevent skewing results to businesses with a single review.
offset | int | Offset the list of returned business results by this amount.






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
