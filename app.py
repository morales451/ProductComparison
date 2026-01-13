"""
RoofSpec Matcher - AI-Powered Roof Coating Specification Comparison Tool

This Streamlit application compares technical specifications from roof coating PDFs
using LLM-based extraction to identify the best candidate matches.
"""

import streamlit as st
import pandas as pd
import json
import os
from io import BytesIO
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv

# PDF parsing libraries
try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader

# LLM libraries
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="RoofSpec Matcher",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .highlight-missing {
        background-color: #ffcccc !important;
    }
    .stDataFrame {
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# ===================== CONFIGURATION =====================

# Roof coating specific metrics to extract
ROOF_COATING_METRICS = [
    "Elongation (Initial)",
    "Elongation (Aged)",
    "Elongation at Break",
    "Tensile Strength",
    "Tensile Strength (Initial)",
    "Tensile Strength (Aged)",
    "Volume Solids",
    "Weight Solids",
    "Permeability",
    "Perm Rating",
    "Solar Reflectance",
    "Thermal Emittance",
    "SRI (Solar Reflectance Index)",
    "Viscosity",
    "Low Temperature Flexibility",
    "Temperature Flexibility",
    "Tear Strength",
    "Adhesion",
    "Dry Time",
    "Coverage Rate",
    "Application Rate",
    "VOC Content",
    "Weathering",
    "Water Absorption",
    "Ponding Water Resistance",
    "UV Resistance",
    "Crack Bridging",
    "Reflectivity",
    "Emissivity"
]

SYSTEM_PROMPT = """You are a technical data extraction specialist for the roof coating and construction materials industry.

Your task is to extract technical specifications from roof coating documents. You MUST be flexible with terminology - different manufacturers use different wording for the same metrics.

**IMPORTANT: This tool handles TWO types of documents:**

1. **PRODUCT DATA SHEETS** - Actual specifications (e.g., "Tensile Strength: 500 psi")
2. **JOB SPECIFICATIONS** - Required minimums (e.g., "Minimum tensile strength of 300 psi" or "shall meet or exceed 300 psi")

**CRITICAL: FLEXIBLE MATCHING RULES**

You must use SEMANTIC MATCHING, not exact text matching. Look for the MEANING of metrics, not exact phrases.

**TERMINOLOGY VARIATIONS - Treat these as THE SAME metric:**

**Elongation variations:**
- "Elongation (Initial)" = "Initial Elongation" = "Initial Percent Elongation" = "Elongation - Initial" = "Initial % Elongation"
- "Elongation (Aged)" = "Aged Elongation" = "Aged Percent Elongation" = "Elongation - Aged"
- "Elongation at Break" = "Elongation %" = "Percent Elongation" = "% Elongation"
→ Output as: "Elongation (Initial)", "Elongation (Aged)", or "Elongation at Break"

**Tensile Strength variations:**
- "Tensile Strength (Initial)" = "Initial Tensile Strength" = "Initial Tensile" = "Tensile - Initial"
- "Tensile Strength (Aged)" = "Aged Tensile Strength" = "Aged Tensile" = "Tensile - Aged"
- "Tensile Strength" = "Tensile" = "Ultimate Tensile Strength"
→ Output as: "Tensile Strength (Initial)", "Tensile Strength (Aged)", or "Tensile Strength"

**Solar Reflectance variations:**
- "Solar Reflectance (Initial)" = "Initial Solar Reflectance" = "Solar Reflectance - Initial" = "Initial Reflectance"
- "Solar Reflectance (Aged)" = "Aged Solar Reflectance" = "Solar Reflectance - Aged" = "Aged Reflectance"
- "Solar Reflectance" = "Reflectance" = "Solar Reflectivity" = "Reflectivity (Solar)"
→ Output as: "Solar Reflectance (Initial)", "Solar Reflectance (Aged)", or "Solar Reflectance"

**Thermal Emittance variations:**
- "Thermal Emittance" = "Emittance" = "Emissivity" = "Thermal Emissivity" = "IR Emittance"
- "Thermal Emittance (Initial)" = "Initial Emittance" = "Initial Thermal Emittance"
- "Thermal Emittance (Aged)" = "Aged Emittance" = "Aged Thermal Emittance"
→ Output as: "Thermal Emittance (Initial)", "Thermal Emittance (Aged)", or "Thermal Emittance"

**Solids variations:**
- "Volume Solids" = "Vol Solids" = "Solids by Volume" = "% Volume Solids" = "Percent Volume Solids"
- "Weight Solids" = "Wt Solids" = "Solids by Weight" = "% Weight Solids" = "Percent Weight Solids"
→ Output as: "Volume Solids" or "Weight Solids"

**Permeability variations:**
- "Permeability" = "Perm Rating" = "Perms" = "Water Vapor Permeability" = "Perm" = "Permeance"
→ Output as: "Permeability"

**Temperature Flexibility variations:**
- "Low Temperature Flexibility" = "Temperature Flexibility" = "Low Temp Flexibility" = "Cold Temperature Flexibility" = "Flexibility at Low Temp"
→ Output as: "Low Temperature Flexibility"

**Tear Strength variations:**
- "Tear Strength" = "Tear Resistance" = "Tear" = "Die C Tear Strength"
→ Output as: "Tear Strength"

**Adhesion variations:**
- "Adhesion" = "Adhesion Strength" = "Bond Strength" = "Peel Adhesion"
→ Output as: "Adhesion"

**Viscosity variations:**
- "Viscosity" = "Viscosity (KU)" = "KU Viscosity" = "Brookfield Viscosity"
→ Output as: "Viscosity"

**VOC variations:**
- "VOC Content" = "VOC" = "VOC Level" = "Volatile Organic Compounds"
→ Output as: "VOC Content"

**Coverage/Application variations:**
- "Coverage Rate" = "Application Rate" = "Coverage" = "Spread Rate" = "Sq Ft per Gallon"
→ Output as: "Coverage Rate"

**Dry Time variations:**
- "Dry Time" = "Drying Time" = "Cure Time" = "Curing Time" = "Time to Dry"
→ Output as: "Dry Time"

**Ponding Water variations:**
- "Ponding Water Resistance" = "Ponding Water" = "Standing Water Resistance" = "Water Ponding"
→ Output as: "Ponding Water Resistance"

**SRI variations:**
- "SRI" = "Solar Reflectance Index" = "Solar Reflective Index"
→ Output as: "SRI"

**HANDLING JOB SPECIFICATIONS (Requirement Documents):**

Job specifications use REQUIREMENT LANGUAGE instead of stating actual values. You MUST recognize and extract these properly.

**Requirement Keywords to Recognize:**
- "minimum" / "min" / "at least" / "not less than"
- "maximum" / "max" / "not more than" / "not to exceed"
- "shall be" / "must be" / "should be"
- "meets or exceeds" / "equal to or greater than"
- "complies with" / "in accordance with"

**How to Extract from Job Specs:**

1. **Minimum Requirements** - Extract with "min" prefix:
   - "Minimum tensile strength of 300 psi" → Output: "Tensile Strength: min 300 psi"
   - "Solar reflectance shall be at least 0.80" → Output: "Solar Reflectance: min 0.80"
   - "Elongation not less than 400%" → Output: "Elongation: min 400%"

2. **Maximum Requirements** - Extract with "max" prefix:
   - "VOC content not to exceed 50 g/L" → Output: "VOC Content: max 50 g/L"
   - "Maximum permeability of 0.5 perms" → Output: "Permeability: max 0.5 perms"

3. **Exact Requirements** - Extract without prefix:
   - "Solar reflectance shall be 0.85" → Output: "Solar Reflectance: 0.85"

4. **Referenced Products** - Extract if mentioned:
   - "Use [Manufacturer X Product Y] or approved equal"
   - Look for metrics associated with that product name in the document

**Examples of Job Spec Extraction:**

Input text: "The coating shall have a minimum initial tensile strength of 300 psi and minimum initial elongation of 500%."
Output JSON:
{
  "Tensile Strength (Initial)": "min 300 psi",
  "Elongation (Initial)": "min 500%"
}

Input text: "Solar reflectance not less than 0.80, thermal emittance of at least 0.85"
Output JSON:
{
  "Solar Reflectance": "min 0.80",
  "Thermal Emittance": "min 0.85"
}

**INSTRUCTIONS:**

1. **SEMANTIC MATCHING**: Look for variations in word order, synonyms, and abbreviations. If you see ANY variation of a metric name, extract it and normalize to the standard name above.

2. **Initial vs Aged**: If a document says "Initial Solar Reflectance", output it as "Solar Reflectance (Initial)". If it just says "Solar Reflectance", output as "Solar Reflectance". Keep Initial/Aged separate when specified.

3. **Always include units**: Extract and include the units (psi, %, perms, etc.). If units are in the header or label, include them with the value.

4. **Handle ranges**: Keep ranges intact: "50-60%" or "400-600 psi"

5. **Detect document type automatically**:
   - If you see requirement language ("minimum", "shall be", "at least"), it's a JOB SPEC → use "min"/"max" prefixes
   - If you see actual values without requirement language, it's a PRODUCT DATA SHEET → use values as-is
   - You may encounter BOTH types in one document!

6. **Search thoroughly**: Check tables, bullet points, specifications sections, AND inline text. Requirements might be in paragraphs like "The coating shall have a minimum tensile strength of 300 psi" or in tables.

7. **Return normalized JSON**: Use the standardized names from the variations list above as keys

   Product Data Sheet Example:
   {"Tensile Strength (Initial)": "500 psi", "Elongation (Initial)": "300%", "Solar Reflectance": "0.85"}

   Job Specification Example:
   {"Tensile Strength (Initial)": "min 300 psi", "Elongation (Initial)": "min 400%", "Solar Reflectance": "min 0.80"}

8. **Missing data**: If you genuinely cannot find a metric after thorough searching, do NOT include it in the JSON.

9. **Be flexible but accurate**: Extract the value that's actually there, but normalize the metric name for consistency. Preserve requirement indicators (min/max) when present.

Extract the data and return ONLY valid JSON. No additional text, explanation, or markdown formatting."""

# ===================== HELPER FUNCTIONS =====================

def get_llm_client() -> Tuple[Optional[object], str]:
    """
    Initialize and return the appropriate LLM client based on available API keys.
    Returns: (client_object, provider_name)
    """
    # Check Streamlit secrets first
    openai_key = st.secrets.get("OPENAI_API_KEY") if hasattr(st, 'secrets') and "OPENAI_API_KEY" in st.secrets else None
    anthropic_key = st.secrets.get("ANTHROPIC_API_KEY") if hasattr(st, 'secrets') and "ANTHROPIC_API_KEY" in st.secrets else None

    # Fallback to environment variables
    if not openai_key:
        openai_key = os.getenv("OPENAI_API_KEY")
    if not anthropic_key:
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    # Try OpenAI first
    if openai_key and OPENAI_AVAILABLE:
        try:
            client = OpenAI(api_key=openai_key)
            return client, "openai"
        except Exception as e:
            st.warning(f"Failed to initialize OpenAI client: {e}")

    # Try Anthropic
    if anthropic_key and ANTHROPIC_AVAILABLE:
        try:
            client = Anthropic(api_key=anthropic_key)
            return client, "anthropic"
        except Exception as e:
            st.warning(f"Failed to initialize Anthropic client: {e}")

    return None, ""


def extract_text(pdf_file) -> str:
    """
    Extract text content from a PDF file.

    Args:
        pdf_file: Uploaded PDF file object (BytesIO or file-like object)

    Returns:
        str: Extracted text content
    """
    try:
        # Reset file pointer to beginning
        pdf_file.seek(0)

        # Create PDF reader
        reader = PdfReader(pdf_file)

        # Extract text from all pages
        text_content = []
        for page_num, page in enumerate(reader.pages):
            try:
                text = page.extract_text()
                if text:
                    text_content.append(f"--- Page {page_num + 1} ---\n{text}")
            except Exception as e:
                st.warning(f"Error extracting text from page {page_num + 1}: {e}")
                continue

        full_text = "\n\n".join(text_content)

        if not full_text.strip():
            st.error("No text could be extracted from the PDF. It might be image-based.")
            return ""

        return full_text

    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""


def parse_technical_data(text: str, doc_name: str, client, provider: str) -> Dict[str, str]:
    """
    Parse technical data from extracted text using LLM.

    Args:
        text: Extracted text from PDF
        doc_name: Name of the document (for reference)
        client: LLM client object
        provider: "openai" or "anthropic"

    Returns:
        Dict[str, str]: Dictionary of metric names to values
    """
    if not text.strip():
        return {}

    user_prompt = f"""Document Name: {doc_name}

Document Content:
{text[:15000]}

Extract all roof coating technical specifications from this document and return them as a JSON object."""

    try:
        if provider == "openai":
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            response_text = response.choices[0].message.content.strip()

        elif provider == "anthropic":
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                temperature=0.1,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            response_text = response.content[0].text.strip()

        else:
            st.error("Unknown LLM provider")
            return {}

        # Clean up response text (remove markdown code blocks if present)
        response_text = response_text.replace("```json", "").replace("```", "").strip()

        # Parse JSON
        data = json.loads(response_text)

        return data

    except json.JSONDecodeError as e:
        st.error(f"Failed to parse JSON from LLM response for {doc_name}: {e}")
        st.text("Response received:")
        st.code(response_text[:500])
        return {}

    except Exception as e:
        st.error(f"Error calling LLM for {doc_name}: {e}")
        return {}


def create_comparison_matrix(reference_data: Dict[str, str],
                            candidate_data: Dict[str, Dict[str, str]],
                            reference_name: str) -> pd.DataFrame:
    """
    Create a comparison matrix DataFrame from reference and candidate data.

    Args:
        reference_data: Dictionary of metrics from reference document
        candidate_data: Dictionary of {doc_name: metrics_dict} for candidates
        reference_name: Name of the reference document

    Returns:
        pd.DataFrame: Comparison matrix with metrics as rows
    """
    # Collect all unique metrics
    all_metrics = set(reference_data.keys())
    for candidate_metrics in candidate_data.values():
        all_metrics.update(candidate_metrics.keys())

    # Sort metrics alphabetically
    all_metrics = sorted(list(all_metrics))

    # Build the dataframe
    df_data = {"Metric": all_metrics}

    # Add reference column
    df_data[f"Reference: {reference_name}"] = [
        reference_data.get(metric, "") for metric in all_metrics
    ]

    # Add candidate columns
    for candidate_name, candidate_metrics in candidate_data.items():
        df_data[f"Candidate: {candidate_name}"] = [
            candidate_metrics.get(metric, "") for metric in all_metrics
        ]

    df = pd.DataFrame(df_data)

    return df


def highlight_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply styling to highlight missing values in the comparison matrix.

    Args:
        df: Comparison DataFrame

    Returns:
        Styled DataFrame
    """
    def highlight_cells(row):
        reference_val = row.iloc[1]  # First column after "Metric"
        styles = [''] * len(row)

        # Don't highlight the metric name or reference column
        styles[0] = ''
        styles[1] = ''

        # Highlight candidate columns where value is missing but reference exists
        if reference_val and reference_val.strip():
            for i in range(2, len(row)):
                if not row.iloc[i] or not row.iloc[i].strip():
                    styles[i] = 'background-color: #ffcccc'

        return styles

    return df.style.apply(highlight_cells, axis=1)


def generate_ai_summary(reference_name: str,
                       reference_data: Dict[str, str],
                       candidate_data: Dict[str, Dict[str, str]],
                       client,
                       provider: str) -> str:
    """
    Generate an AI summary comparing candidates to the reference.

    Args:
        reference_name: Name of reference document
        reference_data: Reference metrics
        candidate_data: Dictionary of candidate metrics
        client: LLM client
        provider: LLM provider name

    Returns:
        str: AI-generated summary
    """
    summary_prompt = f"""You are analyzing roof coating product specifications to find the best match.

**Reference Specification ({reference_name}):**
{json.dumps(reference_data, indent=2)}

**Candidate Products:**
"""

    for candidate_name, candidate_metrics in candidate_data.items():
        summary_prompt += f"\n**{candidate_name}:**\n{json.dumps(candidate_metrics, indent=2)}\n"

    summary_prompt += """

Based on this comparison, provide a concise summary (2-3 paragraphs) that:

1. Identifies which candidate product(s) most closely match the reference specification
2. Highlights any critical metrics where candidates fall short
3. Notes any candidates that exceed the reference in important areas
4. Provides a recommendation on the best overall match

Focus on the most important roof coating metrics like tensile strength, elongation, solar reflectance, and permeability."""

    try:
        if provider == "openai":
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a roof coating technical specialist providing product comparison analysis."},
                    {"role": "user", "content": summary_prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            return response.choices[0].message.content.strip()

        elif provider == "anthropic":
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0.3,
                system="You are a roof coating technical specialist providing product comparison analysis.",
                messages=[
                    {"role": "user", "content": summary_prompt}
                ]
            )
            return response.content[0].text.strip()

        else:
            return "Unable to generate summary: Unknown LLM provider"

    except Exception as e:
        return f"Error generating summary: {e}"


# ===================== MAIN APPLICATION =====================

def main():
    """Main application function"""

    # Header
    st.markdown('<h1 class="main-header">🏗️ RoofSpec Matcher</h1>', unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <p style="font-size: 1.1rem; color: #555;">
                AI-Powered Roof Coating Specification Comparison Tool
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Initialize LLM client
    client, provider = get_llm_client()

    if not client:
        st.error("⚠️ No LLM API key found!")
        st.info("""
            Please configure your API key:

            **Option 1: Environment Variable**
            - Create a `.env` file with: `OPENAI_API_KEY=your_key` or `ANTHROPIC_API_KEY=your_key`

            **Option 2: Streamlit Secrets**
            - Add to `.streamlit/secrets.toml`:
            ```
            OPENAI_API_KEY = "your_key"
            # or
            ANTHROPIC_API_KEY = "your_key"
            ```
        """)
        return

    st.success(f"✅ Using {provider.upper()} for AI processing")

    # Sidebar for file uploads
    st.sidebar.header("📁 Document Upload")

    # Reference document upload
    st.sidebar.subheader("1️⃣ Reference/Spec Document")
    reference_file = st.sidebar.file_uploader(
        "Upload the master specification document",
        type=['pdf'],
        key="reference",
        help="Upload a product data sheet OR job specification with requirements (e.g., 'minimum 300 psi')"
    )

    # Candidate documents upload
    st.sidebar.subheader("2️⃣ Candidate Documents")
    candidate_files = st.sidebar.file_uploader(
        "Upload candidate product documents",
        type=['pdf'],
        accept_multiple_files=True,
        key="candidates",
        help="Upload one or more product spec sheets to compare against the reference"
    )

    # Analysis button
    analyze_button = st.sidebar.button("🔍 Analyze & Compare", type="primary", use_container_width=True)

    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
        ### 📊 Key Metrics Analyzed
        - Elongation (Initial & Aged)
        - Tensile Strength
        - Volume & Weight Solids
        - Permeability / Perm Rating
        - Solar Reflectance & Thermal Emittance
        - Viscosity
        - Low Temperature Flexibility
        - And more...
    """)

    # Main content area
    if analyze_button:
        if not reference_file:
            st.error("❌ Please upload a reference document")
            return

        if not candidate_files or len(candidate_files) == 0:
            st.error("❌ Please upload at least one candidate document")
            return

        # Processing section
        st.header("⚙️ Processing Documents")

        # Extract reference data
        with st.spinner(f"Extracting data from reference document: {reference_file.name}..."):
            reference_text = extract_text(reference_file)
            if not reference_text:
                st.error("Failed to extract text from reference document")
                return

            reference_data = parse_technical_data(
                reference_text,
                reference_file.name,
                client,
                provider
            )

        if not reference_data:
            st.warning("⚠️ No technical data extracted from reference document")
        else:
            st.success(f"✅ Extracted {len(reference_data)} metrics from reference document")

        # Extract candidate data
        candidate_data = {}

        progress_bar = st.progress(0)
        for idx, candidate_file in enumerate(candidate_files):
            with st.spinner(f"Processing candidate {idx+1}/{len(candidate_files)}: {candidate_file.name}..."):
                candidate_text = extract_text(candidate_file)
                if candidate_text:
                    metrics = parse_technical_data(
                        candidate_text,
                        candidate_file.name,
                        client,
                        provider
                    )
                    candidate_data[candidate_file.name] = metrics
                    st.success(f"✅ Extracted {len(metrics)} metrics from {candidate_file.name}")
                else:
                    st.error(f"❌ Failed to extract text from {candidate_file.name}")
                    candidate_data[candidate_file.name] = {}

            progress_bar.progress((idx + 1) / len(candidate_files))

        st.success("🎉 All documents processed!")

        # Create comparison matrix
        st.header("📊 Comparison Matrix")

        if not candidate_data:
            st.error("No candidate data available for comparison")
            return

        df = create_comparison_matrix(
            reference_data,
            candidate_data,
            reference_file.name
        )

        # Display styled dataframe
        styled_df = highlight_missing_values(df)
        st.dataframe(styled_df, use_container_width=True, height=600)

        # Download button for CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Comparison as CSV",
            data=csv,
            file_name="roofspec_comparison.csv",
            mime="text/csv"
        )

        # AI Summary section
        st.header("🤖 AI Analysis Summary")

        with st.spinner("Generating AI summary..."):
            summary = generate_ai_summary(
                reference_file.name,
                reference_data,
                candidate_data,
                client,
                provider
            )

        st.markdown("### Analysis Results")
        st.info(summary)

        # Additional insights
        st.header("📈 Quick Stats")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Reference Metrics", len(reference_data))

        with col2:
            avg_candidate_metrics = sum(len(d) for d in candidate_data.values()) / len(candidate_data)
            st.metric("Avg. Candidate Metrics", f"{avg_candidate_metrics:.1f}")

        with col3:
            st.metric("Candidates Analyzed", len(candidate_data))

    else:
        # Welcome message
        st.info("""
            ### 👋 Welcome to RoofSpec Matcher!

            This tool helps you compare roof coating product specifications against a reference document.

            **Supports TWO use cases:**
            - **Product vs Product**: Compare product data sheets against each other
            - **Job Spec vs Products**: Upload a job specification (with "minimum" requirements) and see which products meet or exceed those specs

            **How to use:**
            1. Upload your reference document (product data sheet OR job spec) in the sidebar
            2. Upload one or more candidate product documents
            3. Click "Analyze & Compare" to start the AI-powered analysis

            The tool will extract technical specifications and create a detailed comparison matrix,
            highlighting any missing data and providing AI-powered insights on the best match.
        """)

        # Show example metrics
        st.markdown("### 🎯 Example Metrics We Analyze")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
                **Physical Properties:**
                - Elongation (Initial & Aged)
                - Tensile Strength
                - Tear Strength
                - Adhesion
            """)

        with col2:
            st.markdown("""
                **Performance Metrics:**
                - Solar Reflectance
                - Thermal Emittance
                - Permeability/Perm Rating
                - Low Temperature Flexibility
            """)


if __name__ == "__main__":
    main()
