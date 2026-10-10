# VS AI Studio V1 Free

A no-paid-API starter prototype for a personal AI creative workspace.

## Included
- Streamlit dashboard
- Image prompt builder
- Structured video prompt builder
- Voice-over script preparation
- Optional local text-to-speech attempt (`pyttsx3`, not installed by default)
- Temporary media preview

## Important limitations
This is a UI/workflow prototype. It does **not** generate AI images or AI videos yet. Those require a compatible model running locally or an API with available quota. Voice cloning is not included.

## Run on Windows
1. Install Python 3.11 or newer from https://www.python.org/downloads/
2. During setup, tick **Add Python to PATH**.
3. Extract this ZIP into a folder.
4. Double-click `run_windows.bat`.
5. When installation finishes, Streamlit should open in your browser. If it does not, open the terminal shown and visit `http://localhost:8501`.

Alternative commands in PowerShell, from the project folder:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Optional local TTS
The app includes a button that attempts to use `pyttsx3`, but it is not a required dependency. To try it:
```powershell
python -m pip install pyttsx3
```
Local voice quality and supported languages depend on installed Windows speech voices. This does not provide AI voice cloning or high-quality singing generation.

## Next milestones
1. Confirm the app starts on the PC.
2. Add a local/free image model if the PC has suitable hardware, or evaluate free API quotas.
3. Evaluate video generation separately; high-quality video models are usually resource-intensive or quota-limited.
4. Add a voice model and media merge workflow.
5. Only add paid services after explicitly reviewing costs.
