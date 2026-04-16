import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
import difflib
import os
import wikipedia
import re
from transformers import pipeline

# -------------------------
# Paths to CSV files
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Load CSVs
job_roles = pd.read_csv(os.path.join(DATA_DIR, "job_roles.csv"))
skills = pd.read_csv(os.path.join(DATA_DIR, "skill_resources.csv"))
students = pd.read_csv(os.path.join(DATA_DIR, "student_profiles.csv"))

# Clean column names
job_roles.columns = [col.strip().replace(" ", "_") for col in job_roles.columns]
skills.columns = [col.strip().replace(" ", "_") for col in skills.columns]
students.columns = [col.strip().replace(" ", "_") for col in students.columns]

# -------------------------
# Greeting
# -------------------------
def get_greeting_response(query):
    query = query.lower().strip()

    greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    thanks = ["thank you", "thanks", "thank u", "thx"]

    if any(g in query for g in greetings):
        return "👋 Hello! How can I help you with your career or skills today?"

    if any(t in query for t in thanks):
        return "😊 You're welcome! Happy to help you anytime."

    return None

# -------------------------
# Wikipedia Answer
# -------------------------
def get_factual_answer(query):
    try:
        search_results = wikipedia.search(query, results=1)
        if search_results:
            summary = wikipedia.summary(search_results[0], sentences=2)
            return summary
        else:
            return "Sorry, I couldn't find anything."
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Be more specific. Did you mean: {', '.join(e.options[:5])}?"
    except:
        return "Sorry, error fetching data."

# -------------------------
# Helper functions
# -------------------------
def extract_keyword(query, remove_words=None):
    if remove_words is None:
        remove_words = [
            "salary", "package", "pay", "role", "job", "career",
            "of", "a", "an", "the", "skills", "skill",
            "available", "tell", "about"
        ]
    pattern = r"\b(" + "|".join(remove_words) + r")\b"
    keyword = re.sub(pattern, "", query.lower()).strip()
    return keyword


def get_job_info(job_name):
    row = job_roles[job_roles["Job_Role"] == job_name].iloc[0]
    return f"""
💼 **Job Role:** {row['Job_Role']}  
🛠️ **Required Skills:** {row['Required_Skills']}  
📂 **Category:** {row['Category']}  
💰 **Average Salary:** ₹{row['Avg_Salary']:,}
"""


def get_skill_resources(skill_name):
    row = skills[skills["Skill"] == skill_name].iloc[0]
    return f"""
🛠️ **Skill:** {row['Skill']}  
📚 **Resources:** {row['Resources']}  
🎓 **Free Certification Available:** {row['Free_Certification']}
"""


def list_students():
    profiles = []
    for _, row in students.iterrows():
        profiles.append(f"""
👤 **Name:** {row['Name']}  
📊 **CGPA:** {row['CGPA']}  
🛠️ **Skills:** {row['Skills']}  
📘 **Subjects:** {row['Subjects']}  
💡 **Projects:** {row['Projects']}
""")
    return "\n\n".join(profiles)


# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Career Chatbot", layout="wide")
st.markdown("""

<style>
    .stApp {
        background: linear-gradient(135deg, #004d4d 0%, #00b3b3 100%);
        background-attachment: fixed;
        color: #ffffff;
    }

</style>
""", unsafe_allow_html=True)
st.title("🤖 Career Assist")
st.write("Ask me about **job roles, skills, or anything else!**")

# -------------------------
# Chat History
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------
# Input
# -------------------------
query = st.text_input("Type your message...")

if query:
    query_lower = query.lower()
    answer_parts = []

    # -------------------------
    # Student queries
    # -------------------------
    if any(word in query_lower for word in ["student", "profile", "cgpa", "projects"]):
        answer_parts.append(list_students())

    # -------------------------
    # Job queries
    # -------------------------
    if any(word in query_lower for word in ["job", "role", "career", "salary", "package", "pay"]):
        job_keyword = extract_keyword(query)
        job_match = difflib.get_close_matches(job_keyword, job_roles["Job_Role"], n=1, cutoff=0.5)

        if job_match:
            job_row = job_roles[job_roles["Job_Role"] == job_match[0]].iloc[0]

            if any(word in query_lower for word in ["salary", "package", "pay"]):
                answer_parts.append(f"💰 Average Salary of {job_row['Job_Role']}: ₹{job_row['Avg_Salary']:,}")
            else:
                answer_parts.append(get_job_info(job_match[0]))
        else:
            software_jobs = job_roles[job_roles['Category'].str.contains(job_keyword, case=False, na=False)]
            if not software_jobs.empty:
                answer_parts.append("💼 Available jobs:\n" + "\n".join(
                    [f"{row['Job_Role']} - ₹{row['Avg_Salary']:,}" for _, row in software_jobs.iterrows()]
                ))

    # -------------------------
    # Skill queries
    # -------------------------
    if any(word in query_lower for word in ["skill", "learn", "resources", "tutorial", "free"]):
        skill_keyword = extract_keyword(query)
        skill_match = difflib.get_close_matches(skill_keyword, skills["Skill"], n=1, cutoff=0.5)

        if skill_match:
            answer_parts.append(get_skill_resources(skill_match[0]))

    # -------------------------
    # General queries
    # -------------------------
    greeting = get_greeting_response(query)

    if greeting:
        answer_parts.append(greeting)
    else:
        answer_parts.append(get_factual_answer(query))

    answer = "\n\n".join(answer_parts)

    st.session_state.history.append((query, answer))

# -------------------------
# Display chat
# -------------------------
for q, a in st.session_state.history:
    st.markdown(f"**🧑 You:** {q}")
    st.markdown(f"**🤖 Bot:** {a}")