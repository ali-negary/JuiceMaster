# Juice Master: Battery Insights Service

JuiceMaster is a Flask-based API for managing batteries and tracking battery-related issues. It provides endpoints to perform CRUD operations on batteries, log battery information, and manage battery issues.

## Table of Contents
- Description 
- Database 
- How to Run 
- API Samples 
- Unit Tests
- Design Choices
- Trade-offs

## Description
JuiceMaster API allows you to perform various operations related to batteries and battery issues. It provides the following APIs:

- **Batteries API:** CRUD operations for managing batteries.
- **Battery Logs API:** Log battery information such as state of charge, voltage, and timestamp.
- **Issues API:** Manage battery issues and associate them with specific batteries.

## Database

JuiceMaster uses a PostgreSQL database and consists of the following tables:

- **batteries:** Stores information about batteries.
- **battery_logs:** Records battery-related data such as state of charge, voltage, and timestamp.
- **issues:** Tracks battery issues, their types, descriptions, and occurrence timestamps.
Here's a brief overview of the columns in each table:

### batteries

- **battery_id:** The unique identifier for each battery.
- **state_of_charge:** The current state of charge of the battery (should be ranged in 0 to 100).
- **capacity:** The capacity of the battery.
- **voltage:** The voltage of the battery.
- **battery_health:** The health status of the battery (can be "BAD", "GOOD", "VERY GOOD", or "EXCELLENT").
- **created_at:** The timestamp indicating when the battery was created.
- **updated_at:** The timestamp indicating the last update to the battery.

### battery_logs

- **battery_id:** The identifier of the associated battery.
- **state_of_charge:** The state of charge of the battery at a specific timestamp.
- **voltage:** The voltage of the battery at a specific timestamp.
- **timestamp:** The timestamp when the battery data was logged.

### issues

- **issue_id:** The unique identifier for each issue.
- **battery_id:** The identifier of the associated battery.
- **issue_type:** The type of battery issue.
- **issue_description:** A description of the battery issue.
- **occurrence_timestamp:** The timestamp when the issue occurred.

## How to Run

To run the JuiceMaster API locally, follow these steps:

1. Make sure you have Docker and Git installed in your device.
2. Clone the repository by entering this command in your terminal: `git clone https://github.com/ali-negary/JuiceMaster.git`
3. Navigate to the project directory: `cd JuiceMaster`
4. Set up the necessary environment variables. Create a `.env` file in the root directory of the project containing DB_USER, DB_PASSWORD, DB_NAME.
Here is a sample content for `.env` file:
```
export DB_USER=juicer
export DB_PASSWORD=juicerpass
export DB_NAME=juice_db
```
5. Build and run the containers using Docker Compose: docker-compose up

The JuiceMaster API will be accessible at http://localhost:5000.

## API Samples

Here are some examples of how to use the JuiceMaster API.

### Get All Batteries

Request: `GET` `127.0.0.1:5000/api/v1/batteries`

Response:
```json
[
  {
    "battery_id": "1",
    "state_of_charge": 80.5,
    "capacity": 100,
    "voltage": 12.5,
    "battery_health": "EXCELLENT",
    "created_at": "2023-05-27T10:00:00Z",
    "updated_at": "2023-05-27T12:00:00Z"
  }, ...
]
```

### Get Battery by ID

Request: `GET` `127.0.0.1:5000/api/v1/batteries/e0d6962e-f532-405a-bab7-9ca5d5e78be9`

Response:
```json
{
    "battery_health": "EXCELLENT",
    "capacity": 5000,
    "created_at": "Mon, 29 May 2023 23:28:58 GMT",
    "id": "e0d6962e-f532-405a-bab7-9ca5d5e78be9",
    "state_of_charge": 69.0,
    "updated_at": "Mon, 29 May 2023 23:28:58 GMT",
    "voltage": 5.0
}
```

### Add Battery

Request: `POST` `127.0.0.1:5000/api/v1/batteries`
```json
{
    "state_of_charge": 100,
    "capacity": 5500,
    "voltage": 5,
    "battery_health": "EXCELLENT"
}
```
Response:
```json
{
    "battery_id": "83bb8bee-09a9-4ce8-ba5e-6cfd2b088ad5",
    "message": "Battery added successfully!"
}
```

### Update Batter by ID

Request: `PUT` `127.0.0.1:5000/api/v1/batteries/3df408fa-c118-4793-a23b-598394949c28`
```json
{
    "state_of_charge": 85,
    "voltage": 24
}
```
Response:
```json
{
    "id": "3df408fa-c118-4793-a23b-598394949c28",
    "message": "Battery updated successfully"
}
```

### Delete Battery by ID

Request: `DELETE` `127.0.0.1:5000/api/v1/batteries/35b7ea51-cb3b-4cc1-83bf-e1a93ae3ae3f`

