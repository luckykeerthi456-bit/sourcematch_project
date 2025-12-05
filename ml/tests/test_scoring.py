import pytest
import sys
from pathlib import Path

# Add parent directory to path so we can import ml.scoring_service
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ml.scoring_service import score_job_application

def test_score_basic():
    job = {"description": "React developer with Docker and Node.js", "requirements": {"required_skills":["React","Docker","Node.js"], "min_experience":2}}
    application = {"resume_text": "Experienced React developer with 3 years experience using React and Docker and Node.js"}
    score, explanation = score_job_application(job, application)
    assert score > 50
    assert 'embedding_similarity' in explanation
    assert isinstance(explanation['matched_skills'], list)

if __name__ == '__main__':
    test_score_basic()
    print('ok')
