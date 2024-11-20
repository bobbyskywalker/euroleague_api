
# EUROLEAGUE REST API & DATA VISUALIZATION

This project provides a REST API with full CRUD functionality for managing basketball Euroleague data.
Frontend side of the application offers simple matplotlib visualizations and comparisons of players' stats.
An application built with FastAPI, structured using the MVC design pattern.

## Demo
![Swagger UI](https://github.com/bobbyskywalker/euroleague_api/blob/main/misc/swagger_demo.gif?raw=true)
![Frontend Homepage](https://github.com/bobbyskywalker/euroleague_api/blob/frontend/misc/front_demo.gif?raw=true)
![Heatmap Demo](https://github.com/bobbyskywalker/euroleague_api/blob/frontend/misc/heatmap_demo.gif?raw=true)
## Features

- Swagger UI for API documentation and testing.
- Multiple GET endpoints for accessing current and historic league data.
- Full CRUD functionality for data creation, retrieval, updating, and deletion.
- SQLite database as the backend for data storage.
- HTTP Basic authentication to secure endpoints.
- HTTP request logging middleware for tracking and debugging API usage.
- Frontend featuring matplotlib visualizations for comparing players' stats.


## Notes
* SQLite database created with https://github.com/bobbyskywalker/euroleague-database-creator
