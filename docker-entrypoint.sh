#!/bin/bash
set -e

if [ -n "$AWS_SM_SECRETS_ID" ]
then
    echo Exporting secrets
    echo "AWS_CONTAINER_CREDENTIALS_RELATIVE_URI=$AWS_CONTAINER_CREDENTIALS_RELATIVE_URI" > /tmp/aws.env
    aws secretsmanager get-secret-value --region $AWS_REGION --secret-id ${AWS_SM_SECRETS_ID} --query SecretString --output text | jq -r 'to_entries|map("\(.key)=\(.value|tostring)")|.[]' > /tmp/secrets.env
    eval $(cat /tmp/secrets.env  /tmp/aws.env | sed 's/^/export /' | sudo tee -a /etc/profile.d/secrets.sh)

    echo Exporting parameters
    aws secretsmanager get-secret-value --region $AWS_REGION --secret-id ${AWS_SM_PARAMETERS_ID} --query SecretString --output text | jq -r 'to_entries|map("\(.key)=\(.value|tostring)")|.[]' > /tmp/parameters.env
    eval $(cat /tmp/parameters.env | sed 's/^/export /')

    echo Exporting signing params
    aws secretsmanager get-secret-value --region $AWS_REGION --secret-id ${AWS_CF_SIGNER_SECRET_ID} --query SecretString --output text | jq -r 'to_entries|map("\(.key)=\(.value|tostring)")|.[]' > /tmp/cloudfront.env
    eval $(cat /tmp/cloudfront.env | sed 's/^/export /')
fi

#=========#
#   SSM   #
#=========#

# Register instance on SSM
if [ -n "$INSTANCE_NAME" ]; then
    echo Creating Activation Key with AWS SSM
    read -r ACTIVATION_CODE ACTIVATION_ID <<< $(aws ssm create-activation --default-instance-name "${INSTANCE_NAME}" --iam-role "KPRSSMRole" --registration-limit 1 --region ${AWS_DEFAULT_REGION} --tags "Key=Name,Value=${INSTANCE_NAME}" "Key=Type,Value=fargate" --query "join(' ', [ActivationCode, ActivationId])" --output text)
    echo Registering SSM Code
    sudo amazon-ssm-agent -register -code "${ACTIVATION_CODE}" -id "${ACTIVATION_ID}" -region "${AWS_DEFAULT_REGION}" -clear -y
    echo Starting SSM Agent Services
    sudo amazon-ssm-agent 2>&1 &
fi

# Google Credentials as JSON
if [ -n "$GOOGLE_CREDENTIALS" ]
then
    echo Creating Google Credentials File based on Env Variable
    echo $GOOGLE_CREDENTIALS | base64 --decode > /tmp/credentials.json
    export GOOGLE_APPLICATION_CREDENTIALS=/tmp/credentials.json
fi

# Unregister instance from SSM on SIGTERM
term_handler() {
    if [ -n "$INSTANCE_NAME" ]; then
        aws ssm deregister-managed-instance --region ${AWS_DEFAULT_REGION} --instance-id $(sudo cat /var/lib/amazon/ssm/registration | jq -r .ManagedInstanceID)
        echo "SSM instance Unregistered"
        exit 143; # 128 + 15 -- SIGTERM
    fi
}
trap 'term_handler' SIGTERM SIGINT ERR


"$@"
