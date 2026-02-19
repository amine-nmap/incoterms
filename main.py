# main.py
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from incoterms_data import INCOTERMS
from recommender import recommend_incoterm, calculate_costs

# ─── Configuration ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Incoterms 2020 – Aide à la décision",
    page_icon="🚢",
    layout="wide"
)

st.title("🚢 Aide à la décision – Incoterms 2020")
st.caption("Application pédagogique Bachelor Commerce International")

# ─── Constantes visuelles ─────────────────────────────────────────────────────
RISK_X = {
    "EXW": 0, "FCA": 2, "FAS": 3,
    "FOB": 4, "CFR": 4, "CIF": 4,
    "CPT": 4, "CIP": 4,
    "DAP": 8, "DPU": 8, "DDP": 10
}

TIMELINE_POINTS = [
    (0,  "Départ\nvendeur"),
    (2,  "Export\nclearance"),
    (4,  "À bord /\ntransporteur"),
    (8,  "Destination\n(bord)"),
    (10, "Import\nclearance")
]

LABELS = {
    "export_clearance": "Dédouanement export",
    "main_carriage":    "Transport principal",
    "insurance":        "Assurance",
    "import_clearance": "Dédouanement import",
    "unloading":        "Déchargement",
    "duties_taxes":     "Droits & taxes import"
}


# ─── Fonctions utilitaires ────────────────────────────────────────────────────
def get_incoterm(code: str) -> dict | None:
    return next((i for i in INCOTERMS if i["code"] == code), None)


def draw_risk_timeline(code: str, ax, title_suffix: str = ""):
    ax.set_xlim(-0.5, 11)
    ax.set_ylim(0, 1)
    ax.axis("off")
    if title_suffix:
        ax.set_title(f"Transfert de risque – {code} {title_suffix}", fontsize=11, fontweight="bold")
    else:
        ax.set_title(f"Transfert de risque – {code}", fontsize=11, fontweight="bold")

    # Zones colorées : vendeur (vert) / acheteur (orange)
    rx = RISK_X.get(code, 4)
    ax.axvspan(-0.5, rx, ymin=0.2, ymax=0.8, alpha=0.15, color="green")
    ax.axvspan(rx, 11,  ymin=0.2, ymax=0.8, alpha=0.15, color="orange")

    # Ligne principale
    ax.hlines(0.5, 0, 10, colors="gray", linewidth=5, zorder=1)

    # Points de la timeline
    for x, label in TIMELINE_POINTS:
        ax.plot(x, 0.5, "o", color="#4A90D9", markersize=10, zorder=2)
        ax.text(x, 0.68, label, ha="center", va="bottom", fontsize=8, color="#333")

    # Point de transfert de risque
    ax.plot(rx, 0.5, "*", color="red", markersize=18, zorder=3)
    ax.text(rx, 0.30, "⚠ Risque\ntransféré", ha="center", va="top",
            color="red", fontsize=9, fontweight="bold")

    # Légende zones
    patch_v = mpatches.Patch(color="green",  alpha=0.4, label="Risque vendeur")
    patch_a = mpatches.Patch(color="orange", alpha=0.4, label="Risque acheteur")
    ax.legend(handles=[patch_v, patch_a], loc="upper right", fontsize=8)


def responsibility_table(incoterm: dict) -> pd.DataFrame:
    rows = []
    for key, label in LABELS.items():
        rows.append({
            "Obligation":      label,
            "Vendeur":  "✅" if incoterm["seller"].get(key) else "❌",
            "Acheteur": "✅" if incoterm["buyer"].get(key)  else "❌",
        })
    return pd.DataFrame(rows)


# ─── Sidebar – paramètres financiers ─────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Paramètres financiers")
    valeur = st.number_input("Valeur marchandise (USD)", min_value=0.0,
                             value=25_000.0, step=500.0, format="%.2f")
    fret = st.number_input("Coût transport principal (USD)", min_value=0.0,
                           value=3_000.0, step=100.0, format="%.2f")
    taux_ass = st.number_input("Taux assurance (%)", min_value=0.0,
                               max_value=10.0, value=0.6, step=0.1) / 100
    taux_douane = st.number_input("Droits de douane import (%)", min_value=0.0,
                                  max_value=40.0, value=8.0, step=0.5) / 100
    frais_dech = st.number_input("Frais déchargement (USD)", min_value=0.0,
                                 value=600.0, step=50.0, format="%.2f")
    st.caption("Ces valeurs sont utilisées dans tous les onglets.")


# ─── Onglets ──────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "🎯 Recommandation",
    "⚖️ Comparaison de 2 Incoterms",
    "📋 Référentiel complet"
])


# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 1 – RECOMMANDATION
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Contexte de la transaction")

    col_left, col_right = st.columns(2)
    with col_left:
        mode_transport = st.selectbox(
            "Mode de transport principal",
            ["Maritime", "Aérien", "Routier", "Ferroviaire", "Multimodal"]
        )
        vendeur_paie = st.radio(
            "Qui paie le transport principal ?",
            ["Vendeur", "Acheteur"],
            horizontal=True
        )
    with col_right:
        assurance = st.checkbox("Assurance requise par le vendeur ?")
        st.info(
            "💡 **Conseil :** Pour les conteneurs maritimes, préférez FCA ou FOB "
            "plutôt que FOB si le chargement est à la charge du vendeur."
        )

    if st.button("🔍 Recommander l'Incoterm adapté", type="primary", use_container_width=True):
        vendeur_paie_bool = (vendeur_paie == "Vendeur")
        code, justification = recommend_incoterm(mode_transport, vendeur_paie_bool, assurance)
        incoterm = get_incoterm(code)

        if not incoterm:
            st.error("Aucun Incoterm trouvé pour ces critères.")
        else:
            # Résultat principal
            st.success(f"### ✅ Incoterm recommandé : **{code} – {incoterm['name']}**")
            st.markdown(f"**Justification :** {justification}")
            st.markdown(f"**Description :** {incoterm['description']}")
            st.markdown(f"**Transfert de risque :** {incoterm['risk_transfer']}")

            st.divider()

            # Responsabilités + coûts
            col_resp, col_cout = st.columns([1.2, 1])

            with col_resp:
                st.markdown("#### 📋 Tableau des responsabilités")
                df = responsibility_table(incoterm)
                st.dataframe(df, use_container_width=True, hide_index=True)

            with col_cout:
                st.markdown("#### 💰 Estimation des coûts")
                cv, ca = calculate_costs(incoterm, valeur, fret, taux_ass, taux_douane, frais_dech)
                st.metric("Coût estimé vendeur", f"{cv:,.2f} USD")
                st.metric("Coût estimé acheteur", f"{ca:,.2f} USD")
                st.metric("Coût total transaction", f"{cv + ca:,.2f} USD",
                          delta=f"Marge risque vendeur : {cv / (cv + ca) * 100:.1f}%"
                          if (cv + ca) > 0 else None)

            st.divider()

            # Graphique timeline
            st.markdown("#### 📍 Visualisation du transfert de risque")
            fig, ax = plt.subplots(figsize=(11, 2.5))
            draw_risk_timeline(code, ax)
            st.pyplot(fig)
            plt.close(fig)

            st.caption(
                "⚠️ Estimation simplifiée – exclut marges, frais bancaires, "
                "TVA et variations locales. Consultez un transitaire pour un chiffrage précis."
            )


# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 2 – COMPARAISON DE 2 INCOTERMS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Comparer deux Incoterms côte à côte")
    st.markdown("Sélectionnez deux Incoterms pour analyser leurs différences en termes de responsabilités, coûts et transfert de risque.")

    all_codes = [i["code"] for i in INCOTERMS]

    col_a, col_b = st.columns(2)
    with col_a:
        code_a = st.selectbox("Incoterm A", all_codes, index=all_codes.index("FOB"))
    with col_b:
        code_b = st.selectbox("Incoterm B", all_codes, index=all_codes.index("CIF"))

    if code_a == code_b:
        st.warning("⚠️ Sélectionnez deux Incoterms différents pour une comparaison utile.")
    else:
        inc_a = get_incoterm(code_a)
        inc_b = get_incoterm(code_b)

        # En-têtes descriptifs
        col_a2, col_b2 = st.columns(2)
        with col_a2:
            st.info(f"**{code_a} – {inc_a['name']}**\n\n{inc_a['description']}")
        with col_b2:
            st.info(f"**{code_b} – {inc_b['name']}**\n\n{inc_b['description']}")

        st.divider()

        # Tableau comparatif des responsabilités
        st.markdown("#### 📋 Comparaison des responsabilités")

        rows = []
        for key, label in LABELS.items():
            v_a = "✅ Vendeur" if inc_a["seller"].get(key) else "❌ Acheteur"
            v_b = "✅ Vendeur" if inc_b["seller"].get(key) else "❌ Acheteur"
            diff = "🔄 Différent" if v_a != v_b else "—"
            rows.append({"Obligation": label, code_a: v_a, code_b: v_b, "Différence": diff})

        df_comp = pd.DataFrame(rows)
        st.dataframe(df_comp, use_container_width=True, hide_index=True)

        st.divider()

        # Comparaison des coûts
        st.markdown("#### 💰 Comparaison des coûts estimés")
        cv_a, ca_a = calculate_costs(inc_a, valeur, fret, taux_ass, taux_douane, frais_dech)
        cv_b, ca_b = calculate_costs(inc_b, valeur, fret, taux_ass, taux_douane, frais_dech)

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric(f"Vendeur – {code_a}", f"{cv_a:,.2f} USD")
        col_m2.metric(f"Acheteur – {code_a}", f"{ca_a:,.2f} USD")
        col_m3.metric(f"Vendeur – {code_b}", f"{cv_b:,.2f} USD",
                      delta=f"{cv_b - cv_a:+,.2f} vs {code_a}")
        col_m4.metric(f"Acheteur – {code_b}", f"{ca_b:,.2f} USD",
                      delta=f"{ca_b - ca_a:+,.2f} vs {code_a}")

        # Graphique barres comparatif
        fig_bar, ax_bar = plt.subplots(figsize=(8, 3))
        categories = ["Coût Vendeur", "Coût Acheteur"]
        x = range(len(categories))
        width = 0.3
        bars_a = ax_bar.bar([i - width / 2 for i in x], [cv_a, ca_a], width,
                            label=code_a, color="#4A90D9", alpha=0.85)
        bars_b = ax_bar.bar([i + width / 2 for i in x], [cv_b, ca_b], width,
                            label=code_b, color="#E8705A", alpha=0.85)

        ax_bar.set_xticks(list(x))
        ax_bar.set_xticklabels(categories)
        ax_bar.set_ylabel("USD")
        ax_bar.set_title(f"Comparaison coûts estimés : {code_a} vs {code_b}")
        ax_bar.legend()
        ax_bar.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}"))

        for bar in list(bars_a) + list(bars_b):
            h = bar.get_height()
            ax_bar.text(bar.get_x() + bar.get_width() / 2, h + 50,
                        f"{h:,.0f}", ha="center", va="bottom", fontsize=8)

        st.pyplot(fig_bar)
        plt.close(fig_bar)

        st.divider()

        # Timelines côte à côte
        st.markdown("#### 📍 Comparaison des transferts de risque")
        fig_t, (ax_t1, ax_t2) = plt.subplots(2, 1, figsize=(11, 5))
        draw_risk_timeline(code_a, ax_t1)
        draw_risk_timeline(code_b, ax_t2)
        fig_t.tight_layout(pad=1.5)
        st.pyplot(fig_t)
        plt.close(fig_t)

        st.caption(
            "⚠️ Estimation simplifiée – exclut marges, frais bancaires, "
            "TVA et variations locales."
        )


# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 3 – RÉFÉRENTIEL COMPLET
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Référentiel des 11 Incoterms 2020")

    # Filtres
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filtre_mode = st.selectbox(
            "Filtrer par mode de transport",
            ["Tous", "Tous modes", "Maritime uniquement"]
        )
    with col_f2:
        filtre_charge = st.selectbox(
            "Filtrer par charge transport vendeur",
            ["Tous", "Vendeur paie fret", "Acheteur paie fret"]
        )

    rows_ref = []
    for inc in INCOTERMS:
        if filtre_mode == "Tous modes" and "any" not in inc["modes"]:
            continue
        if filtre_mode == "Maritime uniquement" and "any" in inc["modes"]:
            continue
        if filtre_charge == "Vendeur paie fret" and not inc["seller"].get("main_carriage"):
            continue
        if filtre_charge == "Acheteur paie fret" and inc["seller"].get("main_carriage"):
            continue

        rows_ref.append({
            "Code":             inc["code"],
            "Nom complet":      inc["name"],
            "Mode":             "Tous" if "any" in inc["modes"] else "Maritime",
            "Export":           "✅ V" if inc["seller"].get("export_clearance") else "✅ A",
            "Fret":             "✅ V" if inc["seller"].get("main_carriage") else "✅ A",
            "Assurance":        "✅ V" if inc["seller"].get("insurance")
                                else ("✅ A" if inc["buyer"].get("insurance") else "—"),
            "Import":           "✅ V" if inc["seller"].get("import_clearance") else "✅ A",
            "Déchargement":     "✅ V" if inc["seller"].get("unloading") else "✅ A",
            "Droits/Taxes":     "✅ V" if inc["seller"].get("duties_taxes") else "✅ A",
            "Transfert risque": inc["risk_transfer"],
        })

    df_ref = pd.DataFrame(rows_ref)
    st.dataframe(df_ref, use_container_width=True, hide_index=True)
    st.caption("V = Vendeur   |   A = Acheteur")

    st.divider()
    st.markdown("#### 🗺️ Positions de transfert de risque sur la chaîne logistique")

    fig_all, ax_all = plt.subplots(figsize=(12, 3.5))
    ax_all.set_xlim(-0.5, 11)
    ax_all.set_ylim(0, 1)
    ax_all.axis("off")

    ax_all.hlines(0.5, 0, 10, colors="lightgray", linewidth=6, zorder=1)

    for x, label in TIMELINE_POINTS:
        ax_all.plot(x, 0.5, "o", color="#4A90D9", markersize=12, zorder=2)
        ax_all.text(x, 0.62, label, ha="center", va="bottom", fontsize=8, color="#333")

    colors_map = {
        0: "#E74C3C", 2: "#E67E22", 3: "#F1C40F",
        4: "#2ECC71", 8: "#3498DB", 10: "#9B59B6"
    }
    plotted_x = {}
    for inc in INCOTERMS:
        rx = RISK_X.get(inc["code"], 4)
        offset = plotted_x.get(rx, 0)
        plotted_x[rx] = offset + 1
        y_pos = 0.5 - 0.08 * offset
        color = colors_map.get(rx, "#555")
        ax_all.plot(rx, y_pos, "D", color=color, markersize=8, zorder=4)
        ax_all.text(rx, y_pos - 0.07, inc["code"], ha="center", va="top",
                    fontsize=7.5, fontweight="bold", color=color)

    st.pyplot(fig_all)
    plt.close(fig_all)