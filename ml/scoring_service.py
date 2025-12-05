# Simple ML scoring service using sentence-transformers
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

# Lazy load model (downloads on first use, not on import)
MODEL_NAME = "all-MiniLM-L6-v2"
model = None

def get_model():
    """Lazy-load the embedding model on first use."""
    global model
    if model is None:
        print("Loading embedding model:", MODEL_NAME)
        model = SentenceTransformer(MODEL_NAME)
    return model

def embed(text):
    if not text or len(text.strip()) == 0:
        return np.zeros(384)
    m = get_model()
    return m.encode([text], convert_to_numpy=True)[0]

def extract_skills_from_text(text):
    # Legacy: not used directly. Keep for compatibility.
    tokens = re.split(r"[^A-Za-z+#]+", text or "")
    tokens = [t.strip() for t in tokens if len(t) > 1]
    return list({t.lower() for t in tokens[:500]})

def exp_years_match(min_years, application):
    # Improved heuristic: find numeric years, ranges like 2018-2021, '4+ years',
    # and basic word-number forms (one, two, three... up to ten).
    text = (application.get("resume_text", "") or "").lower()
    # quick numeric match
    m = re.search(r"(\d{1,2})\s*\+?\s*years?", text)
    if m:
        try:
            years = int(m.group(1))
            return min(1.0, years / max(1, min_years)) if min_years > 0 else 1.0
        except:
            pass
    # year range like 2018-2021 -> estimate diff
    m = re.search(r"(20\d{2})\s*[-–]\s*(20\d{2})", text)
    if m:
        try:
            years = int(m.group(2)) - int(m.group(1))
            years = max(0, years)
            return min(1.0, years / max(1, min_years)) if min_years > 0 else 1.0
        except:
            pass
    # basic word-number mapping
    words = {
        'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10
    }
    for w, val in words.items():
        if re.search(rf"\b{w}\s+years?\b", text):
            years = val
            return min(1.0, years / max(1, min_years)) if min_years > 0 else 1.0
    return 0.0


def normalize_text_for_matching(text: str) -> str:
    # lowercase and replace punctuation with spaces so 'node.js' and 'node js' match
    s = (text or "").lower()
    s = re.sub(r"[\W_]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def match_required_skills(required_skills, resume_text):
    """Return list of required skills that appear in resume_text.

    Matching strategy:
    - Normalize both skill and resume text (lowercase, remove punctuation).
    - Check for exact substring presence of normalized skill in normalized resume text.
    - Also check token-level presence for multi-word skills.
    """
    if not required_skills:
        return []
    norm_text = normalize_text_for_matching(resume_text)
    matches = []
    for skill in required_skills:
        if not skill:
            continue
        skill_norm = normalize_text_for_matching(skill)
        # direct substring match
        if skill_norm and skill_norm in norm_text:
            matches.append(skill)
            continue
        # token-level fallback: check all tokens of skill appear in text
        tokens = [t for t in skill_norm.split() if t]
        if tokens and all(token in norm_text.split() for token in tokens):
            matches.append(skill)
    return matches

def score_job_application(job, application):
    job_desc = job.get("description", "")
    resume_text = application.get("resume_text", "")

    job_vec = embed(job_desc)
    resume_vec = embed(resume_text)
    # cosine_similarity expects 2D array-like inputs; ensure vectors are 2D numpy arrays
    job_vec_2d = np.asarray(job_vec).reshape(1, -1)
    resume_vec_2d = np.asarray(resume_vec).reshape(1, -1)
    emb_sim = float(cosine_similarity(job_vec_2d, resume_vec_2d)[0][0])

    req_skills = job.get("requirements", {}).get("required_skills", []) or []
    matched = match_required_skills(req_skills, resume_text)
    skill_score = (len(matched) / max(1, len(req_skills))) if req_skills else 0.0

    experience_score = exp_years_match(job.get("requirements", {}).get("min_experience", 0), application)

    # composite score: weights chosen for prototype
    # All three scores are 0-1, so weighted sum should be 0-100 max
    composite = (emb_sim * 0.40) + (skill_score * 0.35) + (experience_score * 0.25)
    # normalize to 0-1 range for frontend percentage display
    composite = max(0.0, min(1.0, composite))
    explanation = {
        "embedding_similarity": emb_sim,
        "matched_skills": matched,
        "skill_score": skill_score,
        "experience_score": experience_score,
        "reasons": []
    }
    if skill_score < 0.5 and req_skills:
        explanation["reasons"].append("Missing several required skills")
    if emb_sim < 0.45:
        explanation["reasons"].append("Low semantic similarity between resume and job description")
    if experience_score < 0.5 and job.get("requirements", {}).get("min_experience", 0) > 0:
        explanation["reasons"].append("Insufficient apparent experience")
    return composite, explanation

if __name__ == "__main__":
    # simple manual test
    job = {"description": "Looking for a React developer with 3+ years experience and knowledge of Docker and Node.js", "requirements": {"required_skills": ["React","Docker","Node.js"], "min_experience": 3}}
    application = {"resume_text": "Experienced React developer with 4 years of hands-on experience building web apps using React, Node.js and Docker"}
    score, explanation = score_job_application(job, application)
    print("SCORE:", score)
    print("EXPLANATION:", explanation)
