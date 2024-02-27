# calendar-analysis

Analyzing and visualizing how I spend my time using Google Calendar data.

## Requirements

This project can be built directly on github codespaces using the devcontainer configs or locally with the following requirements.

1. Python 3.12
2. PostgresSQL

## Setup

1. Clone repository
2. Setup and activate virtual environment

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

3. Get Google Calendar API credentials and save them in the root directory as `credentials.json`

## Usage

Run the following command to start the server.

```bash
python manage.py runserver
```
