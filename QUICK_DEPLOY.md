# Quick Deployment Reference

One-page cheat sheet for deploying RoofSpec Matcher.

---

## 🚀 Streamlit Cloud (Easiest - 5 minutes)

```bash
# 1. Code is already pushed to GitHub ✅

# 2. Go to: https://streamlit.io/cloud
# 3. Click "New app"
# 4. Select: morales451/ProductComparison, branch: claude/roofspec-matcher-app-8uuvR
# 5. Add API key in Secrets:
OPENAI_API_KEY = "sk-proj-your-key"

# Done! App at: https://[name].streamlit.app
```

See: `deploy_streamlit_cloud.md` for detailed guide

---

## 🐳 Docker (Local or Cloud)

### Build and Run Locally

```bash
# Quick start with docker-compose
docker-compose up -d

# Or manually
docker build -t roofspec-matcher .
docker run -p 8501:8501 -e OPENAI_API_KEY="your-key" roofspec-matcher

# Access at: http://localhost:8501
```

### Deploy to Google Cloud Run

```bash
gcloud builds submit --tag gcr.io/[PROJECT-ID]/roofspec-matcher
gcloud run deploy roofspec-matcher \
  --image gcr.io/[PROJECT-ID]/roofspec-matcher \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=[your-key]
```

### Deploy to AWS ECS

```bash
# Tag and push
docker tag roofspec-matcher:latest [ECR-URI]:latest
docker push [ECR-URI]:latest

# Deploy via AWS Console or CLI
```

---

## ☁️ Heroku

```bash
# Create app
heroku create roofspec-matcher

# Set API key
heroku config:set OPENAI_API_KEY=your-key

# Deploy
git push heroku claude/roofspec-matcher-app-8uuvR:main

# Open
heroku open
```

---

## 🖥️ AWS EC2

```bash
# 1. Launch Ubuntu EC2 instance
# 2. SSH in
ssh -i your-key.pem ubuntu@[ec2-ip]

# 3. Clone and setup
git clone https://github.com/morales451/ProductComparison.git
cd ProductComparison
git checkout claude/roofspec-matcher-app-8uuvR
bash setup.sh

# 4. Configure API key
nano .env  # Add: OPENAI_API_KEY=your-key

# 5. Run
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &

# Access at: http://[ec2-ip]:8501
```

---

## 🔧 Local Development

```bash
# Setup
bash setup.sh  # or setup.bat on Windows

# Configure
nano .env  # Add API key

# Run
source venv/bin/activate  # or venv\Scripts\activate on Windows
streamlit run app.py

# Access at: http://localhost:8501
```

---

## 🔑 API Keys

### Get OpenAI Key:
1. https://platform.openai.com/api-keys
2. Create key (starts with `sk-proj-...`)
3. Add $5+ credit: https://platform.openai.com/billing

### Get Anthropic Key:
1. https://console.anthropic.com/settings/keys
2. Create key (starts with `sk-ant-...`)
3. Add credits: https://console.anthropic.com/billing

---

## 💰 Cost Per Document

- **OpenAI GPT-4o-mini**: $0.01 - $0.05 per PDF
- **Anthropic Claude Sonnet**: $0.02 - $0.08 per PDF

---

## 📊 Choose Your Platform

| Platform | Time | Difficulty | Cost | Best For |
|----------|------|------------|------|----------|
| **Streamlit Cloud** | 5 min | ⭐ | Free | Quick demo, public |
| **Docker Local** | 10 min | ⭐⭐ | Free | Testing, development |
| **Heroku** | 15 min | ⭐⭐ | $7/mo | Simple hosting |
| **AWS EC2** | 30 min | ⭐⭐⭐ | $10+/mo | Control, custom |
| **Google Cloud Run** | 20 min | ⭐⭐⭐ | Pay per use | Scalable, serverless |

---

## ✅ Post-Deploy Checklist

- [ ] App loads without errors
- [ ] Can upload PDFs
- [ ] LLM extraction works
- [ ] Comparison matrix displays
- [ ] CSV download works
- [ ] API key is secure (not in code)
- [ ] Monitoring API costs

---

## 🆘 Quick Troubleshooting

**"No LLM API key found"**
→ Add key to .env or Streamlit Secrets

**"Failed to extract text from PDF"**
→ PDF must have selectable text (not image-based)

**App is slow**
→ LLM takes 15-30s per document (normal)

**Out of memory**
→ Upgrade Streamlit Cloud tier or use Docker with more RAM

---

## 📚 Full Documentation

- **Complete Guide**: `DEPLOYMENT.md`
- **Streamlit Cloud**: `deploy_streamlit_cloud.md`
- **Setup Instructions**: `README.md`

---

## 🔄 Update Deployed App

```bash
# Make changes locally
git add -A
git commit -m "Update feature"
git push origin claude/roofspec-matcher-app-8uuvR

# Streamlit Cloud: Auto-deploys in 1-2 minutes
# Docker: docker-compose up -d --build
# Heroku: git push heroku [branch]:main
# EC2: git pull && restart streamlit
```

---

**Recommended**: Start with Streamlit Cloud, migrate to Docker/cloud if needed later.
