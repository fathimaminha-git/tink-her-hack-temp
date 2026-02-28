import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- AI SETUP ---
# Securely handle the API Key
# Replace 'YOUR_GEMINI_API_KEY' with your actual key from Google AI Studio
API_KEY = "AIzaSyBHpDa19rZ7Dx4cRFs9ot8JNRpsKnhU7YA"
genai.configure(api_key="AIzaSyBHpDa19rZ7Dx4cRFs9ot8JNRpsKnhU7YA")
model = genai.GenerativeModel('gemini-2.5-flash')

# Initialize Eco-Points in the session so they don't reset on refresh
if 'eco_points' not in st.session_state:
    st.session_state.eco_points = 0

# --- WEBSITE UI DESIGN ---
st.set_page_config(page_title="TrashTalk AI", page_icon="🗑️", layout="centered")

st.title("🗑️ TrashTalk AI")
st.markdown("""
### Earth Deserves Better!
Upload a photo of your trash. Our AI will **roast** your lifestyle choices, identify the waste type, and teach you how to decompose it. 
Earn **1,000 Eco-Points** to get your official certificate!
""")

st.divider()

# --- STEP 1: IMAGE UPLOAD ---
uploaded_file = st.file_uploader("Upload your 'shameful' waste here...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)

    # --- STEP 2: AI PROMPT (The "Brain") ---
    # This tells the AI exactly how to behave
    prompt = """
    You are 'TrashTalk AI', a sarcastic, witty, and slightly mean environmentalist.
    Analyze the image and provide the following:
    1. ROAST: Brutally but funnily roast the user for owning/using this specific item.
    2. IDENTIFY: What is the object and what material is it made of?
    3. WASTE CATEGORY: Is it Recyclable, Organic/Compostable, or Landfill?
    4. DECOMPOSE/DISPOSE: Give a short, practical instruction on how to dispose of it properly.
    5. ECO-POINTS: Reward the user with 20 points for reporting it.
    
    Keep the tone funny, insulting, but educational. Use emojis.
    """

    with st.spinner("Analyzing your terrible life choices..."):
        try:
            # Send image and prompt to Gemini AI
            response = model.generate_content([prompt, image])
            
            # --- STEP 3: DISPLAY RESULTS ---
            st.subheader("🤖 TrashTalk AI's Verdict:")
            st.info(response.text)

            # Update Points
            st.session_state.eco_points += 20
            
        except Exception as e:
            st.error(f"Error: {e}. Make sure your API Key is valid!")

# --- STEP 4: PROGRESS BAR & POINTS ---
st.sidebar.header("Your Progress")
progress_percentage = min(st.session_state.eco_points / 1000, 1.0)
st.sidebar.progress(progress_percentage)
st.sidebar.metric(label="Total Eco-Points", value=f"{st.session_state.eco_points} / 1000")

# --- STEP 5: THE CERTIFICATE ---
if st.session_state.eco_points >= 1000:
    st.balloons()
    st.success("🎉 ACHIEVEMENT UNLOCKED: 1000 ECO-POINTS!")
    
    st.markdown("""
    <div style="border:10px solid #04aa6d; padding:20px; text-align:center;">
        <h1>OFFICIAL CERTIFICATE</h1>
        <p>This certifies that you are a</p>
        <h2>FRIEND OF THE EARTH</h2>
        <p><i>(Who still sucks, but slightly less than before)</i></p>
        <p>Certified by TrashTalk AI 🗑️</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.button("Download Certificate (Coming Soon)")