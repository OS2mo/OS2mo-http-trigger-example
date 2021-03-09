# SPDX-FileCopyrightText: Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./requirements.txt /app/requirements.txt
COPY ./requirements /app/requirements
RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app
COPY ./app /app
