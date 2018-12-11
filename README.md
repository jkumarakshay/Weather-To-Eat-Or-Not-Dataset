# Weather-To-Eat-Or-Not-Dataset
### -- Uncover the nation’s appetite – a decision support dataset for would-be restauranteurs

## Introduction

### Project Scope:
Our project consists of creating a national restaurant dataset using the Yelp Fusion API and other data sources. There are four cities of interest for comparison: Philadelphia, San Francisco, Chicago and Miami. We extracted attributes associated with the restaurants such as coordinates, phone number, operating hour, address, pricing level, rating and count of reviews. Also, we have decided to extract data from openweathermap.org such as humidity, Minimum temperature, Maximum temperature and wind speed for the four cities.

### Motivation and Purpose:
The dataset is ideal for answering questions such as:
* Does weather impact reviewer’s rating?
* Do restaurants benefit from certain characteristics of locations in terms of the reviews they receive? E.g. Chinese restaurant in Chinatown vs. a tourist site.
* Comparison of competing restaurants in the same area? Eg:- Which cafe is better in the University City? Starbucks, Saxby’s or Wawa
* What are the flavor preferences of residents of different cities?
The dataset is also good for developing products such as:
* Geo-mapping/heatmaps of ‘cuisine districts’

* A consulting algorithm that recommends the ideal location/price range/cuisine type given certain inputs from a business owner.

Finally, we believe the dataset may be of interests to several stakeholders:
- Business owners who are interested in entering the market. (Market Analysis )
- Public health agencies who are interested in the population’s access and attitudes in dining out.
- Public agencies interested in studying the local economy.
- Food reviewers who are interested in assessing population’ interest.
- Students/travelers who are looking for a type of restaurant in a new area (via the products of this dataset, e.g. heatmaps)


## Working with the APIs
This program allows users to obtain restaurant review and weather information based on customized location and business type.

The Yelp Fusion APIs offer several endpoints including search, business details, etc. Each endpoint returns a specific facet about the businesses in Yelp's database. Its construct is similar to many database APIs in that one first needs to identify a unique ID of the desired entity by certain parameters in order to obtain more attributes of it, hence the separate end points search and business details.

**Our 'Search' Parameters**

*Name* | *Data Type* | *Description*
------- | -------- | ---------
term | string | Search term, for example "food" or "restaurants". The term may also be business names, such as "Starbucks". If term is not included the endpoint will default to searching across businesses from a small number of popular categories
location | string | Required if either latitude or longitude is not provided. This string indicates the geographic area to be used when searching for businesses. Examples: "New York City", "NYC", "350 5th Ave, New York, NY 10118". Businesses returned in the response may not be strictly within the specified location.
limit | int | Number of business results to return. By default, it will return 20. Maximum is 50.
sort by | string | Suggestion to the search algorithm that the results be sorted by one of the these modes: best_match, rating, review_count or distance. The default is best_match. Note that specifying the sort_by is a suggestion (not strictly enforced) to Yelp's search, which considers multiple input parameters to return the most relevant results. For example, the rating sort is not strictly sorted by the rating value, but by an adjusted rating value that takes into account the number of ratings, similar to a Bayesian average. This is to prevent skewing results to businesses with a single review.
offset | int | Offset the list of returned business results by this amount.

In reviewing the API documentations, we summarized the following limits of the service.
  1. A client is limited to 5,000 APIs per 24 hours resetting every midnight UTC.
  2. If queries-per-second (QPS) against the API are deemed too frequent, the service will return a HTTP 429 error (too many requests). However, the documentation does not specify the maximum allowed frequency. We set our requests to be one second apart.
  ``` JSON
  {
    "error": {
        "code": "TOO_MANY_REQUESTS_PER_SECOND",
        "description": "You have exceeded the queries-per-second limit for this endpoint.
                        Try reducing the rate at which you make queries."
    }
}
 ```
  3. A client can get up to 1,000 businesses from the search endpoint.
  4. Each call can have a maximum of 50 return results. (paging)

