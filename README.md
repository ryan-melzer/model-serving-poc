# Model Serving Modernization Proof of Concept


## Step 0: Setup dependencies (macOS only)

### Install system dependencies

```sh
brew install kind kubectl helm istioctl jq k9s hey uv 
```

### Set up JFrog environment variables if you haven't

```sh
export ARTIFACTORY_USERNAME="<your email address>"
export ARTIFACTORY_PASSWORD="<jfrog token>"
export UV_INDEX_ARTIFACTORY_USERNAME="$ARTIFACTORY_USERNAME"
export UV_INDEX_ARTIFACTORY_PASSWORD="$ARTIFACTORY_PASSWORD"
```

### SSO login

```sh
aws sso login --profile up_ml_prod
```

### Create Python environment and verify installation

```sh
uv lock
uv run python verify_installation.py
```

or

```sh
uv sync
source .venv/bin/activate
python verify_installation.py
```