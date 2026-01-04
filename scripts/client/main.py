import asyncio
import json
import base64
import sys
import queue
import sounddevice as sd
import numpy as np
import websockets
from pynput import keyboard

# Configuration
WS_URL = "ws://localhost:8000/ws/voice"
SAMPLE_RATE = 16000
CHANNELS = 1
BLOCK_SIZE = 4096

# State
audio_queue = asyncio.Queue()
is_recording = False
session_id = "client-session-001"
user_id = "user-001"

def audio_callback(indata, frames, time, status):
    """Callback for sounddevice input stream."""
    if is_recording:
        audio_queue.put_nowait(indata.copy())

async def audio_producer_task(ws):
    """Reads audio queue and sends chunks."""
    seq = 0
    while True:
        data = await audio_queue.get()
        if data is None: break
        
        # Convert float32 numpy to int16 bytes for generic compatibility if needed
        # Or keep raw bytes depending on server expectation.
        # OpenAI Whisper often likes Wav/PCM. 16-bit PCM is standard.
        pcm_data = (data * 32767).astype(np.int16).tobytes()
        b64_data = base64.b64encode(pcm_data).decode('utf-8')
        
        msg = {
            "type": "audio",
            "session_id": session_id,
            "user_id": user_id,
            "chunk_b64": b64_data,
            "sample_rate": SAMPLE_RATE,
            "channels": CHANNELS,
            "seq": seq
        }
        await ws.send(json.dumps(msg))
        seq += 1

async def receive_task(ws):
    """Handles incoming messages from server."""
    async for message in ws:
        data = json.loads(message)
        type_ = data.get("type")
        
        if type_ == "transcript_final":
            print(f"\n[SERVER] Transcript: {data.get('text')}")
        elif type_ == "assistant_response":
            print(f"\n[SERVER] Assistant: {data.get('text')}")
        elif type_ == "tts_chunk":
            # Play audio logic
            # Simpler: just save to file for MVP or log receipt
            print(f"[SERVER] Received audio chunk {len(data['chunk_b64'])} bytes")
            # In a real app, decode b64 -> numpy -> sd.play()
        elif type_ == "error":
            print(f"[SERVER] Error: {data.get('message')}")

async def input_monitor(ws):
    """Monitor keyboard for Press-To-Talk logic."""
    global is_recording
    print("Hold SPACE to talk. Press Q to quit.")
    
    loop = asyncio.get_running_loop()
    
    # We need a non-blocking way to detect keys. 
    # pynput is threaded. 
    
    def on_press(key):
        global is_recording
        try:
            if key == keyboard.Key.space and not is_recording:
                is_recording = True
                print(" [RECORDING] ", end="", flush=True)
                # Send Wake
                asyncio.run_coroutine_threadsafe(
                    ws.send(json.dumps({
                        "type": "wake",
                        "wake_word": "keypress",
                        "timestamp": 0,
                        "session_id": session_id,
                        "user_id": user_id
                    })), loop
                )
        except AttributeError:
            pass

    def on_release(key):
        global is_recording
        try:
            if key == keyboard.Key.space and is_recording:
                is_recording = False
                print(" [STOP] ", flush=True)
                # Send EOU
                asyncio.run_coroutine_threadsafe(
                    ws.send(json.dumps({
                        "type": "eou",
                        "timestamp": 0,
                        "session_id": session_id,
                        "user_id": user_id
                    })), loop
                )
        except AttributeError:
            pass
            
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    
    while True:
        await asyncio.sleep(1)


async def main():
    print(f"Connecting to {WS_URL}...")
    try:
        async with websockets.connect(WS_URL) as ws:
            print("Connected.")
            
            # Start mic
            stream = sd.InputStream(
                samplerate=SAMPLE_RATE, 
                channels=CHANNELS, 
                callback=audio_callback,
                blocksize=BLOCK_SIZE
            )
            stream.start()
            
            await asyncio.gather(
                receive_task(ws),
                audio_producer_task(ws),
                input_monitor(ws)
            )
            
            stream.stop()
            stream.close()
            
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
