import hashlib, os, re
from PyPDF2 import PdfReader

def extract_text_from_pdf(path):
    try:
        reader = PdfReader(path)
        texts = []
        for p in reader.pages:
            try:
                texts.append(p.extract_text() or "")
            except Exception:
                pass
        return "\n".join(texts)
    except Exception:
        with open(path, "rb") as f:
            return f.read().decode(errors="ignore")

def normalize_text(t):
    t = t.lower().strip()
    t = re.sub(r"\s+", " ", t)
    return t

def fingerprint_text(text, salt="sourcematch_salt"):
    hasher = hashlib.sha256()
    hasher.update((salt + normalize_text(text)).encode("utf-8"))
    return hasher.hexdigest()

def extract_text_and_fingerprint(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        text = extract_text_from_pdf(path)
    else:
        # Try common encodings for text files (utf-8, utf-16, latin-1). Some
        # uploaded resumes may be UTF-16 (Windows) which shows up as NUL bytes
        # when decoded with utf-8. Try decodings in order and pick the one that
        # yields readable text.
        raw = None
        with open(path, "rb") as f:
            raw = f.read()
        text = None
        for enc in ("utf-8", "utf-16", "latin-1"):
            try:
                candidate = raw.decode(enc)
                # heuristic: if text contains NULs it's likely wrong decoding
                if candidate.count("\x00") > 0:
                    continue
                text = candidate
                break
            except Exception:
                continue
        if text is None:
            # fallback: decode ignoring errors
            text = raw.decode("utf-8", errors="ignore")
    fingerprint = fingerprint_text(text)
    return text, fingerprint
