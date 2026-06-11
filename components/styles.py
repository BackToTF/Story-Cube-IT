from __future__ import annotations

import streamlit as st


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700;800&family=Nunito+Sans:wght@400;600;700&display=swap');

        .stApp { font-family: 'Nunito Sans', sans-serif; background: radial-gradient(1300px 800px at 50% -20%, #ffffff 0%, #f7f7f4 62%, #f3f3f1 100%); }

        .main .block-container {
            max-width: 1120px;
            padding: 0.8rem 1.2rem 1.2rem 1.2rem;
            border: 1px solid #cfd7de;
            border-radius: 26px;
            background: #fbfbfa;
            box-shadow: 0 18px 42px rgba(15, 36, 56, 0.10);
            margin-top: 10px;
            margin-bottom: 16px;
        }

        .brand-wrap { text-align: center; margin: 4px 0 6px 0; }
        .brand-line { display: inline-flex; align-items: center; gap: 10px; }
        .brand-main {
            margin: 0;
            font-size: clamp(2.2rem, 5vw, 5.2rem);
            font-family: 'Montserrat', sans-serif;
            font-weight: 800;
            letter-spacing: 0.03em;
            color: #003a63;
            line-height: 1;
            text-shadow: 0 1px 0 #001f35;
            text-transform: uppercase;
        }
        .brand-sub {
            margin-top: 6px;
            font-size: clamp(1.8rem, 4vw, 4rem);
            font-family: 'Montserrat', sans-serif;
            font-weight: 800;
            letter-spacing: 0.04em;
            color: #ff9f00;
            text-shadow: 0 1px 0 #d27400;
            text-transform: uppercase;
        }
        .brand-dice {
            width: 46px; height: 46px; border: 3px solid #003a63; border-radius: 12px;
            display: inline-grid; grid-template-columns: repeat(3, 1fr); gap: 3px; padding: 6px;
            background: linear-gradient(180deg, #eff8ff 0%, #dcefff 100%); box-shadow: 0 3px 0 #001f35;
        }
        .brand-dice span {
            width: 8px; height: 8px; border-radius: 50%; background: #1a5b8d;
            justify-self: center; align-self: center; opacity: 0;
        }
        .brand-dice span:nth-child(1), .brand-dice span:nth-child(3), .brand-dice span:nth-child(5), .brand-dice span:nth-child(7), .brand-dice span:nth-child(9) { opacity: 1; }

        .screen-subtitle {
            text-align: center;
            font-size: clamp(1.4rem, 2.2vw, 2rem);
            color: #003a63;
            margin: 0;
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            text-shadow: 0 1px 0 #001f35;
        }
        .screen-note { text-align: center; font-size: clamp(0.96rem, 1.5vw, 1.15rem); color: #10273d; margin: 2px 0 6px 0; }
        .section-title {
            margin: 10px 0 10px 0; padding-top: 6px; border-top: 3px solid #0f4c73;
            font-family: 'Montserrat', sans-serif; font-size: clamp(1.9rem, 2.8vw, 2.8rem);
            color: #003a63; letter-spacing: 0.02em; text-transform: uppercase; font-weight: 800;
        }

        .stButton button, .stFormSubmitButton button {
            border: 1px solid #d77a00; border-radius: 14px; font-weight: 800; font-family: 'Montserrat', sans-serif;
            font-size: 0.98rem; background: linear-gradient(180deg, #ffa600 0%, #ff9800 100%);
            color: #ffffff; text-shadow: 0 1px 0 #b55f00; box-shadow: 0 2px 0 #d77a00; min-height: 42px;
        }

        .stTextInput input, .stTextArea textarea, .stNumberInput input {
            border: 2px solid #c3ced8 !important; border-radius: 14px !important; background: #ffffff !important;
            color: #112336 !important; font-size: 1.05rem !important;
        }

        .stSlider [role='slider'] { background: #ffb000 !important; box-shadow: 0 0 0 2px #ff9800 !important; }

        .dice-roll-stage { border-radius: 16px; border: 1px dashed #99afc1; padding: 10px; background: #ffffff; color: #003a63; text-align: center; font-weight: 700; }

        .dice-icon-card {
            border: 2px solid #0f4c73; border-radius: 22px; padding: 10px 8px; background: #fbfbfa;
            box-shadow: 0 6px 0 rgba(15, 76, 115, 0.18); margin: 0 auto; max-width: 210px;
        }
        .dice-mini-label { text-align: center; color: #0f4c73; font-weight: 800; margin-top: 6px; font-size: 0.92rem; }

        .status-card {
            border: 1px solid #c7d3de;
            border-radius: 12px;
            background: #ffffff;
            padding: 8px 10px;
            min-height: 66px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 4px;
        }
        .status-title {
            font-size: 0.78rem;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            color: #4b647b;
            font-weight: 800;
            font-family: 'Montserrat', sans-serif;
        }
        .status-value {
            font-size: 0.96rem;
            color: #0f3456;
            font-weight: 800;
            line-height: 1.2;
            word-break: break-word;
            font-family: 'Nunito Sans', sans-serif;
        }

        .story-row { display: flex; gap: 12px; align-items: flex-start; margin-bottom: 10px; }
        .story-avatar {
            width: 50px; height: 50px; border-radius: 50%; display: flex; justify-content: center; align-items: center;
            font-family: 'Montserrat', sans-serif; font-size: 1.2rem; font-weight: 800; color: #fff;
            border: 2px solid #d77a00; background: linear-gradient(180deg, #ffb000 0%, #ff8f00 100%); box-shadow: 0 2px 0 #d77a00;
        }
        .story-bubble { flex: 1; border: 2px solid #d4dce3; border-radius: 16px; background: #ffffff; padding: 12px 14px; }
        .story-bubble.intervention { border-color: #1d4ed8; background: #eff6ff; }
        .story-name { font-family: 'Montserrat', sans-serif; color: #003a63; font-size: 1.05rem; margin-bottom: 4px; font-weight: 700; }
        .story-text { margin: 0; color: #102133; font-size: 1.02rem; line-height: 1.4; }
        .story-meta { margin-top: 8px; font-size: 0.92rem; color: #0f4c73; }
        .story-badge {
            display: inline-block; margin-bottom: 6px; padding: 3px 10px; border-radius: 999px;
            background: #dbeafe; color: #1d4ed8; font-size: 0.8rem; font-weight: 800; text-transform: uppercase;
        }
        .story-options { margin-top: 8px; display: flex; flex-wrap: wrap; gap: 6px; }
        .story-option-chip {
            background: #f8fafc; border: 1px solid #c7d3de; border-radius: 999px; padding: 4px 10px;
            color: #0f4c73; font-size: 0.84rem;
        }

        .results-side { border: 2px solid #d4dce3; border-radius: 16px; background: #ffffff; padding: 14px; text-align: center; min-height: 280px; }
        .results-side-title { font-family: 'Montserrat', sans-serif; color: #003a63; font-size: 2rem; margin: 0 0 8px 0; text-transform: uppercase; font-weight: 800; }
        .results-side-archetype { color: #003a63; font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 2.1rem; margin: 6px 0; }
        .results-side-text { color: #112336; font-size: 1.2rem; line-height: 1.35; }

        .final-card { border: 2px solid #c7d3de; border-radius: 18px; background: #fff; padding: 18px; margin-bottom: 14px; }
        .final-player { color: #003a63; font-family: 'Montserrat', sans-serif; font-size: 1.9rem; margin: 0 0 8px 0; font-weight: 800; }
        .final-row { display: flex; gap: 12px; align-items: center; }
        .final-icon {
            width: 64px; height: 64px; border-radius: 50%; display: flex; justify-content: center; align-items: center;
            font-family: 'Montserrat', sans-serif; font-size: 1.7rem; font-weight: 800; color: #fff;
            border: 2px solid #d77a00; background: linear-gradient(180deg, #ffb000 0%, #ff8f00 100%); box-shadow: 0 2px 0 #d77a00;
        }
        .final-archetype { color: #003a63; font-family: 'Montserrat', sans-serif; font-size: 2.4rem; margin: 0; font-weight: 800; }
        .final-description { margin-top: 4px; color: #112336; font-size: 1.25rem; line-height: 1.35; }
        .final-email { margin-top: 8px; color: #0f4c73; font-size: 0.95rem; font-style: italic; }

        @media (max-width: 900px) {
            .main .block-container { padding: 1rem 1rem 1.8rem 1rem; border-radius: 18px; }
            .brand-dice { width: 40px; height: 40px; }
            .story-avatar, .final-icon { width: 44px; height: 44px; font-size: 1.2rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_brand_header() -> None:
    st.markdown(
        """
        <div class='brand-wrap'>
          <div class='brand-line'>
            <div class='brand-dice'>
              <span></span><span></span><span></span>
              <span></span><span></span><span></span>
              <span></span><span></span><span></span>
            </div>
            <h1 class='brand-main'>STORY CUBE</h1>
          </div>
          <div class='brand-sub'>I&D EDITION</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
