ARG USER="simple_user"
ARG PYTHON_IMAGE='python:3.10-alpine'
ARG WORKDIR="/home/$USER"

# --------------------------------------------------------------------------------------------
FROM ${PYTHON_IMAGE} as builder

RUN apk update &&  \
    apk add --no-cache  \
    libffi-dev  \
    build-base

COPY requirements /tmp/requirements

RUN pip install --no-cache-dir --upgrade setuptools pip && \
    pip install --no-cache-dir --prefix /install -r /tmp/requirements/requirements-base.txt && \
    pip install --no-cache-dir --prefix /install-test -r /tmp/requirements/requirements-test.txt
# --------------------------------------------------------------------------------------------
FROM ${PYTHON_IMAGE} as build_wheel
ARG WORKDIR

WORKDIR $WORKDIR
COPY . .
COPY --from=builder /install /usr/local

RUN set -ex && pip install --upgrade setuptools wheel && \
    python setup.py bdist_wheel && \
    mv dist /dist
# --------------------------------------------------------------------------------------------
FROM ${PYTHON_IMAGE} as production
ARG USER
ARG WORKDIR

WORKDIR $WORKDIR
RUN adduser -D "${USER}"

COPY --from=builder --chown=$USER:$USER /install /usr/local
COPY --chown=$USER:$USER --from=build_wheel /dist /tmp/dist

USER $USER
RUN pip install /tmp/dist/* && rm -rf /tmp/dist

CMD [ "simple_server-app", "--host", "0.0.0.0", "--port", "8080"]
# --------------------------------------------------------------------------------------------
FROM production