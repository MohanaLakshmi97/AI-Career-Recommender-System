from sklearn.ensemble import RandomForestClassifier
import pandas as pd

# -------------------------
# TRAIN MODEL ONCE
# -------------------------
job_data = pd.read_csv("data/job_roles.csv")

all_skills = set()

for _, row in job_data.iterrows():
    for skill in row["Required Skills"].split(";"):
        all_skills.add(skill.strip().lower())

all_skills = sorted(all_skills)
skill_to_index = {skill: i for i, skill in enumerate(all_skills)}

X = []
y = []

for _, row in job_data.iterrows():
    vector = [0] * len(all_skills)

    for skill in row["Required Skills"].split(";"):
        vector[skill_to_index[skill.strip().lower()]] = 1

    # CGPA placeholder (important feature)
    vector.append(7.5)

    X.append(vector)
    y.append(row["Job Role"])

model = RandomForestClassifier()
model.fit(X, y)

# -------------------------
# PREDICTION FUNCTION
# -------------------------
def predict_career(skills, cgpa):

    input_vector = [0] * len(all_skills)

    for skill in skills.replace(",", ";").split(";"):
        skill = skill.strip().lower()
        if skill in skill_to_index:
            input_vector[skill_to_index[skill]] = 1

    input_vector.append(cgpa)

    return model.predict([input_vector])[0]