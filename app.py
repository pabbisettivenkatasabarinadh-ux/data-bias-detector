import streamlit as st
import pandas as pd
import pymupdf as fitz
import plotly.express as px
import re 
from collections import Counter
st.set_page_config(page_title="fairhire-bias free hiring",layout="wide")
st.title("fairhire-real world bias solver")
st.write("talent is important just show bias output must be fair chance")

tab1, tab2 = st.tabs(["tab1:student data bias auditor(old data)","tab2:company matcher + resume coach new idea)"])
#tab:1- old data- gender-+tier bias
with tab1:
    st.header("50 students data-bias audit")
    try:
        df=pd.read_csv("resume.csv")
        st.dataframe(df.head(10))
        st.write(f"total students:{len(df)}")
        #tier bias
        df['shortlisted'] = df['shortlisted'].astype(str).str.lower()
        tier_bias=df.groupby('college_tier')['shortlisted'].apply(lambda x:(x=='yes').mean()*100)
        gender_bias=df.groupby('gender')['shortlisted'].apply(lambda x: (x=='yes').mean()*100)
        col1,col2=st.columns(2)
        with col1:
            st.subheader("tier bias")
            st.info("tier3 0%=you are talented but you reject because the clg tier ranking of your is low")
            st.bar_chart(tier_bias)
            for t,p in tier_bias.items():st.metric(f"{t}",f"{p:.0f}%shortlisted")
        with col2:
            st.subheader("gender bias")
            st.error(f"male {gender_bias.get('male',0):.0f}% vs female {gender_bias.get('female',0):.0f}% - girls low!")
            st.write("---")
            st.subheader("detailed count(counter)")
            gender_count=Counter(df['gender'].str.lower())
            st.write(gender_count)
        #gender bias verdict
        if abs(gender_bias.get('male',0)-gender_bias.get('female')) >15:
            st.error(f"gender bias also include here! male{gender_bias.get('male',0):.0f}% vs female{gender_bias.get('female',0):.0f}% -company -hiring girls is low to the job")
            st.write("fix:hire gender in resume-blind hiring!")
        if tier_bias.get('tier1',0) - tier_bias.get('tier3',0) > 50:
            st.error(f"tier bias include! tier1{tier_bias.get('tier1',0):.0f}% vs tier2 {tier_bias.get('tier2',0):.0f}% -talented tier3 -rejected in interview!")

    except:
        st.warning("no resume.csv-keep 50 rows file")
    with tab1:
        st.subheader("students dataset upload - bias audit")
        uploaded_students=st.file_uploader("students palcement upload files like csv",type=['csv'], key="students")

    if uploaded_students:
        df=pd.read_csv(uploaded_students)
    else:
        df=pd.read_csv("resume.csv")
with tab2:
    st.header("tab:2 company matcher+resume  coach (new v3.0)")
    st.write("upload resume pdf - bias words check + count skills and verify")

    upload_pdf=st.file_uploader("upload resume pdf",type=["pdf"])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        company_choice = st.selectbox(" Company", ["Google", "Microsoft", "Amazon", "TCS", "Infosys", "Tesla", "OpenAI", "Other"], key="cc3")
        world_company = st.text_input("Type Company", "Google") if company_choice=="Other" else company_choice
    with c2:
        role = st.selectbox(" Role", ["Software Engineer", "Data Scientist", "Core Engineer", "Web Developer"], key="rr3")
    with c3:
        branch = st.selectbox(" Branch", ["CSE", "EEE", "ECE", "Mech", "Civil", "IT", "Other"], key="bb3")
        if branch=="Other":
            branch = st.text_input("Branch Type", "EEE")
    with c4:
        gender = st.selectbox(" Gender", ["Male", "Female", "Prefer not to say"], key="gg3")

    # 1. SKILL DICT - Ikkada
    role_skills = {
        "Software Engineer": "Python, DSA, OOPS, DBMS, System Design",
        "Data Scientist": "Python, SQL, Machine Learning, Statistics",
        "Core Engineer": "Core Subjects, Problem Solving, Projects",
        "Web Developer": "HTML, CSS, JavaScript, React, Node.js"
    }
    req_str = role_skills[role]
    req_list = [s.strip().lower() for s in req_str.split(',')]
    st.success(f" {branch} | {role} | {world_company} | Skills: {req_str}")

    
    st.subheader(" Gender Bias - 1 Side Bias % | another Side Select Chance")
    left, right = st.columns(2)
    with left:
        st.write("* 1st Side - Gender Bias %*")
        try:
            df_g = pd.read_csv("resume.csv")
            male_rate = (df_g[df_g['gender']=='male']['shortlisted']=='yes').mean()*100
            female_rate = (df_g[df_g['gender']=='female']['shortlisted']=='yes').mean()*100
        except:
            male_rate, female_rate = 75, 35
        bias = male_rate - female_rate
        st.metric(" Male Select %", f"{male_rate:.0f}%")
        st.metric(" Female Select %", f"{female_rate:.0f}%")
        st.error(f" Bias Gap: {bias:.0f}%")
    with right:
        st.write("* 2nd Side - your Select Chance*")
        if gender == "Female":
            st.metric("Female Base Chance", f"{female_rate:.0f}%")
            st.metric("having risk to reject", f"{bias:.0f}%")
        else:
            st.metric("Male Base Chance", f"{male_rate:.0f}%")
            st.success("Advantage ")
    # 2 SIDE CODE END

    # 3. TARVAATA - PDF UPLOAD
    uploaded = st.file_uploader(f" {branch} - Resume PDF", type=['pdf','txt'], key="pdf3")
    if uploaded:
        text = ""
        if uploaded.type == "text/plain":
            text = uploaded.read().decode()
        else:
            try:
                doc = fitz.open(stream=uploaded.read(), filetype="pdf")
                text = " ".join([p.get_text() for p in doc])
            except:
                text=""
        if text:
            emails=re.findall(r"\S+@\S+\.\S+",text)
            found = [s for s in req_list if s in text.lower()]
            missing=[s for s in req_list if s not in text.lower()]
            base=len(found)/len(req_list)*80 + (15 if "project" in text.lower() else 0)
            final_chance=max(0,min(100,int(base - (bias*0.5 if gender=="female" else 0))))
            skill_count=Counter(found)

            st.write(f"found emails:{emails}")
            st.write(f"skill count:{skill_count}")
            st.bar_chart(skill_count)

            st.metric(f" Final Chance - with bias", f"{final_chance}%", delta=f"+{int(bias*0.5)}% Without Bias" if gender=="female" else "advantage")
            st.progress(final_chance)
            st.write(f" already kown skills: {found} | missing skilkls: {missing}")

            st.subheader(" how to escape genderbias at interview")
            if gender=="Female":
                st.write("1. Blind Resume - Gender Hide 2. Skills Top Lo 3. take referral - Chance will increase 40%")
st.divider()
st.subheader("feedback/commentbox")
st.write("give your valuable suggestion - bias free hiring purpose!")

comment=st.text_area("leave your comment:",placeholder="your ideas?")

if st.button("submit comment"):
    if comment:
        st.success(f"thanks bro ! your comment saved:{comment}")
        st.balloons()
    else:
        st.warning("comment empty!")
