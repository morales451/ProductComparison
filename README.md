# RoofSpec Matcher 🏗️

AI-Powered Roof Coating Specification Comparison Tool

---

## 🚀 Quick Start (For Beginners)

**New to deployment?** Start here:

- **📖 [START_HERE.md](START_HERE.md)** - Complete beginner guide (10 minutes)
- **⚡ [DEPLOY_NOW.md](DEPLOY_NOW.md)** - Copy/paste deployment (5 minutes)
- **🤖 Interactive helper**: Run `python deploy_helper.py`

**Experienced developers?** Continue reading below for technical details.

---

## Overview

RoofSpec Matcher is a Streamlit-based application that uses Large Language Models (LLMs) to intelligently extract and compare technical specifications from roof coating product documents. Upload a reference specification and multiple candidate product sheets to get an instant AI-powered comparison.

## Features

- **AI-Powered Extraction**: Uses OpenAI or Anthropic models to extract technical data from PDFs
- **Industry-Specific**: Tailored prompts for roof coating specifications
- **Comprehensive Metrics**: Analyzes 25+ technical metrics including:
  - Physical Properties (Elongation, Tensile Strength, Tear Strength)
  - Composition (Volume/Weight Solids, VOC Content)
  - Performance (Solar Reflectance, Permeability, Temperature Flexibility)
- **Visual Comparison Matrix**: Side-by-side comparison with missing data highlighted
- **AI Summary**: Get intelligent recommendations on the best product match
- **Export Capability**: Download comparison results as CSV

## Tech Stack

- **Python**: 3.10+
- **UI Framework**: Streamlit
- **PDF Parsing**: pypdf / pdfplumber
- **AI Models**: OpenAI GPT-4 or Anthropic Claude
- **Data Processing**: Pandas

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- An API key from OpenAI or Anthropic

### Step 1: Clone or Download

```bash
cd /path/to/RoofSpecMatcher
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Keys

Choose one of the following methods:

#### Option A: Using .env file (Recommended for local development)

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API key:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   # OR
   ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
   ```

#### Option B: Using Streamlit Secrets (Recommended for deployment)

1. Create `.streamlit/secrets.toml`:
   ```bash
   mkdir -p .streamlit
   ```

2. Add your key to `.streamlit/secrets.toml`:
   ```toml
   OPENAI_API_KEY = "sk-your-actual-key-here"
   # OR
   ANTHROPIC_API_KEY = "sk-ant-your-actual-key-here"
   ```

#### Getting API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/

**Note**: You only need ONE API key (either OpenAI or Anthropic). The app will automatically detect which is available.

## Usage

### Starting the Application

```bash
streamlit run app.py
```

The application will open in your default web browser (usually at `http://localhost:8501`).

### Using the Application

1. **Upload Reference Document**
   - In the sidebar, click "Upload the master specification document"
   - Select your reference/spec PDF file
   - This is the target specification you want to match

2. **Upload Candidate Documents**
   - Click "Upload candidate product documents"
   - Select one or more product specification PDFs
   - You can select multiple files at once

3. **Analyze & Compare**
   - Click the "Analyze & Compare" button
   - Wait while the AI processes your documents
   - Progress indicators will show the extraction status

4. **Review Results**
   - **Comparison Matrix**: View side-by-side comparison of all metrics
   - **Missing Data**: Red-highlighted cells indicate where candidates lack reference metrics
   - **AI Summary**: Read the AI-generated analysis and recommendations
   - **Download**: Export the comparison matrix as CSV for further analysis

## Application Structure

```
RoofSpecMatcher/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # API key template
├── .env                  # Your actual API keys (git-ignored)
├── README.md             # This file
└── .streamlit/
    └── secrets.toml      # Alternative API key storage (git-ignored)
```

## Key Metrics Analyzed

The application is specifically designed to extract roof coating specifications:

### Physical Properties
- Elongation (Initial, Aged, at Break)
- Tensile Strength (Initial, Aged)
- Tear Strength
- Adhesion

### Composition & Application
- Volume Solids & Weight Solids
- Viscosity
- Coverage/Application Rate
- Dry Time
- VOC Content

### Performance Metrics
- Solar Reflectance & Thermal Emittance
- SRI (Solar Reflectance Index)
- Permeability / Perm Rating
- Low Temperature Flexibility
- Ponding Water Resistance
- UV Resistance
- Crack Bridging
- Water Absorption

## How It Works

1. **Text Extraction**: The app uses pypdf to extract text from uploaded PDFs

2. **AI Processing**: Each document is sent to the LLM with a specialized prompt that:
   - Identifies roof coating specific metrics
   - Normalizes variations in metric names
   - Preserves units (e.g., "500 psi" not just "500")
   - Returns structured JSON data

3. **Comparison**: Data is aggregated into a Pandas DataFrame showing:
   - Reference specifications in one column
   - Each candidate in subsequent columns
   - Missing values highlighted in red

4. **AI Analysis**: A second LLM call generates a summary that:
   - Identifies the best match(es)
   - Highlights critical differences
   - Provides actionable recommendations

## Troubleshooting

### No text extracted from PDF

**Cause**: The PDF might be image-based (scanned document)

**Solution**:
- Use OCR software to convert the PDF to text first
- Or use a tool like Adobe Acrobat to export as text

### API Key Errors

**Cause**: API key not configured or invalid

**Solution**:
- Verify your .env file or secrets.toml is set up correctly
- Check that your API key is valid and has credits
- Ensure you've copied the key correctly (no extra spaces)

### Import Errors

**Cause**: Missing dependencies

**Solution**:
```bash
pip install -r requirements.txt --upgrade
```

### Model Not Found Errors

**Cause**: Using outdated model names

**Solution**: The app uses `gpt-4o-mini` and `claude-3-5-sonnet-20241022`. These are current as of January 2025, but may need updating in the future.

## Customization

### Adding More Metrics

Edit the `ROOF_COATING_METRICS` list in `app.py` (lines 59-88) to add industry-specific metrics you want to track.

### Changing LLM Models

Modify the model names in:
- Line 271: `model="gpt-4o-mini"` for OpenAI
- Line 282: `model="claude-3-5-sonnet-20241022"` for Anthropic

### Adjusting the System Prompt

Edit `SYSTEM_PROMPT` (lines 90-155) to refine how the AI extracts data from your documents.

## Best Practices

1. **PDF Quality**: Use text-based PDFs, not scanned images
2. **Document Structure**: PDFs with clear tables and sections work best
3. **Naming Convention**: Use descriptive file names for easier identification
4. **API Costs**: Be mindful that each document analysis uses API credits
5. **Data Validation**: Always verify AI-extracted data against source documents

## Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your repository
4. Add API keys in the Streamlit Cloud secrets manager
5. Deploy!

### Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t roofspec-matcher .
docker run -p 8501:8501 --env-file .env roofspec-matcher
```

## License

This project is provided as-is for educational and commercial use.

## Support

For issues, questions, or contributions, please open an issue in the project repository.

## Credits

Built with:
- [Streamlit](https://streamlit.io/)
- [OpenAI](https://openai.com/)
- [Anthropic](https://www.anthropic.com/)
- [pypdf](https://pypdf.readthedocs.io/)

---

**Made with ❤️ for the Roofing Industry**
