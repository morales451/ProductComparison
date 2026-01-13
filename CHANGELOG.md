# RoofSpec Matcher - Changelog

## Version 1.2.0 (2026-01-13) - Job Specification Support

### 🎯 Major New Feature: Job Specification Extraction

**New Capability:** The tool now extracts requirements from job specifications in addition to product data sheets!

**Use Cases Enabled:**
- ✅ Upload a job spec as reference → See which products meet or exceed requirements
- ✅ Compare products against "minimum" and "maximum" requirements
- ✅ Verify "or equal" product substitutions
- ✅ Quick qualification checks for bidding

### 🔧 Changes

#### Enhanced Extraction for Two Document Types

**1. Product Data Sheets (Original)**
- Extracts actual values: "Tensile Strength: 500 psi"
- Output: `{"Tensile Strength": "500 psi"}`

**2. Job Specifications (NEW)**
- Extracts requirements: "Minimum tensile strength of 300 psi"
- Output: `{"Tensile Strength": "min 300 psi"}`
- Recognizes requirement language: "minimum", "shall be", "at least", "not less than", "not to exceed"

#### Requirement Keywords Supported

**Minimum Requirements:**
- "minimum" / "min" / "at least" / "not less than"
- "shall be" / "must be" / "should be"
- "meets or exceeds"

**Maximum Requirements:**
- "maximum" / "max" / "not more than" / "not to exceed"

#### Examples

**Input:** "The coating shall have a minimum initial tensile strength of 300 psi"
**Output:** `{"Tensile Strength (Initial)": "min 300 psi"}`

**Input:** "Solar reflectance not less than 0.80"
**Output:** `{"Solar Reflectance": "min 0.80"}`

**Input:** "VOC content not to exceed 50 g/L"
**Output:** `{"VOC Content": "max 50 g/L"}`

### 📝 Technical Details

**Files Modified:**
- `app.py` - Added job spec handling to SYSTEM_PROMPT (lines 109-232)
- `test_extraction.py` - Added abbreviated job spec handling
- UI updated to mention both document types

**New Files:**
- `JOB_SPEC_GUIDE.md` - Comprehensive guide for using job specifications (91KB)

**Key Prompt Changes:**
- Added "HANDLING JOB SPECIFICATIONS" section
- Automatic document type detection
- Requirement indicator preservation (min/max prefixes)
- Instructions for extracting from requirement language
- Examples of both document types

### 🎯 Usage

**Compare Products Against Job Spec:**
1. Upload job specification PDF as Reference
2. Upload product data sheets as Candidates
3. Click "Analyze & Compare"
4. See which products meet minimum requirements

**Reading Results:**
- **Job Spec**: "min 300 psi"
- **Product A**: "500 psi" ✅ (Exceeds minimum)
- **Product B**: "280 psi" ❌ (Below minimum)
- **Product C**: (empty) ❓ (No data)

### 📊 Impact

**Before v1.2:**
- Could only compare product data sheets
- Job specifications couldn't be processed
- Had to manually check requirements

**After v1.2:**
- ✅ Automatic requirement extraction
- ✅ Clear min/max indicators
- ✅ Side-by-side requirement vs actual comparison
- ✅ AI summary identifies compliance gaps

### 🧪 Testing

Users should test with:
1. A job specification with "minimum" requirements
2. Multiple product data sheets
3. Verify the comparison shows requirements vs actual values

### 📚 Documentation

See `JOB_SPEC_GUIDE.md` for:
- Complete usage instructions
- Common scenarios and workflows
- Tips for best results
- FAQ and troubleshooting

---

## Version 1.1.0 (2026-01-13) - Flexible Terminology Matching

### 🎯 Major Improvement: Semantic Matching

**Problem Solved:** The AI was too strict with terminology and missed metrics when different manufacturers used slightly different wording.

