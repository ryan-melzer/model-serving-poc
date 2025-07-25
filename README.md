# Model Serving Modernization Proof of Concept

## Prerequisites

### Step 0: Setup dependencies (macOS only)

```sh
brew install kind kubectl helm istioctl jq k9s hey
```

Set up JFrog environment variables if you haven't

```sh
export ARTIFACTORY_USERNAME="<your email address>"
export ARTIFACTORY_PASSWORD="<jfrog token>"
export UV_INDEX_ARTIFACTORY_USERNAME="$ARTIFACTORY_USERNAME"
export UV_INDEX_ARTIFACTORY_PASSWORD="$ARTIFACTORY_PASSWORD"
```

SSO login

```sh
aws sso login --profile up_ml_prod
```

### Step 1. Create Hatch environment

```sh
brew install pipx uv
pipx install hatch
hatch config set dirs.env.virtual .hatch
hatch config set dirs.env.uvenv .hatch
```

```sh
# Create lockfile (first time only)
uv lock
```

### Step 2. Verify installation

```sh
hatch run python verify_installation.py
```

or

```sh
hatch shell
python verify_installation.py
```

## Commands

```sh
# Enter environment shell
hatch shell

# Exit environment
exit
```

```sh
# Run Python scripts without shell
hatch run python your_script.py
```
