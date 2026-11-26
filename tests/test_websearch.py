import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx
from fastapi.testclient import TestClient

from app import websearch
from app.main import app
from app.websearch import (WebSearchError, construire_requetes, domaine, extraire_prix,
                           parse_bing, parse_ddg, parse_mojeek, rechercher_web)

client = TestClient(app)

HTML_MOJEKK = """
<html><body><ul>
<li><h2><a href="https://www.fournisseur-a.example/produit/vt-40a">Disjoncteur VT-40A - Fournisseur A - 42,90 €</a></h2>
<p>En stock, livraison 24-48 h, DDP France.</p></li>
<li><h2><a href="https://www.fournisseur-b.example/vt-40a">VT-40A chez Fournisseur B</a></h2>
<p>Sur devis, délai 2 semaines.</p></li>
<li><h2><a href="https://www.mojeek.com/search?q=autre">Mojeek lui-même</a></h2><p>lien interne</p></li>
</ul></body></html>
"""

HTML_BING = """
<html><body><ol><li class="b_algo"><h2><a href="https://www.fournisseur-c.example/cat/vt40a">Acheter VT-40A - Fournisseur C</a></h2>
<p>Prix 38,50 EUR, franco de port.</p></li>
<li class="b_algo"><h2><a href="https://www.bing.com/search?q=x">Bing</a></h2><p>interne</p></li>
</ol></body></html>
"""

HTML_DDG = """
<html><body>
<div class="result"><a class="result__a" href="//duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.fournisseur-d.example%2Fvt40a&amp;rut=abc">VT-40A pas cher - Fournisseur D</a>
<div class="result__snippet">Stock important, 24,90 € TTC.</div></div>
</body></html>
"""


def test_domaine():
    assert domaine("https://www.rs-online.com/fr/x") == "rs-online.com"
    assert domaine("http://exemple.fr") == "exemple.fr"


def test_extraire_prix():
    assert extraire_prix("Prix : 42,90 € HT") == "42,90 €"
    assert extraire_prix("1 250,00 EUR") == "1250,00 €"
    assert extraire_prix("sur devis") is None


def test_parse_mojeek():
    res = parse_mojeek(HTML_MOJEKK)
    assert len(res) == 2
    assert res[0]["url"] == "https://www.fournisseur-a.example/produit/vt-40a"
    assert "Fournisseur A" in res[0]["titre"]


def test_parse_bing_exclut_moteur():
    res = parse_bing(HTML_BING)
    assert len(res) == 1
    assert res[0]["url"] == "https://www.fournisseur-c.example/cat/vt40a"


def test_parse_ddg_decode_uddg():
    res = parse_ddg(HTML_DDG)
    assert len(res) == 1
    assert res[0]["url"] == "https://www.fournisseur-d.example/vt40a"
    assert "24,90" in res[0]["extrait"]


def test_construire_requetes_france_avec_reference():
    reqs = construire_requetes(fabricant="Voltalis", reference="VT-40A", zone="france")
    assert any('"VT-40A"' in r and "prix" in r for r in reqs)
    assert any("livraison France" in r for r in reqs)
    assert len(reqs) <= 4


def test_construire_requetes_monde_sans_reference():
    reqs = construire_requetes(designation="roulement 6204", zone="monde")
    assert any("worldwide" in r for r in reqs)


def _faux_fetch(url):
    if "mojeek.com" in url:
        return HTML_MOJEKK
    if "bing.com" in url:
        return HTML_BING
    raise WebSearchError("connexion refusée")


def test_rechercher_web_avec_faux_fetch(monkeypatch):
    monkeypatch.setattr(websearch, "fetch_url", _faux_fetch)
    res = rechercher_web(fabricant="Voltalis", reference="VT-40A", zone="france")
    assert res["fetch_ok"] is True
    assert len(res["resultats"]) >= 2
    assert res["resultats"][0]["prix_indicatif"] == "42,90 €"
    assert all(r["domaine"] for r in res["resultats"])
    assert len(res["liens_navigateur"]) == len(res["requetes"])
    for bloc in res["liens_navigateur"]:
        noms = [n["nom"] for n in bloc["navigateurs"]]
        assert noms == ["Google", "Bing", "DuckDuckGo"]
        assert all(n["url"].startswith("https://") for n in bloc["navigateurs"])


def test_rechercher_web_sans_reseau(monkeypatch):
    def tout_echoue(url):
        raise WebSearchError("pas de réseau")
    monkeypatch.setattr(websearch, "fetch_url", tout_echoue)
    res = rechercher_web(reference="VT-40A", zone="france")
    assert res["fetch_ok"] is False
    assert res["resultats"] == []
    assert res["liens_navigateur"]


def test_page_web_sans_champ():
    r = client.get("/recherche-web", params={"soumis": "1"})
    assert r.status_code == 200
    assert "au moins un fabricant" in r.text


def test_page_web_formulaire_vide():
    r = client.get("/recherche-web")
    assert r.status_code == 200
    assert "Recherche de fournisseurs sur le web" in r.text


def test_page_web_avec_resultats(monkeypatch):
    monkeypatch.setattr(websearch, "fetch_url", _faux_fetch)
    r = client.get("/recherche-web", params={"soumis": "1", "reference": "VT-40A",
                                              "fabricant": "Voltalis", "zone": "france"})
    assert r.status_code == 200
    assert "Fournisseur A" in r.text
    assert "Ouvrir sur Google" in r.text


def test_page_web_moteurs_bloques(monkeypatch):
    def tout_echoue(url):
        raise WebSearchError("captcha")
    monkeypatch.setattr(websearch, "fetch_url", tout_echoue)
    r = client.get("/recherche-web", params={"soumis": "1", "reference": "VT-40A"})
    assert r.status_code == 200
    assert "refusé" in r.text and "accès automatique" in r.text
    assert "Ouvrir sur DuckDuckGo" in r.text


def test_api_web_422_sans_champ():
    r = client.get("/api/recherche-web")
    assert r.status_code == 422


def test_api_web_avec_resultats(monkeypatch):
    monkeypatch.setattr(websearch, "fetch_url", _faux_fetch)
    r = client.get("/api/recherche-web", params={"reference": "VT-40A", "zone": "europe"})
    assert r.status_code == 200
    body = r.json()
    assert body["fetch_ok"] is True
    assert body["total"] if "total" in body else len(body["resultats"]) >= 1


def test_api_web_erreur_reseau(monkeypatch):
    def tout_echoue(url):
        raise WebSearchError("réseau coupé")
    monkeypatch.setattr(websearch, "fetch_url", tout_echoue)
    r = client.get("/api/recherche-web", params={"designation": "roulement 6204"})
    assert r.status_code == 200
    assert r.json()["fetch_ok"] is False