**Examples of Issues Fixed:**
- "Elongation (Initial)" vs "Initial Percent Elongation" → Now recognized as the same
- "Solar Reflectance Initial" vs "Solar Reflectance" → Now handled correctly
- "Initial Tensile Strength" vs "Tensile Strength (Initial)" → Now matched

### 🔧 Changes

#### Enhanced System Prompt
- **Before:** Simple normalization with 3 examples
- **After:** Comprehensive semantic matching with 80+ terminology variations

#### Specific Improvements

1. **Elongation Matching**
   - Now recognizes: "Initial Elongation", "Initial Percent Elongation", "Elongation - Initial", "Initial % Elongation"
   - Properly distinguishes Initial vs Aged vs at Break

2. **Solar Reflectance Matching**
   - Handles: "Initial Solar Reflectance", "Solar Reflectance - Initial", "Initial Reflectance"
   - Normalizes to standard: "Solar Reflectance (Initial)" or "Solar Reflectance"

3. **Tensile Strength Matching**
   - Recognizes: "Initial Tensile Strength", "Initial Tensile", "Tensile - Initial"
   - Outputs as: "Tensile Strength (Initial)"

4. **Added Variations For:**
   - Thermal Emittance / Emissivity
   - Volume Solids / Weight Solids
   - Permeability / Perm Rating / Perms
   - Temperature Flexibility
   - Tear Strength / Tear Resistance
   - Coverage Rate / Application Rate
   - And 10+ more metrics

### 📝 Technical Details

**Files Modified:**
- `app.py` - Updated SYSTEM_PROMPT (lines 105-203)
- `test_extraction.py` - Updated parse_with_llm() prompt

**Key Prompt Changes:**
- Added "SEMANTIC MATCHING" instruction
- Provided 80+ terminology variations
- Explicit normalization rules for each metric
- Better handling of Initial/Aged qualifiers
- More thorough search instructions

**Backward Compatibility:**
- ✅ Existing extractions still work
- ✅ Output format unchanged (JSON)
- ✅ API usage unchanged

### 🎯 Expected Results

With this update, the app should now successfully extract metrics even when:
- Word order is different ("Initial Elongation" vs "Elongation Initial")
- Abbreviations are used ("Vol Solids" vs "Volume Solids")
- Synonyms are present ("Reflectivity" vs "Reflectance")
- Formatting varies ("Elongation (Initial)" vs "Elongation - Initial")

### 🧪 Testing Recommendations

After deploying this update:
1. Re-run your previous comparisons
2. Check if previously missing metrics are now captured
3. Verify that metric names are normalized consistently

### 📊 Impact

**User Reported Issues:**
- ❌ Before: Missing "Initial Percent Elongation" when looking for "Elongation (Initial)"
- ✅ After: Successfully extracts and normalizes

- ❌ Before: Missing "Solar Reflectance" when expecting "Solar Reflectance Initial"
- ✅ After: Correctly identifies and extracts both variations

---

## Version 1.0.0 (2026-01-13) - Initial Release

- Complete Streamlit application
- AI-powered PDF extraction
- Support for OpenAI and Anthropic
- Comparison matrix with highlighting
- AI summary generation
- CSV export
- Comprehensive deployment documentation

---

## Upgrade Instructions

### For Streamlit Cloud Users:
1. Changes auto-deploy from GitHub (2 minutes)
2. No action needed - just refresh your app!

### For Local Development:
```bash
git pull origin claude/roofspec-matcher-app-8uuvR
# Restart your app
```

### For Docker Users:
```bash
git pull origin claude/roofspec-matcher-app-8uuvR
docker-compose down
docker-compose up -d --build
```

---

## Future Improvements

Planned enhancements:
- [ ] Add support for scanned/image-based PDFs (OCR)
- [ ] Batch processing for multiple comparisons
- [ ] Save comparison history
- [ ] Custom metric definitions
- [ ] Export to Excel with formatting
- [ ] Comparison scoring system

---

**Have suggestions or found an issue?** Open an issue in the GitHub repository!
