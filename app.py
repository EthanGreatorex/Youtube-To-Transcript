# imports

# streamlit is for the web app
import streamlit as st
# pytube is for extracting the url id
from pytube import extract
# pyperclip is for copying the transcript to the clipboard
import pyperclip
# youtube_transcript_api is for fetching the transcript
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

# This is to disable comments being added to the web page by streamlit
magicEnabled = False


'''
Extracts the video ID from the URL
Uses pytubes extract module
'''
def extract_id(URL):
    try:
        ID = extract.video_id(URL)
    except:
        st.error("Invalid URL! Please enter a valid YouTube video URL.")
        st.stop()
    else:
        return ID



'''
Returns data from the video in the following format:

{
    'text': 'Hey there',
    'start': 7.58,
    'duration': 6.13
},
{
    'text': 'how are you',
    'start': 14.08,
    'duration': 7.58
},
# ...
'''
def fetch_transcript(URL):
    try:
        TRANSCRIPT = YouTubeTranscriptApi.get_transcript(URL)
    except TranscriptsDisabled:
        st.error("Transcripts are disabled for this video! Please try another video.")
        st.stop()
    except NoTranscriptFound:
        st.error("No transcript found for this video! Please try another video.")
        st.stop()
    except VideoUnavailable:
        st.error("Video is unavailable! Please try another video.")
        st.stop()
    except Exception:
        st.error(f"Whoops! Looks like I ran into a problem :(")
        st.stop()
    else:
        return TRANSCRIPT


'''
Function to output the transcript in a readable format
'''
def output_transcript(TRANSCRIPT):
    for line in TRANSCRIPT:
        print(line['text'])


st.title("YouTube Video To Transcript Converter")
st.subheader("🤖")
st.write("_Give me a YouTube video URL and I will give you the transcript!_") 

st.error("Warning: YouTube may block the api from fetching the transcript as it is run from a cloud server, if this occurs you will reveive an error message such as '_No transcript found for this video..._' Running the app locally is the only workaround for this issue.")
URL = st.text_input("Enter the URL of the YouTube video 🎧🎞️", placeholder="https://www.youtube.com/imayoutubevideo")

if 'transcript' not in st.session_state:
    st.session_state.transcript = None

submit_button = st.button("Convert 🚀")

if submit_button and URL:
    st.session_state.transcript = None
    progress_bar = st.progress(10, "🪪 Extracting Video ID ... 🪪")
    URL_ID = extract_id(URL)
    progress_bar.progress(30, "📜 Fetching Transcript ...📜")
    TRANSCRIPT = fetch_transcript(URL_ID)
    progress_bar.progress(100, "✅ Transcript Ready! ✅")

    TRANSCRIPT = [line['text'] for line in TRANSCRIPT]
    TRANSCRIPT = ' '.join(TRANSCRIPT)

    st.session_state.transcript = TRANSCRIPT

if st.session_state.transcript:

    TRANSCRIPT = st.session_state.transcript

    copy_button = st.button("Copy Transcript 📋")

    if copy_button:
        try:
            pyperclip.copy(TRANSCRIPT)
        except Exception:
            st.error("Unable to copy transcript! Please try again.")
        else:
            st.subheader("🤖")
            st.write("_Transcript copied to clipboard!_ 📋")

    if st.download_button("Download Transcript 📥", data=TRANSCRIPT, file_name="transcript.txt"):
        st.subheader("🤖")
        st.write("_Transcript downloaded!_ 📥")


    preview_toggle = st.toggle("Preview Transcript 📜", False)

    if preview_toggle:
        st.text_area("Transcript 📜", value=TRANSCRIPT, height=400)