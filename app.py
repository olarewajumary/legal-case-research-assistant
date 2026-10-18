import streamlit as st

from ask import ask, UNPUBLISHED_WARNING

PAGE_TITLE = "Legal Case Research Assistant"
INTRO = (
    "Ask a legal question. Answers come only from a small collection of "
    "33 U.S. court opinions (Ninth and Second Circuits), and every quote is "
    "checked against the opinion. This is a portfolio project, not legal advice."
)


def clean(text):
    """Escape dollar signs so Streamlit does not read them as math."""
    return text.replace("$", "\\$")


st.set_page_config(page_title=PAGE_TITLE)
st.title(PAGE_TITLE)
st.write(INTRO)

question = st.text_input("Your question")

if st.button("Search") and question.strip():
    with st.spinner("Searching the opinions..."):
        out = ask(question.strip())
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