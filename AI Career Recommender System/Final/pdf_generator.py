from fpdf import FPDF
import re

# -------------------------
# STRONG TEXT CLEANER (UNCHANGED)
# -------------------------
def clean_text(text):
    if not isinstance(text, str):
        text = str(text)

    replacements = {
        "•": "-",
        "✔": "-",
        "❌": "-",
        "✅": "-",
        "🌟": "",
        "🎉": "",
        "→": "->",
        "–": "-",
        "—": "-",
        "“": '"',
        "”": '"',
        "’": "'",
        "‘": "'",
        "₹": "Rs."
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    # FINAL SAFETY (VERY IMPORTANT)
    return text.encode("latin-1", "ignore").decode("latin-1")

# ======================================================
# CAREER REPORT PDF (UPGRADED UI - NO LOGIC REMOVED)
# ======================================================
def generate_pdf_report(
    name,
    top_result,
    missing_skills,
    skill_meanings=None,
    resources=None,
    other_roles=None,
    chart_path=None,
    explanation=None
):

    skill_meanings = skill_meanings or {}
    resources = resources or {}
    other_roles = other_roles or []

    pdf = FPDF()
    pdf.add_page()

    # -------------------------
    # HEADER (NEW PREMIUM)
    # -------------------------
    pdf.set_fill_color(142, 68, 173)
    pdf.set_text_color(255, 255, 255)

    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "AI Career Recommendation Report", ln=True, align='C', fill=True)

    pdf.ln(8)
    pdf.set_text_color(0, 0, 0)

    # -------------------------
    # USER DETAILS CARD
    # -------------------------
    pdf.set_fill_color(245, 245, 245)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "User Details", ln=True)

    pdf.set_font("Helvetica", size=12)

    pdf.multi_cell(0, 8, clean_text(
        f"Name: {name}\n"
        f"Top Career Role: {top_result[0]}\n"
        f"Match Score: {round(top_result[1]*100, 2)}%\n"
        f"Category: {top_result[2]}\n"
        f"Average Salary: Rs.{top_result[3]:,.0f}"
    ), fill=True)

    pdf.ln(5)

    # -------------------------
    # WHY THIS CAREER
    # -------------------------
    if explanation:
        pdf.set_text_color(142, 68, 173)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Why this career?", ln=True)

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", size=12)

        for line in explanation.split("\n"):
            if line.strip():
                line = line.replace("**", "")
                pdf.multi_cell(0, 8, clean_text(line))

        pdf.ln(5)

    # -------------------------
    # MISSING SKILLS
    # -------------------------
    if missing_skills:
        pdf.set_text_color(142, 68, 173)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Skills to Improve", ln=True)

        pdf.set_text_color(0, 0, 0)

        for skill in missing_skills:
            meaning = skill_meanings.get(skill.lower(), "Basic understanding required")

            pdf.multi_cell(
                0, 8,
                clean_text(f"• {skill.title()}: {meaning}")
            )
            pdf.ln(1)

        pdf.ln(5)

    # -------------------------
    # LEARNING RESOURCES
    # -------------------------
    if resources:
        pdf.set_text_color(142, 68, 173)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Learning Resources", ln=True)

        pdf.set_text_color(0, 0, 0)

        for skill, links in resources.items():
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 8, clean_text(skill.title()), ln=True)

            pdf.set_font("Helvetica", size=11)
            for link in links:
                pdf.set_text_color(0, 0, 255)
                pdf.multi_cell(0, 8, clean_text(link))
                pdf.set_text_color(0, 0, 0)

        pdf.ln(5)

    # -------------------------
    # OTHER MATCHES
    # -------------------------
    if other_roles:
        pdf.set_text_color(142, 68, 173)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, clean_text("Other Career Matches"), ln=True)

        pdf.set_text_color(0, 0, 0)

        for role, score in other_roles:
            pdf.cell(0, 8, clean_text(f"- {role} ({score}%)"), ln=True)

        pdf.ln(5)

    # -------------------------
    # MATCH CHART
    # -------------------------
    if chart_path:
        try:
            pdf.set_text_color(142, 68, 173)
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, "Match Chart", ln=True)

            pdf.ln(2)
            pdf.image(chart_path, x=10, w=180)
            pdf.ln(5)
        except:
            pdf.cell(0, 8, "Chart could not be loaded.", ln=True)

    # -------------------------
    # FOOTER MESSAGE
    # -------------------------
    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(100, 100, 100)

    pdf.multi_cell(0, 8, clean_text(
        "This report is generated using an AI-based Career Recommendation System. "
        "Continue building your skills, stay consistent, and work towards your professional goals. "
        "Success comes with continuous learning and practical experience."
    ))

    # Save
    safe_name = re.sub(r'\W+', '_', name)
    file_path = f"{safe_name}_career_report.pdf"
    pdf.output(file_path)

    return file_path


