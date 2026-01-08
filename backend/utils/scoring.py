# For prototype the scoring module calls ml.scoring_service directly.
try:
    from ml.scoring_service import score_job_application as ml_score
    from ml.scoring_service import explain_job_application as ml_explain
except ModuleNotFoundError:
    # If the package import fails (for example when running uvicorn from inside
    # the `backend/` directory), add the project root to sys.path so the
    # top-level `ml` package can be found. This keeps the prototype runnable
    # regardless of the current working directory.
    import sys, os
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from ml.scoring_service import score_job_application as ml_score
    from ml.scoring_service import explain_job_application as ml_explain


def score_job_application(job, application):
    return ml_score(job, application)


def explain_job_application(job, application):
    return ml_explain(job, application)
