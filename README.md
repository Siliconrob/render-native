This is an interview application built for [This Dot Labs](https://www.thisdot.co/)

Welcome to this sample application API built in [Python 3.12.4](https://www.python.org/downloads/release/python-3124/) + [FastAPI](https://fastapi.tiangolo.com/) that leverages [REST Countries API](https://restcountries.com/).

There are three components to this system (microservish)
- React UI [live](https://thisdotco.onrender.com) [source](https://github.com/Siliconrob/thisdotco)

The following components are on the **free hosted tier level** of [Render](https://render.com/) and are shutdown when not in use.  Accessing each component from a shutdown state requires it to spin back up and this can **delay requests for a minute or so**.

- [.NET API](https://calamansi.onrender.com) - [code](https://github.com/Siliconrob/calamansi) built with [ServiceStack](https://github.com/ServiceStack/ServiceStack)
- [FastAPI API](https://restful-with-more-fastapi.onrender.com) - [code](https://github.com/Siliconrob/render-native) built with [FastAPI](https://fastapi.tiangolo.com/)

## Proud of

**Use poetry and pydantic typing for the API**

## Highlight

Python is a good choice for handling free flowing data by using dictionaries over strong types

## Improvement

Add in restricted authorization API or tokens

## Demo use

![fastapi](https://github.com/user-attachments/assets/c4d6b33b-ed18-43d4-b02b-74f9bfeb1d5b)

## Flow

![thisdotco-fastapi drawio](https://github.com/user-attachments/assets/70c33793-d10b-41e0-bd6b-a840aca77883)

This API was built on top of FastAPI which is my favorite framework when working with Python.  It is everything that a modern web API should be and is built for maximum productivity with all the correct options builtin to get you off and running along with being setup for long term success i.e. batteries included.

- [OpenAPI](https://restful-with-more-fastapi.onrender.com/docs) reference

## Design

Looking over the [REST Countries API](https://restcountries.com/), two points jump out to me.

- There are only a limited amount of countries in the world.  The API returns 250 for all.  This is a small data amount even pulling in all the details.
- The country data is not changing and would only change if a new country is formed or a major political event occurs.

With this in mind I query 2 endpoints and be done with the entire API implementation if I pull down the full Country data.  Therefore I did that approach.
- An API request checks the in memory cache represntation of all the countries.  If it exists find the country by the various inputs and return the data.  If the all countries data is not cached go grab it from the REST endpoint and cache it.  That means you can take a one time penalty hit for grabbing all the data, but after that point you have immediate access until your cached values expire.
- Countries endpoint has the ability to do a free text search.  This means taking the JSON object and flattening all the data and then doing a string search for the containing term.  If I say free text search for `United` it will return all countries that have that text in any data field of the overall Country data object.
- Languages and Regions endpoints perform an extra manipulation step on the cached all countries data by doing a grouping first either by Region or Language into a dictionary and then performing the id check or return all.

That's it no need to do anything else and it is a straightforward and clear way to build the API.

## Development

This project was built using the default FastAPI template.  Download Python 3.12.4 and I am using [PyCharm](https://www.jetbrains.com/pycharm/) to run the program.  You could use any tool you wish that will open the folder

### Create a venv first in your project folder
- https://docs.python.org/3/library/venv.html

### Copy `.env.example` to a new file `.env`

Fill in environment details. Examples
```
DOMAIN=localhost
ENVIRONMENT=local
PROJECT_NAME="RESTful with more FastAPI"
BASE_REST_URL="https://restcountries.com/v3.1"
PYTHON_VERSION=3.12.4
```

### Command line run, in project root folder
- `pip install poetry` (one time)

### Command line run, in project root folder
- `poetry install`
- `poetry run uvicorn main:app --reload`

### Note
There is a [render.yaml](https://github.com/Siliconrob/render-native/blob/main/render.yaml) that is a detailed Render blueprint you can use for deployment

## Render Deployment

- Signup for a free [Render](https://dashboard.render.com/register) account.  You won't regret it :)
- Connect your [GitHub](https://docs.render.com/github) account
- Choose the `Web Services` [option](https://docs.render.com/web-services)
 - Make sure it is set to `Python 3`
 - Setup a name
 - Set the `Start Command` to `uvicorn main:app --host 0.0.0.0 --port $PORT`
 - Go to `Environment` settings and copy the .env file you have setup above
 ![python_env](https://github.com/user-attachments/assets/0db7b0ec-0f78-48b5-a3eb-4b3df9badbb3)
 - Trigger a manual deployment
