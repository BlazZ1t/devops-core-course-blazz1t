from fastapi import FastAPI, Request
import os
import socket
import platform
import time
import datetime
from contextlib import asynccontextmanager

SERVICE_NAME = os.getenv("SERVICE_NAME", "devops-info-service")
VERSION = os.getenv("VERSION", "1.0.0")
START_TIME_UTC = round(time.time())

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("recording start time")
    START_TIME_UTC = round(time.time())
    print(START_TIME_UTC)
    yield
    print("Clean up...")

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan
)


def get_system_info():
    return {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "architecture": platform.machine(),
        "python_version": platform.python_version()
    }


def get_runtime_info():
    print("Startup seconds are ", START_TIME_UTC)
    return {
        "uptime_seconds": round(time.time()) - START_TIME_UTC,
        "uptime_human": str(datetime.timedelta(seconds=round(time.time())
                                               - START_TIME_UTC)),
        "current_time": time.strftime("%H hours %M minutes", time.localtime()),
        "timezone": time.timezone
    }


def get_endpoints():
    result = []

    for route in app.routes:
        result.append(
            {
                "path": route.path,
                "method": list(route.methods)[0],
                "description": ""
            }
        )

    return result


@app.get("/")
def get_server_info(request: Request):
    get_endpoints()
    return {
        "service": {
            "name": SERVICE_NAME,
            "version": VERSION,
            "description": "DevOps course info service",
            "framework": "FastAPI"
        },
        "system": get_system_info(),
        "runtime": get_runtime_info(),
        "request": {
            "client_ip": request.client.host,
            "user_agent": request.headers.get("user-Agent"),
            "method": request.method,
            "path": request.url.path
        },
        "endpoints": get_endpoints()
    }


@app.get("/health")
def get_health():
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "uptime_seconds": round(time.time()) - START_TIME_UTC
    }
