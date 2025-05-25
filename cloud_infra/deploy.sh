#!/bin/bash

# Exit on error
set -e

echo "🚀 Deploying ComposeMind infrastructure..."

# Initialize Terraform
echo "📦 Initializing Terraform..."
terraform init

# Validate Terraform configuration
echo "🔍 Validating Terraform configuration..."
terraform validate

# Plan the deployment
echo "📝 Planning deployment..."
terraform plan -out=tfplan

# Apply the changes
echo "🔄 Applying changes..."
terraform apply tfplan

# Get the API Gateway URL
API_URL=$(terraform output -raw api_gateway_url)
echo "✅ Deployment complete!"
echo "🌐 API Gateway URL: $API_URL"

# Update environment variables
echo "📝 Updating environment variables..."
echo "REACT_APP_API_URL=$API_URL" > ../comparison_ui/.env

echo "🎉 Done! You can now start the services using docker-compose." 