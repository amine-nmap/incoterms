# incoterms_data.py

INCOTERMS = [
    {
        "code": "EXW",
        "name": "Ex Works",
        "modes": ["any"],
        "risk_transfer": "Lieu de mise à disposition chez le vendeur",
        "description": "Obligation minimale pour le vendeur. L'acheteur prend tout en charge dès l'enlèvement.",
        "seller": {
            "export_clearance": False,
            "main_carriage": False,
            "insurance": False,
            "import_clearance": False,
            "unloading": False,
            "duties_taxes": False
        },
        "buyer": {
            "export_clearance": True,
            "main_carriage": True,
            "insurance": True,
            "import_clearance": True,
            "unloading": True,
            "duties_taxes": True
        }
    },
    {
        "code": "FCA",
        "name": "Free Carrier",
        "modes": ["any"],
        "risk_transfer": "Remise au transporteur nommé par l'acheteur",
        "description": "Le vendeur livre les marchandises dédouanées à l'exportation au transporteur désigné.",
        "seller": {
            "export_clearance": True,
            "main_carriage": False,
            "insurance": False,
            "import_clearance": False,
            "unloading": False,
            "duties_taxes": False
        },
        "buyer": {
            "export_clearance": False,
            "main_carriage": True,
            "insurance": True,
            "import_clearance": True,
            "unloading": True,
            "duties_taxes": True
        }
    },
    {
        "code": "CPT",
        "name": "Carriage Paid To",
        "modes": ["any"],
        "risk_transfer": "Remise au premier transporteur (départ)",
        "description": "Le vendeur paie le fret jusqu'à destination, mais le risque se transfère dès la remise au transporteur.",
        "seller": {
            "export_clearance": True,
            "main_carriage": True,
            "insurance": False,
            "import_clearance": False,
            "unloading": False,
            "duties_taxes": False
        },
        "buyer": {
            "export_clearance": False,
            "main_carriage": False,
            "insurance": True,
            "import_clearance": True,
            "unloading": True,
            "duties_taxes": True
        }
    },
    {
        "code": "CIP",
        "name": "Carriage and Insurance Paid To",
        "modes": ["any"],
        "risk_transfer": "Remise au premier transporteur (départ)",
        "description": "Comme CPT, mais le vendeur doit aussi souscrire une assurance couverture étendue (ICC A).",
        "seller": {
            "export_clearance": True,
            "main_carriage": True,
            "insurance": True,
            "import_clearance": False,
            "unloading": False,
            "duties_taxes": False
        },
        "buyer": {
            "export_clearance": False,
            "main_carriage": False,
            "insurance": False,
            "import_clearance": True,
            "unloading": True,
            "duties_taxes": True
        }
    },
    {
        "code": "DAP",
        "name": "Delivered at Place",
        "modes": ["any"],
        "risk_transfer": "Lieu nommé à destination (prêt à décharger)",
        "description": "Le vendeur livre à destination mais ne décharge pas. L'acheteur gère le dédouanement import.",
        "seller": {
            "export_clearance": True,
            "main_carriage": True,
            "insurance": False,
            "import_clearance": False,
            "unloading": False,
            "duties_taxes": False
        },
        "buyer": {
            "export_clearance": False,
            "main_carriage": False,
            "insurance": True,
            "import_clearance": True,
            "unloading": True,
            "duties_taxes": True
        }
    },
    {
        "code": "DPU",
        "name": "Delivered at Place Unloaded",
        "modes": ["any"],
        "risk_transfer": "Lieu nommé à destination (déchargé)",
        "description": "Seul Incoterm où le vendeur assure le déchargement à destination. Dédouanement import à l'acheteur.",
        "seller": {
            "export_clearance": True,
            "main_carriage": True,
            "insurance": False,
            "import_clearance": False,
            "unloading": True,
            "duties_taxes": False
        },
        "buyer": {
            "export_clearance": False,
            "main_carriage": False,
            "insurance": True,
            "import_clearance": True,
            "unloading": False,
            "duties_taxes": True
        }
    },
    {
        "code": "DDP",
        "name": "Delivered Duty Paid",
        "modes": ["any"],
        "risk_transfer": "Lieu nommé à destination",
        "description": "Obligation maximale pour le vendeur. Il prend tout en charge y compris droits de douane import.",
        "seller": {
            "export_clearance": True,
            "main_carriage": True,
            "insurance": False,
            "import_clearance": True,
            "unloading": False,
            "duties_taxes": True
        },
        "buyer": {
            "export_clearance": False,
            "main_carriage": False,
            "insurance": True,
            "import_clearance": False,
            "unloading": True,
            "duties_taxes": False
        }
    },
    {
        "code": "FAS",
        "name": "Free Alongside Ship",
        "modes": ["sea", "inland_waterway"],
        "risk_transfer": "Le long du navire au port de chargement",
        "description": "Réservé au maritime. Le vendeur livre le long du navire, le risque passe avant chargement.",
        "seller": {
            "export_clearance": True,
            "main_carriage": False,
            "insurance": False,
            "import_clearance": False,
            "unloading": False,
            "duties_taxes": False
        },
        "buyer": {
            "export_clearance": False,
            "main_carriage": True,
            "insurance": True,
            "import_clearance": True,
            "unloading": True,
            "duties_taxes": True
        }
    },
    {
        "code": "FOB",
        "name": "Free On Board",
        "modes": ["sea", "inland_waterway"],
        "risk_transfer": "À bord du navire au port de chargement",
        "description": "Le plus utilisé en maritime. Le risque se transfère une fois la marchandise à bord.",
        "seller": {
            "export_clearance": True,
            "main_carriage": False,
            "insurance": False,
            "import_clearance": False,
            "unloading": False,
            "duties_taxes": False
        },
        "buyer": {
            "export_clearance": False,
            "main_carriage": True,
            "insurance": True,
            "import_clearance": True,
            "unloading": True,
            "duties_taxes": True
        }
    },
    {
        "code": "CFR",
        "name": "Cost and Freight",
        "modes": ["sea", "inland_waterway"],
        "risk_transfer": "À bord du navire au port de chargement",
        "description": "Le vendeur paie le fret maritime, mais le risque se transfère au chargement (avant départ).",
        "seller": {
            "export_clearance": True,
            "main_carriage": True,
            "insurance": False,
            "import_clearance": False,
            "unloading": False,
            "duties_taxes": False
        },
        "buyer": {
            "export_clearance": False,
            "main_carriage": False,
            "insurance": True,
            "import_clearance": True,
            "unloading": True,
            "duties_taxes": True
        }
    },
    {
        "code": "CIF",
        "name": "Cost Insurance and Freight",
        "modes": ["sea", "inland_waterway"],
        "risk_transfer": "À bord du navire au port de chargement",
        "description": "Comme CFR + assurance minimale (ICC C) souscrite par le vendeur. Maritime uniquement.",
        "seller": {
            "export_clearance": True,
            "main_carriage": True,
            "insurance": True,
            "import_clearance": False,
            "unloading": False,
            "duties_taxes": False
        },
        "buyer": {
            "export_clearance": False,
            "main_carriage": False,
            "insurance": False,
            "import_clearance": True,
            "unloading": True,
            "duties_taxes": True
        }
    }
]