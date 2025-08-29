CLOUDRUN_SERVICE_URLS=$(gcloud run services describe "$1" \
    --region "$2"  \
    --format "value(metadata.annotations[\"run.googleapis.com/urls\"])" | tr -d '"[]')

# Build the env vars string conditionally
ENV_VARS="^##^CLOUDRUN_SERVICE_URLS=$CLOUDRUN_SERVICE_URLS"
if [ -n "$3" ]; then
    ENV_VARS="$ENV_VARS,$3"
fi
if [ -n "$4" ]; then
    ENV_VARS="$ENV_VARS,$4"
fi

ENV_VARS="$ENV_VARS##ALLOWED_HOSTS=$3,$4"

# Update service with env vars
gcloud run services update "$1" \
    --region "$2" \
    --update-env-vars "$ENV_VARS"