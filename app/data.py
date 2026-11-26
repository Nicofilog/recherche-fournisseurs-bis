ZONES = ["france", "europe", "monde"]
ZONE_LABELS = {"france": "France", "europe": "Europe", "monde": "Monde"}
INCOTERMS = ["DDP", "FCA", "EXW", "FOB"]

FOURNISSEURS = [
    {"id": "elecdiffusion", "nom": "ElecDiffusion", "zone": "france", "pays": "France",
     "site": "https://www.elecdiffusion.example", "email": "ventes@elecdiffusion.example",
     "telephone": "+33 1 84 60 12 34", "livraison_france": True, "incoterms": ["DDP", "FCA"],
     "enlevement_transporteur": True, "frais_port_ht": 9.90},
    {"id": "composantspro", "nom": "ComposantsPro", "zone": "france", "pays": "France",
     "site": "https://www.composantspro.example", "email": "commercial@composantspro.example",
     "telephone": "+33 2 99 45 67 89", "livraison_france": True, "incoterms": ["DDP", "EXW"],
     "enlevement_transporteur": True, "frais_port_ht": 7.50},
    {"id": "composantsrapides", "nom": "Composants Rapides", "zone": "france", "pays": "France",
     "site": "https://www.composantsrapides.example", "email": "contact@composantsrapides.example",
     "telephone": "+33 4 78 22 10 05", "livraison_france": True, "incoterms": ["DDP"],
     "enlevement_transporteur": False, "frais_port_ht": 0.0},
    {"id": "batipro", "nom": "BatiPro Fournitures", "zone": "france", "pays": "France",
     "site": "https://www.batipro.example", "email": "ventes@batipro.example",
     "telephone": "+33 5 56 33 88 21", "livraison_france": True, "incoterms": ["DDP"],
     "enlevement_transporteur": False, "frais_port_ht": 12.00},
    {"id": "technord", "nom": "TechNord Distribution", "zone": "europe", "pays": "Allemagne",
     "site": "https://www.technord.example", "email": "vertrieb@technord.example",
     "telephone": "+49 40 228 77 410", "livraison_france": True, "incoterms": ["FCA", "DDP"],
     "enlevement_transporteur": True, "frais_port_ht": 15.00},
    {"id": "euroelec", "nom": "EuroElec GmbH", "zone": "europe", "pays": "Allemagne",
     "site": "https://www.euroelec.example", "email": "sales@euroelec.example",
     "telephone": "+49 89 945 66 720", "livraison_france": True, "incoterms": ["EXW", "FCA"],
     "enlevement_transporteur": True, "frais_port_ht": None},
    {"id": "nordicelec", "nom": "NordicElec AB", "zone": "europe", "pays": "Suède",
     "site": "https://www.nordicelec.example", "email": "order@nordicelec.example",
     "telephone": "+46 8 505 630 00", "livraison_france": True, "incoterms": ["DDP", "FCA"],
     "enlevement_transporteur": False, "frais_port_ht": 19.90},
    {"id": "asiacomponents", "nom": "AsiaComponents Ltd", "zone": "monde", "pays": "Chine",
     "site": "https://www.asiacomponents.example", "email": "sales@asiacomponents.example",
     "telephone": "+86 21 6388 0000", "livraison_france": True, "incoterms": ["EXW", "FOB"],
     "enlevement_transporteur": True, "frais_port_ht": 45.00},
    {"id": "globalparts", "nom": "GlobalParts Inc", "zone": "monde", "pays": "États-Unis",
     "site": "https://www.globalparts.example", "email": "sales@globalparts.example",
     "telephone": "+1 888 555 0142", "livraison_france": False, "incoterms": ["EXW"],
     "enlevement_transporteur": True, "frais_port_ht": None},
    {"id": "marketpro", "nom": "MarketPro B2B", "zone": "monde", "pays": "Royaume-Uni",
     "site": "https://www.marketpro.example", "email": "b2b@marketpro.example",
     "telephone": "+44 20 7946 0958", "livraison_france": True, "incoterms": ["DDP"],
     "enlevement_transporteur": False, "frais_port_ht": 11.50},
]

