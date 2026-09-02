# FairHire - Bias Free Hiring v3.0 

*Tagline:* Talent is important, just show bias output must be fair chance

A real-world AI bias detector that solves actual hiring bias using data.
live link  https://data-bias-detector.streamlit.app/


###  Features v3.0

*Tab1: Student Data Bias Auditor (Old Data)*
- 50 students data-bias audit
- College tier bias analysis (Tier 1 vs Tier 3)
- Shortlisted rate visualization

*Tab2: Company Matcher + Resume Coach (New v3.0) - Main Feature*
- Branch: CSE, ECE, EEE, MECH, CIVIL
- Company: Google, Microsoft, Amazon, Infosys, TCS
- Role: Software Engineer, Data Analyst, ML Engineer
- Skills: Python, DSA, OOPS, DBMS, System Design
- Gender Bias Slider: 0-100% (1 side bias % / another side select chance)
- Upload Resume PDF (200MB) - Auto email extraction, skill count, bar_chart, final chance with bias, progress bar, metric
- Tips: How to escape gender bias at interview

###  Tech Stack
- Streamlit, Python, Pandas, PyMuPDF, Regex

###  How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
