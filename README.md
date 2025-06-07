
# 🏀 EUROLEAGUE REST API & DATA VISUALIZATION

## Overview

This project provides a REST API with full CRUD functionality for managing basketball Euroleague data.
Frontend side of the application offers simple matplotlib visualizations of rankings & comparisons of players' stats.
An application built with FastAPI, structured using the MVC design pattern.

## ✅ Features

- Swagger UI for API documentation and testing.
- Multiple GET endpoints for accessing current and historic league data.
- Full CRUD functionality for data creation, retrieval, updating, and deletion.
- SQLite database as the backend for data storage.
- HTTP Basic authentication to secure endpoints.
- HTTP request logging middleware for tracking and debugging API usage.
- Frontend featuring matplotlib visualizations for comparing players' stats.

## 💻 Demo
![Swagger UI](misc/swagger_demo.png)
![Frontend Homepage](misc/front_demo.png)

## 🗒️ Notes
* App is not maintained anymore & the deployment is down, feel free to fork the repo to enhance the API!
* App contains a cronjob to reset and update the sqlite database everyday at 2AM CET.

## Author
* https://github.com/bobbyskywalker