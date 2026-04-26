"""Streamlit-specific presentation helpers (CSS injection, copy strings).

Kept separate from the engine so the analysis modules remain free of any
UI framework dependency and can be tested without importing ``streamlit``.
"""

from __future__ import annotations

import streamlit as st

from analyzer.engine import DomainStatus

_CUSTOM_CSS = """
<style>
.stApp { background-color: #F5D3D6; }
html, body, p { font-family: 'Georgia', serif !important; color: #3B2A20 !important; }
h1 {
    text-align: center; color: #C25953 !important;
    font-weight: 800; text-transform: uppercase; letter-spacing: 4px;
    border-bottom: 3px double #C25953; padding-bottom: 15px;
}
.subtitle { text-align: center; font-style: italic; color: #4A6C6B; margin-bottom: 40px; }
.stButton > button {
    background-color: #E2AD5B; color: #3B2A20; border: 2px solid #A67531;
    border-radius: 0px; font-weight: bold; text-transform: uppercase;
    letter-spacing: 2px; width: 100%; box-shadow: 4px 4px 0px #A67531;
}
[data-testid="stMetricValue"] { color: #C25953 !important; font-weight: bold; }
[data-testid="stExpander"] summary svg { display: none !important; }
[data-testid="stExpander"] details {
    background-color: #FDF6E3; border: 2px solid #8C6A50;
    border-radius: 0px; box-shadow: 4px 4px 0px #8C6A50; padding: 10px;
}
[data-testid="stExpander"] summary::after {
    content: "✒️"; font-size: 1.5rem; position: absolute; right: 10px;
}
</style>
"""

DOMAIN_NOTICES: dict[DomainStatus, str] = {
    DomainStatus.SATIRE: (
        "Ah, a purveyor of whimsical tall tales. We find this publication's penchant "
        "for creative satire quite unsuitable for our curated collection. Please, "
        "kindly leave it at the door."
    ),
    DomainStatus.RESTRICTED: (
        "NOTICE: This domain is restricted by the Grand Authority. "
        "Its publications are not permitted within these walls."
    ),
}

ERROR_EMPTY_URL = "The Inspector requires a valid URL."
ERROR_LOCAL_URL = "Local and private network addresses are strictly forbidden by hotel policy"
ERROR_EMPTY_DOC = "The Inspector's messenger has returned empty-handed"
ERROR_DENIED = "Entry refused. The establishment has denied access"

VERDICT_CLEAR = "The Inspector has found no cause for alarm. This document may circulate freely."
VERDICT_FLAGGED = "Official Verdict: Misinformation Detected"

DISCLAIMER = (
    "Notice to Guests: The Grand Integrity Desk employs heuristic analysis only. "
    "Its findings are preliminary in nature and do not constitute a definitive verdict. "
    "The management accepts no liability for conclusions drawn without further verification."
)


def inject_custom_css() -> None:
    """Inject the Grand Hotel theme CSS into the current Streamlit page."""
    st.markdown(_CUSTOM_CSS, unsafe_allow_html=True)
