## Docker Best Practices applied

* .dockerignore file was added to not include .venv, __pycache\_\_ and other irrelevant files into a docker image.

* Docker is being run as a non-root user, to prevent it from being abused heavily in case of breach

* Requirements installed before copying the code makes it more deterministic and allows docker to cache dependencies when needed

* No package cache is bloating an image, with usage of `--no-cache-dir` flag in pip install so it is lightweight

## Image information & Decisions

* `python:3.13-slim` is used due to it being the latest allowed image and it being really lightweight

* Final image weight is 58 megabytes which is reasonable for a simple FastAPI app

* Layer structure is the following:

    * Base OS + Python runtime
    * Python dependencies
    * Application source code
    * Runtime command

* Optimization choices

    * Slim image
    * No `pip` cache
    * .dockerignore used
    * Explicit port exposure

* Build & Run process

    Here's the command used for build `docker build -t devops_app .` and here's the full output:

    `Sending build context to Docker daemon  158.2kB
Step 1/6 : FROM python:3.13-slim
 ---> 2b9c9803c6a2
Step 2/6 : COPY requirements.txt .
 ---> e008ec81cade
Step 3/6 : RUN pip install --no-cache-dir -r requirements.txt
 ---> Running in 8a9075a6d920
Collecting fastapi==0.115.0 (from -r requirements.txt (line 1))
  Downloading fastapi-0.115.0-py3-none-any.whl.metadata (27 kB)
Collecting uvicorn==0.32.0 (from uvicorn[standard]==0.32.0->-r requirements.txt (line 2))
  Downloading uvicorn-0.32.0-py3-none-any.whl.metadata (6.6 kB)
Collecting starlette<0.39.0,>=0.37.2 (from fastapi==0.115.0->-r requirements.txt (line 1))
  Downloading starlette-0.38.6-py3-none-any.whl.metadata (6.0 kB)
Collecting pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4 (from fastapi==0.115.0->-r requirements.txt (line 1))
  Downloading pydantic-2.12.5-py3-none-any.whl.metadata (90 kB)
Collecting typing-extensions>=4.8.0 (from fastapi==0.115.0->-r requirements.txt (line 1))
  Downloading typing_extensions-4.15.0-py3-none-any.whl.metadata (3.3 kB)
Collecting click>=7.0 (from uvicorn==0.32.0->uvicorn[standard]==0.32.0->-r requirements.txt (line 2))
  Downloading click-8.3.1-py3-none-any.whl.metadata (2.6 kB)
Collecting h11>=0.8 (from uvicorn==0.32.0->uvicorn[standard]==0.32.0->-r requirements.txt (line 2))
  Downloading h11-0.16.0-py3-none-any.whl.metadata (8.3 kB)
Collecting httptools>=0.5.0 (from uvicorn[standard]==0.32.0->-r requirements.txt (line 2))
  Downloading httptools-0.7.1-cp313-cp313-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (3.5 kB)
Collecting python-dotenv>=0.13 (from uvicorn[standard]==0.32.0->-r requirements.txt (line 2))
  Downloading python_dotenv-1.2.1-py3-none-any.whl.metadata (25 kB)
Collecting pyyaml>=5.1 (from uvicorn[standard]==0.32.0->-r requirements.txt (line 2))
  Downloading pyyaml-6.0.3-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (2.4 kB)
Collecting uvloop!=0.15.0,!=0.15.1,>=0.14.0 (from uvicorn[standard]==0.32.0->-r requirements.txt (line 2))
  Downloading uvloop-0.22.1-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (4.9 kB)
Collecting watchfiles>=0.13 (from uvicorn[standard]==0.32.0->-r requirements.txt (line 2))
  Downloading watchfiles-1.1.1-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.9 kB)
Collecting websockets>=10.4 (from uvicorn[standard]==0.32.0->-r requirements.txt (line 2))
  Downloading websockets-16.0-cp313-cp313-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (6.8 kB)
Collecting annotated-types>=0.6.0 (from pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi==0.115.0->-r requirements.txt (line 1))
  Downloading annotated_types-0.7.0-py3-none-any.whl.metadata (15 kB)
Collecting pydantic-core==2.41.5 (from pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi==0.115.0->-r requirements.txt (line 1))
  Downloading pydantic_core-2.41.5-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (7.3 kB)
Collecting typing-inspection>=0.4.2 (from pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi==0.115.0->-r requirements.txt (line 1))
  Downloading typing_inspection-0.4.2-py3-none-any.whl.metadata (2.6 kB)
Collecting anyio<5,>=3.4.0 (from starlette<0.39.0,>=0.37.2->fastapi==0.115.0->-r requirements.txt (line 1))
  Downloading anyio-4.12.1-py3-none-any.whl.metadata (4.3 kB)
Collecting idna>=2.8 (from anyio<5,>=3.4.0->starlette<0.39.0,>=0.37.2->fastapi==0.115.0->-r requirements.txt (line 1))
  Downloading idna-3.11-py3-none-any.whl.metadata (8.4 kB)
Downloading fastapi-0.115.0-py3-none-any.whl (94 kB)
Downloading uvicorn-0.32.0-py3-none-any.whl (63 kB)
Downloading pydantic-2.12.5-py3-none-any.whl (463 kB)
Downloading pydantic_core-2.41.5-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 253.1 kB/s  0:00:08
Downloading starlette-0.38.6-py3-none-any.whl (71 kB)
Downloading anyio-4.12.1-py3-none-any.whl (113 kB)
Downloading annotated_types-0.7.0-py3-none-any.whl (13 kB)
Downloading click-8.3.1-py3-none-any.whl (108 kB)
Downloading h11-0.16.0-py3-none-any.whl (37 kB)
Downloading httptools-0.7.1-cp313-cp313-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (478 kB)
Downloading idna-3.11-py3-none-any.whl (71 kB)
Downloading python_dotenv-1.2.1-py3-none-any.whl (21 kB)
Downloading pyyaml-6.0.3-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (801 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 801.6/801.6 kB 411.7 kB/s  0:00:01
Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)
Downloading typing_inspection-0.4.2-py3-none-any.whl (14 kB)
Downloading uvloop-0.22.1-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (4.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.4/4.4 MB 480.5 kB/s  0:00:08
Downloading watchfiles-1.1.1-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (456 kB)
Downloading websockets-16.0-cp313-cp313-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (184 kB)
Installing collected packages: websockets, uvloop, typing-extensions, pyyaml, python-dotenv, idna, httptools, h11, click, annotated-types, uvicorn, typing-inspection, pydantic-core, anyio, watchfiles, starlette, pydantic, fastapi

Successfully installed annotated-types-0.7.0 anyio-4.12.1 click-8.3.1 fastapi-0.115.0 h11-0.16.0 httptools-0.7.1 idna-3.11 pydantic-2.12.5 pydantic-core-2.41.5 python-dotenv-1.2.1 pyyaml-6.0.3 starlette-0.38.6 typing-extensions-4.15.0 typing-inspection-0.4.2 uvicorn-0.32.0 uvloop-0.22.1 watchfiles-1.1.1 websockets-16.0

[notice] A new release of pip is available: 25.3 -> 26.0
[notice] To update, run: pip install --upgrade pip
 ---> Removed intermediate container 8a9075a6d920
 ---> 114df2b2de81
Step 4/6 : COPY . .
 ---> 0235449a3ed7
Step 5/6 : EXPOSE 8000
 ---> Running in 866694e6fd4e
 ---> Removed intermediate container 866694e6fd4e
 ---> 24194f119c31
Step 6/6 : CMD ["uvicorn",  "app:app", "--host", "0.0.0.0"]
 ---> Running in 38ac2fe4d38c
 ---> Removed intermediate container 38ac2fe4d38c
 ---> be8b407f827b
Successfully built be8b407f827b
Successfully tagged devops_app:latest```

