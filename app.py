import streamlit as st
import pdfplumber
import matplotlib.pyplot as plt
import re
from collections import Counter

st.set_page_config(page_title="AI Resume Analyzer", page_icon="", layout="wide")

st.title(" AI Resume Analyzer Pro")
st.write("Upload your resume and get instant AI-powered analysis, ATS score, and skill insights.")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content
    return text

skills = [
"Python","Java","C++","SQL","Machine Learning","Deep Learning","AI",
"Data Analysis","Pandas","NumPy","HTML","CSS","JavaScript","React",
"Node","MongoDB","Git","Docker","Kubernetes","AWS","Linux"
]

job_keywords = [
"develop","design","build","optimize","analyze","deploy",
"collaborate","implement","research","improve"
]

sections = [
"education","experience","skills","projects","certifications","summary"
]

if uploaded_file:

    resume_text = extract_text(uploaded_file)

    st.subheader("📄 Resume Preview")
    st.text(resume_text[:2000])

    text_lower = resume_text.lower()

    st.divider()

    st.subheader(" Skill Detection")

    found_skills = []

    for skill in skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    col1,col2 = st.columns(2)

    with col1:
        st.write("### Detected Skills")
        if found_skills:
            for s in found_skills:
                st.success(s)
        else:
            st.warning("No technical skills detected")

    with col2:
        st.write("### Missing Skills")
        missing = [s for s in skills if s not in found_skills]
        for m in missing[:8]:
            st.info(m)

    st.divider()

    st.subheader(" Resume Skill Score")

    skill_score = int((len(found_skills)/len(skills))*100)

    st.progress(skill_score)

    st.write(f"### Skill Score: {skill_score}/100")

    if skill_score < 40:
        st.error("Your resume lacks strong technical keywords.")
    elif skill_score < 70:
        st.warning("Decent resume but can be improved.")
    else:
        st.success("Strong technical resume!")

    st.divider()

    st.subheader(" Skill Visualization")

    values = [1 if s in found_skills else 0 for s in skills]

    fig, ax = plt.subplots()

    ax.barh(skills, values)

    st.pyplot(fig)

    st.divider()

    st.subheader(" ATS Resume Score")

    ats_score = 0

    if len(found_skills) > 5:
        ats_score += 30

    for sec in sections:
        if sec in text_lower:
            ats_score += 10

    if len(resume_text) > 1500:
        ats_score += 20

    ats_score = min(ats_score,100)

    st.progress(ats_score)

    st.write(f"### ATS Compatibility Score: {ats_score}/100")

    if ats_score < 50:
        st.error("Low ATS score. Improve formatting and keywords.")
    elif ats_score < 75:
        st.warning("Moderate ATS compatibility.")
    else:
        st.success("Excellent ATS optimization!")

    st.divider()

    st.subheader(" Action Word Analysis")

    words = re.findall(r'\b\w+\b', text_lower)

    counter = Counter(words)

    found_keywords = []

    for word in job_keywords:
        if counter[word] > 0:
            found_keywords.append(word)

    st.write("Detected Action Words:")

    if found_keywords:
        st.write(found_keywords)
    else:
        st.warning("Add strong action words like developed, built, designed.")

    st.divider()

    st.subheader("🧾 Resume Section Check")

    missing_sections = []

    for sec in sections:
        if sec not in text_lower:
            missing_sections.append(sec)

    if missing_sections:
        for ms in missing_sections:
            st.warning(f"Missing section: {ms}")
    else:
        st.success("All important sections detected!")

    st.divider()

    st.subheader("✨ AI Resume Suggestions")

    suggestions = []

    if "github" not in text_lower:
        suggestions.append("Add your GitHub profile link.")

    if "linkedin" not in text_lower:
        suggestions.append("Add LinkedIn profile.")

    if skill_score < 60:
        suggestions.append("Add more technical skills relevant to your field.")

    if "project" not in text_lower:
        suggestions.append("Include projects to demonstrate practical experience.")

    if "internship" not in text_lower:
        suggestions.append("Consider adding internships or practical work experience.")

    if suggestions:
        for s in suggestions:
            st.write("✔",s)
    else:
        st.success("Great resume structure!")

    st.divider()

    st.subheader(" Resume Word Frequency")

    common = counter.most_common(10)

    labels = [x[0] for x in common]
    values = [x[1] for x in common]

    fig2, ax2 = plt.subplots()

    ax2.bar(labels,values)

    st.pyplot(fig2)

st.sidebar.title("About This Project")

st.sidebar.write("""
AI Resume Analyzer Pro

Features:
- Resume parsing
- Skill detection
- Skill visualization
- ATS compatibility score
- Resume keyword analysis
- Resume section checker
- AI improvement suggestions
""")

st.sidebar.write("Built with Python & Streamlit ")
