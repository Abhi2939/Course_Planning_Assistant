## 🧪 Evaluation

### Test Set (25 Queries)

The evaluation set includes:

* **10 prerequisite checks**
* **5 multi-hop prerequisite chains**
* **5 program requirement queries**
* **5 out-of-scope / not-in-catalog queries**

---

### 📊 Results

| Metric                    | Score    |
| ------------------------- | -------- |
| **Citation Coverage**     | **0.96** |
| **Prerequisite Accuracy** | **1.00** |
| **Abstention Accuracy**   | **0.60** |

---

### 📈 Interpretation

* ✅ **High Citation Coverage (96%)**
  Most responses include proper citations, ensuring strong grounding.

* ✅ **Perfect Prerequisite Reasoning (100%)**
  The system correctly evaluates eligibility and prerequisite chains.

* ⚠️ **Moderate Abstention Accuracy (60%)**
  Some out-of-scope queries still produce partial answers instead of abstaining.

---

### 🔍 Failure Analysis

Main failure cases:

* Model attempts to infer missing information (e.g., course schedule, instructors)
* Retrieval sometimes returns loosely related chunks for ambiguous queries
* Prompt adherence to strict abstention can be improved

---

### 🚀 Improvements Planned

* Strengthen abstention rule in prompt
* Add stricter filtering for out-of-scope queries
* Introduce confidence threshold before answering
* Improve query classification for POLICY vs COURSE

---

## 🧾 Example Outputs

### 1. Eligibility Check

**Query:**
Can I take CS 225 after CS 124?

**Output:**

* Decision: Not Eligible
* Why: Missing prerequisite CS 126/128
* Citations: CS 225

---

### 2. Course Plan

**Query:**
Suggest next courses after CS 124

**Output:**

* CS 225
* CS 173
* Justification based on prerequisites

---

### 3. Safe Abstention

**Query:**
Who teaches CS 225?

**Output:**
"I don't have that information in the catalog."

---
