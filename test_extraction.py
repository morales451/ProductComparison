"""
Test utility for PDF text extraction and data parsing

This script allows you to test the PDF extraction and LLM parsing
functionality without running the full Streamlit application.

Usage:
    python test_extraction.py path/to/your/pdf/file.pdf
"""

import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import functions from main app
try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader

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

import os


def extract_text_from_file(pdf_path: str) -> str:
    """Extract text from a PDF file."""
    try:
        reader = PdfReader(pdf_path)
        text_content = []

        for page_num, page in enumerate(reader.pages):
            try:
                text = page.extract_text()
                if text:
                    text_content.append(f"--- Page {page_num + 1} ---\n{text}")
            except Exception as e:
                print(f"Warning: Error extracting text from page {page_num + 1}: {e}")
                continue

        full_text = "\n\n".join(text_content)
        return full_text

    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""


def get_llm_client():
    """Initialize LLM client."""
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if openai_key and OPENAI_AVAILABLE:
        return OpenAI(api_key=openai_key), "openai"
    elif anthropic_key and ANTHROPIC_AVAILABLE:
        return Anthropic(api_key=anthropic_key), "anthropic"
    else:
        return None, None


def parse_with_llm(text: str, doc_name: str, client, provider: str):
    """Parse technical data using LLM."""

    system_prompt = """You are a technical data extraction specialist for the roof coating and construction materials industry.

Your task is to extract technical specifications from roof coating product documentation. You MUST be flexible with terminology - different manufacturers use different wording for the same metrics.

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
→ Output as: "Thermal Emittance (Initial)", "Thermal Emittance (Aged)", or "Thermal Emittance"

**Solids variations:**
- "Volume Solids" = "Vol Solids" = "Solids by Volume" = "% Volume Solids" = "Percent Volume Solids"
- "Weight Solids" = "Wt Solids" = "Solids by Weight" = "% Weight Solids" = "Percent Weight Solids"
→ Output as: "Volume Solids" or "Weight Solids"

**Permeability variations:**
- "Permeability" = "Perm Rating" = "Perms" = "Water Vapor Permeability" = "Perm" = "Permeance"
→ Output as: "Permeability"

**INSTRUCTIONS:**

1. **SEMANTIC MATCHING**: Look for variations in word order, synonyms, and abbreviations.

2. **Initial vs Aged**: If a document says "Initial Solar Reflectance", output it as "Solar Reflectance (Initial)". If it just says "Solar Reflectance", output as "Solar Reflectance".

3. **Always include units**: Extract and include the units (psi, %, perms, etc.).

4. **Search thoroughly**: Check tables, bullet points, specifications sections, AND inline text.

5. **Return normalized JSON**: Use the standardized names from the variations list above as keys

6. **Missing data**: If you genuinely cannot find a metric, do NOT include it in the JSON.

Extract the data and return ONLY valid JSON. No additional text, explanation, or markdown formatting."""

    user_prompt = f"""Document Name: {doc_name}

Document Content:
{text[:15000]}

Extract all roof coating technical specifications from this document."""

    try:
        if provider == "openai":
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
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
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            response_text = response.content[0].text.strip()

        else:
            return None

        # Clean response
        response_text = response_text.replace("```json", "").replace("```", "").strip()

        # Parse JSON
        data = json.loads(response_text)
        return data

    except Exception as e:
        print(f"Error during LLM parsing: {e}")
        return None


def main():
    """Main test function."""
    if len(sys.argv) < 2:
        print("Usage: python test_extraction.py path/to/pdf/file.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]

    if not Path(pdf_path).exists():
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"Testing PDF Extraction: {pdf_path}")
    print(f"{'='*60}\n")

    # Step 1: Extract text
    print("Step 1: Extracting text from PDF...")
    text = extract_text_from_file(pdf_path)

    if not text:
        print("❌ Failed to extract text from PDF")
        sys.exit(1)

    print(f"✅ Extracted {len(text)} characters")
    print(f"\nFirst 500 characters of extracted text:")
    print("-" * 60)
    print(text[:500])
    print("-" * 60)

    # Step 2: Initialize LLM
    print("\nStep 2: Initializing LLM client...")
    client, provider = get_llm_client()

    if not client:
        print("❌ No LLM API key found. Please configure OPENAI_API_KEY or ANTHROPIC_API_KEY in .env")
        sys.exit(1)

    print(f"✅ Using {provider.upper()} for parsing")

    # Step 3: Parse with LLM
    print("\nStep 3: Parsing technical data with LLM...")
    doc_name = Path(pdf_path).name
    data = parse_with_llm(text, doc_name, client, provider)

    if not data:
        print("❌ Failed to parse data with LLM")
        sys.exit(1)

    print(f"✅ Extracted {len(data)} metrics")

    # Display results
    print(f"\n{'='*60}")
    print("EXTRACTED TECHNICAL DATA")
    print(f"{'='*60}\n")

    print(json.dumps(data, indent=2))

    print(f"\n{'='*60}")
    print(f"Test completed successfully!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
