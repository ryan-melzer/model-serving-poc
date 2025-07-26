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

### Get CA cert to use upwork mlflow locally

```sh
aws acm-pca get-certificate-authority-certificate --certificate-authority-arn \
 "arn:aws:acm-pca:us-west-2:208818359839:certificate-authority/05d76ba2-332d-4c73-9dfd-642f35563b2c" |\
 jq -r '.Certificate,.CertificateChain' > /tmp/upwork.pem
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