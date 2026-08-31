import os
import wave
import tempfile
import threading

import pyaudio
import pyttsx3

from faster_whisper import WhisperModel


# ============================================================
# TARS VOICE SYSTEM
# ============================================================

class TARSVoice:

    def __init__(self):

        # ----------------------------------------------------
        # AUDIO SETTINGS
        # ----------------------------------------------------

        self.sample_rate = 16000
        self.channels = 1
        self.sample_format = pyaudio.paInt16

        self.chunk = 1024

        self.audio = pyaudio.PyAudio()

        # ----------------------------------------------------
        # WHISPER
        # ----------------------------------------------------

        print("Loading TARS voice model...")

        self.whisper = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8",
        )

        print("Whisper loaded.")

        # ----------------------------------------------------
        # TEXT TO SPEECH
        # ----------------------------------------------------

        self.tts = pyttsx3.init()

        self.tts.setProperty(
            "rate",
            175,
        )

        self.tts.setProperty(
            "volume",
            1.0,
        )

        # ----------------------------------------------------
        # STATE
        # ----------------------------------------------------

        self.is_speaking = False
        self.is_listening = False

    # ========================================================
    # MICROPHONE
    # ========================================================

    def record_audio(
        self,
        duration=5,
    ):

        print()
        print("🎙 Listening...")

        self.is_listening = True

        stream = self.audio.open(
            format=self.sample_format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk,
        )

        frames = []

        try:

            for _ in range(
                int(
                    self.sample_rate
                    / self.chunk
                    * duration
                )
            ):

                data = stream.read(
                    self.chunk,
                    exception_on_overflow=False,
                )

                frames.append(data)

        finally:

            stream.stop_stream()
            stream.close()

            self.is_listening = False

        # ----------------------------------------------------
        # TEMP WAV FILE
        # ----------------------------------------------------

        filename = tempfile.mktemp(
            suffix=".wav"
        )

        with wave.open(
            filename,
            "wb",
        ) as wf:

            wf.setnchannels(
                self.channels
            )

            wf.setsampwidth(
                self.audio.get_sample_size(
                    self.sample_format
                )
            )

            wf.setframerate(
                self.sample_rate
            )

            wf.writeframes(
                b"".join(frames)
            )

        return filename

    # ========================================================
    # SPEECH TO TEXT
    # ========================================================

    def listen(
        self,
        duration=5,
    ):

        filename = None

        try:

            filename = self.record_audio(
                duration
            )

            print("🧠 Transcribing...")

            segments, info = (
                self.whisper.transcribe(
                    filename,
                    beam_size=3,
                    language="en",
                    vad_filter=True,
                )
            )

            text = " ".join(
                segment.text
                for segment in segments
            ).strip()

            if text:

                print(
                    f"You said: {text}"
                )

            else:

                print(
                    "No speech detected."
                )

            return text

        except Exception as e:

            print(
                f"Voice recognition error: {e}"
            )

            return ""

        finally:

            if filename and os.path.exists(
                filename
            ):

                try:
                    os.remove(filename)

                except Exception:
                    pass

    # ========================================================
    # TEXT TO SPEECH
    # ========================================================

    def speak(
        self,
        text,
    ):

        if not text:
            return

        try:

            self.is_speaking = True

            print(
                f"TARS: {text}"
            )

            self.tts.say(
                text
            )

            self.tts.runAndWait()

        except Exception as e:

            print(
                f"TTS error: {e}"
            )

        finally:

            self.is_speaking = False

    # ========================================================
    # ASYNC SPEAK
    # ========================================================

    def speak_async(
        self,
        text,
    ):

        thread = threading.Thread(
            target=self.speak,
            args=(text,),
            daemon=True,
        )

        thread.start()

    # ========================================================
    # TEST
    # ========================================================

    def close(self):

        try:

            self.audio.terminate()

        except Exception:
            pass


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print()
    print(
        "=========================================="
    )
    print(
        "          TARS VOICE SYSTEM"
    )
    print(
        "=========================================="
    )
    print()

    voice = TARSVoice()

    try:

        text = voice.listen(
            duration=5
        )

        if text:

            voice.speak(
                f"You said {text}"
            )

        else:

            voice.speak(
                "I did not hear anything."
            )

    except KeyboardInterrupt:

        print(
            "\nVoice test stopped."
        )

    finally:

        voice.close()

        print()
        print(
            "Voice test complete."
        )
