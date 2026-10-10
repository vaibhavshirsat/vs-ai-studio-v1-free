import os
import io
import streamlit as st
from PIL import Image

st.set_page_config(page_title="VS AI Studio V1 Free", page_icon="🎬", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 1.5rem; max-width: 1200px;}
.hero {padding: 1.3rem; border-radius: 18px; background: linear-gradient(135deg,#151927,#252b45); color: white;}
.small-muted {color: #aab1c5; font-size: .92rem;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>🎬 VS AI Studio <span style="font-size: .55em;">V1 Free</span></h1>
  <p>Create prompts, organize reference media, prepare voice-over scripts, and plan AI videos.</p>
  <p class="small-muted">Free starter prototype • No paid API required • Generation integrations can be added later</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Studio Menu")
    page = st.radio("Open workspace", [
        "🏠 Dashboard",
        "🖼️ Image Studio",
        "🎥 Video Studio",
        "🎙️ Voice Studio",
        "📁 Media Library",
        "⚙️ Setup & Limits"
    ])
    st.divider()
    st.caption("V1 Free prototype — does not call paid AI APIs.")

if "media" not in st.session_state:
    st.session_state.media = []
if "prompt_history" not in st.session_state:
    st.session_state.prompt_history = []

if page == "🏠 Dashboard":
    st.subheader("Welcome to your creative workspace")
    c1, c2, c3 = st.columns(3)
    c1.metric("Workspaces", "3", "Image • Video • Voice")
    c2.metric("API spend", "₹0", "No API connected")
    c3.metric("Generation", "Not connected", "Prototype mode")
    st.info("This first version gives you a working interface and prompt workflow. It does not yet generate AI images or videos by itself.")
    st.markdown("### Start here")
    st.markdown("""
    1. Open **Image Studio** to write and save an image prompt.
    2. Open **Video Studio** to plan a text-to-video or image-to-video scene.
    3. Open **Voice Studio** to prepare a voice-over script and optionally try local text-to-speech.
    4. Use **Media Library** to upload and preview reference files during this session.
    """)
    st.warning("Uploaded media and session history are temporary in this prototype. Download important files before closing the app.")

elif page == "🖼️ Image Studio":
    st.subheader("Image Studio")
    st.write("Prepare a prompt and upload a reference image. Actual AI generation will be connected in a later step.")
    mode = st.selectbox("Task", ["Text to Image", "Edit a Reference Image", "Thumbnail / Poster", "Character Reference"])
    prompt = st.text_area("Describe the image", placeholder="Example: Cinematic devotional scene, warm sunrise, detailed fabric, vertical 9:16...", height=130)
    negative = st.text_input("Avoid (optional)", placeholder="blurry, distorted hands, extra fingers, text artifacts")
    aspect = st.selectbox("Aspect ratio", ["9:16 — Shorts/Reels", "16:9 — YouTube", "1:1 — Square", "4:5 — Portrait", "3:2 — Landscape"])
    reference = st.file_uploader("Reference image (optional)", type=["png", "jpg", "jpeg", "webp"], key="image_ref")
    if reference:
        st.image(reference, caption="Reference image", width=300)
    if st.button("Save Image Prompt", type="primary"):
        if not prompt.strip():
            st.error("Enter a prompt first.")
        else:
            item = {"type": "Image Prompt", "task": mode, "prompt": prompt.strip(), "avoid": negative, "aspect": aspect}
            st.session_state.prompt_history.append(item)
            st.success("Prompt saved in this session.")
    if st.session_state.prompt_history:
        latest = st.session_state.prompt_history[-1]
        if latest.get("type") == "Image Prompt":
            st.markdown("#### Latest saved prompt")
            st.code(f"Task: {latest['task']}\nAspect: {latest['aspect']}\nPrompt: {latest['prompt']}\nAvoid: {latest['avoid']}")
            st.download_button("Download prompt as TXT", f"Task: {latest['task']}\nAspect: {latest['aspect']}\nPrompt: {latest['prompt']}\nAvoid: {latest['avoid']}\n", file_name="vs_image_prompt.txt")

elif page == "🎥 Video Studio":
    st.subheader("Video Studio")
    st.write("Build a structured prompt for a video model. Video generation is not connected in V1.")
    mode = st.selectbox("Generation mode", ["Text to Video", "Image to Video", "Continue / Extend a Clip"])
    subject = st.text_input("Subject / character", placeholder="A peaceful spiritual teacher in a traditional ashram")
    action = st.text_area("Action and motion", placeholder="Slowly raises one hand to bless the viewer, smiles naturally...", height=90)
    camera = st.selectbox("Camera movement", ["Static camera", "Slow push-in", "Slow pull-back", "Pan left", "Pan right", "Tracking shot"])
    setting = st.text_input("Environment", placeholder="Warm morning light, temple courtyard, subtle incense")
    duration = st.selectbox("Target duration", ["5 seconds", "8 seconds", "10 seconds", "15 seconds", "30 seconds"])
    ratio = st.selectbox("Video format", ["9:16 vertical", "16:9 landscape", "1:1 square"])
    style = st.selectbox("Visual style", ["Cinematic realistic", "Documentary", "Animation", "3D animated", "Illustration"])
    audio = st.selectbox("Audio plan", ["Generate audio if supported", "Add voice-over later", "No audio"])
    ref_video = st.file_uploader("Starting image or reference clip (optional)", type=["png", "jpg", "jpeg", "webp", "mp4", "mov"], key="video_ref")
    if ref_video:
        st.caption(f"Reference selected: {ref_video.name}")
        if ref_video.type.startswith("image"):
            st.image(ref_video, width=250)
        elif ref_video.type.startswith("video"):
            st.video(ref_video)
    if st.button("Build Video Prompt", type="primary"):
        if not subject.strip() or not action.strip():
            st.error("Please add a subject and describe the action.")
        else:
            video_prompt = (
                f"Create a {duration} {ratio} {style} video. "
                f"Subject: {subject.strip()}. Action: {action.strip()}. "
                f"Camera: {camera}. Environment: {setting or 'Use a visually coherent environment'}. "
                f"Audio: {audio}. Maintain consistent character appearance, natural motion, realistic anatomy, "
                "stable scene continuity, and no sudden cuts unless requested."
            )
            st.session_state.prompt_history.append({"type": "Video Prompt", "prompt": video_prompt})
            st.success("Video prompt created.")
            st.code(video_prompt)
            st.download_button("Download video prompt", video_prompt, file_name="vs_video_prompt.txt")

elif page == "🎙️ Voice Studio":
    st.subheader("Voice Studio")
    st.write("Prepare voice-over text. Optional local TTS may work if you install a system voice engine; quality and Marathi support depend on your computer.")
    language = st.selectbox("Language", ["Marathi", "Hindi", "English", "Mixed"])
    voice_style = st.selectbox("Delivery style", ["Warm and reassuring", "Devotional", "Energetic", "Calm narration", "Professional explainer", "Emotional"])
    script = st.text_area("Voice-over script", placeholder="Type the words you want spoken here...", height=180)
    st.caption("This prototype does not clone voices. Only use voices and recordings you own or have permission to use.")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Prepare Voice Script", type="primary"):
            if not script.strip():
                st.error("Enter a script first.")
            else:
                formatted = f"Language: {language}\nDelivery: {voice_style}\n\n{script.strip()}"
                st.session_state.prompt_history.append({"type": "Voice Script", "prompt": formatted})
                st.success("Voice script prepared.")
                st.code(formatted)
                st.download_button("Download voice script", formatted, file_name="vs_voice_script.txt")
    with c2:
        if st.button("Try Local Text-to-Speech"):
            if not script.strip():
                st.error("Enter a script first.")
            else:
                try:
                    import pyttsx3
                    engine = pyttsx3.init()
                    engine.setProperty("rate", 155)
                    output_path = os.path.abspath("vs_voice_output.wav")
                    engine.save_to_file(script.strip(), output_path)
                    engine.runAndWait()
                    if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
                        with open(output_path, "rb") as f:
                            audio_bytes = f.read()
                        st.audio(audio_bytes, format="audio/wav")
                        st.download_button("Download WAV", audio_bytes, file_name="vs_voice_output.wav", mime="audio/wav")
                    else:
                        st.warning("The local speech engine did not produce an audio file. Check your system TTS voices.")
                except Exception as e:
                    st.warning("Local TTS is not ready on this PC. Install the optional requirements and a compatible system voice engine.")
                    st.caption(f"Technical detail: {e}")

elif page == "📁 Media Library":
    st.subheader("Media Library")
    st.write("Upload reference files to preview them during this app session. Files are not permanently stored.")
    uploads = st.file_uploader("Upload images, audio or video", type=["png", "jpg", "jpeg", "webp", "mp3", "wav", "mp4", "mov"], accept_multiple_files=True)
    if uploads:
        for f in uploads:
            st.markdown(f"**{f.name}** · {f.type or 'unknown type'} · {len(f.getvalue())/1024:.1f} KB")
            if (f.type or "").startswith("image"):
                st.image(f, width=250)
            elif (f.type or "").startswith("audio"):
                st.audio(f)
            elif (f.type or "").startswith("video"):
                st.video(f)

elif page == "⚙️ Setup & Limits":
    st.subheader("Setup & Limits")
    st.markdown("""
    **Current V1 status**
    - Dashboard and prompt builder: included
    - Reference media preview: included
    - Local text-to-speech: optional, depends on PC setup
    - AI image generation: not connected
    - AI video generation: not connected
    - Voice cloning: not included
    - Cloud storage / user accounts: not included

    **Cost protection**
    - No API keys are required for this prototype.
    - Do not paste API keys into chat or public repositories.
    - Later, connect a model only after checking its free tier, quotas and terms.
    """)
    st.markdown("**Recommended next step:** confirm the app runs, then add one generation provider at a time.")
