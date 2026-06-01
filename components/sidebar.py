import streamlit as st


PAGES = [
    "Project Overview",
    "Dataset & EDA",
    "Baseline Models",
    "Fusion Strategies",
    "Fairness Analysis",
    "Research Context",
]


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown("""
        <div style="padding:1rem 0 0.5rem 0;">
            <div style="font-family:'Space Mono',monospace;font-size:1.3rem;font-weight:700;
                        color:#2dd4bf;letter-spacing:-0.5px;">FairCV</div>
            <div style="font-size:0.72rem;color:#7d8590;text-transform:uppercase;
                        letter-spacing:1px;margin-top:2px;">Research Dashboard</div>
        </div>
        <hr style="border-color:#30363d;margin:0.8rem 0 1rem 0;">
        """, unsafe_allow_html=True)

        # Use query_params to persist selection across reruns
        params = st.query_params
        default_idx = 0
        if "p" in params:
            try:
                default_idx = int(params["p"])
            except Exception:
                default_idx = 0
        default_idx = max(0, min(default_idx, len(PAGES) - 1))

        selected_idx = st.radio(
            "nav",
            range(len(PAGES)),
            index=default_idx,
            format_func=lambda i: PAGES[i],
            label_visibility="collapsed",
        )
        st.query_params["p"] = str(selected_idx)

        st.markdown("""
        <hr style="border-color:#30363d;margin:1.5rem 0 1rem 0;">
        <div style="font-size:0.68rem;color:#7d8590;text-transform:uppercase;
                    letter-spacing:1px;margin-bottom:0.8rem;">Quick Stats</div>
        """, unsafe_allow_html=True)

        for val, label in [
            ("24,000", "Resume Profiles"),
            ("3",      "Fusion Strategies"),
            ("5",      "Research Questions"),
            ("12",     "Experiments"),
            ("3",      "Classifiers"),
        ]:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:0.35rem 0;border-bottom:1px solid #30363d30;">
                <span style="font-size:0.8rem;color:#7d8590;">{label}</span>
                <span style="font-family:'Space Mono',monospace;font-size:0.9rem;
                             color:#2dd4bf;font-weight:700;">{val}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top:1.5rem;font-size:0.68rem;color:#7d8590;line-height:1.5;">
            Dataset: FairCVdb<br>Peña et al., 2023<br>Springer Nature Computer Science
        </div>
        """, unsafe_allow_html=True)

    return PAGES[selected_idx]
