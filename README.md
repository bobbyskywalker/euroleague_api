
# EUROLEAGUE API

This project provides a REST API with full CRUD functionality for managing basketball Euroleague data. App built with FastAPI.





## Demo
![Swagger UI](https://github.com/bobbyskywalker/euroleague_api/blob/main/misc/swagger_demo.gif?raw=true)

## Features

- Swagger UI
- Multiple GET requests related to current & historic league data
- Rest of the CRUD functionality



## Notes

* Player yob (year of birth) is stored in the base as DATE type (eg. 1991-01-01), the month & day are not valid
* Docker default database location is within the project scope
* SQLite database created with https://github.com/bobbyskywalker/euroleague-database-creator
