import streamlit as st
from mlx_lm import load, generate
import random
import time

st.set_page_config(
    page_title="PlainSpeak",
    page_icon="📖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400;1,600&family=Source+Code+Pro:wght@500&display=swap');

html, body, [class*="css"], .stApp {
    background-color: #F8F5EF !important;
    color: #1C1C1A !important;
    font-family: 'Lora', Georgia, serif !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 5rem 2rem 6rem 2rem !important; max-width: 680px !important; }

.eyebrow { font-family: 'Source Code Pro', monospace; font-size: 12px; letter-spacing: 3px; text-transform: uppercase; color: #2D4A3E; margin-bottom: 1.5rem; display: block; }
.hero-title { font-family: 'Lora', Georgia, serif; font-size: 2.8rem; font-weight: 600; font-style: italic; color: #1C1C1A; line-height: 1.15; margin-bottom: 1.25rem; white-space: nowrap; }
.intro { font-family: 'Lora', Georgia, serif; font-size: 1.1rem; color: #5C5850; line-height: 1.85; }
.intro em { color: #2D4A3E; font-style: italic; }
.rule { border: none; border-top: 1px solid #E2DDD6; margin: 2.5rem 0; }
.section-label { font-family: 'Source Code Pro', monospace; font-size: 12px; letter-spacing: 3px; text-transform: uppercase; color: #A09890; margin-bottom: 0.75rem; display: block; }

div[data-testid="stSelectbox"] > label { display: none !important; }
div[data-testid="stSelectbox"] > div > div {
    background-color: #FDFAF6 !important; border: 1px solid #D5D0C8 !important;
    border-radius: 6px !important; font-family: 'Lora', Georgia, serif !important;
    font-size: 1rem !important; font-style: italic !important; color: #3C3830 !important;
}

div[data-testid="stTextArea"] > label { display: none !important; }
textarea {
    background-color: #FDFAF6 !important; border: 1px solid #D5D0C8 !important;
    border-radius: 6px !important; color: #1C1C1A !important;
    font-family: 'Lora', Georgia, serif !important; font-size: 1.1rem !important;
    font-style: italic !important; line-height: 1.85 !important;
    padding: 1.25rem 1.5rem !important; caret-color: #2D4A3E !important;
}
textarea:focus { border-color: #2D4A3E !important; box-shadow: 0 0 0 3px rgba(45,74,62,0.08) !important; outline: none !important; }
textarea::placeholder { color: #C8C3BC !important; font-style: italic !important; }

.char-count { font-family: 'Source Code Pro', monospace; font-size: 12px; color: #B8B2AA; margin-top: 0.4rem; }

.stButton > button {
    background-color: #2D4A3E !important; color: #F8F5EF !important;
    border: none !important; border-radius: 5px !important;
    font-family: 'Source Code Pro', monospace !important; font-size: 13px !important;
    font-style: normal !important; font-weight: 500 !important;
    letter-spacing: 3px !important; text-transform: uppercase !important;
    padding: 0.85rem 2.5rem !important; width: 100% !important; transition: all 0.2s ease !important;
}
.stButton > button:hover { background-color: #3A5F51 !important; box-shadow: 0 4px 20px rgba(45,74,62,0.22) !important; transform: translateY(-1px) !important; }

.output-card { background: #FDFAF6; border: 1px solid #E2DDD6; border-left: 4px solid #2D4A3E; border-radius: 6px; padding: 2rem 2rem 1.5rem; margin-top: 0.75rem; }
.output-text { font-family: 'Lora', Georgia, serif; font-size: 1.2rem; line-height: 1.9; color: #1C1C1A; margin: 0 0 1.5rem 0; }
.output-meta { font-family: 'Source Code Pro', monospace; font-size: 12px; color: #B8B2AA; line-height: 1.8; }

.transparency { background: #F3F0E8; border: 1px solid #E2DDD6; border-radius: 5px; padding: 1.25rem 1.5rem; margin-top: 1.25rem; font-family: 'Lora', Georgia, serif; font-size: 0.95rem; font-style: italic; color: #7A7570; line-height: 1.85; }
.transparency a { color: #2D4A3E !important; text-decoration: underline !important; font-style: normal !important; }

.wit { font-family: 'Lora', Georgia, serif; font-size: 1rem; font-style: italic; color: #C4BFB8; margin-top: 1.5rem; text-align: center; }

.footer { font-family: 'Source Code Pro', monospace; font-size: 13px; color: #B8B2AA; text-align: center; margin-top: 5rem; line-height: 2.4; }
.footer a { color: #2D4A3E !important; text-decoration: none !important; }
.footer a:hover { text-decoration: underline !important; }
</style>
""", unsafe_allow_html=True)

EXAMPLES = {
    "— pick an example —": "",
    "Genesis 1:1–2 (KJV)": "In the beginning God created the heaven and the earth. And the earth was without form, and void; and darkness was upon the face of the deep.",
    "Romeo & Juliet": "Wherefore art thou Romeo? Deny thy father and refuse thy name; Or, if thou wilt not, be but sworn my love, And I'll no longer be a Capulet.",
    "Adam Smith": "The invisible hand of the market, whereby individuals pursuing their own self-interest are led, as if by an invisible hand, to promote ends which were no part of their original intention.",
    "Legal boilerplate": "The party of the first part hereby agrees to indemnify and hold harmless the party of the second part from any and all claims, damages, losses, costs and expenses arising out of or resulting from the performance of this agreement.",
    "Psalms 23:1 (KJV)": "The LORD is my shepherd; I shall not want.",
    "Matthew 5:13 (KJV)": "Ye are the salt of the earth: but if the salt have lost his savour, wherewith shall it be salted?",
}

LOADING_LINES = [
    "Unlocking the vault...", "Time traveling to plain English...",
    "Finding your seat at the table...", "Making the fancy people nervous...",
    "Doing what school never did...", "Cracking it open...",
]

WIT_LINES = [
    "Dense text is just plain text with a superiority complex.",
    "Knowledge shouldn't come with a dress code.",
    "If it took 400 years to write, it can take a few seconds to translate.",
    "Somewhere, a professor is uncomfortable right now.",
    "School should have had this. We're not mad. Just saying.",
    "You now have a seat at the intellectual table.",
]

# Session state init
if "result" not in st.session_state:
    st.session_state.result = None
if "elapsed" not in st.session_state:
    st.session_state.elapsed = None
if "wit_line" not in st.session_state:
    st.session_state.wit_line = ""
if "textarea_value" not in st.session_state:
    st.session_state.textarea_value = ""

def on_example_change():
    chosen = st.session_state.example_select
    if chosen != "— pick an example —":
        st.session_state.textarea_value = EXAMPLES[chosen]
        st.session_state.main_textarea = EXAMPLES[chosen]
        st.session_state.result = None

@st.cache_resource(show_spinner=False)
def load_model():
    return load("plainspeak-model")

with st.spinner("Loading model into memory..."):
    model, tokenizer = load_model()

# Hero
st.markdown('<span class="eyebrow">PlainSpeak &nbsp;·&nbsp; SmolLM2-1.7B &nbsp;·&nbsp; Runs 100% on your machine</span>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">I taught a tiny AI to speak human.</h1>', unsafe_allow_html=True)
st.markdown('<p class="intro">Give it anything written to impress instead of communicate.<br>Get back what it <em>actually means.</em></p>', unsafe_allow_html=True)
st.markdown('<hr class="rule">', unsafe_allow_html=True)

# Examples
st.markdown('<span class="section-label">Try an example</span>', unsafe_allow_html=True)
st.selectbox(
    "Try an example",
    options=list(EXAMPLES.keys()),
    index=0,
    label_visibility="hidden",
    key="example_select",
    on_change=on_example_change
)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<span class="section-label">Your text</span>', unsafe_allow_html=True)

user_input = st.text_area(
    "Your text",
    height=185,
    placeholder="Paste a passage that made your eyes glaze over. Shakespeare, legalese, an academic abstract — anything that felt like it wasn't written for you.",
    label_visibility="hidden",
    key="main_textarea"
)
st.session_state.textarea_value = st.session_state.get("main_textarea", "")
user_input = st.session_state.textarea_value

if user_input:
    st.markdown(f'<p class="char-count">{len(user_input)} characters &nbsp;·&nbsp; ~{len(user_input.split())} words</p>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Translate →", key="translate_btn"):
    current_input = user_input.strip()
    if not current_input:
        st.warning("Nothing to translate yet — paste something above first.")
    else:
        with st.spinner(random.choice(LOADING_LINES)):
            prompt = f"### Original:\n{current_input}\n\n### Plain English:"
            start = time.time()
            result = generate(model, tokenizer, prompt=prompt, max_tokens=200, verbose=False)
            elapsed = round(time.time() - start, 1)

        output = result.strip()
        if "### " in output:
            output = output.split("### ")[0].strip()

        st.session_state.result = output
        st.session_state.elapsed = elapsed
        st.session_state.wit_line = random.choice(WIT_LINES)

if st.session_state.result:
    st.markdown('<hr class="rule">', unsafe_allow_html=True)
    st.markdown('<span class="section-label">Plain English</span>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="output-card">
        <p class="output-text">{st.session_state.result}</p>
        <p class="output-meta">Generated in {st.session_state.elapsed}s &nbsp;·&nbsp; {len(st.session_state.result.split())} words &nbsp;·&nbsp; Runs entirely on your machine — nothing sent to the cloud</p>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="transparency">
        <strong style="font-style:normal; color:#5C5850;">How this works:</strong>
        PlainSpeak is a 1.7B parameter model fine-tuned on 1,500 curated literary pairs.
        It performs best on 19th century prose, Shakespeare, and King James Bible passages.
        Results on legal, scientific, or highly abstract text may vary — this is v1, built in one evening.
        <a href="https://github.com/Brandi-Kinard/plainspeak">See the full model card →</a>
    </div>""", unsafe_allow_html=True)
    st.markdown(f'<p class="wit">{st.session_state.wit_line}</p>', unsafe_allow_html=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    Built by <a href="https://www.linkedin.com/in/brandi-kinard/" target="_blank">Brandi Kinard</a>
    &nbsp;·&nbsp; <a href="https://github.com/Brandi-Kinard/plainspeak" target="_blank">GitHub</a>
    &nbsp;·&nbsp; <a href="https://huggingface.co/Brandi-Kinard/plainspeak-smollm2-1.7b" target="_blank">Model on Hugging Face</a>
    <br>SmolLM2-1.7B · LoRA fine-tuned · 1,500 curated pairs · M1 Mac · No cloud compute
</div>""", unsafe_allow_html=True)
