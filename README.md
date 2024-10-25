# EUROLEAGUE API

REST API offering basketball EUROLEAGUE data fetching from SQLite database. 
Created with FastAPI.



## Demo
![Swagger UI](https://github.com/bobbyskywalker/euroleague_api/blob/main/misc/swagger_demo.gif?raw=true)

## Features

- Swagger UI
- Multiple GET requests related to current & historic league data



## Notes

* Player yob (year of birth) is stored in the base as DATE type (eg. 1991-01-01), the month & day are not valid
* For team codes just GET the team list
