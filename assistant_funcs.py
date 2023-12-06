import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def get_weather_by_location(latitude, longitude, weather_variable="temperature_2m"):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Prepare the API call
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": weather_variable
    }

    # Call the API
    responses = openmeteo.weather_api(url, params=params)

    # Process the first location response
    response = responses[0]

    # Process hourly data
    hourly = response.Hourly()
    hourly_data_values = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s"),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )
    }
    hourly_data[weather_variable] = hourly_data_values
    weather_data = pd.DataFrame(data=hourly_data)
    # convert the dataframe to a JSON string
    weather_data_json = weather_data.to_json(orient="records")
    # convert json to one string:
    weather_data_json_str = "".join(weather_data_json.splitlines())
    return weather_data_json_str

def get_daily_weather_by_location(latitude, longitude, weather_variable=["weather_code", "temperature_2m_max", "temperature_2m_min"]):
    '''
        
    '''
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": weather_variable
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s"),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}
    daily_data["weather_code"] = daily_weather_code
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min

    weather_data = pd.DataFrame(data = daily_data)
    # convert the dataframe to a JSON string
    weather_data_json = weather_data.to_json(orient = "records")
    # convert json to one string:
    weather_data_json_str = "".join(weather_data_json.splitlines())
    return weather_data_json_str

def get_text_from_first_google_search_result(query: str):
    '''
    Assistant tool function to get the text from the first Google search result
    '''
    base_google_url = "https://www.google.com"
    search_url = f"{base_google_url}/search?q={query}"

    headers = {'User-Agent': 'Mozilla/5.0'}
    search_response = requests.get(search_url, headers=headers)

    if search_response.status_code != 200:
        return "Failed to retrieve search results"

    soup = BeautifulSoup(search_response.text, 'html.parser')

    # Find the first search result URL
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # Check if the href contains a URL and extract it
        if '/url?q=' in href:
            # Parse the query string to extract the actual URL
            url_parts = urlparse(href)
            query_string = parse_qs(url_parts.query)
            actual_url = query_string.get('q', [None])[0]
            if actual_url:
                # Fetch the content from the actual URL
                page_response = requests.get(actual_url, headers=headers)
                if page_response.status_code == 200:
                    page_soup = BeautifulSoup(page_response.text, 'html.parser')
                    return page_soup.get_text(separator='\n')
                break

    return "Failed to extract URL or retrieve data"
