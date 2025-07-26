# https://bitbucket.techops.usw2.upwork/projects/AGORA/repos/python-mesh-stage1
FROM 474230206603.dkr.ecr.us-west-2.amazonaws.com/upwork/docker-python-mesh-stage1:v1.0.1

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED=True
ENV APP_HOME=/app
ENV PYTHONPATH=$APP_HOME/src
ENV UV_NATIVE_TLS=true
ENV UV_HTTP_TIMEOUT=15000
# Suppress MLflow git warnings since git is removed for security
ENV GIT_PYTHON_REFRESH=quiet

USER root
WORKDIR $APP_HOME

# Install internal project dependencies.
COPY --chown=appuser:appgroup pyproject.toml uv.lock ./
RUN --mount=type=secret,id=ARTIFACTORY_USERNAME,uid=101 \
    --mount=type=secret,id=ARTIFACTORY_PASSWORD,uid=101 \
    export UV_INDEX_ARTIFACTORY_USERNAME="$(cat /run/secrets/ARTIFACTORY_USERNAME)"; \
    export UV_INDEX_ARTIFACTORY_PASSWORD="$(cat /run/secrets/ARTIFACTORY_PASSWORD)"; \
    echo $UV_INDEX_ARTIFACTORY_USERNAME; \
    uv venv --python 3.13 /venv && \
    . /venv/bin/activate && \
    uv sync --active --compile-bytecode --no-cache --frozen --no-install-project && \
    chown -R appuser:appuser /venv

# Copy local code to the container image.
COPY --chown=appuser:appgroup .git/ .git/
COPY --chown=appuser:appgroup certs/ certs/
#COPY --chown=appuser:appgroup /tmp/upwork.pem /tmp/upwork.pem
RUN mkdir -p src && chown appuser:appgroup src/
#COPY --chown=appuser:appgroup src/ src/
COPY --chown=appuser:appgroup train_model.py src/
#COPY --chown=appuser:appgroup README.md run.sh config.yaml ./
COPY --chown=appuser:appgroup README.md ./

# Install project.
RUN . /venv/bin/activate && \
    uv sync --active --no-cache --frozen && \
    chown -R appuser:appuser /venv

# Uninstall development libraries due to infosec requirements.
RUN python3 -m pip uninstall -y hatch uv && apt remove -y --purge git
#USER appuser

#CMD ["/app/run.sh"]
CMD ["/venv/bin/python", "/app/train_model.py"]
