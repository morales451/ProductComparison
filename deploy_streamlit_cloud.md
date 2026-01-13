# Quick Deploy to Streamlit Cloud

## 5-Minute Deployment Guide

### Step 1: Push Your Code to GitHub ✅

Your code is already on GitHub at:
- Repository: `morales451/ProductComparison`
- Branch: `claude/roofspec-matcher-app-8uuvR`

### Step 2: Go to Streamlit Cloud

1. Open: https://streamlit.io/cloud
2. Click **"Sign up"** (or "Sign in" if you have an account)
3. Authenticate with your GitHub account

### Step 3: Create New App

1. Click the **"New app"** button
2. Fill in the form:
   - **Repository**: `morales451/ProductComparison`
   - **Branch**: `claude/roofspec-matcher-app-8uuvR`
   - **Main file path**: `app.py`
   - **App URL** (optional): Choose a custom subdomain

3. Click **"Deploy!"**

### Step 4: Configure Your API Key

**IMPORTANT**: Your app won't work until you add an API key!

1. While the app is deploying, click **"Advanced settings"** (or go to Settings after deployment)
2. Find the **"Secrets"** section
3. Add your API key in TOML format:

```toml
# If using OpenAI:
OPENAI_API_KEY = "sk-proj-your-actual-key-here"

# OR if using Anthropic:
ANTHROPIC_API_KEY = "sk-ant-your-actual-key-here"
```

4. Click **"Save"**

### Step 5: Access Your App

Your app will be available at:
```
https://[your-custom-name].streamlit.app
```

Or find the URL in your Streamlit Cloud dashboard.

---

## Getting Your API Keys

### OpenAI (GPT)
1. Go to: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-proj-...`)
4. Add $5-10 credit at: https://platform.openai.com/settings/organization/billing/overview

### Anthropic (Claude)
1. Go to: https://console.anthropic.com/settings/keys
2. Click "Create Key"
3. Copy the key (starts with `sk-ant-...`)
4. Add credits at: https://console.anthropic.com/settings/billing

---

## Cost Estimates

### Per Document Analysis:
- **OpenAI GPT-4o-mini**: ~$0.01 - $0.05 per PDF
- **Anthropic Claude Sonnet**: ~$0.02 - $0.08 per PDF

### Monthly Estimates:
- **Light usage** (50 PDFs/month): $1-3
- **Medium usage** (200 PDFs/month): $5-15
- **Heavy usage** (1000 PDFs/month): $25-50

---

## Troubleshooting

### "No LLM API key found" Error
- Go to your app settings
- Check that you added the key to **Secrets** section
- Make sure format is correct (TOML format, no extra quotes)
- Save and wait for app to restart

### App Won't Start
- Check the logs in Streamlit Cloud dashboard
- Verify `requirements.txt` has all dependencies
- Ensure `app.py` is at the root of your repository

### "Module not found" Error
- Check that all imports in `requirements.txt` are correct
- Try restarting the app from dashboard

---

## Next Steps After Deployment

1. **Test the app**: Upload a sample PDF and verify it works
2. **Share the URL**: Send the link to your team
3. **Monitor usage**: Check Streamlit Cloud analytics
4. **Monitor costs**: Check your API provider billing dashboard
5. **Update code**: Push changes to GitHub, app auto-updates

---

## Making Updates

```bash
# 1. Make changes to your code locally
# Edit app.py or other files

# 2. Commit and push
git add -A
git commit -m "Update feature"
git push origin claude/roofspec-matcher-app-8uuvR

# 3. Streamlit Cloud auto-deploys (takes 1-2 minutes)
```

---

## Free Tier Limitations

Streamlit Cloud free tier includes:
- ✅ 1 GB RAM
- ✅ 1 CPU core
- ✅ Unlimited viewers
- ✅ Auto-sleep after inactivity (wakes on visit)
- ✅ Public apps only

For private apps or more resources, upgrade to paid tier ($20/month).

---

## Support

- **Streamlit Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **Community Forum**: https://discuss.streamlit.io/
- **Status Page**: https://streamlitstatus.com/

---

**That's it! Your RoofSpec Matcher app should now be live! 🎉**
