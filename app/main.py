from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .data import categories, fournisseurs_index, offres_enrichies, produits_index
from .search import (formater_prix, logistique_texte, normalize, options_filtres,
                     offres_produit, rechercher)

app = FastAPI(title="Recherche produits fournisseurs")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


def _bool(v):
    return str(v).lower() in ("1", "true", "on", "yes", "oui")


def _float(v):
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _params(request: Request):
    q = request.query_params
    return {"q": q.get("q", "").strip(), "fabricant": q.get("fabricant", "").strip() or None,
            "zone": q.get("zone") or None, "categorie": q.get("categorie") or None,
            "prix_min": _float(q.get("prix_min")), "prix_max": _float(q.get("prix_max")),
            "dispo": _bool(q.get("dispo")), "livraison_france": _bool(q.get("livraison_france")),
            "enlevement": _bool(q.get("enlevement")), "incoterms": q.get("incoterms") or None,
            "tri": q.get("tri", "pertinence")}


def _ligne(offre, num=None):
    p, f = offre["produit"], offre["fournisseur"]
    return {"num": num, "produit_id": p["id"], "designation": p["designation"],
            "fabricant": p["fabricant"], "reference": p["reference"], "categorie": p["categorie"],
            "fournisseur": f["nom"], "fournisseur_id": f["id"], "zone": f["zone"], "pays": f["pays"],
            "prix_ht": offre["prix_ht"], "prix_affiche": formater_prix(offre), "devise": offre["devise"],
            "delai": offre["delai"], "stock_texte": offre["stock_texte"], "stock": offre["stock"],
            "incoterms": offre["incoterms"], "livraison_france": offre["livraison_france"],
            "enlevement": offre["enlevement"], "frais_port_ht": offre["frais_port_ht"],
            "logistique": logistique_texte(offre), "site": f["site"], "email": f["email"],
            "telephone": f["telephone"], "score": None}


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    p = _params(request)
    resultats = rechercher(**p)
    lignes = [_ligne(o, i + 1) for i, o in enumerate(resultats)]
    return templates.TemplateResponse(request, "index.html", {
        "lignes": lignes, "total": len(lignes),
        "options": options_filtres(), "params": p,
        "categories": categories(),
        "nb_produits": len(produits_index()), "nb_fournisseurs": len(fournisseurs_index()),
        "nb_offres": len(offres_enrichies())})


@app.get("/produit/{pid}", response_class=HTMLResponse)
def fiche_produit(request: Request, pid: str, tri: str = "pertinence"):
    pi = produits_index()
    if pid not in pi:
        return templates.TemplateResponse(request, "404.html", {}, status_code=404)
    produit = pi[pid]
    offres = offres_produit(pid, tri=tri)
    lignes = [_ligne(o, i + 1) for i, o in enumerate(offres)]
    return templates.TemplateResponse(request, "produit.html", {
        "produit": produit, "lignes": lignes, "tri": tri,
        "options": options_filtres(), "normalize": normalize})


@app.get("/api/recherche")
def api_recherche(request: Request):
    p = _params(request)
    resultats = rechercher(**p)
    return {"total": len(resultats),
            "resultats": [_ligne(o, i + 1) for i, o in enumerate(resultats)]}


@app.get("/api/produit/{pid}")
def api_produit(pid: str, tri: str = "pertinence"):
    pi = produits_index()
    if pid not in pi:
        return JSONResponse({"detail": "Produit introuvable"}, status_code=404)
    offres = offres_produit(pid, tri=tri)
    return {"produit": pi[pid],
            "offres": [_ligne(o, i + 1) for i, o in enumerate(offres)]}


@app.get("/api/options")
def api_options():
    return options_filtres()


@app.get("/sante")
def sante():
    return {"statut": "ok", "produits": len(produits_index()),
            "fournisseurs": len(fournisseurs_index()), "offres": len(offres_enrichies())}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