# ======================================================
# SKILL PLAN PDF (UNCHANGED)
# ======================================================
def generate_skill_plan_pdf(
    name,
    dream_role,
    existing_skills,
    missing_skills,
    resources,
    skill_desc_map=None
):

    pdf = FPDF()
    pdf.add_page()

    # -------------------------
    # HEADER (PREMIUM STYLE)
    # -------------------------
    pdf.set_fill_color(142, 68, 173)
    pdf.set_text_color(255, 255, 255)

    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "AI Skill Development Report", ln=True, align='C', fill=True)

    pdf.ln(8)
    pdf.set_text_color(0, 0, 0)

    # -------------------------
    # USER DETAILS
    # -------------------------
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "User Details", ln=True)

    pdf.set_font("Helvetica", "", 12)

    pdf.multi_cell(0, 8, clean_text(
        f"Name: {name}\n"
        f"Target Role: {dream_role}"
    ))

    pdf.ln(5)

    # -------------------------
    # SKILL SUMMARY
    # -------------------------
    pdf.set_text_color(142, 68, 173)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Skill Summary", ln=True)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 12)

    pdf.multi_cell(
        0, 8,
        clean_text(f"✔ Existing Skills: {', '.join(existing_skills) if existing_skills else 'None'}")
    )

    pdf.multi_cell(
        0, 8,
        clean_text(f"⚠ Missing Skills: {', '.join(missing_skills) if missing_skills else 'None'}")
    )

    pdf.ln(5)

    # -------------------------
    # SKILL GAP (FIXED FORMAT)
    # -------------------------
    if missing_skills:
        pdf.set_text_color(142, 68, 173)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Skills to Learn", ln=True)

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "", 12)

        for skill in missing_skills:
            desc = skill_desc_map.get(skill.strip().lower(), "Description not available")
            pdf.multi_cell(0, 8, clean_text(f"• {skill}: {desc}"))

        pdf.ln(5)

    # -------------------------
    # LEARNING RESOURCES
    # -------------------------
    if resources:
        pdf.set_text_color(142, 68, 173)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Learning Resources", ln=True)

        pdf.set_text_color(0, 0, 0)

        for skill, links in resources.items():
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 8, clean_text(skill), ln=True)

            pdf.set_font("Helvetica", "", 11)
            for link in links:
                pdf.set_text_color(0, 0, 255)
                pdf.multi_cell(0, 7, clean_text(link))
                pdf.set_text_color(0, 0, 0)

        pdf.ln(5)

    # -------------------------
    # ROADMAP
    # -------------------------
    pdf.set_text_color(142, 68, 173)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Career Roadmap", ln=True)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 11)

    roadmap = [
        "Learn missing skills step by step",
        "Build small projects using these skills",
        "Upload projects to GitHub",
        "Apply skills in real-world scenarios",
        "Prepare for internships and interviews"
    ]

    for step in roadmap:
        pdf.multi_cell(0, 7, clean_text(f"• {step}"))

    pdf.ln(6)

    # -------------------------
    # FOOTER
    # -------------------------
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(120, 120, 120)

    pdf.multi_cell(
        0, 6,
        clean_text("This report is generated by AI Career Recommender System. Keep learning and growing 🚀")
    )

    # -------------------------
    # SAVE FILE
    # -------------------------
    safe_name = re.sub(r'\W+', '_', name)
    path = f"{safe_name}_skill_plan.pdf"
    pdf.output(path)

    return path