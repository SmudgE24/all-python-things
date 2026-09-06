import pyaudio
import numpy as np


audio = pyaudio.PyAudio()

stream = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=44100,
    input=True,
    input_device_index=0,
    frames_per_buffer=1024
)


print("Listening to raw microphone audio...")
print("Speak loudly. Press Ctrl+C to stop.")


try:

    while True:

        data = stream.read(
            1024,
            exception_on_overflow=False
        )

        samples = np.frombuffer(
            data,
            dtype=np.int16
        )

        volume = np.abs(samples).mean()

        print(
            "Volume:",
            int(volume)
        )


except KeyboardInterrupt:

    print("\nStopped.")


stream.stop_stream()
stream.close()

audio.terminate()