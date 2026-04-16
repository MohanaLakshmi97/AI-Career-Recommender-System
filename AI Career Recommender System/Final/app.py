import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from streamlit_lottie import st_lottie
import re
import time
import os


def generate_explanation(skills, top_role, required_skills, cgpa):
    user_skills = [s.strip().lower() for s in skills.split(";")]
    req_skills = [s.strip().lower() for s in required_skills.split(";")]

    matched = [s for s in user_skills if s in req_skills]

    explanation = f"**You are recommended for {top_role} because:**\n\n"

    if matched:
        explanation += f"✔ You have relevant skills like **{', '.join(matched)}**.\n\n"

    explanation += "✔ These skills match the core requirements of the role.\n\n"

    if len(matched) == len(req_skills):
        explanation += "🎉 You already have all the required skills for this role.\n\n"
    else:
        explanation += "✔ You can further improve by learning missing skills.\n\n"

    return explanation
skill_desc_data = pd.read_csv("data/skill_descriptions.csv")
skill_desc_map = dict(zip(
    skill_desc_data["Skill"].str.strip().str.lower(),
    skill_desc_data["Description"]
))

# ── Lottie Loader ──────────────────────────────────────
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None


from model import (
    calculate_match_score,
    get_missing_skills,
    get_learning_resources,
    get_skill_description,
)

from ml_model import predict_career
from pdf_generator import generate_pdf_report, generate_skill_plan_pdf


# ── Page Config ─────────────────────────────────────────
st.set_page_config(page_title="AI Career Recommender", page_icon="🎓", layout="wide")


