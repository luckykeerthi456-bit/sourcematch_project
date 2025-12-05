"""
Small helper script to import the ML scoring module and force the sentence-transformers
model to download into the cache. Run this once after installing ML dependencies to
avoid long downloads during backend startup.

Usage:
    python scripts/preload_model.py
"""

import time

print("Preloading ML model (this may take a few minutes)...")
try:
    from ml import scoring_service
    # scoring_service loads the model at import time; if it exposes the model
    # object we can reference it to ensure it's initialized.
    try:
        model = getattr(scoring_service, 'model', None)
        if model is not None:
            print("Model object loaded:", type(model))
        else:
            print("Model imported; scoring_service did not expose model object explicitly.")
    except Exception:
        pass
    print("Done. The model should be cached for future runs.")
except Exception as e:
    print("Failed to preload model:", e)
    raise

# small sleep to let any background downloads settle
time.sleep(0.5)
