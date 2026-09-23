"""
SRS §8.4 — Faz 1 demo başarı senaryosu, uçtan uca (gerçek JWT girişi, gerçek içerik dosyaları,
sahte LLM). Adım numaraları SRS'teki numaralarla aynıdır.
"""
import json
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core import auth, logger
from app.content import progress_store as ps
from app.llm.mock_adapter import MockAdapter
from app.models.user import UserCreate, UserRole
from app.api import chat as chat_api, tasks as tasks_api, proficiency as prof_api, progress as progress_api

OUT_OF_SCOPE = "Docker is ... Bu bilgi şirket dökümanlarından değil, genel teknik bilgimden geliyor."
QUIZ = json.dumps({"questions": [
    {"question": f"Q{i}", "options": ["a", "b", "c", "d"], "correct_index": 1} for i in range(4)
]})


@pytest.fixture
def demo(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "USERS_FILE", str(tmp_path / "users.json"))
    monkeypatch.setattr(ps, "DATA_DIR", str(tmp_path))
    monkeypatch.setattr(logger, "_LOG_FILE", str(tmp_path / "app.log"))
    monkeypatch.setattr(chat_api, "check_llm_rate_limit", lambda uid: None)
    chat_api._sessions.clear()
    mock = MockAdapter()
    for mod in (chat_api, tasks_api, prof_api, progress_api):
        monkeypatch.setattr(mod, "get_llm_adapter", lambda m=mock: m)
    auth.create_user(UserCreate(first_name="Admin", last_name="TechNova", username="admin", password="admin123",
                                area="backend", experience_level="senior", language="tr", role=UserRole.admin))
    return TestClient(app), mock


def _login(client, username, password):
    r = client.post("/auth/login", json={"username": username, "password": password})
    assert r.status_code == 200
    return r.json(), {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_phase1_demo_scenario(demo):
    client, mock = demo

    # 1. Yönetici sisteme giriş yapar
    admin, admin_h = _login(client, "admin", "admin123")

    # 2. Yeni çalışan profili oluşturur (Ayşe Kaya, Backend, Junior, "Python biliyor, Docker bilmiyor")
    r = client.post("/auth/users", headers=admin_h, json={
        "first_name": "Ayşe", "last_name": "Kaya", "username": "ayse", "password": "pw12345",
        "area": "backend", "experience_level": "junior", "language": "tr",
        "notes": [{"key": "Python", "value": "biliyor"}, {"key": "Docker", "value": "bilmiyor"}],
    })
    assert r.status_code == 200

    # 3. Çalışan sisteme giriş yapar, adıyla karşılanır
    login, h = _login(client, "ayse", "pw12345")
    assert login["user"]["first_name"] == "Ayşe"
    ayse_id = login["user"]["id"]
    path = client.get("/tasks/learning-path", headers=h).json()
    assert any("Docker" in p["task"]["title"] for p in path)

    # 4-5. "Docker bilmiyorum" notuna itiraz eder, sistem Docker yeterlilik testi başlatır
    mock.reply = QUIZ
    quiz = client.post("/proficiency/generate", headers=h, json={"note_key": "Docker"}).json()
    assert len(quiz["questions"]) == 4

    # 6. Çalışan testi geçer → Docker görevi öğrenme yolundan çıkar
    r = client.post("/proficiency/submit", headers=h, json={
        "note_key": "Docker", "answers": [1, 1, 1, 1], "questions": quiz["questions"]}).json()
    assert r["passed"] is True
    path = client.get("/tasks/learning-path", headers=h).json()
    assert not any("Docker" in p["task"]["title"] for p in path)
    assert client.get("/auth/me", headers=h).json()["notes"][1]["verified"] is True

    # 7. Öğrenme yolunda ilerler, göreve soru sorar
    first = path[0]["task"]["id"]
    mock.reply = "Şirketimiz mikroservis mimarisi kullanır."
    r = client.post("/chat", headers=h, json={"message": "Mimari nedir?", "task_id": first})
    assert r.status_code == 200

    # 8. Kapsam içi soruya md'den yanıt verilir (kaynak notu yok)
    assert "genel teknik bilgimden" not in r.json()["reply"]
    assert "Şirketimiz" in mock.calls[-1]["system_prompt"] or "TechNova" in mock.calls[-1]["system_prompt"]

    # 9. Kapsam dışı ama alakalı soruya kendi bilgisiyle yanıt verir
    mock.reply = OUT_OF_SCOPE
    client.post("/chat", headers=h, json={"message": "Kubernetes nedir?"})
    assert any(g.signal == "out_of_scope" for g in ps.get_gaps(ayse_id))

    # 10. Bir görevi tamamlar, LLM çıktıyı değerlendirir
    mock.reply = '{"passed": true, "feedback": "Doğru."}'
    r = client.post("/tasks/complete", headers=h, json={"task_id": first, "user_output": "3 bileşen: ...", "elapsed_minutes": 30}).json()
    assert r["passed"] is True and r["next_task_id"]

    # 11. İlerleme ekranında tamamlanan görev ve yüzde güncellenir
    stats = client.get("/tasks/stats", headers=h).json()
    assert stats["completed"] == 1 and stats["completion_percentage"] > 0

    # 12. Oturum özeti LLM tarafından üretilir
    mock.reply = "Bugün mimariyi öğrendin."
    assert client.post("/progress/me/session-summary", headers=h).json()["summary"] == "Bugün mimariyi öğrendin."

    # 13. Yönetici panelinden çalışanın ilerleme raporu görüntülenir
    rep = client.get(f"/progress/admin/{ayse_id}", headers=admin_h).json()
    assert rep["stats"]["completed"] == 1
    assert rep["stats"]["total"] == len(path)
    assert any(g["signal"] == "out_of_scope" for g in rep["gaps"])
    assert rep["proficiency_tests"][0]["passed"] is True

    # Çalışan yönetici raporuna erişemez (NFR-2.5)
    assert client.get(f"/progress/admin/{ayse_id}", headers=h).status_code == 403
