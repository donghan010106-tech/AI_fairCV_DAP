import streamlit as st


def render_sidebar() -> str:
    with st.sidebar:
        # Logo / brand
        st.markdown("""
        <div style="padding: 1rem 0 0.5rem 0;">
            <div style="font-family:'Space Mono',monospace; font-size:1.3rem; font-weight:700; color:#2dd4bf; letter-spacing:-0.5px;">
                ⚖️ FairCV
            </div>
            <div style="font-size:0.72rem; color:#7d8590; text-transform:uppercase; letter-spacing:1px; margin-top:2px;">
                Research Dashboard
            </div>
        </div>
        <hr style="border-color:#30363d; margin: 0.8rem 0 1.2rem 0;">
        """, unsafe_allow_html=True)

        pages = [
            "🏠 Project Overview",
            "🗄️ Dataset & EDA",
            "🔬 Baseline Models",
            "🔀 Fusion Strategies",
            "⚖️ Fairness Analysis",
            "📚 Research Context",
        ]

        if "page" not in st.session_state:
            st.session_state.page = pages[0]

        selected = st.radio(
            "Navigation",
            pages,
            index=pages.index(st.session_state.page),
            label_visibility="collapsed",
        )
        st.session_state.page = selected

        # Quick stats
        st.markdown("""
        <hr style="border-color:#30363d; margin: 1.5rem 0 1rem 0;">
        <div style="font-size:0.68rem; color:#7d8590; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.8rem;">
            Quick Stats
        </div>
        """, unsafe_allow_html=True)

        stats = [
            ("24,000", "Resume Profiles"),
            ("3", "Fusion Strategies"),
            ("5", "Research Questions"),
            ("12", "Experiments"),
            ("3", "Classifiers"),
        ]
        for val, label in stats:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center;
                        padding:0.35rem 0; border-bottom:1px solid #30363d30;">
                <span style="font-size:0.8rem; color:#7d8590;">{label}</span>
                <span style="font-family:'Space Mono',monospace; font-size:0.9rem;
                             color:#2dd4bf; font-weight:700;">{val}</span>
            </div>
            """, unsafe_allow_html=True)

        # Dataset citation
        st.markdown("""
        <div style="margin-top:1.5rem; font-size:0.68rem; color:#7d8590; line-height:1.5;">
            <strong style="color:#30363d;">Dataset</strong><br>
            FairCVdb — Peña et al., 2023<br>
            Springer Nature Computer Science
        </div>
        """, unsafe_allow_html=True)

    return selected
