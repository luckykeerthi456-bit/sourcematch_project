# Simple ML scoring service using sentence-transformers
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
import os
import json

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


def _read_threshold_from_settings():
    # try backend settings file first (backend/semantic_settings.json)
    try:
        settings_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "semantic_settings.json"))
        if os.path.exists(settings_path):
            with open(settings_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return float(data.get("skill_threshold", 0.62))
    except Exception:
        pass
    # fallback to env var
    try:
        return float(os.getenv("SKILL_SIM_THRESHOLD", 0.62))
    except Exception:
        return 0.62


def match_required_skills(required_skills, resume_text, skill_embeddings=None):
    """Return list of required skills that semantically appear in resume_text.

    New strategy (semantic matching):
    - Prefer semantic similarity using sentence embeddings (embed).
      For each required skill phrase, compute embedding and compare with
      the resume embedding using cosine similarity. If similarity is above
      SKILL_SIM_THRESHOLD, consider it a match.
    - Fallback to legacy normalized substring/token checks for short-circuit
      or when the embedding model is not available.

    This allows matching equivalent phrases like "football" and "soccer player".
    """
    if not required_skills:
        return []

    # Normalize quick lookup text for fallback matching
    norm_text = normalize_text_for_matching(resume_text)
    matches = []

    # Pre-compute resume embedding once for efficiency when using semantic match
    resume_vec = None
    model_available = True
    try:
        resume_vec = embed(resume_text)
        resume_vec = np.asarray(resume_vec).reshape(1, -1)
    except Exception:
        # If embedding model fails to load for any reason, we'll fallback
        resume_vec = None
        model_available = False

    # similarity threshold for skill <-> resume matching (0-1)
    SKILL_SIM_THRESHOLD = _read_threshold_from_settings()

    # If skill_embeddings provided, prefer using them to avoid recomputing embeddings
    use_precomputed = skill_embeddings is not None and isinstance(skill_embeddings, (list, tuple)) and len(skill_embeddings) > 0

    for idx, skill in enumerate(required_skills):
        if not skill:
            continue
        # 1) Semantic matching using precomputed embedding if available
        matched = False
        if use_precomputed and idx < len(skill_embeddings):
            try:
                se = np.asarray(skill_embeddings[idx]).reshape(1, -1)
                sim = float(cosine_similarity(se, resume_vec)[0][0]) if model_available and resume_vec is not None else 0.0
                if sim >= SKILL_SIM_THRESHOLD:
                    matches.append(skill)
                    matched = True
            except Exception:
                matched = False

        # 2) If not matched and model available, compute on-the-fly embedding for this skill
        if not matched and model_available and resume_vec is not None:
            try:
                skill_vec = embed(skill)
                skill_vec = np.asarray(skill_vec).reshape(1, -1)
                sim = float(cosine_similarity(skill_vec, resume_vec)[0][0])
                if sim >= SKILL_SIM_THRESHOLD:
                    matches.append(skill)
                    matched = True
            except Exception:
                matched = False

        if matched:
            continue

        # 3) Legacy fallback: normalized substring or token-level check
        skill_norm = normalize_text_for_matching(skill)
        if skill_norm and skill_norm in norm_text:
            matches.append(skill)
            continue
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
    skill_embeddings = job.get("skill_embeddings", None)
    matched = match_required_skills(req_skills, resume_text, skill_embeddings)
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


def explain_job_application(job, application):
    """Return a detailed explainability report for why a resume scored as it did for a job.

    The report includes per-skill similarity scores (semantic if available),
    match method (semantic precomputed / semantic on-the-fly / substring),
    tokens matched, and the contribution of each component to the final score.
    """
    job_desc = job.get("description", "")
    resume_text = application.get("resume_text", "")

    # Compute job and resume embeddings (best-effort)
    try:
        job_vec = embed(job_desc)
        job_vec_2d = np.asarray(job_vec).reshape(1, -1)
    except Exception:
        job_vec_2d = None
    try:
        resume_vec = embed(resume_text)
        resume_vec_2d = np.asarray(resume_vec).reshape(1, -1)
    except Exception:
        resume_vec_2d = None

    emb_sim = 0.0
    if job_vec_2d is not None and resume_vec_2d is not None:
        emb_sim = float(cosine_similarity(job_vec_2d, resume_vec_2d)[0][0])

    req_skills = job.get("requirements", {}).get("required_skills", []) or []
    skill_embeddings = job.get("skill_embeddings", None)

    # Skill-level details
    per_skill = []
    # Precompute normalized resume text for substring matches
    norm_text = normalize_text_for_matching(resume_text)
    resume_vec_for_sim = None
    try:
        resume_vec_for_sim = resume_vec_2d
    except Exception:
        resume_vec_for_sim = None

    SKILL_SIM_THRESHOLD = _read_threshold_from_settings()
    use_precomputed = skill_embeddings is not None and isinstance(skill_embeddings, (list, tuple)) and len(skill_embeddings) > 0

    for idx, skill in enumerate(req_skills):
        detail = {"skill": skill, "matched": False, "method": None, "similarity": None, "tokens_matched": []}
        if not skill:
            per_skill.append(detail)
            continue

        # Try precomputed semantic
        sim = None
        if use_precomputed and idx < len(skill_embeddings) and resume_vec_for_sim is not None:
            try:
                se = np.asarray(skill_embeddings[idx]).reshape(1, -1)
                sim = float(cosine_similarity(se, resume_vec_for_sim)[0][0])
                detail["similarity"] = sim
                if sim >= SKILL_SIM_THRESHOLD:
                    detail["matched"] = True
                    detail["method"] = "semantic_precomputed"
            except Exception:
                sim = None

        # On-the-fly semantic
        if not detail["matched"] and sim is None and resume_vec_for_sim is not None:
            try:
                skill_vec = embed(skill)
                skill_vec = np.asarray(skill_vec).reshape(1, -1)
                sim = float(cosine_similarity(skill_vec, resume_vec_for_sim)[0][0])
                detail["similarity"] = sim
                if sim >= SKILL_SIM_THRESHOLD:
                    detail["matched"] = True
                    detail["method"] = "semantic_on_the_fly"
            except Exception:
                pass

        # Legacy substring/token fallback
        if not detail["matched"]:
            skill_norm = normalize_text_for_matching(skill)
            if skill_norm and skill_norm in norm_text:
                detail["matched"] = True
                detail["method"] = "substring"
                detail["tokens_matched"] = [skill_norm]
            else:
                tokens = [t for t in skill_norm.split() if t]
                matched_tokens = [t for t in tokens if t in norm_text.split()]
                if tokens and len(matched_tokens) == len(tokens):
                    detail["matched"] = True
                    detail["method"] = "tokens_all"
                    detail["tokens_matched"] = matched_tokens
                elif matched_tokens:
                    # partial token match
                    detail["tokens_matched"] = matched_tokens

        per_skill.append(detail)

    matched_skills = [d["skill"] for d in per_skill if d["matched"]]
    skill_score = (len(matched_skills) / max(1, len(req_skills))) if req_skills else 0.0
    experience_score = exp_years_match(job.get("requirements", {}).get("min_experience", 0), application)

    # Composite breakdown
    weights = {"embedding": 0.40, "skills": 0.35, "experience": 0.25}
    emb_contrib = emb_sim * weights["embedding"]
    skills_contrib = skill_score * weights["skills"]
    exp_contrib = experience_score * weights["experience"]
    composite = emb_contrib + skills_contrib + exp_contrib
    composite = max(0.0, min(1.0, composite))

    report = {
        "composite_score": composite,
        "components": {
            "embedding_similarity": {"value": emb_sim, "weight": weights["embedding"], "contribution": emb_contrib},
            "skill_score": {"value": skill_score, "weight": weights["skills"], "contribution": skills_contrib},
            "experience_score": {"value": experience_score, "weight": weights["experience"], "contribution": exp_contrib},
        },
        "per_skill": per_skill,
        "matched_skills": matched_skills,
        "settings": {"skill_similarity_threshold": SKILL_SIM_THRESHOLD}
    }

    return report

if __name__ == "__main__":
    # simple manual test
    job = {"description": "Looking for a React developer with 3+ years experience and knowledge of Docker and Node.js", "requirements": {"required_skills": ["React","Docker","Node.js"], "min_experience": 3}}
    application = {"resume_text": "Experienced React developer with 4 years of hands-on experience building web apps using React, Node.js and Docker"}
    score, explanation = score_job_application(job, application)
    print("SCORE:", score)
    print("EXPLANATION:", explanation)
