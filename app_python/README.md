### Overview 

This is a service that sends basic information about the server it runs on, about the app itself, and can do a health check (so it doesn't have to go to a hospital).

### Prerequisites

For running this project you have to have Python 3.11+ installed

### Installation

`python -m venv .venv`
For linux: `.venv/Scripts/activate`
For windows: `.venv/Scripts/Acticate.ps1`
`pip install -r requirements.txt`

### Running the application

`uvicorn app:app`

For custom config there are flags `--host` and `--port` for setting the host and the port respectively (duh)

### API Endpoints

`GET /` - Serice and system information
`GET /health` - Health check

### Configuration

SERVICE_NAME - sets service name
VERSION - sets service version