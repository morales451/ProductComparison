# 🚀 DEPLOY IN 5 MINUTES - COPY/PASTE GUIDE

**No thinking required. Just follow these exact steps.**

---

## 🎯 Three Ways to Deploy (Pick ONE)

### 🤖 Way 1: Let the Script Do Everything (EASIEST)

Just run this command:

```bash
python deploy_helper.py
```

Follow the interactive prompts. The script will:
- ✅ Check your setup
- ✅ Help you configure API keys
- ✅ Guide you through deployment

**That's it!** The script handles everything.

---

### ⚡ Way 2: Just Get It Online Now (FASTEST)

#### Step 1: Get API Key (2 min)

Go to ONE of these:

**OpenAI** (recommended):
1. Visit: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy it (starts with `sk-proj-`)
4. Add $5 at: https://platform.openai.com/billing

**OR Anthropic**:
1. Visit: https://console.anthropic.com/settings/keys
2. Click "Create key"
3. Copy it (starts with `sk-ant-`)

#### Step 2: Deploy to Streamlit Cloud (3 min)

1. **Open**: https://share.streamlit.io/signup

2. **Click**: "Continue with GitHub"

3. **Click**: "New app" button

4. **Type exactly**:
   ```
   Repository: morales451/ProductComparison
   Branch: claude/roofspec-matcher-app-8uuvR
   Main file: app.py
   ```

5. **Click**: "Advanced settings" at bottom

6. **In the Secrets box, paste** (use YOUR actual key):

   For OpenAI:
   ```
   OPENAI_API_KEY = "sk-proj-paste-your-real-key-here"
   ```

   For Anthropic:
   ```
   ANTHROPIC_API_KEY = "sk-ant-paste-your-real-key-here"
   ```

7. **Click**: "Deploy!"

8. **Wait** 2 minutes

9. **Done!** Your app is at: `https://[your-name].streamlit.app`

---

### 🏠 Way 3: Test on Your Computer First (SAFEST)

#### Step 1: Setup (1 min)

**Mac/Linux:**
```bash
cd /home/user/ProductComparison
bash setup.sh
```

**Windows:**
```bash
cd C:\path\to\ProductComparison
setup.bat
```

#### Step 2: Add API Key (1 min)

**Mac/Linux:**
```bash
nano .env
```

**Windows:**
```bash
notepad .env
```

Replace `your_openai_api_key_here` with your actual key:
```
OPENAI_API_KEY=sk-proj-your-actual-key
```

Save and close.

#### Step 3: Run (30 sec)

**Mac/Linux:**
```bash
source venv/bin/activate
streamlit run app.py
```

**Windows:**
```bash
venv\Scripts\activate
streamlit run app.py
```

Browser opens automatically at `http://localhost:8501`

**Test it** with a PDF, then deploy using Way 2 above.

---

## ❓ Something Not Working?

### "No API key found"
→ You didn't paste your key correctly. Make sure:
- No extra spaces
- Quotes are included: `"sk-proj-..."`
- Key starts with `sk-proj-` (OpenAI) or `sk-ant-` (Anthropic)

### "Module not found"
→ Run setup again:
```bash
bash setup.sh  # or setup.bat on Windows
```

### "Failed to extract text"
→ Your PDF is a scanned image. Try a different PDF with selectable text.

### App is slow
→ Normal! LLM takes 20-30 seconds per PDF.

### Still stuck?
→ Open `START_HERE.md` for the full detailed guide

---

## 💡 Quick Tips

**Cost**: ~$0.01-0.05 per PDF analyzed (very cheap!)

**Free hosting**: Streamlit Cloud is free for public repos

**Updates**: After deployment, just push to GitHub:
```bash
git add -A
git commit -m "Update"
git push origin claude/roofspec-matcher-app-8uuvR
```
App updates automatically in 2 minutes!

---

## ✅ Deployment Checklist

After deploying, test:
- [ ] App loads without errors
- [ ] Can upload PDFs
- [ ] "Analyze & Compare" button works
- [ ] See comparison table
- [ ] Can download CSV

**All working?** 🎉 Share your URL with others!

---

## 📞 Need More Hand-Holding?

- **Full beginner guide**: Open `START_HERE.md`
- **Interactive script**: Run `python deploy_helper.py`
- **Detailed docs**: Open `DEPLOYMENT.md`

---

**You got this! Pick a method above and go! 🚀**
