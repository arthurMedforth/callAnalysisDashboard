# 🛡️ Hiya Spam Protection Dashboard

This is an interactive analytics dashboard built to support Hiya's carrier partners by visualizing key threat detection and call protection metrics. It provides a clear, data-driven view of call classification performance, protection rates, and threat origin.

---

## 🚀 How to Run

1. **Install dependencies**  
   Make sure you have Python 3.8+ installed, then run:

   ```
   pip install -r requirements.txt
   ```

   Dependencies include:
   - `streamlit`
   - `pandas`
   - `plotly`
   - `numpy`
   - `openpyxl`

2. **Add your input data**  
   Place your Excel file (e.g., `Example call data.xlsx`) in the root directory.  
   The data must contain at least the following columns:

   - `date` (datetime)
   - `calling phone number` (string/integer)
   - `flagged` (categorical: `neutral`, `spam`, `fraud`)

3. **Run the app**  

   ```
   streamlit run hiya_dashboard.py
   ```

   The dashboard will open in your browser at `http://localhost:8501`.

---

## 🎯 Purpose of the Dashboard

This tool is designed to help **carrier partners** understand how Hiya’s protection platform is performing on their network. It provides monthly reporting with visual insights into:

- The **volume of incoming calls** and how many were flagged as threats
- The **effectiveness of spam and fraud detection**
- The **geographic origin of risky calls**
- A breakdown of **call types by threat level**

---

## 📊 Presentation Outline (for Stakeholders / Carrier Briefing)

This dashboard supports a short (15 min) carrier-facing presentation, structured into 4–5 slides:

### Slide 1: Introduction & Goals
- Brief overview of Hiya’s mission and spam protection services
- Set the stage for understanding call trends and threat mitigation

### Slide 2: Monthly Protection Summary
- Key KPIs: total calls, threats blocked, spam, and fraud volumes
- Value highlight: **% protection rate**, i.e., blocked vs. total

### Slide 3: Day-by-Day Effectiveness
- Daily metrics for volume and protection
- Use this to highlight spikes or trends in malicious activity

### Slide 4: Threat Geography & Type Breakdown
- Visualize which regions are generating threats
- Breakdown of `spam` vs. `fraud` vs. `neutral` to understand threat makeup

### Slide 5: Business Impact Summary
- Total threats prevented = fewer customer complaints
- High fraud interception rate = brand safety + regulatory compliance
- Strategic takeaway: **Hiya adds measurable value to your voice network**

---

## ✅ Features

- Streamlit-based interactive UI
- Custom CSS styling for clean carrier-grade presentation
- Exportable filtered data (CSV)
- Filters by date and classification type
- Visuals powered by Plotly (bar charts, pie charts, time series)

---

## 📂 File Structure

```
hiya_dashboard.py           # Main Streamlit app
README.md                   # This file
requirements.txt            # Python dependencies
Example call data.xlsx      # Input dataset (sample)
```

---

## 🧠 Future Enhancements (Optional)

- Authentication for carrier-specific dashboards
- Real-time ingestion of call logs
- False-positive / precision-recall metrics for classification quality
- Drill-down into individual call traces

---

**Author:** _[Your Name]_  
**Use case:** Hiya – Forward Deployed Engineering Interview Exercise  
**Date:** July 2025
