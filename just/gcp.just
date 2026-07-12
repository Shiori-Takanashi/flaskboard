# just/gcp.just

# ==========================================
# GCP-SETTING
# ==========================================

set dotenv-load := true
set dotenv-path := ".env.gcp"

PROJECT_ID := env("PROJECT_ID")
REGION := env("REGION")
SERVICE_NAME := env("SERVICE_NAME")
REPOSITORY := env("REPOSITORY")
IMAGE_NAME := env("IMAGE_NAME")
IMAGE_TAG := env("IMAGE_TAG")
PORT := env("PORT")
DESCRIPTION := env("DESCRIPTION")

IMAGE_URL := REGION + "-docker.pkg.dev/" + PROJECT_ID + "/" + REPOSITORY + "/" + IMAGE_NAME + ":" + IMAGE_TAG


# ==========================================
# Artifact Registry
# ==========================================

g-repo:
    gcloud services enable artifactregistry.googleapis.com \
        --project="{{PROJECT_ID}}"

    gcloud artifacts repositories describe "{{REPOSITORY}}" \
        --location="{{REGION}}" \
        --project="{{PROJECT_ID}}" \
        >/dev/null 2>&1 \
    || gcloud artifacts repositories create "{{REPOSITORY}}" \
        --repository-format=docker \
        --location="{{REGION}}" \
        --description="{{DESCRIPTION}}" \
        --project="{{PROJECT_ID}}"


# ==========================================
# Build
# ==========================================

g-build:
    gcloud builds submit . \
        --project="{{PROJECT_ID}}" \
        --region="{{REGION}}" \
        --tag="{{IMAGE_URL}}" \
        --ignore-file=".gcloudignore"


# ==========================================
# Deploy
# ==========================================

g-deploy:
    gcloud run deploy "{{SERVICE_NAME}}" \
        --project="{{PROJECT_ID}}" \
        --image="{{IMAGE_URL}}" \
        --region="{{REGION}}" \
        --port="{{PORT}}" \
        --allow-unauthenticated

# ==========================================
# Release
# ==========================================

g-release: g-build g-deploy
