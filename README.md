# AI Reports API

AI Reports API is a FastAPI-based backend application that leverages Large Language Models (LLMs) like Google Gemini and OpenAI to automatically generate  reports individually or in massive parallel batches.

## Features

- **Asynchronous Batch Processing**: Process reports concurrently without hanging the HTTP connection. The API utilizes FastAPI's `BackgroundTasks`, buffering requests on a background queue.
- **Polling Architecture**: Initiate a batch and immediately receive a `job_id`. Your frontend can poll for fractional live progress without missing a beat or crashing due to server timeouts.
- **Data Persistence**: Active job tracking seamlessly buffers results locally into `data/jobs/job_id.json`, ensuring fault-tolerance mapping across active page-reloads.

## Prerequisites

- Python 3.10+
- Virtual Environment

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ai-reports
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate on Windows
   .venv\Scripts\activate
   
   # Activate on Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**:
   Copy the existing `.env.example` to `.env` (or create a new `.env` file in the root directory) and fill out the required API keys. Note: For Gemini Batch Processing, the standard API key requires no dedicated GCP billing!
   ```env
   # OpenAI configuration
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4o # Model parameter
   
   # Gemini configuration
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## 🏎️ Running the Application

You can start the FastAPI server executing the main runner script:

```bash
python -m app.main
```

The server will start running on port `8081`. You can customize the `host` and `port` settings inside `app/main.py`.

### API Documentation

FastAPI automatically generates interactive API documentation. Once the server is running, you can access:

- **Swagger UI**: [http://localhost:8081/docs](http://localhost:8081/docs)
- **ReDoc**: [http://localhost:8081/redoc](http://localhost:8081/redoc)

## Endpoints

The endpoints are mapped accurately under the `/api/v1/reports` prefix structure natively:

- `GET /health` - API server health monitor.
- `POST /` - Generate a single synchronous AI report.
- `POST /batch` - Queue a parallel batch list of reports to Gemini asynchronously. Returns a `{job_id}` immediately.
- `GET /batch/status?job_id=xxx` - Poll the status of a scheduled generation. Returns fractional metadata `{"status": "processing", "completed_count": 1, "total_count": 10}` or ultimately injects all completed payloads safely.
