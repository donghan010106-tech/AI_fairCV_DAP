"""Sidebar navigation for FairCV Dashboard."""

import streamlit as st


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown("""
        <div style="padding: 1rem 0 1.5rem 0; border-bottom: 1px solid #30363d; margin-bottom: 1rem;">
            <div style="font-family: 'Space Mono', monospace; font-size: 1.1rem; font-weight: 700; color: #2dd4bf;">⚖️ FairCV</div>
            <div style="font-size: 0.72rem; color: #7d8590; text-transform: uppercase; letter-spacing: 1px; margin-top: 2px;">Research Dashboard</div>
        </div>
        """, unsafe_allow_html=True)

        pages = [
            "🏠 Project Overview",
            "📊 Progress Tracker",
            "🗄️ Dataset Analysis",
            "🤖 Model Development",
            "📚 Research Papers",
            "🚀 Improvement Roadmap",
        ]

        if "page" not in st.session_state:
            st.session_state.page = pages[0]

        st.markdown("<div style='font-size:0.7rem; color:#7d8590; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;'>Navigation</div>", unsafe_allow_html=True)

        for p in pages:
            active = st.session_state.page == p
            style = "background:rgba(45,212,191,0.1); border:1px solid rgba(45,212,191,0.3); color:#2dd4bf;" if active else "background:transparent; border:1px solid transparent; color:#7d8590;"
            if st.button(p, key=f"nav_{p}", use_container_width=True):
                st.session_state.page = p
                st.rerun()

        # Project status panel
        st.markdown("""
        <div style="margin-top: 2rem; padding: 1rem; background: #161b22; border: 1px solid #30363d; border-radius: 10px;">
            <div style="font-size: 0.7rem; color: #7d8590; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">Project Status</div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="font-size: 0.82rem; color: #e6edf3;">Overall Progress</span>
                <span style="font-family: 'Space Mono', monospace; font-size: 0.82rem; color: #2dd4bf;">62%</span>
            </div>
            <div style="background: #0d1117; border-radius: 4px; height: 6px; margin-bottom: 12px;">
                <div style="background: linear-gradient(90deg, #2dd4bf, #38bdf8); width: 62%; height: 100%; border-radius: 4px;"></div>
            </div>
            <div style="font-size: 0.75rem; color: #7d8590; margin-bottom: 4px;">✅ 6 of 10 stages done</div>
            <div style="font-size: 0.75rem; color: #f59e0b;">🔄 Optimization phase next</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top: 1.5rem; padding: 1rem; background: #161b22; border: 1px solid #30363d; border-radius: 10px;">
            <div style="font-size: 0.7rem; color: #7d8590; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">Best Model</div>
            <div style="font-family: 'Space Mono', monospace; font-size: 1.1rem; color: #38bdf8; margin-bottom: 4px;">LR</div>
            <div style="font-size: 0.78rem; color: #7d8590; margin-bottom: 2px;">F1 = 0.966</div>
            <div style="font-size: 0.78rem; color: #7d8590;">ROC-AUC = 0.997</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top: auto; padding-top: 2rem; font-size: 0.7rem; color: #7d8590; text-align: center; border-top: 1px solid #30363d; margin-top: 1rem;">
            Capstone Project · 2024–2025<br/>
            FairCVdb · BiDAlab UAM
        </div>
        """, unsafe_allow_html=True)

    return st.session_state.page
