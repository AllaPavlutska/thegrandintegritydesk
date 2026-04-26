"""Streamlit entry point for The Grand Integrity Desk.

This module is intentionally thin: all analysis logic lives in the
``analyzer`` package, so this file is concerned only with composing the
UI and wiring user input through to the engine and database.
"""

from __future__ import annotations

import warnings

import streamlit as st

from analyzer import DatabaseManager, MisinformationEngine, is_local_url
from analyzer.engine import DomainStatus
from analyzer.ui import (
    DISCLAIMER,
    DOMAIN_NOTICES,
    ERROR_DENIED,
    ERROR_EMPTY_DOC,
    ERROR_EMPTY_URL,
    ERROR_LOCAL_URL,
    VERDICT_CLEAR,
    VERDICT_FLAGGED,
    inject_custom_css,
)

warnings.filterwarnings("ignore")


@st.cache_resource
def get_system_components() -> tuple[MisinformationEngine, DatabaseManager]:
    """Return process-wide singletons for the engine and database."""
    return MisinformationEngine(), DatabaseManager()


def _render_payload(title: str, text: str) -> None:
    with st.expander("Review Confiscated Payload"):
        st.markdown(f"**Document Title:** {title}")
        st.markdown(f"**Content Snippet:** {text[:400]}...")


def _handle_submission(
    url: str,
    engine: MisinformationEngine,
    db: DatabaseManager,
) -> None:
    """Validate, classify, analyze, and render results for a submitted URL."""
    if not url:
        st.error(ERROR_EMPTY_URL)
        return

    if is_local_url(url):
        st.error(ERROR_LOCAL_URL)
        return

    with st.spinner("The Inspector is reviewing the document..."):
        domain_status = engine.check_domain_type(url)

        if domain_status in DOMAIN_NOTICES:
            st.warning(DOMAIN_NOTICES[domain_status])
            return

        try:
            title, text = engine.extract_text(url)
            result = engine.analyze(text)
        except ValueError:
            st.error(ERROR_EMPTY_DOC)
            return
        except Exception:
            st.error(ERROR_DENIED)
            return

        db.log_detection(url, title, result.is_misinfo, result.confidence)

        st.divider()
        if result.is_misinfo == 0:
            st.success(VERDICT_CLEAR)
        else:
            st.error(VERDICT_FLAGGED)

        _, col2 = st.columns(2)
        col2.metric(label="Certainty Score", value=f"{result.confidence * 100:.1f}%")

        _render_payload(title, text)


def main() -> None:
    st.set_page_config(page_title="The Grand Information Hotel", layout="centered")
    inject_custom_css()

    engine, db = get_system_components()

    st.markdown("<h1>The Grand Integrity Desk</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='subtitle'>Please submit the document for formal inspection.</p>",
        unsafe_allow_html=True,
    )

    url_input = st.text_input(
        "Target URL",
        placeholder="— INSERT URL HERE —",
        label_visibility="collapsed",
    )

    if st.button("Submit for Review", use_container_width=True):
        _handle_submission(url_input, engine, db)

    st.markdown("---")
    st.caption(DISCLAIMER)


# Keep the unused-import linters happy: DomainStatus is part of the
# public surface re-exported through ``analyzer`` and is available here
# for downstream tooling that imports from ``app``.
_ = DomainStatus

if __name__ == "__main__":
    main()
