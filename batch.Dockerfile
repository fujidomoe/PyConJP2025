FROM python:3.12.3

ARG requirements_suffix=".lock"
ARG TOPA_ENV

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV TZ Asia/Tokyo

RUN set -eux; \
  apt-get update -y \
  && apt-get upgrade -y \
  && apt-get install -y --no-install-recommends \
    vim \
    sqlite3 \
    make \
    openssh-client \
    git \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip

WORKDIR /opt/pyconjp2025
ENV PYTHONPATH /opt/pyconjp2025

COPY requirements$requirements_suffix ./
COPY ./pyproject.toml ./

RUN pip install --no-cache-dir -r requirements$requirements_suffix

COPY ./src ./src
ENTRYPOINT ["/usr/bin/make", "-C", "src"]
CMD ["bash"]
