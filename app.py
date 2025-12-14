import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import requests
from io import BytesIO
from dotenv import load_dotenv
import json
import base64
import time

# ================= Load API Key =================
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

# ================= Page Config =================
st.set_page_config(page_title="Image Chatbot", page_icon="🤖", layout="wide")

# ================= Session State =================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "image" not in st.session_state:
    st.session_state.image = None
if "system_instruction" not in st.session_state:
    st.session_state.system_instruction = ""

# ================= Custom CSS =================
st.markdown("""
    <style>
        .header-title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: white;
            margin-bottom: 20px;
        }
        .chat-box {
            max-height: 450px;
            overflow-y: auto;
            overflow-x: hidden;
            padding: 10px;
            border-radius: 12px;
            background-color: #f7f7f7;
        }
        /* Custom scrollbar styling */
        .chat-box::-webkit-scrollbar {
            width: 10px;
        }
        .chat-box::-webkit-scrollbar-track {
            background: #e0e0e0;
            border-radius: 10px;
        }
        .chat-box::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 10px;
        }
        .chat-box::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
        .user-msg {
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            color: white;
            padding: 12px;
            border-radius: 15px;
            margin: 5px 0;
            text-align: right;
            max-width: 70%;
            float: right;
            clear: both;
        }
        .bot-msg {
            background: #e0e0e0;
            color: black;
            padding: 12px;
            border-radius: 15px;
            margin: 5px 0;
            text-align: left;
            max-width: 70%;
            float: left;
            clear: both;
        }
        .image-card {
            border-radius: 15px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
            padding: 5px;
            margin-bottom: 15px;
            max-width: 400px;
        }
        .sidebar .stButton>button {
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# ================= Header =================
st.markdown('<div class="header-title">🤖 Image Chatbot</div>', unsafe_allow_html=True)

# ================= Sidebar =================
st.sidebar.header("📂 Upload Image / Options")

# Image upload or URL
uploaded_file = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
image_url = st.sidebar.text_input("Or enter an image URL")

if uploaded_file:
    st.session_state.image = Image.open(uploaded_file)
elif image_url:
    try:
        response = requests.get(image_url)
        st.session_state.image = Image.open(BytesIO(response.content))
    except:
        st.sidebar.error("⚠️ Invalid URL or failed to load image")

# Clear Chat Button
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = []

# Download Chat Button
if st.sidebar.button("💾 Download Chat"):
    if st.session_state.messages:
        chat_data = json.dumps(st.session_state.messages, indent=2)
        st.sidebar.download_button(
            label="Download Chat as JSON",
            data=chat_data,
            file_name="chat_history.json",
            mime="application/json"
        )
    else:
        st.sidebar.info("No chat to download!")

# ================= Customize Chatbot Behavior =================
st.sidebar.divider()
st.sidebar.header("🎯 Customize Chatbot")

# System instruction input
system_instruction = st.sidebar.text_area(
    "System Instructions",
    value=st.session_state.system_instruction,
    height=150,
    help="Define how the chatbot should behave. Examples:\n"
         "- 'You are a friendly and helpful assistant.'\n"
         "- 'Answer in a professional, technical style.'\n"
         "- 'Always be concise and use bullet points.'\n"
         "- 'Respond as a creative writing coach.'"
)

# Update session state when instruction changes
if system_instruction != st.session_state.system_instruction:
    st.session_state.system_instruction = system_instruction
    # Clear chat when instructions change to apply new behavior
    if st.session_state.messages:
        st.sidebar.info("💡 Clear chat to apply new instructions")

# Preset instruction templates
st.sidebar.subheader("📋 Presets")
preset_col1, preset_col2 = st.sidebar.columns(2)

with preset_col1:
    if st.button("👨‍💼 Professional", use_container_width=True):
        st.session_state.system_instruction = "You are a professional, knowledgeable assistant. Provide clear, accurate, and well-structured responses. Use formal language and be concise."
        st.rerun()
    
    if st.button("😊 Friendly", use_container_width=True):
        st.session_state.system_instruction = "You are a friendly and approachable assistant. Be warm, conversational, and helpful. Use a casual but respectful tone."
        st.rerun()

with preset_col2:
    if st.button("🎨 Creative", use_container_width=True):
        st.session_state.system_instruction = "You are a creative and imaginative assistant. Think outside the box, use vivid descriptions, and encourage creative thinking."
        st.rerun()
    
    if st.button("📚 Educational", use_container_width=True):
        st.session_state.system_instruction = "You are an educational assistant. Explain concepts clearly, provide examples, and help users learn. Break down complex topics into understandable parts."
        st.rerun()

# Reset instruction button
if st.sidebar.button("🔄 Reset Instructions", use_container_width=True):
    st.session_state.system_instruction = ""
    st.rerun()

# ================= Main Chat Area =================
# Show uploaded image as small card
if st.session_state.image:
    st.image(st.session_state.image, caption="Selected Image", width=350)

# Scrollable chat container
st.markdown('<div class="chat-box">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">{msg["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ================= Chat Input =================
if prompt := st.chat_input("Ask something about the image..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        # Cache model selection to avoid listing models on every request
        if "selected_model" not in st.session_state:
            # List all available models
            all_models = list(genai.list_models())
            
            # Find models that support generateContent
            supported_models = [
                m for m in all_models 
                if 'generateContent' in m.supported_generation_methods
            ]
            
            if not supported_models:
                available_names = [m.name for m in all_models[:5]]  # Show first 5 for debugging
                raise Exception(
                    f"No models found that support generateContent. "
                    f"Available models: {', '.join(available_names)}"
                )
            
            # Prefer models with 'flash' or 'pro' in the name (usually support vision)
            # Sort to prefer flash models (faster) then pro models
            preferred = [m for m in supported_models if 'flash' in m.name.lower()]
            if not preferred:
                preferred = [m for m in supported_models if 'pro' in m.name.lower()]
            if not preferred:
                preferred = supported_models
            
            # Select the first preferred model
            selected = preferred[0]
            model_name = selected.name  # Keep full name like "models/gemini-1.5-flash-001"
            
            # Store in session state
            st.session_state.selected_model = model_name
            st.session_state.model_display_name = model_name.replace('models/', '')
            st.sidebar.info(f"📌 Model: {st.session_state.model_display_name}")
        
        # Use cached model with system instruction if provided
        try:
            if st.session_state.system_instruction:
                # Try to use system_instruction parameter (works for Gemini 1.5+)
                model = genai.GenerativeModel(
                    st.session_state.selected_model,
                    system_instruction=st.session_state.system_instruction
                )
            else:
                model = genai.GenerativeModel(st.session_state.selected_model)
        except Exception:
            # Fallback: if system_instruction parameter not supported, prepend to prompt
            model = genai.GenerativeModel(st.session_state.selected_model)
            if st.session_state.system_instruction:
                prompt = f"[System Instruction: {st.session_state.system_instruction}]\n\nUser: {prompt}"

        # Prepare multimodal parts: text + binary image (downscale to reduce tokens)
        parts = [prompt]
        if st.session_state.image:
            img = st.session_state.image.copy()
            max_dim = 512
            w, h = img.size
            scale = min(1.0, max_dim / max(w, h))
            if scale < 1.0:
                img = img.resize((int(w * scale), int(h * scale)))
            img_bytes = BytesIO()
            img.save(img_bytes, format="PNG")
            parts.append({"mime_type": "image/png", "data": img_bytes.getvalue()})

        # Retry with backoff for quota (429) errors
        attempts = 0
        answer = None
        last_error = None
        while attempts < 3 and answer is None:
            try:
                response = model.generate_content(parts)
                answer = response.text
            except Exception as gen_err:
                last_error = gen_err
                err_str = str(gen_err)
                if "429" in err_str or "quota" in err_str.lower():
                    # Respect suggested retry delay if present, else default 45s
                    time.sleep(45)
                    attempts += 1
                    continue
                else:
                    raise

        if answer is None:
            raise last_error if last_error else RuntimeError("Failed to get response after retries")

        # Save assistant response
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.write(answer)

    except Exception as e:
        st.error(f"❌ Error: {e}")
