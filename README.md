# ComposeMind - LCM-Inspired Reasoning & Composition Engine

A cloud-native, Dockerized reasoning and composition system inspired by Latent Concept Models (LCMs). The system breaks down tasks into sentence-level goals, composes content step-by-step via LLM, and traces reasoning using visual graphs.

## 🚀 Features

- Cloud-native architecture using AWS services
- Dockerized components for easy deployment
- Step-by-step content planning and generation
- Visual reasoning trace using Mermaid.js
- Side-by-side comparison with GPT outputs

## 🏗️ Project Structure

```
composemind/
├── composition_engine/       # Stepwise content planning and generation
├── embedding_layer/          # Sentence & paragraph embedding
├── reasoning_trace/          # Trace logs + JSON generation
├── comparison_ui/            # React + Mermaid.js frontend
├── cloud_infra/              # Terraform & AWS Lambda setup
```

## 🛠️ Setup & Deployment

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/composemind.git
   cd composemind
   ```

2. Set up AWS credentials:
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_REGION=your_region
   ```

3. Deploy infrastructure:
   ```bash
   cd cloud_infra
   terraform init
   terraform apply
   ```

4. Start services:
   ```bash
   docker-compose up -d
   ```

## 🔒 Security

- All services run in Docker containers
- AWS IAM roles for secure access
- API Gateway for secure endpoints
- No local package installations required

## 📝 License

MIT License - See LICENSE file for details 