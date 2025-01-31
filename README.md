# Backend API for Service Manager - Python and Django

## Overview

This backend API is designed to manage services, handle data submissions, and provide reporting functionalities. It allows clients to load service configurations, submit data for specific services, retrieve submitted entries, and generate reports. The API is built with Python and Django, using PostgreSQL as the database.

## Features

1. **Data Loading**
   Populate the database with service data and associated field configurations using seed data from the service configuration JSON through a data migration. This will involve extracting the service and field information from the JSON and programmatically loading it into the relevant database models.

2. **Data Submission**
   Secure the endpoint to handle form data submissions for a selected service by allowing the client to specify the serviceId in the request, which identifies the service the data corresponds to. Upon receiving the submission, the data is validated against the field configuration defined for the selected service to ensure it meets the required criteria. After successful validation, the data is stored in the database, and ensuring proper tracking and management of their submission.

3. **Data Retrieval**
   The endpoint retrieves all submitted entries for a specific service, supporting efficient data retrieval through filtering, sorting, and pagination. Users can filter the data based on specified fields and values, sort the results by relevant criteria such as submission date or service ID, and paginate through the entries to view data in manageable chunks, enhancing the user experience and performance when dealing with large datasets.
   
4. **Reporting**
   An endpoint to fetch reporting data, designed to analyze and generate insights from submitted data. This endpoint provides dashboard metrics such as the total submissions per service, trends in submissions over time, and the most frequently used services. These insights enable users to monitor service performance, identify usage patterns, and make data-driven decisions efficiently.

## Database Configuration
   The backend uses **PostgreSQL** for storing services, field configurations, form submissions, and other necessary data.

## Setup Instructions

### Prerequisites
1. Python (3.8 or higher)
2. PostgreSQL (latest stable version recommended)
3. Git
4. Virtual environment tools (`venv` or `virtualenv`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/service_manager_backend.git

2. Navigate to the project directory:
   ```bash
   cd service_manager_backend

3. Set up a virtual environment:
   ```bash
   python -m venv venv

4. Install the dependencies:
   ```bash
   pip install -r requirements.txt

5. Run database migrations:
   ```bash
   python manage.py migrate

6. Start the server:
   ```bash
   python manage.py runserver

## Database Setup Instructions

1. Install PostgreSQL on your system.
2. Create a new PostgreSQL database:
   ```bash
   CREATE DATABASE mydb;
3. Create a new user and assign privileges to the database:
   ```bash
   CREATE USER myuser WITH PASSWORD 'mypassword';
   GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;

## API Usage Details

1. Login
   - Endpoint:
     ```bash
     GET /api/login
   - Description: Authenticate with a predefined username and password to receive a JWT authentication token, including access and refresh tokens, for secure access to protected resources.

2. Load Service
   - Endpoint:
     ```bash
     GET /services/
   - Description: Fetches all services

3. Load Field Configuration
   - Endpoint:
     ```bash
     GET /services/<int:service_id>/fields/
   - Description: Retrieve the complete set of fields configured for a specific service, identified by its service ID.

4. Submit Service Data
   - Endpoint:
     ```bash
     POST /services/<int:service_id>/submit/
   - Description: Submit form data for a specific service, identified by its service ID. The provided data is validated against the configured fields for the service and stored in the database upon successful validation.

5. List of Submissions
   - Endpoint:
     ```bash
     GET /services/<int:service_id>/submissions/
   - Description: Retrieve a list of all submissions associated with a specific service, identified by its service ID. Supports filtering, sorting, and pagination for efficient data retrieval.

6. Submission Detail
   - Endpoint:
     ```bash
     GET /submissions/<int:submission_id>/
   - Description: Retrieve detailed information about a specific submission, identified by its submission ID.

7. Dashboard
   - Endpoint:
     ```bash
     GET /dashboard/<str:filter_type>/
   - Description: Provides insights into submission data, including:
        1. Total submissions per service.
        2. Submission trends over time, filtered by day, week, or month.
        3. The most frequently used services.
