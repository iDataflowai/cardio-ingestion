
---

# **cardio-ingestion**

**Raw biomarker ingestion, canonicalization, quality checks, and structured payload generation for the iDataflow Cardio Intelligence system.**
Part of the **iDataflow.ai** personal AI portfolio by **Bhagwat Chate**.

---

## **Vision**

**To transform raw cardiovascular biomarker inputs into a clean, canonical, validated, and structured data envelope that the scoring and agentic reasoning engines can fully trust.**

This repository ensures that all downstream cardiovascular intelligence layers operate on **accurate, standardized, safe, and clinically meaningful data** — exactly how FAANG-grade HealthTech systems ingest and normalize medical data.

---

## **Objectives**

### **1. Standardize biomarker inputs across labs and sources**

Unify naming, units, and formats into one canonical internal structure.

### **2. Apply strict QC (Quality Checks)**

Detect missing values, invalid ranges, duplicates, and biologically implausible values.

### **3. Normalize biomarker units and values**

Ensure consistent internal representation (mg/dL → mmol/L, ratios, flags, etc.).

### **4. Build a structured ingestion payload**

Output a deterministic JSON envelope containing biomarkers, metadata, QC summary, and version.

### **5. Guarantee reproducible, versioned ingestion**

Transformations remain consistent, traceable, and safe for clinical-grade intelligence.

### **6. Protect downstream scoring & agent layers**

Prevent bad, messy, or inconsistent data from reaching the intelligence engine.

---

## **Responsibilities**

### **1. Raw Input Handling**

* Accept input from API/UI
* Clean & interpret raw fields
* Remove noise and irrelevant fields

### **2. Canonicalization**

* Standardize biomarker names
* Resolve aliases (e.g., “AST (SGOT)” → “AST”)
* Map units & convert automatically
* Attach reference ranges

### **3. QC Engine (Quality Checks)**

* Validate numeric formats
* Identify missing or duplicate markers
* Verify biological ranges
* Generate QC summary (PASS / WARN / ERROR)

### **4. Normalization Engine**

* Convert units and values
* Normalize ratios
* Format precision

### **5. Structured Payload Builder**

Generates the master ingestion schema:

```json
{
  "sample_id": "...",
  "user_id": "...",
  "trace_id": "...",
  "biomarkers": { },
  "metadata": { },
  "qc_summary": { },
  "version": "v1.0"
}
```

### **6. Logging & Traceability**

* Structured logs
* Ingestion-level trace_id propagation

### **7. Downstream Integration**

Feeds clean output into:

* **cardio-score**
* **cardio-agent**
* **cardio-api**

---

## **Recommended Folder Structure**

```
cardio-ingestion/
│
├── src/
│   ├── cardio_ingestion/
│   │   ├── ingestion/
│   │   ├── canonicalizer/
│   │   ├── qc/
│   │   ├── schemas/
│   │   ├── builders/
│   │   ├── utils/
│   │   └── config/
│   │
│   └── main.py
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── docs/
│   ├── ingestion_flow.md
│   ├── canonicalization_reference.md
│   ├── qc_rules_spec.md
│   └── payload_contract.md
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## **Core Pipeline Overview**

1. **Raw Input → Parsing**
2. **Canonicalization → Standard biomarker dictionary**
3. **QC Engine → Validity, completeness, biological safety**
4. **Normalization → Unit/value consistency**
5. **Payload Builder → Final structured ingestion envelope**
6. **Emit payload to scoring layer**

Every step is deterministic, logged, and versioned.

---

## **Integration Points**

### **Downstream Repositories**

* `cardio-score` — Receives the structured biomarkers for scoring
* `cardio-agent` — Uses normalized biomarker data for reasoning
* `cardio-api` — Provides ingestion endpoints
* `cardio-frontend` — Displays ingestion output

---

## **Technology Stack**

* Python 3.11
* Pydantic (validation & schemas)
* AWS LAMBDA (ZIP deployment)
* AWS RDS (PostgreSQL)
* AWS Secrets Manager
* AWS S3 (raw + structured payload archival)
* AWS CloudWatch (logs + metrics)
* AWS IAM (secure permissions)
* Structured Logging (JSON logs)
* GitHub Actions CI/CD

---

## **Upcoming Enhancements**

* Full biomarker canonical map (150+ markers)
* Detailed QC rules & configs
* Example ingestion payloads
* Ingestion versioning system
* Lab-specific mapping profiles
* S3 archival support

---

## **License**

MIT License
Part of the **iDataflow.ai** personal AI portfolio.
Created by **Bhagwat Chate**.

---