PRODUITS = [
    {"id": "p01", "fabricant": "Voltalis", "reference": "VT-40A-30MA-A",
     "designation": "Disjoncteur différentiel 30 mA 40 A type A",
     "categorie": "Électricité industrielle",
     "caracteristiques": {"Pôles": "2P", "Sensibilité": "30 mA", "Courant nominal": "40 A", "Type": "A"}},
    {"id": "p02", "fabricant": "Voltalis", "reference": "VT-MT16C",
     "designation": "Disjoncteur magnétothermique 16 A courbe C",
     "categorie": "Électricité industrielle",
     "caracteristiques": {"Courant nominal": "16 A", "Courbe": "C", "Pouvoir de coupure": "6 kA"}},
    {"id": "p03", "fabricant": "Elektra", "reference": "EL-CT25-230",
     "designation": "Contacteur 25 A bobine 230 V",
     "categorie": "Électricité industrielle",
     "caracteristiques": {"Courant": "25 A", "Bobine": "230 V AC", "Contacts": "3 NO"}},
    {"id": "p04", "fabricant": "Roulex", "reference": "RL-6204-2RS",
     "designation": "Roulement à billes 6204-2RS étanche",
     "categorie": "Roulements",
     "caracteristiques": {"Alésage": "20 mm", "Diamètre extérieur": "47 mm", "Largeur": "14 mm", "Étanchéité": "2RS"}},
    {"id": "p05", "fabricant": "Roulex", "reference": "RL-608ZZ",
     "designation": "Roulement miniature 608 ZZ",
     "categorie": "Roulements",
     "caracteristiques": {"Alésage": "8 mm", "Diamètre extérieur": "22 mm", "Largeur": "7 mm", "Étanchéité": "ZZ"}},
    {"id": "p06", "fabricant": "AirFlex", "reference": "AF-VDE-50-100",
     "designation": "Vérin pneumatique double effet 50 x 100 mm",
     "categorie": "Pneumatique",
     "caracteristiques": {"Alésage": "50 mm", "Course": "100 mm", "Raccordement": "G1/4"}},
    {"id": "p07", "fabricant": "AirFlex", "reference": "AF-EV-5-2-24DC",
     "designation": "Électrovanne 5/2 voies 24 V DC",
     "categorie": "Pneumatique",
     "caracteristiques": {"Fonction": "5/2", "Commande": "24 V DC", "Raccordement": "G1/8"}},
    {"id": "p08", "fabricant": "Sensea", "reference": "SN-M12-PNP-NO",
     "designation": "Capteur inductif M12 PNP normalement ouvert",
     "categorie": "Capteurs",
     "caracteristiques": {"Filetage": "M12", "Portée": "4 mm", "Sortie": "PNP NO", "Tension": "10-30 V DC"}},
    {"id": "p09", "fabricant": "Sensea", "reference": "SN-PT-0-10BAR",
     "designation": "Capteur de pression 0-10 bar sortie 4-20 mA",
     "categorie": "Capteurs",
     "caracteristiques": {"Étendue": "0-10 bar", "Sortie": "4-20 mA", "Raccord": "G1/4"}},
    {"id": "p10", "fabricant": "CableSud", "reference": "CS-H07RN-3G25",
     "designation": "Câble souple H07RN-F 3G2,5 mm² au mètre",
     "categorie": "Câblage",
     "caracteristiques": {"Section": "3 x 2,5 mm²", "Tension": "450/750 V", "Souplesse": "H07RN-F"}},
    {"id": "p11", "fabricant": "GlandPro", "reference": "GP-PE-M20",
     "designation": "Presse-étoupe M20 laiton nickelé avec contre-écrou",
     "categorie": "Câblage",
     "caracteristiques": {"Filetage": "M20 x 1,5", "Plage câble": "6-12 mm", "Matière": "Laiton nickelé", "IP": "IP68"}},
    {"id": "p12", "fabricant": "DriveTech", "reference": "DT-VF-22KW",
     "designation": "Variateur de fréquence 2,2 kW 230 V monophasé",
     "categorie": "Variation de vitesse",
     "caracteristiques": {"Puissance": "2,2 kW", "Alimentation": "230 V mono", "Courant": "10,5 A"}},
    {"id": "p13", "fabricant": "Motivia", "reference": "MV-ASY-15KW-1500",
     "designation": "Moteur asynchrone triphasé 1,5 kW 1500 tr/min",
     "categorie": "Moteurs",
     "caracteristiques": {"Puissance": "1,5 kW", "Vitesse": "1500 tr/min", "Alimentation": "230/400 V", "Hauteur d'axe": "90L"}},
    {"id": "p14", "fabricant": "Safelec", "reference": "SL-AU-22-1NC",
     "designation": "Bouton d'arrêt d'urgence Ø22 mm 1 contact NC",
     "categorie": "Sécurité machine",
     "caracteristiques": {"Diamètre": "Ø22 mm", "Contacts": "1 NC", "Déverrouillage": "Par rotation"}},
    {"id": "p15", "fabricant": "Safelec", "reference": "SL-LED-24V-VERT",
     "designation": "Voyant lumineux LED 24 V vert Ø22 mm",
     "categorie": "Sécurité machine",
     "caracteristiques": {"Tension": "24 V", "Couleur": "Vert", "Diamètre": "Ø22 mm"}},
    {"id": "p16", "fabricant": "RailFix", "reference": "RF-DIN-35-1M",
     "designation": "Rail DIN 35 mm perforé longueur 1 m acier zingué",
     "categorie": "Coffrets et armoires",
     "caracteristiques": {"Profil": "35 mm", "Longueur": "1 m", "Matière": "Acier zingué"}},
]


