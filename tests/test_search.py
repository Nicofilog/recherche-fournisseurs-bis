import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient

from app.data import FOURNISSEURS, OFFRES, PRODUITS
from app.main import app
from app.search import normalize, rechercher, offres_produit, tokenize

client = TestClient(app)


def test_normalize_supprime_accents():
    assert normalize("Élévation ç") == "elevation c"


def test_tokenize_ignore_espaces_vides():
    assert tokenize("  disjoncteur   40 A ") == ["disjoncteur", "40", "a"]


def test_recherche_par_reference_exacte():
    res = rechercher(q="6204-2RS")
    assert res
    assert all(o["produit"]["reference"] == "RL-6204-2RS" for o in res)


def test_recherche_par_fabricant():
    res = rechercher(fabricant="Voltalis")
    assert len(res) >= 2
    assert all(o["produit"]["fabricant"] == "Voltalis" for o in res)


def test_recherche_texte_designation_partielle():
    res = rechercher(q="capteur pression")
    assert any(o["produit"]["id"] == "p09" for o in res)


def test_recherche_tous_tokens_requis():
    res = rechercher(q="disjoncteur 40 A")
    assert all(o["produit"]["id"] == "p01" for o in res)
    assert not any(o["produit"]["id"] == "p02" for o in res)


def test_filtre_zone_france():
    res = rechercher(zone="france")
    assert res
    assert all(o["fournisseur"]["zone"] == "france" for o in res)


def test_filtre_prix_max():
    res = rechercher(prix_max=10)
    assert res
    assert all(o["prix_ht"] is not None and o["prix_ht"] <= 10 for o in res)


def test_filtre_prix_min_exclut_sur_devis():
    res = rechercher(prix_min=5)
    assert all(o["prix_ht"] is not None and o["prix_ht"] >= 5 for o in res)


def test_filtre_stock_disponible():
    res = rechercher(dispo=True)
    assert res
    assert all(o["stock"] > 0 for o in res)


def test_filtre_livraison_france():
    res = rechercher(livraison_france=True)
    assert res
    assert all(o["livraison_france"] for o in res)


def test_filtre_incoterms():
    res = rechercher(incoterms="EXW")
    assert res
    assert all(o["incoterms"] == "EXW" for o in res)


def test_filtre_categorie():
    res = rechercher(categorie="Roulements")
    assert res
    assert all(o["produit"]["categorie"] == "Roulements" for o in res)


def test_tri_pertinence_france_dabord():
    res = rechercher(q="disjoncteur différentiel 30 mA", tri="pertinence")
    zones = [o["fournisseur"]["zone"] for o in res]
    assert zones == sorted(zones, key=lambda z: {"france": 0, "europe": 1, "monde": 2}[z])


def test_tri_prix_croissant():
    res = rechercher(tri="prix_asc")
    prix = [o["prix_ht"] for o in res if o["prix_ht"] is not None]
    assert prix == sorted(prix)


def test_tri_delai():
    res = rechercher(q="roulement", tri="delai")
    delais = [o["delai_jours"] for o in res]
    assert delais == sorted(delais)


def test_offres_produit_regroupe_toutes_offres():
    res = offres_produit("p01")
    assert len(res) >= 4
    assert all(o["produit_id"] == "p01" for o in res)


def test_donnees_coherentes():
    fids = {f["id"] for f in FOURNISSEURS}
    pids = {p["id"] for p in PRODUITS}
    for o in OFFRES:
        assert o["fournisseur_id"] in fids
        assert o["produit_id"] in pids
    assert len(pids) == len(PRODUITS)


def test_api_sante():
    r = client.get("/sante")
    assert r.status_code == 200
    body = r.json()
    assert body["statut"] == "ok"
    assert body["produits"] == len(PRODUITS)


def test_api_recherche_json():
    r = client.get("/api/recherche", params={"q": "6204", "zone": "france"})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] >= 1
    for ligne in body["resultats"]:
        assert ligne["zone"] == "france"
        assert "logistique" in ligne
        assert ligne["email"]


def test_api_recherche_filtres_combines():
    r = client.get("/api/recherche", params={"prix_max": 5, "dispo": "1"})
    body = r.json()
    assert body["total"] >= 1
    for ligne in body["resultats"]:
        assert ligne["prix_ht"] <= 5
        assert ligne["stock"] > 0


def test_page_index_200():
    r = client.get("/")
    assert r.status_code == 200
    assert "Recherche" in r.text


def test_page_index_avec_query():
    r = client.get("/", params={"q": "vérin"})
    assert r.status_code == 200
    assert "Vérin pneumatique" in r.text


def test_page_produit_200():
    r = client.get("/produit/p01")
    assert r.status_code == 200
    assert "Disjoncteur différentiel" in r.text
    assert "mailto" in r.text
    assert "Sélectionner ceux avec e-mail public" in r.text


def test_page_produit_404():
    r = client.get("/produit/inconnu")
    assert r.status_code == 404


def test_api_produit_json():
    r = client.get("/api/produit/p04")
    assert r.status_code == 200
    body = r.json()
    assert body["produit"]["reference"] == "RL-6204-2RS"
    assert len(body["offres"]) >= 3


def test_api_produit_404():
    r = client.get("/api/produit/inconnu")
    assert r.status_code == 404


def test_api_options():
    r = client.get("/api/options")
    assert r.status_code == 200
    body = r.json()
    assert "france" in [z for z, _ in body["zones"]]
    assert "DDP" in body["incoterms"]
