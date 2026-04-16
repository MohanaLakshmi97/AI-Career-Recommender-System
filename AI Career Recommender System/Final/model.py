import pandas as pd

# -------------------------
# LOAD CSV SAFELY (FIXED)
# -------------------------
skill_desc_data = pd.read_csv("data/skill_descriptions.csv")


# -------------------------
# MATCH SCORE (UNCHANGED)
# -------------------------
def calculate_match_score(student_skills, job_skills):
    student_skills = {s.strip().lower() for s in student_skills.replace(",", ";").split(";")}
    job_skills = {s.strip().lower() for s in job_skills.split(";")}

    if not job_skills:
        return 0

    return len(student_skills & job_skills) / len(job_skills)


# -------------------------
# MISSING SKILLS (UNCHANGED)
# -------------------------
def get_missing_skills(student_skills, job_skills):
    student_skills = {s.strip().lower() for s in student_skills.replace(",", ";").split(";")}
    job_skills = {s.strip().lower() for s in job_skills.split(";")}
    return list(job_skills - student_skills)


# -------------------------
# LEARNING RESOURCES (UNCHANGED)
# -------------------------
def get_learning_resources(missing_skills, resource_df, grouped=False):
    resources = {}

    for skill in missing_skills:
        matches = resource_df[
            resource_df["Skill"].fillna("").str.lower() == skill.lower()
        ]

        if not matches.empty:
            links = matches["Resources"].values[0].split(",")
            resources[skill] = [link.strip() for link in links if link.strip()]

    return resources if not grouped else {"All": resources}


# -------------------------
# SKILL DESCRIPTION (FIXED SAFELY)
# -------------------------
def get_skill_description(skill, skill_desc_df=skill_desc_data):

    if skill is None:
        return "Skill information will be updated soon."

    skill = str(skill).lower().strip()

    # -------------------------
    # CSV LOOKUP (SAFE FIX)
    # -------------------------
    try:
        match = skill_desc_df[
            skill_desc_df["Skill"].fillna("").str.lower() == skill
        ]

        if not match.empty:
            return match["Description"].values[0]

    except Exception:
        pass  # prevent crash if CSV missing/invalid

    # -------------------------
    # FALLBACK DICTIONARY
    # -------------------------
    descriptions = {
        "python": "Popular programming language for data and software development.",
        "sql": "Used for managing and querying relational databases.",
        "excel": "Spreadsheet tool used for data organization and analysis.",
        "tableau": "Data visualization tool for BI and dashboards.",
        "tensorflow": "Open-source ML framework for deep learning.",
        "java": "Widely used programming language for backend and app development.",
        "spring": "Java framework for building web applications.",
        "pandas": "Python library for data analysis and manipulation.",
        "numpy": "Python library for numerical computations.",
        "html": "Standard markup language for creating web pages.",
        "css": "Stylesheet language used to describe the look of a webpage.",
        "javascript": "Scripting language for interactive web applications.",
        "react": "JavaScript library for building user interfaces.",
        "node.js": "Backend JavaScript runtime environment.",
        "mongodb": "NoSQL database used for scalable applications.",
        "aws": "Cloud computing platform by Amazon.",
        "linux": "Open-source operating system widely used in servers.",
        "docker": "Tool for containerizing applications.",
        "kubernetes": "System for managing containerized applications.",
        "git": "Version control system for tracking code changes.",
        "ci/cd": "Automation process for software development and deployment.",
        "power bi": "Microsoft tool for business intelligence dashboards.",
        "communication": "Ability to clearly express ideas and collaborate.",
        "spark": "Big data processing framework.",
        "etl": "Process of extracting, transforming, and loading data.",
        "selenium": "Automation tool for testing web applications.",
        "figma": "UI/UX design and prototyping tool."
    }

    return descriptions.get(skill, "Skill information will be updated soon.")