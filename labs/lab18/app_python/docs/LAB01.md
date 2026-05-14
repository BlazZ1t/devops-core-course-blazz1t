# DevOps Info Service – Documentation

## 1. Framework Selection

### Chosen Framework: FastAPI

**FastAPI** was selected to build the DevOps Info Service because it is lightweight, high-performance, and designed for building APIs quickly and correctly.

**Reasons for choosing FastAPI:**
- High performance (built on Starlette and Pydantic)
- Async support out of the box
- Simple and readable code
- Automatic request handling and validation
- Ideal for microservices and DevOps tooling

### Comparison With Alternatives

| Framework | Language | Performance | Async Support | Use Case |
|---------|---------|-------------|---------------|----------|
| **FastAPI** | Python | ⭐⭐⭐⭐ | Yes (native) | Modern APIs, microservices |
| Flask | Python | ⭐⭐ | Limited | Small/simple APIs |
| Django REST | Python | ⭐⭐ | Partial | Large monolithic apps |
| Express.js | JavaScript | ⭐⭐⭐ | Yes | Node.js ecosystems |

**Conclusion:**  
FastAPI provides the best balance between performance, simplicity, and modern API development for this project.

---

## 2. Best Practices Applied

### 2.1 Environment-Based Configuration

Configuration values such as service name, version, host, and port are read from environment variables.


SERVICE_NAME = os.getenv("SERVICE_NAME", "devops-info-service")
VERSION = os.getenv("VERSION", "1.0.0")
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'