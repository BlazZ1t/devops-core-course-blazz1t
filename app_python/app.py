from fastapi import FastAPI, Request
import logging
from pythonjsonlogger import jsonlogger
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

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(message)s %(name)s"
)

logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global START_TIME_UTC

    START_TIME_UTC = round(time.time())

    logger.info(
        "Application startup",
        extra={
            "service": SERVICE_NAME,
            "version": VERSION,
            "host": HOST,
            "port": PORT,
            "debug": DEBUG
        }
    )

    yield

    logger.info("Application shutdown")

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    client_ip = request.client.host
    method = request.method
    path = request.url.path
    user_agent = request.headers.get("user-agent")

    try:
        response = await call_next(request)
        status_code = response.status_code

    except Exception as e:
        logger.exception(
            "Request failed",
            extra={
                "method": method,
                "path": path,
                "client_ip": client_ip
            }
        )
        raise e

    process_time = round((time.time() - start_time) * 1000, 2)

    logger.info(
        "HTTP request",
        extra={
            "method": method,
            "path": path,
            "status_code": status_code,
            "client_ip": client_ip,
            "user_agent": user_agent,
            "duration_ms": process_time
        }
    )

    return response


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
