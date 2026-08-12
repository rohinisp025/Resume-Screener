import streamlit as st
import time
from task import resume_screening

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide"
)
# ---------------------------
# SIDEBAR
# ---------------------------
with st.sidebar:

    st.image("https://img.icons8.com/color/96/resume.png", width=80)

    st.title("AI Resume Screener")

    st.markdown("---")

    st.success("✔ Upload Resume")

    st.success("✔ Paste Job Description")

    st.success("✔ Analyze Resume")

    st.success("✔ Download Report")

    st.markdown("---")

    st.info("""
### Technologies

- Python
- Streamlit
- OpenRouter API
- OpenAI SDK
- PyMuPDF
- python-docx
""")
# ---------------------------
# CUSTOM CSS
# ---------------------------
st.markdown("""
<style>

.stApp{
background:linear-gradient(135deg,#EEF5FF,#FFFFFF);
}

.title{
font-size:45px;
font-weight:bold;
text-align:center;
color:#0F172A;
}

.subtitle{
text-align:center;
color:#64748B;
font-size:18px;
margin-bottom:25px;
}

div[data-testid="stMetric"]{

background:white;

padding:20px;

border-radius:15px;

box-shadow:0px 6px 15px rgba(0,0,0,.15);

}

div.stButton>button{

background:#2563EB;

color:white;

height:55px;

font-size:20px;

border-radius:10px;

border:none;

}

div.stButton>button:hover{

background:#1E40AF;

}

.block-container{

padding-top:2rem;

padding-bottom:2rem;

}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# HEADER
# ---------------------------

st.markdown("""
<h1 style='text-align:center;color:#2563EB;'>
📄 AI Resume Screener
</h1>

<h4 style='text-align:center;color:gray;'>
Analyze Resume using Artificial Intelligence
</h4>
""", unsafe_allow_html=True)

# ---------------------------
# INPUT SECTION
# ---------------------------

left, right = st.columns(2)

with left:

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    resume = st.file_uploader(
        "📂 Upload Resume",
        type=["pdf", "docx"]
    )

    st.markdown("</div>", unsafe_allow_html=True)

with right:

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    job_description = st.text_area(
        "📋 Job Description",
        height=250,
        placeholder="Paste the Job Description here..."
    )

    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

c1, c2, c3 = st.columns([1,2,1])

with c2:

    analyze = st.button(
        "🤖 Analyze Resume",
        use_container_width=True
    )

# ---------------------------
# ANALYSIS
# ---------------------------

if analyze:

    if resume is None:

        st.warning("Please upload a resume.")

        st.stop()

    if job_description.strip() == "":

        st.warning("Please paste the Job Description.")

        st.stop()

    with st.spinner("Analyzing Resume..."):

        progress = st.progress(0)

        for i in range(101):

            time.sleep(0.02)

            progress.progress(i)

    result = resume_screening(
        resume,
        job_description
    )

    score = result["score"]
    verdict = result["verdict"]

    matching_skills = result["matching_skills"]

    missing_skills = result["missing_skills"]

    strengths = result["strengths"]

    suggestions = result["suggestions"]

    recommendation = result["recommendation"]

    st.balloons()

    st.success("Analysis Completed Successfully 🎉")
        # ---------------------------
    # RESULT DASHBOARD
    # ---------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="score-card">
                ATS Match Score<br>
                {score}%
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        if verdict.lower() == "strong":
            st.success("✅ STRONG MATCH")

        elif verdict.lower() == "moderate":
            st.warning("⚠️ MODERATE MATCH")

        else:
            st.error("❌ WEAK MATCH")

        st.progress(int(score))

    st.write("---")

    # ---------------------------
    # MATCHING SKILLS
    # ---------------------------
    m1,m2,m3=st.columns(3)

    m1.metric("ATS Score",f"{score}%")

    m2.metric("Verdict",verdict)

    m3.metric("Skills Found",len(matching_skills))
    st.subheader("🎯 Matching Skills")

    if matching_skills:
        for skill in matching_skills:
            st.markdown(
                f"<span class='skill'>{skill}</span>",
                unsafe_allow_html=True
            )
    else:
        st.info("No matching skills found.")

    st.write("")

    # ---------------------------
    # MISSING SKILLS
    # ---------------------------

    st.subheader("❌ Missing Skills")

    if missing_skills:
        for skill in missing_skills:
            st.markdown(
                f"- {skill}"
            )
    else:
        st.success("No important skills are missing.")

    st.write("")

    # ---------------------------
    # STRENGTHS
    # ---------------------------

    st.subheader("💪 Strengths")

    if strengths:
        for item in strengths:
            st.success(item)
    else:
        st.info("No strengths available.")

    st.write("")

    # ---------------------------
    # SUGGESTIONS
    # ---------------------------

    st.subheader("💡 Suggestions")

    if suggestions:
        for item in suggestions:
            st.warning(item)
    else:
        st.info("No suggestions available.")

    st.write("")

    # ---------------------------
    # RECOMMENDATION
    # ---------------------------

    st.subheader("📌 Final Recommendation")

    st.markdown(f"""
    ### ⭐ Final Recommendation

    > {recommendation}
    """)

    st.write("")

    # ---------------------------
    # DOWNLOAD REPORT
    # ---------------------------

    report = f"""
AI Resume Screener Report

=================================

ATS Match Score : {score}%

Verdict : {verdict}

---------------------------------

Matching Skills

{chr(10).join(matching_skills)}

---------------------------------

Missing Skills

{chr(10).join(missing_skills)}

---------------------------------

Strengths

{chr(10).join(strengths)}

---------------------------------

Suggestions

{chr(10).join(suggestions)}

---------------------------------

Recommendation

{recommendation}
"""

    st.download_button(
        "📥 Download Report",
        report,
        file_name="Resume_Report.txt",
        mime="text/plain"
    )

# ---------------------------
# FOOTER
# ---------------------------

st.markdown(
    """
    <div class='footer'>
        Made with ❤️ using Streamlit & OpenRouter AI
    </div>
    """,
    unsafe_allow_html=True
)