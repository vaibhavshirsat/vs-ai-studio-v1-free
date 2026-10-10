import os
import io
import base64
import tempfile
import streamlit as st
from PIL import Image

st.set_page_config(page_title="VS AI Studio V2 Engine", page_icon="🎬", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 1.2rem; max-width: 1250px;}
.hero {padding: 1.25rem 1.5rem; border-radius: 18px; background: linear-gradient(135deg,#151927,#252b45); color: white;}
div.stButton > button[kind="primary"] {border-radius: 10px; font-weight: 650;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>🎬 VS AI Studio <span style="font-size:.55em">V2 Engine</span></h1>
<p>Image generation • Video generation workflow • Voice-over</p>
<p style="color:#b9c2dc">Real model integrations where configured. No claim of unlimited free generation.</p>
</div>
""", unsafe_allow_html=True)

def get_secret(name, fallback=""):
    try:
        return st.secrets.get(name, fallback)
    except Exception:
        return os.getenv(name, fallback)

def save_bytes_download(data, filename, mime):
    st.download_button(f"Download {filename}", data=data, file_name=filename, mime=mime)

with st.sidebar:
    st.header("Studio")
    page = st.radio("Workspace", [
        "🏠 Dashboard", "🖼️ Image Engine", "🎥 Video Engine",
        "🎙️ Voice Studio", "📁 Media Tools", "⚙️ API Setup"
    ])
    st.divider()
    st.caption("API keys must be configured as Streamlit secrets. Never put keys in public code.")

if "generated_images" not in st.session_state:
    st.session_state.generated_images = []
if "history" not in st.session_state:
    st.session_state.history = []

if page == "🏠 Dashboard":
    st.subheader("Engine status")
    c1,c2,c3 = st.columns(3)
    c1.metric("Image engine", "Ready to configure")
    c2.metric("Video engine", "API-dependent")
    c3.metric("Voice", "Local TTS option")
    st.info("This version calls a real image-generation API when you configure a valid key and a model that your account can access. Video generation may require paid access. The app will not enable billing for you.")
    st.markdown("### Recommended order")
    st.markdown("1. Configure a provider key in **API Setup**.\n2. Test one image in **Image Engine**.\n3. Try local text-to-speech in **Voice Studio**.\n4. Configure video only after checking the provider's current pricing and account access.")

elif page == "🖼️ Image Engine":
    st.subheader("Real AI Image Generation")
    st.write("Uses Google's Gen AI Python SDK. Model access and price depend on your account; image generation models may not have a free tier.")
    api_key = get_secret("GEMINI_API_KEY")
    if not api_key:
        st.warning("GEMINI_API_KEY is not configured. Add it under Streamlit app Settings → Secrets, or use a local .env/environment variable. Do not paste the key into the prompt.")
    prompt = st.text_area("Image prompt", height=150, placeholder="A cinematic devotional portrait of Lord Shiva in the Himalayas...")
    aspect = st.selectbox("Aspect ratio", ["9:16", "16:9", "1:1", "4:5", "3:2"])
    size = st.selectbox("Image size", ["1K", "2K", "4K"], index=0)
    model = st.selectbox("Image model", ["gemini-3.1-flash-image", "gemini-3-pro-image"], index=0)
    ref = st.file_uploader("Reference image (optional)", type=["png","jpg","jpeg","webp"], key="img_ref")
    if ref:
        st.image(ref, caption="Reference image", width=280)
    allow_call = st.checkbox("I checked the current pricing and understand this API request may be billable.")
    if st.button("Generate Image", type="primary", disabled=not bool(prompt.strip())):
        if not api_key:
            st.error("Missing API key. Configure GEMINI_API_KEY in Streamlit Secrets first.")
        elif not allow_call:
            st.error("Confirm the pricing checkbox before making an API request.")
        else:
            try:
                from google import genai
                client = genai.Client(api_key=api_key)
                input_items = [{"type":"text","text":prompt.strip()}]
                if ref:
                    ref_bytes = ref.getvalue()
                    input_items.insert(0, {
                        "type":"image",
                        "mime_type": ref.type or "image/png",
                        "data": base64.b64encode(ref_bytes).decode("utf-8")
                    })
                with st.spinner("Generating image… this may take a little while."):
                    result = client.interactions.create(
                        model=model,
                        input=input_items,
                        response_format={"type":"image","mime_type":"image/png","aspect_ratio":aspect,"image_size":size}
                    )
                image_data = None
                for step in getattr(result, "steps", []) or []:
                    for part in getattr(step, "content", []) or []:
                        if getattr(part, "type", "") == "image":
                            image_data = getattr(part, "data", None)
                if image_data is None:
                    out_img = getattr(result, "output_image", None)
                    image_data = getattr(out_img, "data", None) if out_img else None
                if isinstance(image_data, str):
                    image_bytes = base64.b64decode(image_data)
                elif image_data:
                    image_bytes = image_data
                else:
                    image_bytes = None
                if image_bytes:
                    st.image(image_bytes, caption="Generated image", use_container_width=True)
                    save_bytes_download(image_bytes, "vs_ai_generated.png", "image/png")
                    st.session_state.generated_images.append({"prompt":prompt.strip(),"bytes":image_bytes})
                    st.success("Image generated successfully.")
                else:
                    st.warning("The API returned a response, but this SDK response format did not expose image bytes as expected. Check SDK version/model access and share the error/output details (never share your key).")
                    st.write(getattr(result, "output_text", str(result)))
            except Exception as e:
                st.error("Image generation failed. Check the model name, API access, quota, SDK version and billing status.")
                st.code(str(e))
    st.caption("If the selected model has no free tier, this request can cost money after billing is enabled. The checkbox is a reminder, not a spending cap.")

elif page == "🎥 Video Engine":
    st.subheader("Video generation")
    st.warning("Video generation is not activated in this build because provider access and pricing vary. We will not make a video API call until a provider/model and cost are confirmed.")
    mode = st.selectbox("Workflow", ["Text to Video", "Image to Video", "Storyboard plan"])
    subject = st.text_input("Subject", placeholder="A devotional scene in a Himalayan temple")
    action = st.text_area("Motion / action", placeholder="The subject slowly raises a hand; mist moves gently; camera pushes in.")
    camera = st.selectbox("Camera", ["Slow push-in","Static camera","Pan left","Pan right","Tracking shot"])
    duration = st.selectbox("Target duration", ["5 seconds","8 seconds","10 seconds","15 seconds"])
    ratio = st.selectbox("Aspect ratio", ["9:16 vertical","16:9 landscape","1:1 square"])
    audio = st.selectbox("Audio", ["Voice-over added later","Model-generated audio if supported","No audio"])
    if st.button("Build production video prompt", type="primary"):
        if not subject.strip() or not action.strip():
            st.error("Enter a subject and motion.")
        else:
            p = f"Create a {duration} {ratio} cinematic video. Subject: {subject}. Motion: {action}. Camera: {camera}. Audio: {audio}. Maintain consistent appearance, natural movement, coherent physics, stable framing and no unexpected cuts."
            st.code(p)
            save_bytes_download(p.encode(), "vs_video_prompt.txt", "text/plain")
            st.success("Prompt plan generated. This does not render a video yet.")

elif page == "🎙️ Voice Studio":
    st.subheader("Voice-over Studio")
    script = st.text_area("Text to speak", height=180, placeholder="नमस्कार मित्रांनो, आपल्या VS AI Studio मध्ये स्वागत आहे.")
    rate = st.slider("Speaking rate", 100, 220, 155)
    st.caption("Local TTS uses installed system voices; language/voice quality varies. This is not voice cloning or singing generation.")
    if st.button("Generate local voice", type="primary"):
        if not script.strip():
            st.error("Enter text first.")
        else:
            try:
                import pyttsx3
                with tempfile.TemporaryDirectory() as td:
                    out = os.path.join(td, "vs_voice.wav")
                    engine = pyttsx3.init()
                    engine.setProperty("rate", rate)
                    engine.save_to_file(script.strip(), out)
                    engine.runAndWait()
                    if os.path.exists(out) and os.path.getsize(out) > 1000:
                        audio = open(out, "rb").read()
                        st.audio(audio, format="audio/wav")
                        save_bytes_download(audio, "vs_voice.wav", "audio/wav")
                    else:
                        st.warning("No audio file was produced. Check installed Windows speech voices and TTS setup.")
            except Exception as e:
                st.error("Local TTS is not installed or no compatible system voice is available.")
                st.code(str(e))
                st.info("Optional install: python -m pip install pyttsx3")

elif page == "📁 Media Tools":
    st.subheader("Media tools")
    files = st.file_uploader("Upload image/audio/video files", type=["png","jpg","jpeg","webp","wav","mp3","mp4","mov"], accept_multiple_files=True)
    if files:
        for f in files:
            st.markdown(f"**{f.name}** · {len(f.getvalue())/1024:.1f} KB")
            if (f.type or "").startswith("image"):
                st.image(f, width=280)
            elif (f.type or "").startswith("audio"):
                st.audio(f)
            elif (f.type or "").startswith("video"):
                st.video(f)
    st.markdown("### Image resize")
    img_file = st.file_uploader("Choose an image to resize", type=["png","jpg","jpeg","webp"], key="resize")
    if img_file:
        try:
            image = Image.open(img_file).convert("RGB")
            st.image(image, caption=f"Original: {image.width}×{image.height}", width=320)
            max_width = st.slider("Output width", 256, 4096, min(2048, image.width))
            if st.button("Resize image"):
                ratio = max_width / image.width
                resized = image.resize((max_width, max(1, int(image.height*ratio))))
                buf = io.BytesIO()
                resized.save(buf, format="PNG")
                st.image(resized, caption=f"Resized: {resized.width}×{resized.height}", width=320)
                save_bytes_download(buf.getvalue(), "vs_resized.png", "image/png")
        except Exception as e:
            st.error(str(e))

elif page == "⚙️ API Setup":
    st.subheader("Configure secrets")
    st.markdown("""
    **For Streamlit Community Cloud**
    1. Open your app dashboard on Streamlit Community Cloud.
    2. Open app menu → **Settings** → **Secrets**.
    3. Add the following TOML entry (replace the placeholder locally; never share the real key):
    ```toml
    GEMINI_API_KEY = "PASTE_YOUR_KEY_HERE"
    ```
    4. Save and reboot the app.

    **For local Windows**
    Set an environment variable named `GEMINI_API_KEY`, or create a local `.streamlit/secrets.toml` file. Do not commit secrets.toml to GitHub.

    Get keys from Google AI Studio. Check current model availability and pricing before generating images. A valid key does not mean all models are free.
    """)
    st.markdown("[Open Google AI Studio](https://aistudio.google.com/)")
    st.markdown("[Official image-generation docs](https://ai.google.dev/gemini-api/docs/image-generation)")
    st.markdown("[Official pricing](https://ai.google.dev/gemini-api/docs/pricing)")
