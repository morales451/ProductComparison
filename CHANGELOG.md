# RoofSpec Matcher - Changelog

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
