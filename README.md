# 🛡️ Spam Protection Dashboard

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
