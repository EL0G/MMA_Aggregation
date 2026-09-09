# MMA Event Aggregator

A full-stack application that collects MMA event data from multiple promotions and displays it in a unified calendar.

The project uses Python-based ingestion pipelines to scrape and normalize event data from different MMA organizations, stores the resulting data in PostgreSQL, exposes it through a FastAPI backend, and displays events through a React frontend.

## Current Promotions

The ingestion pipeline currently collects event data from:

* UFC
* ONE Championship
* PFL
* RIZIN

## Tech Stack

**Frontend**

* React
* FullCalendar
* Vite

**Backend**

* Python
* FastAPI
* PostgreSQL
* psycopg

**Data Ingestion**

* Python
* BeautifulSoup
* Requests

## Architecture

```text
MMA Promotion Websites
        │
        ▼
   Python Scrapers
        │
        ▼
  Data Normalization
        │
        ▼
     PostgreSQL
        │
        ▼
     FastAPI API
        │
        ▼
 React + FullCalendar
```

The ingestion layer is kept separate from the backend. Scrapers collect event information from each promotion, normalize the data into a common format, and insert it into PostgreSQL.

The FastAPI backend reads from the database and exposes the stored events to the frontend.

## Data Pipeline

Each promotion has its own scraper because event information is published in different formats and page structures.

The ingestion pipeline follows a common flow:

```text
Scrape → Normalize → Store
```

Promotion-specific data is converted into a consistent event representation before being inserted into PostgreSQL.

For example, the normalization layer handles differences in date formats, including Japanese-formatted dates used by some event sources.

## Database

Event data is stored in PostgreSQL.

The core event table currently stores information such as:

```text
id
event_name
event_date
```

Duplicate event insertion is prevented at the database/ingestion level so that the pipeline can be run repeatedly without continuously creating duplicate events.

## API

The FastAPI backend provides event data stored in PostgreSQL to the frontend.

Example endpoint:

```http
GET /events
```

This returns the MMA events available in the database for use by the frontend.

## Frontend

The frontend is built with React and uses FullCalendar to display MMA events in a calendar interface.

Event data is retrieved from the FastAPI backend and transformed into the format expected by FullCalendar.

## Project Structure

The project is organized around three main components:

```text
project/
├── backend/
│   ├── main.py
│   └── ...
│
├── ingestion/
│   ├── scrapers/
│   ├── processing/
│   └── ...
│
├── frontend/
│   └── ...
│
└── .env
```

The exact structure may evolve as additional promotions and features are added.

## Running the Project

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure PostgreSQL

Create the required PostgreSQL database and set the connection information in `.env`.

### 3. Run the ingestion pipeline

Run the ingestion process to collect and store event data:

```bash
python ingestion/run_pipeline.py
```

### 4. Start the backend

```bash
uvicorn backend.main:app --reload
```

### 5. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

## Planned Improvements

Future improvements include:

* Support for additional MMA promotions
* Automated ingestion runs with GitHub Actions
* Improved event filtering and organization
* Promotion-specific event styling
* More detailed event and fight information
* Improved frontend design and responsiveness
* More robust database and API architecture

## Motivation

MMA events are spread across many different promotions, each with its own website and schedule. This project aims to provide a single place to discover and view upcoming events across the MMA ecosystem.
