FROM python:3.11.2-buster as build

WORKDIR /opt/fastapi_solution

COPY ./requirements.txt .

RUN python -m venv venv \
    && venv/bin/pip install --no-cache-dir --upgrade pip \
    && venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.11.2-buster

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/fastapi_solution/venv/bin:${PATH}"

ARG APP=/opt/fastapi_solution
ARG USER=web

WORKDIR ${APP}

RUN groupadd -r ${USER} \
    && useradd -d ${APP} -r -g ${USER} ${USER}

COPY --chown=${USER}:${USER} --from=build ${APP}/venv ./venv
COPY --chown=${USER}:${USER} . .

USER ${USER}

CMD ["python",  "src/main.py"]
