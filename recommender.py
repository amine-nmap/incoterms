# recommender.py
from incoterms_data import INCOTERMS


def recommend_incoterm(
    mode_transport: str,
    vendeur_paie_transport_principal: bool,
    assurance_requise: bool = False
) -> tuple[str, str]:
    """
    Recommande un Incoterm selon des critères simples.
    Retourne (code Incoterm, justification)
    """
    mode_lower = mode_transport.lower()
    is_maritime = any(
        keyword in mode_lower
        for keyword in ["maritime", "sea", "ocean", "mer", "fluvial", "inland"]
    )

    compatibles = [
        inc for inc in INCOTERMS
        if "any" in inc["modes"]
        or (is_maritime and any(m in inc["modes"] for m in ["sea", "inland_waterway"]))
    ]

    if not compatibles:
        return "N/A", "Aucun Incoterm compatible avec ce mode de transport."

    if vendeur_paie_transport_principal:
        if assurance_requise and is_maritime:
            return (
                "CIF",
                "Le vendeur paie le fret + assurance minimale (ICC C). "
                "Idéal pour le maritime quand le vendeur veut couvrir le risque pendant le transit."
            )
        elif assurance_requise:
            return (
                "CIP",
                "Le vendeur paie le fret + assurance étendue (ICC A). "
                "Recommandé pour tous modes quand une couverture complète est exigée."
            )
        else:
            return (
                "CPT",
                "Le vendeur prend en charge le transport principal. "
                "Le risque se transfère dès la remise au premier transporteur."
            )
    else:
        if is_maritime:
            return (
                "FOB",
                "L'acheteur organise le fret maritime. "
                "Le vendeur livre à bord du navire et gère l'export. Standard maritime."
            )
        else:
            return (
                "FCA",
                "L'acheteur organise le transport principal. "
                "Le vendeur gère l'export et remet au transporteur désigné."
            )


def calculate_costs(incoterm: dict, valeur: float, fret: float,
                    taux_assurance: float, taux_douane: float,
                    frais_dechargement: float) -> tuple[float, float]:
    """
    Calcule les coûts estimés pour le vendeur et l'acheteur.
    Retourne (cout_vendeur, cout_acheteur)
    """
    cout_vendeur = 0.0
    if incoterm["seller"].get("main_carriage"):
        cout_vendeur += fret
    if incoterm["seller"].get("insurance"):
        cout_vendeur += valeur * taux_assurance
    if incoterm["seller"].get("duties_taxes"):
        cout_vendeur += valeur * taux_douane

    cout_acheteur = valeur
    if incoterm["buyer"].get("main_carriage"):
        cout_acheteur += fret
    if incoterm["buyer"].get("insurance"):
        cout_acheteur += valeur * taux_assurance
    if incoterm["buyer"].get("duties_taxes"):
        cout_acheteur += valeur * taux_douane
    if incoterm["buyer"].get("unloading"):
        cout_acheteur += frais_dechargement

    return cout_vendeur, cout_acheteur