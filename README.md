# Weather-To-Eat-Or-Not-Dataset
### -- Uncover the nation’s appetite – a decision support dataset for would-be restauranteurs

## Introduction - Abeer
Scope, motivation and purpose.



## Data Dictionary - Devanshi

Explanation of each attribute in Yelp and OpenWeatherMap and why certain attributes were eliminated in dataset.


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