Due to the aforementioned limits, our data scope is to query the top 1000 restaurants for one city. We had to use the `offset` parameter, so that we obtain 1,000 in 20 calls. Results from all 20 queries from the same day were stored in a list and output to one JSON file.

![offset demo](https://raw.githubusercontent.com/AkshayJk1995/Weather-To-Eat-Or-Not-Dataset/master/offset.png)

The dataset generates a "pulse" for each restaurant by keeping track of the daily comment growth for each restaurant, despite Yelp does not provide the historical view of a business. This provides important intelligence on the business, and also enables users to associate the volume of comments with any number of measures of interest for a particular day to understand the factors impacting restaurant businesses. For example, the daily weather information is provided to address the question whether weather impacts people's dinning behaviors. Please refer to the automation manual for how to set up the daily queries.

In storing the results of our queries, we made the decision to store our daily results in separate files so that historical files are preserved and the JSON format cannot be corrupted by errors. The process of aggregating the daily results is discussed below.

## Data aggregation/processing

The two programs work on digging into the JSON files returned by the Yelp Fusion API and OpenWeatherMap API, choosing required fields and combine data for each city and across cities in CSV format.

The JSON file returned from OpenWeatherMap API is extracted as a dictionary of dictionaries. Each file consists of each day's statistics in each city. On investigation, it turns out that OpenWeatherMap API sometimes concatenates the same data twice and stores it in one file. This causes the system to fail while creating the dataset. This requires manual intervention as it is difficult to correct the syntax of a JSON file using Python. The time complexity of extracting weather data is O(n<sup>4</sup>). The extracted fields are:

#### *Weather Information Dataset*

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
coord.lon, coord.lat | decimal | Longitude and latitude values for the given city

```JSON
{
  "coord": {
    "lon": -75.16,
    "lat": 39.95
  },
  "weather": [
    {
      "id": 803,
      "main": "Clouds",
      "description": "broken clouds",
      "icon": "04n"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 273.23,
    "pressure": 1019,
    "humidity": 83,
    "temp_min": 271.15,
    "temp_max": 274.85
  },
  "visibility": 16093,
  "wind": {
    "speed": 1.15,
    "deg": 274.504
  },
  "clouds": {
    "all": 75
  },
  "dt": 1543552500,
  "sys": {
    "type": 1,
    "id": 4743,
    "message": 0.0041,
    "country": "US",
    "sunrise": 1543579340,
    "sunset": 1543613777
  },
  "id": 4560349,
  "name": "Philadelphia",
  "cod": 200
}
```

The JSON file returned from Yelp Fusion API is extracted as a list of dictionaries. Extracting restaurant data is a more convoluted process since the nesting go as deep as 4-5 levels. This shows the level of detail returned each day. Unlike weather data, the data returned has always been clean. Due to the level of nesting, the complexity of extracting data is O(n<sup>5</sup>). The extracted fields are:
#### *Restaurant Review Dataset*

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

```JSON
[
  {
    "businesses": [
      {
        "id": "kT8IlV47kz1rz2lTuNyO1w",
        "alias": "christies-deli-philadelphia",
        "name": "Christie's Deli",
        "image_url": "https://s3-media3.fl.yelpcdn.com/bphoto/h7eEiQigXwXVq6MYdhG8vg/o.jpg",
        "is_closed": false,
        "url": "https://www.yelp.com/biz/christies-deli-philadelphia?adjust_creative=czYYjyLsMG5Xo5jy1DcI4A&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=czYYjyLsMG5Xo5jy1DcI4A",
        "review_count": 79,
        "categories": [
          {
            "alias": "delis",
            "title": "Delis"
          },
          {
            "alias": "breakfast_brunch",
            "title": "Breakfast & Brunch"
          },
          {
            "alias": "sandwiches",
            "title": "Sandwiches"
          }
        ],
        "rating": 5,
        "coordinates": {
          "latitude": 39.9630809276773,
          "longitude": -75.1693602651358
        },
        "transactions": [],
        "price": "$",
        "location": {
          "address1": "1822 Spring Garden St",
          "address2": "Unit B",
          "address3": "",
          "city": "Philadelphia",
          "zip_code": "19130",
          "country": "US",
          "state": "PA",
          "display_address": [
            "1822 Spring Garden St",
            "Unit B",
            "Philadelphia, PA 19130"
          ]
        },
        "phone": "+12155630555",
        "display_phone": "(215) 563-0555",
        "distance": 1045.8502098235545
      }
    ] }
    ]

```

In the program, datacombination.py, data from all the 4 cities were combined. During combination, an extra field was created using Pandas DataFrame to mention clearly the city in which the given restaurant is located.

#### *Eliminated Attributes from each dataset*
##### Restaurant Reviews
*Name* | *Data Type* | *Reason not considered*
------- | -------- | ---------
business.alias | string | Every Yelp business has both a unique ID as well as a unique alias (eg: "name-of-business-separated-by-hyphen"). These can be used interchangeably. However, the business alias contains unicode characters and hence we thought using the business id is ideal and also we have the business name captured in column 'name'
business.image_url | string | Since our output presents the data in a csv format, decision to use just the URL of the business page on Yelp and not the the URL of the image was taken
business.location | object | The location object includes address1, address2, address3, city, state, zip and country. The attribute display_address, instead, merges all these elements as an array of strings which gives the address of the business in the standard address
business.phone | string | This attribute displays the phone number of the business in a simple format like - +17864520068 whereas the attribute we have used is the display_phone which displays the same number in a better standard format - (786) 452-0068

##### Weather Information
*Name* | *Data Type* | *Reason not considered*
------- | -------- | ---------
weather.id | int | Displays the weather condition ID. Since the weather parameters and condition attributes are considered, this column was eliminated
weather.icon | string | Since our output presents the data in a csv format, use of the description of weather parameter and not related icon seemed fit
base.stations | string | This is an internal parameter for OpenWeatherMap to source weather data from meteorological broadcast services, raw data from airport weather stations, radar stations and other official weather stations
sys.type, sys.id, sys.message | number | These are internal parameters of the Sys structure that contain general information about the request and the surrounding area for where the request was made
cod | int | An internal parameter indicating the structure defined for JSON to be unmarshaled into

The processing will work even if the dataset is expanded to contain all cities in the United States, if not the world, as all that needs to be clear is the naming scheme of the files, which is taken care of by this system. The consistency in data returned by the two APIs adds to our confidence in stating so.

## Challenges/Discussions/Future Work
- The dataset only contains the top-rated restaurants. It may take the inclusion of businesses with lower rating to design an algorithm that predicts business viability in a select locale.
- We found out that Yelp's limits were enforced in a funny way. On day 1, a total of 86 calls were accepted before the server gave an out of limit message. On day 3, only 20 calls were accepted. A closer look at the results from the 86 calls revealed that the server was looping through the same 1000 restaurants and giving out repeated returns.
- Multiple returns from the same city name may create confusion. We made sure the querying result reflects the city of our choosing.
![many Philadelphias](https://raw.githubusercontent.com/AkshayJk1995/Weather-To-Eat-Or-Not-Dataset/master/owmcity.png)
- We plan to integrate the [American Community Survey](https://www.census.gov/programs-surveys/acs/guidance/subjects.html) to the dataset by matching the neighborhood characteristics including the following. This would require us to first generate a geography ID based on the coordinates of restaurants using the census.gov [geocoder API](https://www.census.gov/geo/maps-data/data/geocoder.html), and then query the geography of interest using the [ACS APIs](https://www.census.gov/data/developers/data-sets/acs-1year.html). Of note, the Census Bureau has made a large amount of its data repository [machine-discoverable](https://www.census.gov/data/developers/updates/new-discovery-tool.html) for users needing to retrieve historical data.

  - Social: ancestry, language spoken at home, marital status, migration/residence 1 year ago, school enrollment, etc.
  - Housing: computer and internet use, kitchen facilities, occupants per room, owner/renter, vehicle available, etc.
  - Economic: employment status, health insurance coverage, industry and occupation, etc.
  - Demographic: age;sex, total population
=======


- The distance field doesn't seem to be reflective of actual querying location (PHL) and other cities.

- Timing of the API calls may yield better results in warmer seasons.
