"""
Client API pour communiquer avec le backend Django ProSMAT
"""
import requests
import streamlit as st
from typing import Optional, Dict, Any, List

API_BASE = st.secrets.get("API_BASE_URL", "http://localhost:8000/api")
BASE_URL  = API_BASE.replace("/api", "")


def _headers(token: str) -> Dict:
    return {"Authorization": f"Token {token}", "Content-Type": "application/json"}


def check_backend() -> bool:
    """Vérifie que le backend Django est accessible."""
    try:
        r = requests.get(f"{BASE_URL}/api/auth/token/", timeout=3)
        return r.status_code in (200, 400, 405)  # 400/405 = endpoint existe mais mauvaise méthode
    except requests.RequestException:
        return False


def login(username: str, password: str) -> Optional[str]:
    """Retourne le token si succès, None sinon."""
    try:
        r = requests.post(
            f"{BASE_URL}/api/auth/token/",
            json={"username": username, "password": password},
            timeout=10,
        )
        if r.status_code == 200:
            return r.json().get("token")
    except requests.RequestException:
        pass
    return None


def login_full(username: str, password: str) -> Dict:
    """Login complet — retourne token + infos utilisateur."""
    try:
        r = requests.post(
            f"{BASE_URL}/api/auth/token/",
            json={"username": username, "password": password},
            timeout=10,
        )
        if r.status_code == 200:
            token = r.json().get("token")
            # Récupérer les infos user
            user_info = {"username": username, "role": "—", "region": "—"}
            try:
                ru = requests.get(
                    f"{API_BASE}/users/me/",
                    headers=_headers(token),
                    timeout=5,
                )
                if ru.status_code == 200:
                    d = ru.json()
                    user_info = {
                        "username":   d.get("username", username),
                        "full_name":  f"{d.get('first_name','')} {d.get('last_name','')}".strip() or username,
                        "email":      d.get("email", ""),
                        "role":       d.get("role", "—"),
                        "region":     d.get("region", "—"),
                    }
            except Exception:
                pass
            return {"success": True, "token": token, "user": user_info}
        elif r.status_code == 400:
            return {"success": False, "message": "Identifiants incorrects."}
        else:
            return {"success": False, "message": f"Erreur serveur ({r.status_code})."}
    except requests.ConnectionError:
        return {"success": False, "message": "Impossible de joindre le serveur Django."}
    except requests.Timeout:
        return {"success": False, "message": "Le serveur met trop de temps à répondre."}
    except Exception as e:
        return {"success": False, "message": str(e)}


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
