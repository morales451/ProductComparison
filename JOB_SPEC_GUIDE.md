# Using Job Specifications with RoofSpec Matcher

## Overview

RoofSpec Matcher now supports **TWO types of comparisons**:

1. **Product vs Product** - Compare actual product data sheets
2. **Job Spec vs Products** - See which products meet or exceed job requirements

This guide explains how to use job specifications effectively.

---

## What is a Job Specification?

A **job specification** (or construction specification) is a document that lists **minimum requirements** for a project, not actual product values.

### Examples:

**Job Specification Language:**
- "Minimum tensile strength of 300 psi"
- "Solar reflectance shall be at least 0.80"
- "Elongation not less than 400%"
- "Use [Product XYZ] or approved equal"

**Product Data Sheet Language:**
- "Tensile Strength: 500 psi"
- "Solar Reflectance: 0.85"
- "Elongation: 425%"

---

## Use Cases

### Use Case 1: Check if Your Product Meets a Job Spec

**Scenario:** You receive a job specification from a contractor and need to know if your product qualifies.

**Steps:**
1. Upload the **job specification PDF** as the Reference document
2. Upload **your product data sheet** as a Candidate
3. Click "Analyze & Compare"

**What You'll See:**

| Metric | Job Spec Requirement | Your Product |
|--------|---------------------|--------------|
| Tensile Strength (Initial) | min 300 psi | 500 psi ✅ |
| Elongation (Initial) | min 400% | 425% ✅ |
| Solar Reflectance | min 0.80 | 0.85 ✅ |

**Result:** You can clearly see your product meets or exceeds all requirements!

---

### Use Case 2: Compare Multiple Products Against a Job Spec

**Scenario:** You're a contractor with a job spec, and you want to see which manufacturer products qualify.

**Steps:**
1. Upload the **job specification PDF** as the Reference
2. Upload **multiple product data sheets** as Candidates
3. Click "Analyze & Compare"

**What You'll See:**

| Metric | Job Requirement | Product A | Product B | Product C |
|--------|----------------|-----------|-----------|-----------|
| Tensile Strength (Initial) | min 300 psi | 500 psi ✅ | 280 psi ❌ | 350 psi ✅ |
| Solar Reflectance | min 0.80 | 0.85 ✅ | 0.75 ❌ | 0.82 ✅ |

**Result:** Products A and C meet the requirements, Product B does not!

---

### Use Case 3: Verify "Or Equal" Substitutions

**Scenario:** Job spec says "Use Brand X Product Y or approved equal"

**Steps:**
1. Upload the **job specification** as Reference
   - The AI will extract requirements mentioned in the spec
2. Upload **Brand X Product Y data sheet** as first Candidate
3. Upload **your alternative product** as second Candidate
4. Click "Analyze & Compare"

**What You'll See:**
- Side-by-side comparison of requirements
- See if your product truly matches or exceeds the specified product
- AI summary highlighting differences

---

## How the AI Handles Job Specs

### Requirement Language Recognition

The AI automatically detects requirement language and adds **"min"** or **"max"** indicators:

**Input (Job Spec):**
"The roof coating shall have a minimum initial tensile strength of 300 psi and minimum initial elongation of 500 percent."

**Extracted:**
```json
{
  "Tensile Strength (Initial)": "min 300 psi",
  "Elongation (Initial)": "min 500%"
}
```

**Input (Product Data Sheet):**
"Initial Tensile Strength: 500 psi, Initial Elongation: 425%"

**Extracted:**
```json
{
  "Tensile Strength (Initial)": "500 psi",
  "Elongation (Initial)": "425%"
}
```

### Requirement Keywords Recognized

The AI recognizes these as requirements:
- "minimum" / "min" / "at least" / "not less than"
- "maximum" / "max" / "not more than" / "not to exceed"
- "shall be" / "must be" / "should be"
- "meets or exceeds" / "equal to or greater than"

---

## Reading the Comparison Table

When comparing job specs vs products, the table shows:

### Minimum Requirements:
- **Job Spec Column**: "min 300 psi"
- **Product Column**: "500 psi"
- **Interpretation**: Product exceeds minimum (GOOD!)

### Maximum Requirements:
- **Job Spec Column**: "max 50 g/L"
- **Product Column**: "35 g/L"
- **Interpretation**: Product is under maximum (GOOD!)

### Missing Values:
- **Job Spec Column**: "min 400%"
- **Product Column**: (empty/red)
- **Interpretation**: Product data sheet doesn't list this metric (NEED MORE INFO)

---

## Tips for Best Results

### 1. Upload Complete Documents

**Good:**
- Full job specification PDF with all sections
- Complete product data sheet / technical data sheet

**Bad:**
- Screenshots of partial pages
- Incomplete documents with references to "see other document"

### 2. Text-Based PDFs Only

