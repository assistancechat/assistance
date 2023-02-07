# Copied from
# https://github.com/whitphx/streamlit-stt-app/blob/main/app_deepspeech.py


import logging
import logging.handlers
import os
import tempfile
import threading
import time
from collections import deque
from pathlib import Path
from typing import List

import av
import numpy as np
import pydub
import streamlit as st
import whisper
from streamlit_webrtc import WebRtcMode, webrtc_streamer

HERE = Path(__file__).parent

logger = logging.getLogger(__name__)
from assistance._admin import categories

CATEGORY = categories.DEMO
TITLE = "Speech to Text"


async def main():
    temp_dir = tempfile.mkdtemp()
    save_path = os.path.join(temp_dir, "temp.wav")

    model = None

    if "audio" not in st.session_state:
        st.session_state.audio = pydub.AudioSegment.empty()

    frames_deque_lock = threading.Lock()
    frames_deque: deque = deque([])

    async def queued_audio_frames_callback(
        frames: List[av.AudioFrame],
    ) -> av.AudioFrame:
        with frames_deque_lock:
            frames_deque.extend(frames)

        # Return empty frames to be silent.
        new_frames = []
        for frame in frames:
            input_array = frame.to_ndarray()
            new_frame = av.AudioFrame.from_ndarray(
                np.zeros(input_array.shape, dtype=input_array.dtype),
                layout=frame.layout.name,
            )
            new_frame.sample_rate = frame.sample_rate
            new_frames.append(new_frame)

        return new_frames

    webrtc_ctx = webrtc_streamer(
        key="speech-to-text-w-video",
        mode=WebRtcMode.SENDRECV,
        queued_audio_frames_callback=queued_audio_frames_callback,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": True, "audio": True},
    )

    status_indicator = st.empty()

    if not webrtc_ctx.state.playing:
        return

    status_indicator.write("Model loading... (however you can start talking)")
    text_output = st.empty()
    i = 0

    while True:
        if model is None:
            model = whisper.load_model("large")

        if webrtc_ctx.state.playing:
            audio_frames = []
            with frames_deque_lock:
                while len(frames_deque) > 0:
                    frame = frames_deque.popleft()
                    audio_frames.append(frame)

            if len(audio_frames) == 0:
                time.sleep(0.1)
                status_indicator.write("No frame arrived.")
                continue

            i += 1

            status_indicator.write(
                "Model is waiting a bit to collect more audio. Say something!"
            )

            for audio_frame in audio_frames:
                sound = pydub.AudioSegment(
                    data=audio_frame.to_ndarray().tobytes(),
                    sample_width=audio_frame.format.bytes,
                    frame_rate=audio_frame.sample_rate,
                    channels=len(audio_frame.layout.channels),
                )
                st.session_state.audio += sound

            if i % 50 == 1 and len(st.session_state.audio) > 0:
                status_indicator.write("Model is processing a batch of audio now.")

                st.session_state.audio = st.session_state.audio.set_channels(
                    1
                ).set_frame_rate(16000)
                st.session_state.audio.export(save_path, format="wav")

                result = model.transcribe(save_path)
                predicted_text = result["text"]

                text_output.markdown(f"**Text:** {predicted_text}")
        else:
            status_indicator.write("Stopped.")
            break
