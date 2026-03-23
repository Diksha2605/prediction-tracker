import httpx
import streamlit as st

BASE_URL = "http://localhost:8000"
TIMEOUT  = 10.0


def get_headers():
    token = st.session_state.get("token", "")
    return {"Authorization": f"Bearer {token}"}


def register(name, email, password):
    try:
        r = httpx.post(f"{BASE_URL}/api/users/register",
                       json={"name": name, "email": email, "password": password},
                       timeout=TIMEOUT)
        return r.json(), r.status_code
    except Exception as e:
        return {"detail": f"Cannot connect to server. Is FastAPI running? ({e})"}, 503


def login(email, password):
    try:
        r = httpx.post(f"{BASE_URL}/api/users/login",
                       json={"email": email, "password": password},
                       timeout=TIMEOUT)
        return r.json(), r.status_code
    except Exception as e:
        return {"detail": f"Cannot connect to server. Is FastAPI running? ({e})"}, 503


def get_predictions(status=None, category=None):
    try:
        params = {}
        if status:   params["status"]   = status
        if category: params["category"] = category
        r = httpx.get(f"{BASE_URL}/api/predictions",
                      headers=get_headers(), params=params, timeout=TIMEOUT)
        return r.json() if r.status_code == 200 else []
    except Exception:
        return []


def create_prediction(title, notes, deadline, confidence, category):
    try:
        payload = {
            "title":              title,
            "notes":              notes,
            "deadline":           str(deadline) if deadline else None,
            "initial_confidence": confidence,
            "category":           category or None,
        }
        r = httpx.post(f"{BASE_URL}/api/predictions",
                       headers=get_headers(), json=payload, timeout=TIMEOUT)
        return r.json(), r.status_code
    except Exception as e:
        return {"detail": str(e)}, 503


def get_prediction(prediction_id):
    try:
        r = httpx.get(f"{BASE_URL}/api/predictions/{prediction_id}",
                      headers=get_headers(), timeout=TIMEOUT)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def update_confidence(prediction_id, confidence, note):
    try:
        r = httpx.post(
            f"{BASE_URL}/api/predictions/{prediction_id}/confidence",
            headers=get_headers(),
            json={"confidence": confidence, "note": note},
            timeout=TIMEOUT)
        return r.json(), r.status_code
    except Exception as e:
        return {"detail": str(e)}, 503


def resolve_prediction(prediction_id, status):
    try:
        r = httpx.patch(
            f"{BASE_URL}/api/predictions/{prediction_id}",
            headers=get_headers(),
            json={"status": status},
            timeout=TIMEOUT)
        return r.json(), r.status_code
    except Exception as e:
        return {"detail": str(e)}, 503


def delete_prediction(prediction_id):
    try:
        r = httpx.delete(
            f"{BASE_URL}/api/predictions/{prediction_id}",
            headers=get_headers(), timeout=TIMEOUT)
        return r.status_code
    except Exception:
        return 503


def get_calibration():
    try:
        r = httpx.get(f"{BASE_URL}/api/analytics/calibration",
                      headers=get_headers(), timeout=TIMEOUT)
        return r.json() if r.status_code == 200 else {}
    except Exception:
        return {}


def get_bias_report():
    try:
        r = httpx.get(f"{BASE_URL}/api/analytics/bias",
                      headers=get_headers(), timeout=TIMEOUT)
        return r.json() if r.status_code == 200 else {}
    except Exception:
        return {}


def get_decay_curve(prediction_id):
    try:
        r = httpx.get(f"{BASE_URL}/api/analytics/decay/{prediction_id}",
                      headers=get_headers(), timeout=TIMEOUT)
        return r.json() if r.status_code == 200 else {}
    except Exception:
        return {}