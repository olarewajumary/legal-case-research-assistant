import time

import streamlit as st

from ask import ask, UNPUBLISHED_WARNING
from limiter import (
    allow_request,
    SESSION_LIMIT,
    WINDOW_SECONDS,
    DAILY_LIMIT,
    DAY_SECONDS,
)

PAGE_TITLE = "Legal Case Research Assistant"
INTRO = (
    "Ask a legal question. Answers come only from a small collection of "
    "33 U.S. court opinions (Ninth and Second Circuits), and every quote is "
    "checked against the opinion. This is a portfolio project, not legal advice."
)
SESSION_MESSAGE = "You have asked several questions in a short time. Please wait a few minutes and try again."
DAILY_MESSAGE = "This free demo has reached its daily limit. Please try again tomorrow."
ERROR_MESSAGE = "Something went wrong, possibly because the demo is busy. Please try again in a minute."


def clean(text):
    """Escape dollar signs so Streamlit does not read them as math."""
    return text.replace("$", "\\$")


@st.cache_resource
def shared_history():
    """One list of request times shared by every visitor while the app is running."""
    return []


def show_result(out):
    """Display one ask() result."""
    if out["status"] == "refused":
        st.info(out["message"])
    elif out["status"] == "unverified":
        st.warning(out["message"])
    else:
        for claim in out["claims"]:
            st.markdown(f"**{clean(claim['statement'])}**")
            st.caption(f"{claim['case_name']} ({claim['court']}, {claim['date_filed']})")
            if claim["unpublished"]:
                st.warning(UNPUBLISHED_WARNING)
            st.markdown(f"> {clean(claim['quote'])}")
            st.markdown(f"[Read the opinion]({claim['url']})")


st.set_page_config(page_title=PAGE_TITLE)
st.title(PAGE_TITLE)
st.write(INTRO)

question = st.text_input("Your question")

if st.button("Search") and question.strip():
    now = time.time()
    session_history = st.session_state.setdefault("history", [])
    daily_history = shared_history()
    if not allow_request(session_history, now, SESSION_LIMIT, WINDOW_SECONDS):
        st.warning(SESSION_MESSAGE)
    elif not allow_request(daily_history, now, DAILY_LIMIT, DAY_SECONDS):
        st.warning(DAILY_MESSAGE)
    else:
        session_history.append(now)
        daily_history.append(now)
        try:
            with st.spinner("Searching the opinions..."):
                out = ask(question.strip())
            show_result(out)
        except Exception as error:
            print("ask failed:", type(error).__name__, error)
            st.error(ERROR_MESSAGE)