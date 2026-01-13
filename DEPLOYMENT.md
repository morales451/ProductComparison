# RoofSpec Matcher - Deployment Guide

This guide covers multiple deployment options for the RoofSpec Matcher application.

## Table of Contents
1. [Streamlit Cloud (Recommended - Easiest)](#option-1-streamlit-cloud-recommended)
2. [Docker Deployment](#option-2-docker-deployment)
3. [AWS/GCP/Azure Deployment](#option-3-cloud-platforms)
4. [Local Network Deployment](#option-4-local-network)

---

## Option 1: Streamlit Cloud (Recommended)

**Best for**: Quick deployment, free hosting, minimal configuration
**Cost**: Free for public repos, paid plans for private repos

### Prerequisites
- GitHub account
- Your code pushed to a GitHub repository
- OpenAI or Anthropic API key

### Step-by-Step Instructions

#### 1. Prepare Your Repository

Ensure all files are committed and pushed to GitHub:

```bash
git status
git add -A
git commit -m "Prepare for deployment"
git push -u origin claude/roofspec-matcher-app-8uuvR
```

#### 2. Sign Up for Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click "Sign up" and authenticate with your GitHub account
3. Grant Streamlit access to your repositories

#### 3. Deploy the App

1. Click "New app" button
2. Select your repository: `morales451/ProductComparison`
3. Select branch: `claude/roofspec-matcher-app-8uuvR`
4. Main file path: `app.py`
5. Click "Deploy"

#### 4. Configure Secrets (API Keys)

**CRITICAL**: Before your app works, you must add your API key:

1. In Streamlit Cloud dashboard, click on your app
2. Click the menu (⋮) → "Settings"
3. Go to "Secrets" section
4. Add your API key in TOML format:

```toml
# For OpenAI
OPENAI_API_KEY = "sk-your-actual-key-here"

# OR for Anthropic
ANTHROPIC_API_KEY = "sk-ant-your-actual-key-here"
```

5. Click "Save"
6. The app will automatically restart with the new secrets

#### 5. Access Your App

Your app will be available at:
```
https://[your-app-name].streamlit.app
```

You can customize the URL in the app settings.

### Streamlit Cloud Benefits
- ✅ Free for public repositories
- ✅ Automatic HTTPS
- ✅ Auto-restarts on code changes
- ✅ Built-in secrets management
- ✅ No server management needed
- ✅ Scales automatically

### Streamlit Cloud Limitations
- Max 1GB RAM on free tier
- App sleeps after inactivity (restarts on next visit)
- Public repos only on free tier

---

## Option 2: Docker Deployment

**Best for**: On-premise deployment, custom infrastructure, full control
**Cost**: Infrastructure costs only

### Files Created

I've created a `Dockerfile` and `docker-compose.yml` for you.

### Quick Start with Docker

```bash
# 1. Build the image
docker build -t roofspec-matcher .

# 2. Run with environment variables
docker run -p 8501:8501 \
  -e OPENAI_API_KEY="your-key-here" \
  roofspec-matcher

# OR use docker-compose (recommended)
docker-compose up -d
```

### Using docker-compose (Recommended)

1. Create a `.env` file (already exists):
```bash
OPENAI_API_KEY=your_key_here
```

2. Start the application:
```bash
docker-compose up -d
```

3. Access at: http://localhost:8501

4. View logs:
```bash
docker-compose logs -f
```

5. Stop the application:
```bash
docker-compose down
```

### Deploy Docker to Cloud

**AWS (ECS/Fargate)**
```bash
# Build and tag
docker build -t roofspec-matcher .
docker tag roofspec-matcher:latest [your-ecr-repo]:latest

# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin [your-ecr-repo]
docker push [your-ecr-repo]:latest

# Deploy to ECS using AWS Console or CLI
```

**Google Cloud Run**
```bash
# Build and push
gcloud builds submit --tag gcr.io/[PROJECT-ID]/roofspec-matcher

# Deploy
gcloud run deploy roofspec-matcher \
  --image gcr.io/[PROJECT-ID]/roofspec-matcher \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=[your-key]
```

**Azure Container Instances**
```bash
# Build and push to Azure Container Registry
az acr build --registry [registry-name] --image roofspec-matcher .

# Deploy
az container create \
  --resource-group [resource-group] \
  --name roofspec-matcher \
  --image [registry-name].azurecr.io/roofspec-matcher \
  --dns-name-label roofspec-matcher \
  --ports 8501 \
  --environment-variables OPENAI_API_KEY=[your-key]
```

---

## Option 3: Cloud Platforms

### AWS EC2

1. Launch an EC2 instance (Ubuntu 20.04 or later)
2. SSH into the instance
3. Install dependencies:
```bash
sudo apt update
sudo apt install -y python3.10 python3-pip git
```

4. Clone your repository:
```bash
git clone https://github.com/morales451/ProductComparison.git
cd ProductComparison
git checkout claude/roofspec-matcher-app-8uuvR
```

5. Run setup:
```bash
bash setup.sh
```

6. Configure environment:
```bash
nano .env  # Add your API key
```

7. Run with nohup (keeps running after logout):
```bash
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
```

8. Configure security group to allow port 8501

9. Access at: http://[ec2-public-ip]:8501

### Heroku

1. Create a `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. Create `setup.sh` for Heroku:
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

3. Deploy:
```bash
heroku create roofspec-matcher
heroku config:set OPENAI_API_KEY=your_key_here
git push heroku claude/roofspec-matcher-app-8uuvR:main
```

### DigitalOcean App Platform

1. Connect your GitHub repository
2. Select branch and `app.py`
3. Add environment variable: `OPENAI_API_KEY`
4. Deploy

---

## Option 4: Local Network

**Best for**: Internal company use, no internet exposure needed

### Using ngrok (Temporary Public URL)

```bash
# 1. Start your app locally
streamlit run app.py

# 2. In another terminal, expose with ngrok
ngrok http 8501
```

You'll get a temporary public URL like: `https://abc123.ngrok.io`

### Using Tailscale (Secure Private Network)

1. Install Tailscale on your server and client devices
2. Run the app on your server
3. Access via Tailscale IP from any device on your network

---

## Choosing the Right Option

| Option | Best For | Difficulty | Cost |
|--------|----------|------------|------|
| **Streamlit Cloud** | Quick public demo, MVP | ⭐ Easy | Free/Paid |
| **Docker** | Professional deployment, on-premise | ⭐⭐ Medium | Infrastructure only |
| **AWS/GCP/Azure** | Enterprise, custom needs | ⭐⭐⭐ Advanced | Pay-as-you-go |
| **Local Network** | Internal tools, testing | ⭐ Easy | Free |

---

## Post-Deployment Checklist

After deploying, verify:

- [ ] App loads without errors
- [ ] Can upload reference PDF
- [ ] Can upload candidate PDFs
- [ ] "Analyze & Compare" button works
- [ ] LLM extraction completes successfully
- [ ] Comparison matrix displays correctly
- [ ] AI summary generates
- [ ] CSV download works
- [ ] API costs are within budget
- [ ] Error handling works (try uploading a bad PDF)

---

## Troubleshooting

### "No LLM API key found" Error
- **Streamlit Cloud**: Check Secrets section in app settings
- **Docker**: Verify `.env` file or environment variables
- **EC2/Other**: Check `.env` file exists and is loaded

### "Failed to extract text from PDF" Error
- PDF might be image-based (needs OCR)
- Try with a different PDF that has selectable text

### App is Slow
- LLM processing takes time (15-30 seconds per PDF)
- Consider using a faster model (gpt-4o-mini is already optimized)
- For Streamlit Cloud: upgrade to paid tier for more resources

### Out of Memory
- Streamlit Cloud free tier: 1GB RAM limit
- Solution: Upgrade tier or deploy to Docker/cloud with more RAM

### SSL/HTTPS Issues
- Streamlit Cloud: Automatic HTTPS
- Custom domain: Use Cloudflare or AWS CloudFront

---

## Monitoring & Maintenance

### Monitor API Costs
- OpenAI: https://platform.openai.com/usage
- Anthropic: https://console.anthropic.com/settings/billing

### Monitor App Usage (Streamlit Cloud)
- View analytics in Streamlit Cloud dashboard
- Check active users, load times, errors

### Update the App
```bash
# Make changes locally
git add -A
git commit -m "Update feature X"
git push origin claude/roofspec-matcher-app-8uuvR

# Streamlit Cloud auto-deploys
# Docker: rebuild and restart
docker-compose down
docker-compose up -d --build
```

---

## Security Best Practices

1. **Never commit API keys to git** (already protected by .gitignore)
2. **Use environment variables** for secrets
3. **Enable authentication** if handling sensitive data
4. **Use HTTPS** (automatic on Streamlit Cloud)
5. **Monitor API usage** to prevent abuse
6. **Set rate limits** if exposing publicly
7. **Regular security updates**: `pip install --upgrade -r requirements.txt`

---

## Getting Help

- **Streamlit Docs**: https://docs.streamlit.io/
- **Streamlit Forum**: https://discuss.streamlit.io/
- **Docker Docs**: https://docs.docker.com/
- **GitHub Issues**: Report problems in your repository

---

## Next Steps

For most users, I recommend starting with **Streamlit Cloud** because:
- It's free for public repositories
- Takes 5 minutes to set up
- No infrastructure management
- Automatic scaling and HTTPS
- Easy secret management

Once you've validated the app works, you can migrate to Docker or cloud platforms if needed for:
- Private/proprietary use
- Higher performance requirements
- Custom infrastructure needs
- Integration with existing systems
