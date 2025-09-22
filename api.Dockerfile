FROM tiangolo/uwsgi-nginx:python3.12

ARG requirements_suffix=".lock"
ARG uwsgi_file="./docker_env/uwsgi/uwsgi.ini"
ARG nginx_conf="./docker_env/nginx/nginx.conf"


ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV TZ Asia/Tokyo

RUN set -eux; \
  apt-get update -y \
  && apt-get upgrade -y \
  && apt-get install -y --no-install-recommends \
    vim \
    ca-certificates \
    curl \
    make \
    openssh-client \
    git \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip

WORKDIR /opt/pyconjp2025
ENV PYTHONPATH /opt/pyconjp2025

COPY requirements$requirements_suffix ./
COPY pyproject.toml ./

RUN pip install --no-cache-dir -r requirements$requirements_suffix

COPY ./src ./src
COPY $uwsgi_file /app/uwsgi.ini
COPY $nginx_conf /app/nginx.conf
ENV NGINX_MAX_UPLOAD 10m
