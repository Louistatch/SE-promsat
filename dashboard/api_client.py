"""
Client API pour communiquer avec le backend Django ProSMAT
"""
import requests
import streamlit as st
from typing import Optional, Dict, Any, List

API_BASE = st.secrets.get("API_BASE_URL", "http://localhost:8000/api")


def _headers(token: str) -> Dict:
    return {"Authorization": f"Token {token}", "Content-Type": "application/json"}


def login(username: str, password: str) -> Optional[str]:
    """Retourne le token si succès, None sinon."""
    try:
        r = requests.post(
            f"{API_BASE.replace('/api', '')}/api/auth/token/",
            json={"username": username, "password": password},
            timeout=10,
        )
        if r.status_code == 200:
            return r.json().get("token")
    except requests.RequestException:
        pass
    return None


def get(endpoint: str, token: str, params: Dict = None) -> Optional[Any]:
    try:
        r = requests.get(
            f"{API_BASE}/{endpoint}",
            headers=_headers(token),
            params=params or {},
            timeout=15,
        )
        if r.status_code == 200:
            return r.json()
    except requests.RequestException:
        pass
    return None


def post(endpoint: str, token: str, data: Dict) -> Optional[Any]:
    try:
        r = requests.post(
            f"{API_BASE}/{endpoint}",
            headers=_headers(token),
            json=data,
            timeout=15,
        )
        if r.status_code in (200, 201):
            return r.json()
        return {"error": r.json(), "status": r.status_code}
    except requests.RequestException as e:
        return {"error": str(e)}


def patch(endpoint: str, token: str, data: Dict) -> Optional[Any]:
    try:
        r = requests.patch(
            f"{API_BASE}/{endpoint}",
            headers=_headers(token),
            json=data,
            timeout=15,
        )
        if r.status_code == 200:
            return r.json()
    except requests.RequestException:
        pass
    return None


# ── Helpers métier ──────────────────────────────────────────────────────────

def fetch_stats(token: str) -> Dict:
    return get("statistiques/", token) or {}


def fetch_indicateurs(token: str) -> List:
    data = get("indicateurs/?page_size=200", token)
    if isinstance(data, dict):
        return data.get("results", [])
    return data or []


def fetch_periodes(token: str) -> List:
    data = get("periodes/", token)
    if isinstance(data, dict):
        return data.get("results", [])
    return data or []


def fetch_realisations(token: str, params: Dict = None) -> List:
    data = get("realisations/?page_size=500", token, params)
    if isinstance(data, dict):
        return data.get("results", [])
    return data or []


def fetch_alertes(token: str) -> List:
    data = get("alertes/?page_size=200", token)
    if isinstance(data, dict):
        return data.get("results", [])
    return data or []


def fetch_activites(token: str) -> List:
    data = get("activites/?page_size=200", token)
    if isinstance(data, dict):
        return data.get("results", [])
    return data or []


def fetch_synthese(token: str) -> List:
    data = get("synthese-nationale/", token)
    if isinstance(data, dict):
        return data.get("results", [])
    return data or []


def create_realisation(token: str, payload: Dict) -> Dict:
    return post("realisations/", token, payload) or {}


def valider_realisation(token: str, pk: int) -> Dict:
    return post(f"realisations/{pk}/valider/", token, {}) or {}


def resoudre_alerte(token: str, pk: int) -> Dict:
    return post(f"alertes/{pk}/resoudre/", token, {}) or {}