# ── Custom CSS ───────────────────────────────────────────
st.markdown("""
<style>
body {
    background-color: #f5f6fa;
}
.main {
    padding: 2rem;
}
h1, h2, h3 {
    color: #2c3e50;
    font-family: 'Segoe UI', sans-serif;
}
.block-container {
    padding-top: 2rem;
}
.stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    padding: 10px 16px;
    border: none;
    font-weight: bold;
}
.stButton > button:hover {
    background-color: #45a049;
}
.stDownloadButton > button {
    background-color: #3498db;
    color: white;
    border-radius: 8px;
    padding: 10px 16px;
    border: none;
    font-weight: bold;
}
.stDownloadButton > button:hover {
    background-color: #2980b9;
}
.card {
    background-color: #ffffff;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)


# ── Load Data ─────────────────────────────────────────────
job_data       = pd.read_csv("data/job_roles.csv")
student_data   = pd.read_csv("data/student_profiles.csv")
resources_data = pd.read_csv("data/skill_resources.csv")


# ── SESSION STATE SAFE INIT ───────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = None

if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None

if "missing" not in st.session_state:
    st.session_state.missing = []

if "student_name" not in st.session_state:
    st.session_state.student_name = ""

if "skills" not in st.session_state:
    st.session_state.skills = ""

if "cgpa" not in st.session_state:
    st.session_state.cgpa = 0.0


# ── Sidebar Navigation ───────────────────────────────────
PAGES = ["🏠 Welcome", "🎯 Career Recommender", "📘 Interest-Based Skill Planner"]
page = st.sidebar.radio("Navigate", PAGES)


# ───────────────────────────── 1. WELCOME ─────────────────────────────
if page == "🏠 Welcome":
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        background-attachment: fixed;
        color: #ffffff;
    }
    .card {
        background-color: rgba(0, 0, 0, 0.55);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 2px 6px 10px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='color:#1abc9c;'>🤖 Welcome to the AI Career Recommender System</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <div class="card">
            <p style='font-size:18px;'>✨ Empower your future with AI-driven career guidance.</p>
            <ul style='font-size:17px; line-height:1.6;'>
                <li>🔍 <b>Discover</b> careers based on your skills and CGPA.</li>
                <li>📈 <b>Analyze</b> gaps and plan your learning path.</li>
                <li>📄 <b>Download</b> a custom career roadmap as PDF.</li>
            </ul>
            <p style='font-size:16px; margin-top:20px;'>Use the <b>sidebar</b> to navigate:</p>
            <ul style='font-size:17px; line-height:1.6;'>
                <li>🎯 Career Recommender</li>
                <li>📘 Interest-Based Skill Planner</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        lottie_robot = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_puciaact.json")
        if lottie_robot:
            st_lottie(lottie_robot, height=250, key="robot_hello")

    st.markdown("""
    <div class="pulse-box">
    ✅ You're ready! Use the <b>sidebar</b> to begin your personalized career journey 🚀✨
    </div>
    <style>
    @keyframes pulse {
      0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(26, 188, 156, 0.7); }
      70% { transform: scale(1.02); box-shadow: 0 0 0 10px rgba(26, 188, 156, 0); }
      100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(26, 188, 156, 0); }
    }
    .pulse-box {
      animation: pulse 2s infinite;
      background-color: #16a085;
      padding: 15px 25px;
      border-radius: 12px;
      font-size: 18px;
      font-weight: bold;
      color: white;
      box-shadow: 2px 4px 12px rgba(0,0,0,0.2);
      text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# ───────────────────── 2. CAREER RECOMMENDER ──────────────────────────
elif page == "🎯 Career Recommender":

    st.markdown("""
    <div class='career-page'>
        <h1>🎯 Career Recommender</h1>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #c8a2c8 0%, #e6d6f5 100%);
        background-attachment: fixed;
        color: #2c2c2c;
    }
    </style>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    student_name = col1.text_input("👤 Enter your name")
    skills = col1.text_input("🛠️ Enter skills (Python;SQL;Tableau)")
    cgpa = col2.slider("🎓 CGPA", 5.0, 10.0, 8.0)

    if st.button("🚀 Recommend Career"):

        # Check empty fields
        if not student_name or not skills:
            st.warning("⚠️ Enter name and skills")
            st.stop()

        # ✅ Name validation (NEW)
        if not re.match("^[A-Za-z ]+$", student_name):
            st.error("❌ Please enter a valid name (only alphabets allowed)")
            st.stop()
        

        # (Optional but good) Clean name
        student_name = student_name.title()

        # Continue your logic
        results = []

        for _, row in job_data.iterrows():
            score = calculate_match_score(skills, row["Required Skills"])
            results.append((
                row["Job Role"],
                score,
                row["Category"],
                row["Avg Salary"],
                row["Required Skills"]
            ))

        results.sort(key=lambda x: x[1], reverse=True)
        if not results or results[0][1] == 0:
            st.error("❌ No suitable career found for the given skills")
            st.info("👉 Try entering relevant skills like Python, SQL, Java, etc.")
            st.stop()

        st.session_state.results = results
        st.session_state.student_name = student_name
        st.session_state.skills = skills
        st.session_state.cgpa = cgpa


    # ---------------- RESULTS ----------------
    if st.session_state.results:

        results = st.session_state.results
        top_role, top_score, top_cat, top_salary, top_req = results[0]

        st.subheader(f"👋 Hello, {st.session_state.student_name}!")
        st.markdown(f"### 🌟 Best Match: {top_role}")

        st.write(f"💡 Match Score: {round(top_score*100,2)}%")
        st.write(f"📂 Category: {top_cat}")
        st.write(f"💰 Avg Salary: ₹{top_salary:,.0f}")
        st.markdown("### 🤖 Why this career?")

        explanation = generate_explanation(
            st.session_state.skills,
            top_role,
            top_req,
            st.session_state.cgpa
        )

        st.markdown(explanation)
        
        missing = get_missing_skills(st.session_state.skills, top_req)
        st.session_state.missing = missing

        if missing:
            st.markdown("### ❌ Missing Skills")

            for sk in missing:
                # FIX 1: removed wrong 2-argument call
                desc = get_skill_description(sk)
                st.write(f"- {sk}: {desc}")

        if missing:
            st.markdown("### 🧠 Learning Resources")

            res = get_learning_resources(missing, resources_data, grouped=False)

            for sk, links in res.items():
                st.write(f"**{sk}**")
                for link in links:
                    st.markdown(f"[Learn here]({link})")

        st.markdown("### 🔍 Other Matches")

        for job, score, cat, salary, _ in results[1:3]:
            st.write(f"- {job} ({round(score*100,1)}%)")

        st.markdown("### 📊 Match Chart")

        labels = [r[0] for r in results[:3]]
        scores = [r[1]*100 for r in results[:3]]

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.barh(labels[::-1], scores[::-1])

        ax.set_xlim(0, 100)

        st.pyplot(fig)

        # 🤖 ML Prediction
        prediction = predict_career(st.session_state.skills, st.session_state.cgpa)
        st.info(f"🤖 ML Prediction: {prediction}")

        # 📄 Generate PDF
        if st.button("📄 Generate PDF"):

            chart_path = "chart.png"

            # ✅ FIX 1: Better chart saving
            fig.savefig(chart_path, bbox_inches='tight')

            # ✅ FIX 2: Prepare skill descriptions
            skill_meanings = {}

            for sk in st.session_state.missing:
                desc = get_skill_description(sk)

                if not desc:
                    desc = "Basic understanding required"

                skill_meanings[sk.lower()] = desc

            # ✅ FIX 3: Resources
            resources = get_learning_resources(
                st.session_state.missing,
                resources_data,
                grouped=False
            )

            # ✅ FIX 4: Other roles WITH percentage
            other_roles = [(r[0], round(r[1]*100, 2)) for r in results[1:4]]

            # ✅ FINAL CALL
            explanation = generate_explanation(
                st.session_state.skills,
                top_role,
                top_req,
                st.session_state.cgpa
            )

            st.session_state.pdf_path = generate_pdf_report(
                st.session_state.student_name,
                results[0],
                st.session_state.missing,
                skill_meanings,
                resources,
                other_roles,
                chart_path,
                explanation   # ✅ NEW PARAMETER
            )

            st.success("✅ PDF Generated!")

    # 📥 Download Button
    if st.session_state.pdf_path:
        with open(st.session_state.pdf_path, "rb") as f:
            st.download_button("⬇️ Download PDF", f, file_name="Career_Report.pdf")


# ───────────────────── 3. SKILL PLANNER ─────────────────────────────
else:
    st.markdown("<h1 style='color:#8e44ad;'>📘 Interest-Based Skill Planner</h1>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    interested_role = st.selectbox(
        "🎯 Select Your Dream Job Role",
        job_data["Job Role"].unique()
    )

    existing_skills = st.text_input(
        "🔎 Skills You Already Have (e.g., Python;SQL;Excel)",
        key="existing_input"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if interested_role:

        row = job_data[job_data["Job Role"] == interested_role].iloc[0]

        required = [s.strip() for s in row["Required Skills"].split(";")]

        # ✅ Handle both comma and semicolon
        skills_input = existing_skills.replace(",", ";") if existing_skills else ""

        existing = [
            s.strip().lower()
            for s in skills_input.split(";")
            if s.strip()
        ]


        # ✅ Missing skills
        missing = [s for s in required if s.lower() not in existing]

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.markdown(
            f"<h4>🔑 Skill Breakdown for <span style='color:#8e44ad'>{interested_role}</span></h4>",
            unsafe_allow_html=True,
        )

        for sk in required:
            status = "✅" if sk.lower() in existing else "❌"
            st.markdown(
                f"{status} <b>{sk}</b> — {get_skill_description(sk)}",
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

        res = {}

        if missing:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### 🚀 Skills to Add & Resources")

            res = get_learning_resources(missing, resources_data, grouped=False)

            for sk, links in res.items():
                st.markdown(f"**{sk.title()}**:")
                for link in links:
                    st.markdown(f"- [🔗 Learn here]({link})")

            st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.success("🎉 You already have all the required skills for your dream role!")

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.markdown("### 🗺️ Short Roadmap Guidance")

        st.info("""
1. **Start** with free beginner tutorials (Docs, Coursera, etc.)  
2. **Build** small hands-on projects to apply the skills  
3. **Contribute** to GitHub or open-source if possible  
4. **Certify** yourself with relevant credentials (AWS, TensorFlow, etc.)  
5. **Showcase** your work on LinkedIn and GitHub regularly
""")

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("📥 Download Skill Plan as PDF"):

            try:
                pdf_path = generate_skill_plan_pdf(
                    name=st.session_state.student_name if st.session_state.student_name else "Student",
                    dream_role=interested_role,
                    existing_skills=existing,
                    missing_skills=missing,
                    resources=res,
                    skill_desc_map=skill_desc_map
                )

                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "Download PDF",
                        f,
                        file_name=pdf_path.split("/")[-1]
                    )

            except Exception as e:
                st.error(f"⚠️ Could not generate PDF: {e}")