- PDFs must have selectable text (not scanned images)
- Test: Try to select/copy text in the PDF with your cursor
- If you can't select text, it's image-based (won't work)

### 3. Clear Requirement Statements

The AI works best when job specs use clear language:

**Best:**
- "Minimum tensile strength: 300 psi"
- "Solar reflectance shall be at least 0.80"

**Less Clear:**
- "Tensile strength similar to Product XYZ" (too vague)
- "Meet industry standards" (no specific values)

### 4. Referenced Products

If the job spec says "Use Product XYZ or equal", the AI will try to extract metrics mentioned for Product XYZ in the document.

---

## Common Scenarios

### Scenario: Some Requirements Missing from Product Data

**Problem:**
```
| Metric | Job Spec | Your Product |
|--------|----------|--------------|
| Tensile Strength | min 300 psi | 500 psi ✅ |
| Low Temp Flexibility | min -20°F | (missing) ❌ |
```

**Solutions:**
1. Check if your product data sheet has that metric under a different name
2. Contact your lab for test results
3. If your product doesn't have that property, you may not meet the job spec

### Scenario: Job Spec Has Product Name, Not Requirements

**Example:** "Use Manufacturer X Cool-Coat 100 or approved equal"

**What to Do:**
1. Try to find the data sheet for "Cool-Coat 100"
2. Upload that as your reference instead of the job spec
3. Compare your products against that reference

### Scenario: Multiple Requirement Options

**Example:** "Use either: Option A (elastomeric, min 500% elongation) OR Option B (acrylic, min 0.90 reflectance)"

**What to Do:**
1. The AI will extract both sets of requirements
2. Check which set your product matches
3. Note in your proposal which option you're meeting

---

## Example Workflows

### Workflow 1: Quick Qualification Check

**Goal:** "Can I bid on this job?"

1. Upload job spec PDF
2. Upload your product data sheet
3. Review comparison table
4. If all requirements show values ≥ minimums → You qualify!
5. If missing data → Get more test results
6. If values < minimums → You don't qualify

**Time:** 2 minutes

---

### Workflow 2: Competitive Analysis

**Goal:** "Which competitors qualify for this job?"

1. Upload job spec PDF
2. Upload 5+ competitor product data sheets
3. Review comparison table
4. AI summary tells you which products meet all requirements
5. Export CSV for your records

**Time:** 5 minutes

---

### Workflow 3: Substitution Request

**Goal:** "Prove my product is 'equal to' the specified product"

1. Upload job spec
2. Upload specified product data sheet as Candidate #1
3. Upload your product data sheet as Candidate #2
4. Show comparison table to architect/engineer
5. Use AI summary to highlight how your product meets or exceeds

**Time:** 3 minutes

---

## Interpreting AI Summary

After analysis, the AI provides a summary. For job specs, it will:

**1. Identify Compliance:**
"Product A meets all minimum requirements specified in the job specification."

**2. Highlight Gaps:**
"Product B falls short in Solar Reflectance (0.75 vs. min 0.80 required)."

**3. Note Exceedances:**
"Product C significantly exceeds requirements, with tensile strength 67% above the minimum."

**4. Missing Data:**
"Unable to verify compliance for Low Temperature Flexibility as this metric was not found in Product data sheet."

---

## FAQs

### Q: Can I upload multiple job specs?

A: Currently, the tool supports ONE reference document. If you have multiple job specs:
- Run separate analyses for each
- Or merge requirements into one document if they're similar

### Q: What if the job spec references standards like ASTM D-412?

A: The AI extracts numeric requirements but doesn't look up standards. If the job spec says "Must meet ASTM D-412" without stating specific values, you'll need to look up that standard separately.

### Q: How accurate is the extraction from job specs?

A: Very accurate for clearly stated requirements ("minimum 300 psi"). Less reliable for vague statements ("industry standard quality").

### Q: Can it handle ranges?

A: Yes! "300-500 psi" will be extracted as-is. The AI understands this is a range.

### Q: What about "not to exceed" requirements?

A: Yes! The AI extracts these with "max" prefix:
- "VOC not to exceed 50 g/L" → "VOC Content: max 50 g/L"

### Q: Does it understand "or equal" clauses?

A: The AI recognizes when a product is referenced but extracts metrics, not the product name itself. You should compare against that product's actual data sheet.

---

## Limitations

**What This Tool CAN Do:**
✅ Extract numeric requirements from job specs
✅ Compare products against those requirements
✅ Handle "minimum"/"maximum" language
✅ Normalize different terminology

**What This Tool CANNOT Do:**
❌ Look up industry standards (like ASTM specs)
❌ Determine "or equal" based on brand names alone
❌ Handle image-based PDFs (scanned documents)
❌ Make legal determinations about spec compliance
❌ Interpret vague requirements ("high quality", "durable")

---

## Getting Help

**If metrics aren't extracting:**
1. Check that your PDF has selectable text
2. Verify the job spec uses specific numeric requirements
3. Try the test script: `python test_extraction.py your_jobspec.pdf`
4. Check CHANGELOG.md for known issues

**If results seem wrong:**
1. Review the extracted JSON in comparison table
2. Manually verify a few metrics against the source PDF
3. Report specific extraction issues with PDF examples

---

## Version History

- **v1.2.0** - Added job specification support
- **v1.1.0** - Added flexible terminology matching
- **v1.0.0** - Initial product-only comparison

---

**Questions?** Open an issue in the GitHub repository or check the other documentation files!
