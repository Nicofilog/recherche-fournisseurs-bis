import re
import unicodedata

from .data import INCOTERMS, ZONE_LABELS, ZONES, categories, offres_enrichies


def normalize(texte):
    if texte is None:
        return ""
    texte = unicodedata.normalize("NFKD", str(texte))
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    return texte.lower()


def tokenize(query):
    return [t for t in re.split(r"\s+", normalize(query).strip()) if t]


def produit_matches(produit, tokens):
    champs = " ".join([
        produit["fabricant"], produit["reference"], produit["designation"],
        produit["categorie"], " ".join(produit.get("caracteristiques", {}).values()),
    ])
    hay = normalize(champs)
    return all(t in hay for t in tokens)


def produit_match_details(produit, tokens):
    ref = normalize(produit["reference"])
    fab = normalize(produit["fabricant"])
    des = normalize(produit["designation"])
    score = 0
    for t in tokens:
        if t in ref:
            score += 3
        if t in fab:
            score += 2
        if t in des:
            score += 1
    return score


ZONE_RANG = {"france": 0, "europe": 1, "monde": 2}


def score_pertinence(offre):
    f = offre["fournisseur"]
    s = 0
    s += {"france": 30, "europe": 20, "monde": 10}[f["zone"]]
    if offre["prix_public"] and offre["prix_ht"] is not None:
        s += 20
    if offre["livraison_france"]:
        s += 20
    if offre["stock"] > 0:
        s += 10
    if offre["enlevement"]:
        s += 5
    return s


def filtrer(offres, q="", zone=None, categorie=None, prix_min=None, prix_max=None,
            dispo=False, livraison_france=False, incoterms=None, enlevement=False,
            fabricant=None):
    tokens = tokenize(q)
    res = []
    for o in offres:
        p = o["produit"]
        f = o["fournisseur"]
        if tokens and not (produit_matches(p, tokens) or all(t in normalize(f["nom"]) for t in tokens)):
            continue
        if fabricant and normalize(fabricant) not in normalize(p["fabricant"]):
            continue
        if zone and f["zone"] != zone:
            continue
        if categorie and p["categorie"] != categorie:
            continue
        if prix_min is not None and (o["prix_ht"] is None or o["prix_ht"] < prix_min):
            continue
        if prix_max is not None and (o["prix_ht"] is None or o["prix_ht"] > prix_max):
            continue
        if dispo and o["stock"] <= 0:
            continue
        if livraison_france and not o["livraison_france"]:
            continue
        if enlevement and not o["enlevement"]:
            continue
        if incoterms and o["incoterms"] not in incoterms:
            continue
        res.append(o)
    return res


def trier(offres, tri, tokens):
    if tri == "prix_asc":
        return sorted(offres, key=lambda o: (o["prix_ht"] is None, o["prix_ht"] or 0))
    if tri == "prix_desc":
        return sorted(offres, key=lambda o: (o["prix_ht"] is None, -(o["prix_ht"] or 0)))
    if tri == "delai":
        return sorted(offres, key=lambda o: o["delai_jours"])
    if tri == "zone":
        return sorted(offres, key=lambda o: (ZONE_RANG[o["fournisseur"]["zone"]], -(score_pertinence(o))))
    return sorted(offres, key=lambda o: (
        ZONE_RANG[o["fournisseur"]["zone"]],
        -(score_pertinence(o) + produit_match_details(o["produit"], tokens)),
    ))


def rechercher(q="", zone=None, categorie=None, prix_min=None, prix_max=None, dispo=False,
               livraison_france=False, incoterms=None, enlevement=False, fabricant=None,
               tri="pertinence"):
    tokens = tokenize(q)
    offres = filtrer(offres_enrichies(), q=q, zone=zone, categorie=categorie, prix_min=prix_min,
                     prix_max=prix_max, dispo=dispo, livraison_france=livraison_france,
                     incoterms=incoterms, enlevement=enlevement, fabricant=fabricant)
    return trier(offres, tri, tokens)


def offres_produit(produit_id, tri="pertinence"):
    offres = [o for o in offres_enrichies() if o["produit_id"] == produit_id]
    return trier(offres, tri, [])


def options_filtres():
    return {"zones": [(z, ZONE_LABELS[z]) for z in ZONES],
            "categories": categories(),
            "incoterms": INCOTERMS,
            "tris": [("pertinence", "Pertinence (France d'abord, prix public, livrable)"),
                     ("prix_asc", "Prix croissant"), ("prix_desc", "Prix décroissant"),
                     ("delai", "Délai croissant"), ("zone", "Zone (France, Europe, Monde)")]}


def formater_prix(offre):
    if not offre["prix_public"] or offre["prix_ht"] is None:
        return "sur devis"
    return f"{offre['prix_ht']:.2f} € HT"


def logistique_texte(offre):
    f = offre["fournisseur"]
    parts = []
    parts.append("Livraison France : " + ("oui" if offre["livraison_france"] else "non"))
    parts.append(f"Incoterms : {offre['incoterms']}")
    if offre["frais_port_ht"]:
        parts.append(f"Frais de port : {offre['frais_port_ht']:.2f} € HT")
    parts.append("Enlèvement transporteur : " + ("oui" if offre["enlevement"] else "non"))
    parts.append(f"Zone fournisseur : {ZONE_LABELS[f['zone']]} ({f['pays']})")
    return " · ".join(parts)