Response:
```json
{
    "message": "Battery deleted successfully"
}
```


### Get Issues by Battery ID

Request: `GET` `127.0.0.1:5000/api/v1/batteries/e0d6962e-f532-405a-bab7-9ca5d5e78be9/issues`

Response:
```json
[
    {
        "id": "54cdad99-38f4-499b-a40e-9245f8846d7b",
        "issue_description": "battery temperature over 70 degrees.",
        "issue_type": "high temperature",
        "occurrence_timestamp": "Tue, 30 May 2023 18:47:33 GMT"
    }, ...
]
```


### Add Issue for Battery

Request: `POST` `127.0.0.1:5000/api/v1/batteries/e0d6962e-f532-405a-bab7-9ca5d5e78be9/issues`
```json
{
    "issue_type": "high temperature",
    "issue_description": "battery temperature over 90 degrees."
}
```
Response:
```json
{
    "id": "c02b167a-d21a-4e2a-8630-4f215dd1a124",
    "message": "Issue added successfully"
}
```

### Update Battery Issue By IDs

Request: `PUT` `127.0.0.1:5000/api/v1/batteries/e0d6962e-f532-405a-bab7-9ca5d5e78be9/issues/7ae29228-35bb-4999-87c9-4f3b426f88b4`
```json
{
    "issue_type": "over_charge",
    "issue_description": "battery charge over 80%."
}
```
Response:
```json
{
    "message": "Issue updated successfully"
}
```

### Delete Battery Issue

Request: `DELETE` `127.0.0.1:5000/api/v1/batteries/e0d6962e-f532-405a-bab7-9ca5d5e78be9/issues/136f8897-f272-4e01-a8a4-347692848cc3`

Response:
```json
{
    "message": "Issue deleted successfully"
}
```

## Unit Tests

The JuiceMaster application has a comprehensive suite of unit tests to ensure the correctness and reliability of its codebase. These tests are designed to verify the functionality of individual components or units of code in isolation.

### Testing framework
The unit tests are implemented using the `pytest` framework, which provides a simple and expressive way to write tests.

### Key Components Tested
The unit tests cover various key components and functionalities of the JuiceMaster application, including:
- **Battery health check:** Tests for the `HealthCheck` class, which checks the health condition of a battery based on its state of charge values.
- **Battery issues:** Tests for the `battery_issues.py` APIs, which checks all the CRUD requests.
- **Battery subscriber:** Tests for the `battery_subscriber.py` APIs, which checks all the CRUD requests.

### Running the Tests

1. Run `pip install -r requirements.txt` to install all the requirements.
2. Navigate to the root directory of the project.
3. Check if pytest is installed with this command: `pytest --version`
4. Run `python -m pytest` in terminal.


## Design Choices

- **Microservices Architecture:** The application is designed as a microservice architecture, with separate components for different functionalities. This promotes scalability, maintainability, and modularity. The use of microservices allows for independent development and deployment of individual components, making it easier to scale and maintain the system.
- **Database Schema:** The chosen database schema includes three tables: batteries, battery_logs, and issues. The batteries table stores information about batteries, while the battery_logs table logs state-of-charge and voltage data over time. The issues table tracks battery-related issues. This schema allows for efficient storage and retrieval of battery data while maintaining data integrity.
- **ORM Framework:** SQLAlchemy is used as the ORM (Object-Relational Mapping) framework. It provides a high-level interface for interacting with the database, allowing for efficient database operations and abstraction of low-level SQL queries. SQLAlchemy provides flexibility and compatibility with multiple database systems.
- **Containerization with Docker:** Docker and Docker Compose are used to containerize the application. Docker provides a lightweight and portable containerization solution, ensuring consistent behavior across different environments. Docker Compose is used to orchestrate multiple containers, allowing for easy setup and deployment of the application along with its dependencies.

## Trade-offs

- **Complexity vs. Simplicity:**
  - **Microservices:** While the microservices architecture provides scalability and modularity, it also introduces additional complexity, compared to monolithic design. 
  - **Postgres:** The choice of database is a trade-off depending on the requirements. For this project SQLite could have been a good choice. But for the long run it would be less than useful.
- **Performance vs. Storage:** The choice of database schema and data types involves a trade-off between performance and storage requirements. For example, using UUIDs as primary keys provides uniqueness and easy integration with other systems but may have some impact on performance and storage compared to integer-based primary keys. 
- **Ease of Deployment vs. Customization:** Using Docker and Docker Compose simplifies the deployment process by providing a standardized environment. However, it may limit the level of customization and fine-tuning available for specific deployment scenarios. Also, it makes debugging a pain!
- **Documentation:** I usually document APIs using Swagger or Postman documentation. In this project, due to lack of time I decided to give a sample of only successful response of APIs in this readme file.

------
**Note:** Certain sections of this readme were written with the assistance of ChatGPT, a language model developed by OpenAI.
