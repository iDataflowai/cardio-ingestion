---

# **cardio-ingestion**

**High-fidelity cardiovascular biomarker ingestion, canonicalization, normalization, QC validation, and structured payload persistence for the iDataflow Cardio Intelligence System (CIS).**

Part of the **iDataflow.ai** personal AI portfolio by **Bhagwat Chate**.

---

# **Vision**

To provide a **clinical-grade ingestion pipeline** that transforms raw biomarker inputs into a **canonical, normalized, validated, and structured data envelope** — forming the trusted foundation for scoring engines and multi-agent cardiovascular reasoning.

This repository ensures that every downstream component works with **accurate, consistent, and safe biomarker data**, exactly how **FAANGM-grade HealthTech platforms** are engineered.

---

# **Objectives**

## **1. Standardize biomarker inputs**

Unify biomarker names, aliases, units, and formats from any lab source into a single canonical schema.

## **2. Apply rigorous QC (Quality Checks)**

Validate biological plausibility, detect missing values, and ensure all dominant biomarkers required by CIS buckets are present.

## **3. Normalize biomarker units & values**

Convert mg/dL ↔ mmol/L ↔ µmol/L and ensure uniform internal representation.

## **4. Generate a deterministic structured payload**

Produce a machine-verifiable JSON envelope for scoring & agent reasoning.

## **5. Ensure versioned, reproducible ingestion flows**

Every transformation step is deterministic, traceable, and governed by DB-based configs.

## **6. Protect downstream clinical intelligence**

Invalid, inconsistent, or incomplete samples are intercepted at ingestion, not at scoring.

---

# **Key Responsibilities**

## **1. Raw Input Handling**

Handles all incoming biomarker payloads from S3/API and prepares them for processing.

**Responsibilities**

* Load raw payloads from S3.
* Validate structure using Pydantic.
* Attach a `trace_id` for full pipeline observability.
* Ensure consistent input formatting before transformation.

---

## **2. Canonicalization**

Maps raw biomarker labels to a single unified vocabulary driven entirely by database configuration.

**Powered by table:**
`cis_biomarker_alias_map`

**Responsibilities**

* Convert lab-specific or variant biomarker names → canonical names.
* Drop unmappable biomarkers safely.
* Ensure downstream scoring and agent layers always operate on a stable, deterministic name set.

---

## **3. Unit Conversion Engine**

Normalizes all biomarker values to CIS-standard units using a DB-driven rule set.

**Powered by table:**
`cis_unit_conversion`

**Responsibilities**

* Convert units using `(value × factor + offset)`.
* Support multiple unit variants per biomarker.
* Preserve comments, range fields, and metadata.
* Ensure internal representation is consistent across labs.

---

## **4. QC Engine**

Applies clinical and rule-based quality checks using bucket definitions and biomarker roles.

**Powered by table:**
`cis_biomarker_weightage_mapping`

**Responsibilities**

* Validate presence of Dominant / Secondary / Supplementary biomarkers.
* Detect missing, null, empty, or invalid biomarkers.
* Assign `qc_check` to each biomarker: `"valid"` or `"invalid"`.
* Produce the final QC summary:

```json
"qc_summary": {
  "missing_critical_markers": false,
  "missing_critical_biomarkers": [],
  "total_invalid_markers": 0,
  "implausible_markers": [],
  "overall_status": "valid"
}
```

Dominant biomarkers act as **hard gates** — missing even one marks the entire sample invalid.

---

## **5. Structured Payload Persistence**

Stores the final, validated, and normalized sample envelope as the authoritative CIS record.

**Stored in table:**
`structured_biomarker_samples`

**Schema**

* `user_id`
* `sample_id`
* `trace_id`
* `structured_payload` (JSONB)
* `qc_overall_status`
* `version`
* `created_at`

**Responsibilities**

* Persist ingestion results for scoring + agent layers.
* Maintain full versioning and traceability.
* Provide a single source of truth for downstream CIS operations.

---

# **Final Pipeline Overview (Locked)**

```
Raw Input (S3 / API)
        ↓
Pydantic Validation
        ↓
Name Canonicalization
        ↓
Unit Conversion (DB-driven)
        ↓
QC Engine (bucket-role logic, dominant biomarker enforcement)
        ↓
Final Structured Envelope
        ↓
Persist to structured_biomarker_samples
        ↓
CIS Scoring Engine → Agent Reasoning Pipeline
```

---

# **Database Tables Created by This Pipeline**

### **1. cis_biomarker_alias_map**

Mapping of raw → canonical biomarker names.

### **2. cis_biomarker_master**

Master list of 37 canonical biomarkers.

### **3. cis_unit_conversion**

Unit normalization rules.

### **4. cis_biomarker_weightage_mapping**

Bucket-role assignments (dominant, secondary, supplementary).

### **5. structured_biomarker_samples**

Final enriched sample envelope storage.

These five tables form the **complete ingestion data layer v1.0**.

---

# **Recommended Folder Structure**

```
cardio-ingestion/
│
├── src/
│   ├── ingestion/         # Raw loading, validation
│   ├── canonicalizer/     # Name mapping + unit conversion
│   ├── qc/                # Quality check engine
│   ├── repository/        # Persistence layer
│   ├── schemas/           # Pydantic schemas
│   ├── utils/             # Shared utilities
│   ├── logger/            # Structured logging
│   └── orchestration/     # IngestionOrchestrator (main pipeline)
│
├── tests/
│
├── docs/
│   ├── ingestion_flow.md
│   ├── canonicalization_reference.md
│   ├── qc_rules_spec.md
│   └── payload_contract.md
│
├── requirements.txt
└── README.md
```

---

# **Integration Points**

### **Upstream**

* API / UI / Batch loaders
* S3 raw files

### **Downstream (CIS Core)**

* **cardio-score** — biomarker scoring, bucket severity
* **cardio-agent** — multi-agent clinical reasoning
* **cardio-api** — serves results to frontend/apps
* **cardio-frontend** — visualization

---

# **Tech Stack**

* **Python 3.11**
* **Pydantic** (models, validation)
* **PostgreSQL (AWS RDS)**
* **AWS S3** (raw payloads)
* **AWS Secrets Manager**
* **Structured Logging (JSON)**
* **GitHub Actions (CI/CD)**
* **FAANG-grade modular pipeline architecture**

---

# **Upcoming Enhancements**

* Lab-specific canonicalization profiles
* Biological plausibility matrix
* QC severity scoring
* Unit consistency dashboard
* Pydantic v2 migration
* S3 archival of final envelopes

---

# **License**

MIT License
Part of the **iDataflow.ai** personal AI portfolio.
Created by **Bhagwat Chate**.

---