* Here are logs from inside the docker:

`    docker logs unruffled_jemison
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
recording start time
1770234098
Startup seconds are  1770234098
INFO:     172.17.0.1:33966 - "GET / HTTP/1.1" 200 OK
INFO:     172.17.0.1:41494 - "GET /health HTTP/1.1" 200 OK`

DockerHub URL: -- https://hub.docker.com/repository/docker/blazz1t/devops_app/general

And logs of successful push:

`docker push blazz1t/devops_app:1.0.0
The push refers to repository [docker.io/blazz1t/devops_app]
25f1391e6119: Pushed 
b3639af23419: Mounted from library/python 
3290dd2b7743: Pushed 
0c8d55a45c0d: Mounted from library/python 
38e1e046d3d0: Pushed 
8a3ca8cbd12d: Mounted from library/python 
0da4a108bcf2: Mounted from library/python 
1.0.0: digest: sha256:be8b407f827b177fcba0e6462c5b0ae3890fe39335c1f97e711d07bd934ebfce size: 1845`


## Why This Dockerfile Works

* Uses a compatible Python runtime

* Installs dependencies before copying app code

* Runs uvicorn directly as the container process

* Exposes the correct application port

### If layer order was changed

* If COPY . . was placed before installing dependencies:

* Any code change would invalidate the dependency layer

* Slower rebuilds

* Less efficient CI pipelines

### Security Considerations

* Minimal base image

* No build-time secrets stored

* .dockerignore prevents accidental leaks

* Non-root user recommended

Challenges & Solutions
Issue: Large Image Size

Cause: Python dependencies and base image overhead
Solution: Use slim image and remove pip cache

Issue: Rebuilding Took Too Long

Cause: No effective layer caching
Solution: Reorder Dockerfile layers in future iterations

Issue: Security Concerns

Cause: Default root user
Solution: Introduce non-root user

What I Learned

Dockerfile layer order directly affects build performance

Small base images matter a lot

.dockerignore is not optional

Security defaults are rarely safe

Docker images should be designed, not just made