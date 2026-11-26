# Recherche de produits fournisseurs

Application web en **Python / FastAPI** pour rechercher des produits chez des fournisseurs,
inspirée du skill « recherche-fournisseurs » : recherche par fabricant, référence ou
désignation, filtres logistiques, classement par pertinence (zone France d'abord, prix public,
livrable en France), et génération de mails de demande de devis personnalisés.

Les données sont un **jeu de démonstration intégré** (fournisseurs, produits et prix fictifs).

## Lancer l'application

```bash
pip install -r requirements.txt
python -m app.main
```

Puis ouvrir http://127.0.0.1:8000 (serveur local uniquement).

Alternative : `uvicorn app.main:app --host 127.0.0.1 --port 8000` depuis la racine du projet.

## Fonctionnalités

- **Recherche texte** sur fabricant, référence, désignation, catégorie et caractéristiques
  (tous les mots saisis doivent correspondre, accents ignorés), champ fabricant dédié.
- **Filtres** : zone fournisseur (France / Europe / Monde), catégorie, prix min/max (HT),
  en stock uniquement, livrable en France, enlèvement par transporteur (EXW/FCA), Incoterms.
- **Tris** : pertinence (France d'abord, puis Europe, puis Monde ; prix public et livrable
  favorisés), prix croissant/décroissant, délai, zone.
- **Tableau des offres** : fournisseur, zone/pays, référence, prix HT (ou « sur devis »),
  délai, stock, logistique (livraison France, Incoterms, frais de port, enlèvement), site,
  e-mail public, téléphone.
- **Fiche produit** (`/produit/{id}`) : regroupe toutes les offres fournisseurs pour un produit,
  avec cases à cocher, bouton « Sélectionner ceux avec e-mail public », et génération d'un
  **mail de demande de devis personnalisé** par fournisseur sélectionné (lien `mailto:`
  pré-rempli + bouton copier), avec quantité, adresse de livraison, Incoterms préférés et
  délai souhaité.

## API JSON

- `GET /api/recherche?q=&fabricant=&zone=&categorie=&prix_min=&prix_max=&dispo=1&livraison_france=1&enlevement=1&incoterms=&tri=`
- `GET /api/produit/{id}?tri=`
- `GET /api/options`
- `GET /sante`

## Tests

```bash
pytest -q
```

## Structure

```
app/
  main.py        routes FastAPI (pages HTML + API JSON)
  search.py      moteur de recherche, filtres, score de pertinence
  data.py        jeu de données de démonstration (fournisseurs, produits, offres)
  templates/     pages HTML (Jinja2)
  static/        feuille de style
tests/
  test_search.py tests du moteur et de l'API
```
