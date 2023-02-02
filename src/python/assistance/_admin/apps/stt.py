# Copied from
# https://github.com/whitphx/streamlit-stt-app/blob/main/app_deepspeech.py


import whisper

import logging
import logging.handlers
import threading
import time
from collections import deque
from pathlib import Path
from typing import List

import av
import numpy as np
import pydub
import streamlit as st

from streamlit_webrtc import WebRtcMode, webrtc_streamer

HERE = Path(__file__).parent

logger = logging.getLogger(__name__)
from assistance._admin import categories

CATEGORY = categories.DEMO
TITLE = "Speech to Text"


async def main():
    model = whisper.load_model("base")

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

    status_indicator.write("Loading...")
    text_output = st.empty()
    sound_arrays = []

    while True:
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

            status_indicator.write("Running. Say something!")

            sample_rate = None
            for audio_frame in audio_frames:
                if sample_rate is None:
                    sample_rate = audio_frame.sample_rate

                assert audio_frame.sample_rate == sample_rate

                sound_arrays.append(audio_frame.to_ndarray())

            if len(sound_arrays) > 200:
                concatenated_sound_arrays = np.concatenate(sound_arrays, axis=None)
                audio_as_np_float32 = concatenated_sound_arrays.astype(np.float32)
                max_int16 = 2**15
                audio_normalised = audio_as_np_float32 / max_int16

                st.audio(audio_normalised, sample_rate=sample_rate * 2)

                text = model.transcribe(audio_normalised)
                text_output.markdown(f"**Text:** {text}")
                break
        else:
            status_indicator.write("Stopped.")
            break
