import streamlit as st
import google.generativeai as genai
import json

# Configuration
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3-flash-preview')

st.set_page_config(page_title="The Bias Lens", page_icon="🚩")

st.title("🚩 The Bias Lens")
st.markdown("### Simple Clickbait & Fake News Detector")

user_input = st.text_area("Paste news text or a short paragraph here:", height=150)

if st.button("Analyze Content"):
    if user_input:
        with st.spinner("Analyzing with Gemini AI..."):
            # Strict system prompt for JSON output
            prompt = f"""
                    You are a 2026 News Verifier. 
                    Analyze the text based on events up to April 2026. 
                    Identify if this is a factual report of diplomatic activities.

                    Return STRICT JSON:
                    - sensationalism_score: integer 1-10
                    - fallacies: list
                    - red_flags: list
                    - truth_probability: integer 0-100 (If the event is verified in your 2026 database, this should be high)
                    - summary: string

                    Text: {user_input}
                    """
            
            try:
                response = model.generate_content(prompt)
                # Clean the response text to ensure it's valid JSON
                clean_json = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(clean_json)

                # Layout
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Truth Probability", f"{data['truth_probability']}%")
                with col2:
                    st.metric("Sensationalism", f"{data['sensationalism_score']}/10")

                st.progress(data['truth_probability'] / 100)

                st.subheader("🚩 Red Flag Sentences")
                for item in data['red_flags']:
                    st.error(item)

                st.subheader("🧠 Logical Fallacies Found")
                if data['fallacies']:
                    for f in data['fallacies']:
                        st.warning(f)
                else:
                    st.success("No major logical fallacies detected.")

                st.info(f"**AI Summary:** {data['summary']}")

            except Exception as e:
                st.error(f"Error: {e}. Try again or check your API key.")
    else:
        st.warning("Please paste some text first!")