def _offre(produit_id, fournisseur_id, prix_ht, delai, delai_jours, stock, incoterms,
           livraison_france, enlevement, frais_port_ht=0.0, prix_public=True, stock_texte=None):
    return {"produit_id": produit_id, "fournisseur_id": fournisseur_id, "prix_ht": prix_ht,
            "devise": "EUR", "delai": delai, "delai_jours": delai_jours, "stock": stock,
            "stock_texte": stock_texte or (f"{stock} en stock" if stock > 0 else "Sur commande"),
            "incoterms": incoterms, "frais_port_ht": frais_port_ht, "livraison_france": livraison_france,
            "enlevement": enlevement, "prix_public": prix_public}


OFFRES = [
    _offre("p01", "elecdiffusion", 42.90, "24-48 h", 2, 85, "DDP", True, True),
    _offre("p01", "composantspro", 38.50, "24 h", 1, 140, "DDP", True, True, 7.50),
    _offre("p01", "technord", 36.20, "3-5 jours", 4, 60, "FCA", True, True, 15.00),
    _offre("p01", "euroelec", 33.80, "1 semaine", 7, 45, "EXW", True, True),
    _offre("p01", "asiacomponents", 24.90, "2-3 semaines", 18, 500, "EXW", True, True, 45.00),
    _offre("p01", "marketpro", 39.90, "5-7 jours", 6, 30, "DDP", True, False, 11.50),

    _offre("p02", "composantsrapides", 8.90, "24 h", 1, 320, "DDP", True, False),
    _offre("p02", "elecdiffusion", 9.40, "24-48 h", 2, 210, "DDP", True, True),
    _offre("p02", "batipro", 7.60, "48 h", 2, 95, "DDP", True, False, 12.00),
    _offre("p02", "asiacomponents", 3.20, "2-3 semaines", 18, 2000, "EXW", True, True, 45.00),
    _offre("p02", "globalparts", 5.10, "3 semaines", 21, 150, "EXW", False, True),

    _offre("p03", "elecdiffusion", 28.70, "24-48 h", 2, 55, "DDP", True, True),
    _offre("p03", "technord", 26.40, "3-5 jours", 4, 70, "FCA", True, True, 15.00),
    _offre("p03", "composantspro", 29.90, "48 h", 2, 0, "DDP", True, True, 7.50, stock_texte="Sur commande"),
    _offre("p03", "euroelec", None, "sur devis", 14, 0, "EXW", True, True, prix_public=False, stock_texte="Sur devis"),

    _offre("p04", "composantspro", 6.80, "24 h", 1, 480, "DDP", True, True, 7.50),
    _offre("p04", "technord", 5.90, "2-3 jours", 3, 260, "FCA", True, True, 15.00),
    _offre("p04", "nordicelec", 7.40, "5-7 jours", 6, 120, "DDP", True, False, 19.90),
    _offre("p04", "asiacomponents", 1.85, "3-4 semaines", 25, 5000, "FOB", True, True, 45.00),

    _offre("p05", "composantsrapides", 1.20, "24 h", 1, 1500, "DDP", True, False),
    _offre("p05", "elecdiffusion", 1.45, "24-48 h", 2, 900, "DDP", True, True),
    _offre("p05", "asiacomponents", 0.35, "3-4 semaines", 25, 20000, "EXW", True, True, 45.00),
    _offre("p05", "marketpro", 1.10, "4-6 jours", 5, 300, "DDP", True, False, 11.50),

    _offre("p06", "batipro", 89.00, "48-72 h", 3, 22, "DDP", True, False, 12.00),
    _offre("p06", "technord", 79.50, "3-5 jours", 4, 35, "FCA", True, True, 15.00),
    _offre("p06", "euroelec", 71.20, "1-2 semaines", 10, 18, "EXW", True, True),
    _offre("p06", "asiacomponents", 48.90, "4-6 semaines", 35, 200, "FOB", True, True, 45.00),

    _offre("p07", "technord", 34.00, "3-5 jours", 4, 40, "DDP", True, True, 15.00),
    _offre("p07", "composantspro", 36.50, "24-48 h", 2, 0, "DDP", True, True, 7.50, stock_texte="Sur commande"),
    _offre("p07", "asiacomponents", 19.90, "3-4 semaines", 25, 300, "EXW", True, True, 45.00),

    _offre("p08", "composantspro", 24.90, "24 h", 1, 130, "DDP", True, True, 7.50),
    _offre("p08", "elecdiffusion", 26.50, "24-48 h", 2, 75, "DDP", True, True),
    _offre("p08", "nordicelec", 28.90, "5-7 jours", 6, 50, "FCA", True, False, 19.90),
    _offre("p08", "asiacomponents", 12.40, "2-3 semaines", 18, 800, "EXW", True, True, 45.00),
    _offre("p08", "globalparts", None, "sur devis", 21, 0, "EXW", False, True, prix_public=False, stock_texte="Sur devis"),

    _offre("p09", "technord", 68.00, "3-5 jours", 4, 25, "DDP", True, True, 15.00),
    _offre("p09", "euroelec", 62.50, "1-2 semaines", 10, 12, "EXW", True, True),
    _offre("p09", "asiacomponents", 39.90, "4-6 semaines", 35, 90, "EXW", True, True, 45.00),
    _offre("p09", "marketpro", 74.00, "5-7 jours", 6, 8, "DDP", True, False, 11.50),

    _offre("p10", "batipro", 2.35, "24-48 h", 2, 5000, "DDP", True, False, 12.00, stock_texte="En stock (m)"),
    _offre("p10", "elecdiffusion", 2.60, "24 h", 1, 3200, "DDP", True, True, stock_texte="En stock (m)"),
    _offre("p10", "cable-sud-direct", None, "sur devis", 5, 10000, "EXW", True, True, prix_public=False, stock_texte="En stock (m)"),

    _offre("p11", "composantsrapides", 3.90, "24 h", 1, 600, "DDP", True, False),
    _offre("p11", "elecdiffusion", 4.20, "24-48 h", 2, 350, "FCA", True, True),
    _offre("p11", "batipro", 3.40, "48 h", 2, 210, "DDP", True, False, 12.00),
    _offre("p11", "asiacomponents", 0.95, "3-4 semaines", 25, 5000, "EXW", True, True, 45.00),

    _offre("p12", "elecdiffusion", 289.00, "24-48 h", 2, 14, "DDP", True, True),
    _offre("p12", "technord", 265.00, "3-5 jours", 4, 9, "FCA", True, True, 15.00),
    _offre("p12", "euroelec", 249.00, "2 semaines", 14, 6, "EXW", True, True),
    _offre("p12", "marketpro", 310.00, "5-7 jours", 6, 11, "DDP", True, False, 11.50),

    _offre("p13", "batipro", 189.00, "48-72 h", 3, 7, "DDP", True, False, 12.00),
    _offre("p13", "technord", 175.00, "1 semaine", 7, 5, "FCA", True, True, 15.00),
    _offre("p13", "euroelec", 168.00, "2-3 semaines", 18, 3, "EXW", True, True),
    _offre("p13", "asiacomponents", 119.00, "6-8 semaines", 49, 40, "FOB", True, True, 45.00),

    _offre("p14", "composantspro", 18.90, "24 h", 1, 95, "DDP", True, True, 7.50),
    _offre("p14", "elecdiffusion", 19.50, "24-48 h", 2, 60, "DDP", True, True),
    _offre("p14", "asiacomponents", 8.90, "3-4 semaines", 25, 400, "EXW", True, True, 45.00),

    _offre("p15", "composantsrapides", 4.90, "24 h", 1, 700, "DDP", True, False),
    _offre("p15", "elecdiffusion", 5.20, "24-48 h", 2, 450, "DDP", True, True),
    _offre("p15", "marketpro", 5.80, "4-6 jours", 5, 120, "DDP", True, False, 11.50),

    _offre("p16", "batipro", 3.20, "24-48 h", 2, 800, "DDP", True, False, 12.00),
    _offre("p16", "elecdiffusion", 3.50, "24 h", 1, 500, "FCA", True, True),
    _offre("p16", "asiacomponents", 1.10, "3-4 semaines", 25, 3000, "EXW", True, True, 45.00),
]

FOURNISSEURS.append({
    "id": "cable-sud-direct", "nom": "CableSud (vente directe)", "zone": "france", "pays": "France",
    "site": "https://www.cablesud.example", "email": "devis@cablesud.example",
    "telephone": "+33 3 88 17 45 60", "livraison_france": True, "incoterms": ["EXW", "DDP"],
    "enlevement_transporteur": True, "frais_port_ht": None,
})


def fournisseurs_index():
    return {f["id"]: f for f in FOURNISSEURS}


def produits_index():
    return {p["id"]: p for p in PRODUITS}


def offres_enrichies():
    fi = fournisseurs_index()
    pi = produits_index()
    out = []
    for o in OFFRES:
        r = dict(o)
        r["fournisseur"] = fi[o["fournisseur_id"]]
        r["produit"] = pi[o["produit_id"]]
        out.append(r)
    return out


def categories():
    return sorted({p["categorie"] for p in PRODUITS})
