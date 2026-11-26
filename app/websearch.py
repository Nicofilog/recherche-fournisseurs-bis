import re
from urllib.parse import parse_qs, quote_plus, urlparse

import httpx
from bs4 import BeautifulSoup

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

MOTEURS = [
    {"nom": "Mojeek", "url": "https://www.mojeek.com/search?q={q}"},
    {"nom": "Bing", "url": "https://www.bing.com/search?q={q}&count=20"},
    {"nom": "DuckDuckGo", "url": "https://lite.duckduckgo.com/lite/?q={q}"},
]

NAVIGATEURS = [
    ("Google", "https://www.google.com/search?q={q}"),
    ("Bing", "https://www.bing.com/search?q={q}"),
    ("DuckDuckGo", "https://duckduckgo.com/?q={q}"),
]

MOTEURS_PROPRES = ("mojeek.com", "bing.com", "microsoft.com", "duckduckgo.com", "google.com")


class WebSearchError(Exception):
    pass


def fetch_url(url):
    try:
        with httpx.Client(timeout=15, follow_redirects=True,
                          headers={"User-Agent": UA, "Accept-Language": "fr-FR,fr;q=0.9"}) as c:
            r = c.get(url)
            r.raise_for_status()
            return r.text
    except Exception as e:
        raise WebSearchError(str(e))


def domaine(url):
    try:
        return (urlparse(url).netloc or "").replace("www.", "")
    except Exception:
        return ""


def nettoyer_texte(t):
    return re.sub(r"\s+", " ", t or "").strip()


def extraire_prix(*textes):
    texte = " ".join(textes)
    m = re.search(r"(\d{1,3}(?:[ \u00a0]\d{3})*[.,]\d{2})\s*(?:€|EUR|euros?)", texte, re.I)
    return (m.group(1).replace(" ", "") + " €") if m else None


def _lien_reel(href):
    if not href:
        return None
    if href.startswith("//"):
        href = "https:" + href
    if "duckduckgo.com/l/" in href:
        qs = parse_qs(urlparse(href).query)
        if "uddg" in qs:
            return qs["uddg"][0]
    if href.startswith("http"):
        return href
    return None


def _exclure(url):
    d = domaine(url) or ""
    return any(d == m or d.endswith("." + m) for m in MOTEURS_PROPRES)


def parse_mojeek(html):
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for li in soup.select("li"):
        a = li.select_one("h2 a") or li.select_one("a.title")
        if not a:
            continue
        url = _lien_reel(a.get("href", ""))
        if not url or _exclure(url):
            continue
        titre = nettoyer_texte(a.get_text())
        p = li.select_one("p")
        extrait = nettoyer_texte(p.get_text()) if p else ""
        if titre and url:
            out.append({"titre": titre, "url": url, "extrait": extrait})
    return out


def parse_bing(html):
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for li in soup.select("li.b_algo"):
        a = li.select_one("h2 a")
        if not a:
            continue
        url = _lien_reel(a.get("href", ""))
        if not url or _exclure(url):
            continue
        titre = nettoyer_texte(a.get_text())
        p = li.select_one("p")
        extrait = nettoyer_texte(p.get_text()) if p else ""
        if titre and url:
            out.append({"titre": titre, "url": url, "extrait": extrait})
    return out


def parse_ddg(html):
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for a in soup.select("a.result__a"):
        url = _lien_reel(a.get("href", ""))
        if not url or _exclure(url):
            continue
        titre = nettoyer_texte(a.get_text())
        extrait = ""
        parent = a.find_parent(class_="result")
        if parent:
            sn = parent.select_one(".result__snippet")
            if sn:
                extrait = nettoyer_texte(sn.get_text())
        if titre and url:
            out.append({"titre": titre, "url": url, "extrait": extrait})
    if not out:
        for a in soup.select("a[rel='nofollow']"):
            url = _lien_reel(a.get("href", ""))
            if not url or _exclure(url):
                continue
            titre = nettoyer_texte(a.get_text())
            if titre and url and len(titre) > 10:
                out.append({"titre": titre, "url": url, "extrait": ""})
    return out


PARSEURS = {"Mojeek": parse_mojeek, "Bing": parse_bing, "DuckDuckGo": parse_ddg}


def construire_requetes(fabricant="", reference="", designation="", zone="france", livraison=False):
    produit = " ".join(x for x in [reference, fabricant] if x).strip() or designation
    ref = f'"{reference}"' if reference else (produit or "")
    reqs = []
    if reference:
        reqs.append(f"{ref} {fabricant} prix acheter".strip())
        reqs.append(f"{ref} distributeur officiel revendeur")
    if designation:
        reqs.append(f"{designation} prix acheter distributeur")
    if zone == "france":
        reqs.append(f"{ref} livraison France".strip())
    elif zone == "europe":
        reqs.append(f"{ref} livraison Europe prix".strip())
    else:
        reqs.append(f"{ref} worldwide buy price".strip())
    if livraison:
        reqs.append(f"{ref} enlèvement transporteur EXW FCA Incoterms".strip())
    vus = set()
    out = []
    for r in reqs:
        r = re.sub(r"\s+", " ", r).strip()
        if r and r.lower() not in vus:
            vus.add(r.lower())
            out.append(r)
    return out[:4]


def rechercher_web(fabricant="", reference="", designation="", zone="france",
                    livraison=False, max_results=10):
    requetes = construire_requetes(fabricant, reference, designation, zone, livraison)
    resultats = []
    vus = set()
    erreurs = []
    fetch_ok = False
    for q in requetes:
        for moteur in MOTEURS:
            url = moteur["url"].format(q=quote_plus(q))
            try:
                html = fetch_url(url)
            except WebSearchError as e:
                erreurs.append(f"{moteur['nom']}: {e}")
                continue
            ajoutes = 0
            for r in PARSEURS[moteur["nom"]](html):
                cle = domaine(r["url"]) + "|" + r["url"]
                if cle in vus:
                    continue
                vus.add(cle)
                r["domaine"] = domaine(r["url"])
                r["prix_indicatif"] = extraire_prix(r["titre"], r["extrait"])
                r["requete"] = q
                r["moteur"] = moteur["nom"]
                resultats.append(r)
                ajoutes += 1
                if len(resultats) >= max_results:
                    break
            if ajoutes:
                fetch_ok = True
                break
            if len(resultats) >= max_results:
                break
        if len(resultats) >= max_results:
            break
    liens = [{"requete": q,
              "navigateurs": [{"nom": n, "url": t.format(q=quote_plus(q))} for n, t in NAVIGATEURS]}
             for q in requetes]
    return {"requetes": requetes, "resultats": resultats[:max_results],
            "liens_navigateur": liens, "fetch_ok": fetch_ok, "erreurs": erreurs[:5]}
