# 🚀 Deploy Your RoofSpec Matcher in 10 Minutes

**For complete beginners - no tech skills needed!**

---

## ⚡ Super Quick Path (Choose ONE)

### Option A: I Want to Test Locally First (Safest)
👉 Follow: **[Part 1: Test Locally](#part-1-test-locally-recommended)**

### Option B: Deploy to Internet Now (Fastest)
👉 Follow: **[Part 2: Deploy Online](#part-2-deploy-to-internet)**

---

## Part 1: Test Locally (Recommended)

**Why?** Make sure it works before putting it online.

### Step 1: Get an API Key (5 minutes)

You need ONE of these (pick the easier one for you):

#### 🟢 OpenAI (Easier - widely accepted)

1. Go to: https://platform.openai.com/signup
2. Create account (use Google/Microsoft to sign up faster)
3. Click your profile (top right) → "API keys"
4. Click "Create new secret key"
5. **COPY THE KEY** (starts with `sk-proj-...`)
   - ⚠️ You can only see it ONCE! Save it somewhere safe!
6. Add $5 credit:
   - Go to: https://platform.openai.com/settings/organization/billing
   - Click "Add payment method"
   - Add card and $5-10 credit

#### 🔵 Anthropic/Claude (Alternative)

1. Go to: https://console.anthropic.com/
2. Create account
3. Go to "API Keys" in settings
4. Create key (starts with `sk-ant-...`)
5. **COPY THE KEY**
6. Add $5 credit in billing section

---

### Step 2: Setup Your Computer (2 minutes)

#### On Mac/Linux:

Open Terminal and run:

```bash
cd /home/user/ProductComparison
bash setup.sh
```

Wait for it to finish (installs everything automatically).

#### On Windows:

Open Command Prompt and run:

```bash
cd C:\path\to\ProductComparison
setup.bat
```

Wait for it to finish.

---

### Step 3: Add Your API Key (1 minute)

A file called `.env` was created. Open it:

#### On Mac/Linux:
```bash
nano .env
```

#### On Windows:
```bash
notepad .env
```

You'll see:
```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

**Replace the placeholder with your ACTUAL key:**

If you got OpenAI key:
```
OPENAI_API_KEY=sk-proj-abc123youractualkey456
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

Or if you got Anthropic key:
```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=sk-ant-abc123youractualkey456
```

**Save the file:**
- Nano: Press `Ctrl+X`, then `Y`, then `Enter`
- Notepad: Click File → Save

---

### Step 4: Run the App (30 seconds)

#### On Mac/Linux:
```bash
source venv/bin/activate
streamlit run app.py
```

#### On Windows:
```bash
venv\Scripts\activate
streamlit run app.py
```

**It works!** A browser window should open automatically at `http://localhost:8501`

If not, manually open your browser and go to: http://localhost:8501

---

### Step 5: Test It (2 minutes)

1. Find a PDF on your computer (any PDF with text)
2. In the app sidebar:
   - Upload it as "Reference Document"
   - Upload another PDF as "Candidate"
3. Click "Analyze & Compare"
4. Wait 20-30 seconds
5. You should see a comparison table!

**If it works:** 🎉 Success! Now go to Part 2 to put it online.

**If it doesn't work:** See [Troubleshooting](#troubleshooting) below.

---

## Part 2: Deploy to Internet

**This makes your app accessible from anywhere via a URL.**

### Step 1: Make Sure Your Code is on GitHub (1 minute)

Your code is already here:
- **Repository**: `morales451/ProductComparison`
- **Branch**: `claude/roofspec-matcher-app-8uuvR`

✅ Already done!

---

### Step 2: Sign Up for Streamlit Cloud (2 minutes)

1. **Go to**: https://share.streamlit.io/signup

2. **Click**: "Continue with GitHub"

3. **Log in** with your GitHub account (the one that has the ProductComparison repo)

4. **Grant access** when GitHub asks for permission

5. You'll see the Streamlit Cloud dashboard

---

### Step 3: Create Your App (2 minutes)

1. **Click** the big **"New app"** button (top right)

2. **Fill in the form**:
   ```
   Repository:      morales451/ProductComparison
   Branch:          claude/roofspec-matcher-app-8uuvR
   Main file path:  app.py
   App URL:         [pick any name you want]-roofspec
   ```

3. **DON'T CLICK DEPLOY YET!**

4. **Click**: "Advanced settings" (at the bottom)

5. **In the "Secrets" box**, paste this:

   If you have OpenAI key:
   ```toml
   OPENAI_API_KEY = "sk-proj-your-actual-key-here"
   ```

   If you have Anthropic key:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-your-actual-key-here"
   ```

   ⚠️ **IMPORTANT**:
   - Keep the quotes `""`
   - Replace `your-actual-key-here` with your REAL key
   - Don't add spaces around the `=`

6. **NOW CLICK**: "Deploy!" button

---

### Step 4: Wait for Deployment (2 minutes)

You'll see a screen with logs scrolling by. This is normal!

Wait for:
- ✅ Building container...
- ✅ Installing dependencies...
- ✅ Running app...

When you see: **"Your app is live!"** → Success! 🎉

---

### Step 5: Access Your App

Your app is now live at:
```
https://[your-name]-roofspec.streamlit.app
```

**Share this URL with anyone!** They can use your app without installing anything.

---

## 🎉 You're Done!

Your RoofSpec Matcher is now live on the internet!

### What You Can Do Now:

- ✅ Share the URL with colleagues
- ✅ Upload your actual roof coating PDFs
- ✅ Compare products
- ✅ Download comparison results as CSV

### Making Changes:

When you want to update the app:

1. Make changes to `app.py` on your computer
2. Push to GitHub:
   ```bash
   git add app.py
   git commit -m "Updated feature"
   git push origin claude/roofspec-matcher-app-8uuvR
   ```
3. Streamlit Cloud will auto-deploy in 2 minutes!

---

## 🆘 Troubleshooting

### "No LLM API key found" Error

**Problem**: Your API key isn't set up correctly.

**Fix**:
1. Go to your app in Streamlit Cloud dashboard
2. Click the menu (⋮) → Settings
3. Go to "Secrets" section
4. Make sure your key is there in the correct format:
   ```toml
   OPENAI_API_KEY = "sk-proj-actual-key"
   ```
5. Click "Save"
6. App will restart automatically

### "Failed to extract text from PDF"

**Problem**: Your PDF is a scanned image, not text-based.

**Fix**:
- Only use PDFs with selectable text (you can highlight text with your cursor)
- If you have a scanned PDF, you'll need to OCR it first
- Try with a different PDF to test

### App is Slow

**Normal!** LLM processing takes 15-30 seconds per PDF. This is expected.

### "Module not found" Error

**Fix**:
1. Make sure you pushed all files to GitHub:
   ```bash
   git status  # Check what's not pushed
   git add -A
   git commit -m "Add missing files"
   git push origin claude/roofspec-matcher-app-8uuvR
   ```
2. Streamlit Cloud will rebuild automatically

### Local App Won't Start

**Problem**: Virtual environment or dependencies issue.

**Fix**:
```bash
# Delete old environment
rm -rf venv

# Run setup again
bash setup.sh  # or setup.bat on Windows
```

### I Forgot My API Key

**Problem**: You lost the key you created.

**Fix**:
- You can't recover the old key
- Create a NEW key at the same place:
  - OpenAI: https://platform.openai.com/api-keys
  - Anthropic: https://console.anthropic.com/settings/keys
- Update your `.env` file or Streamlit Secrets with the new key

---

## 💰 How Much Will This Cost?

### Streamlit Cloud: FREE
- Free for public GitHub repositories
- No credit card needed
- Unlimited users can access your app

### API Costs:
- **Per PDF analysis**: $0.01 - $0.05
- **If you analyze 100 PDFs**: $1-5 total
- **Monthly budget**: Start with $5-10, monitor usage

### Where to Check Costs:
- OpenAI: https://platform.openai.com/usage
- Anthropic: https://console.anthropic.com/settings/billing

**Set a usage limit** to avoid surprises:
- OpenAI: Go to Billing → Usage limits → Set to $10/month
- Anthropic: Set budget alerts in billing settings

---

## 📞 Need More Help?

### Common Questions:

**Q: Can I make this private?**
A: Yes! Streamlit Cloud paid tier ($20/mo) supports private repos.

**Q: Can I use my own domain?**
A: Yes! Configure custom domain in Streamlit Cloud settings (paid tier).

**Q: How many PDFs can I upload at once?**
A: 1 reference + unlimited candidates. But processing takes time, so 5-10 is practical.

**Q: Can I save comparison results?**
A: Yes! Click "Download Comparison as CSV" button.

**Q: Is my data secure?**
A: PDFs are processed in memory and not saved. LLM providers (OpenAI/Anthropic) process the text per their privacy policies.

---

## 🎯 Quick Command Reference

### Start Local App:
```bash
# Mac/Linux
source venv/bin/activate && streamlit run app.py

# Windows
venv\Scripts\activate && streamlit run app.py
```

### Update Deployed App:
```bash
git add -A
git commit -m "Update"
git push origin claude/roofspec-matcher-app-8uuvR
```

### Check Git Status:
```bash
git status
```

### View Logs (Local):
Just check your terminal window where app is running.

---

## ✅ Verification Checklist

Before sharing your app with others:

- [ ] App loads without errors
- [ ] Successfully uploaded a reference PDF
- [ ] Successfully uploaded candidate PDF(s)
- [ ] "Analyze & Compare" button works
- [ ] Comparison matrix displays
- [ ] Can see red highlighting for missing data
- [ ] AI summary generates at bottom
- [ ] CSV download button works
- [ ] Checked API usage/costs
- [ ] Tested with real roof coating PDFs
- [ ] URL is shareable and works in incognito mode

---

## 🚀 You Got This!

Remember:
1. **Test locally first** (Part 1) - Optional but recommended
2. **Get API key** - Required
3. **Deploy to Streamlit Cloud** (Part 2) - 5 minutes
4. **Share your URL** - Done!

**Need help?** Check the troubleshooting section above.

**Still stuck?** Check the full guides:
- `DEPLOYMENT.md` - Complete technical guide
- `README.md` - Setup and usage guide

---

**Made with ❤️ for vibecoding beginners**
