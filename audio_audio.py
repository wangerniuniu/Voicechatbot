# -*- coding: utf-8 -*-
from pyaudio import PyAudio,paInt16
import pyaudio
import wave
import numpy as np
def play():
    chunk = 128
    f=wave.open(r"cache.wav",'rb')
    p=PyAudio()
    # 打开数据流
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    # 读取数据
    data = f.readframes(chunk)
    # 播放
    while data != b"":
        stream.write(data)
        data = f.readframes(chunk)
        # 停止数据流
    print("播放结束")
    stream.stop_stream()
    stream.close()
    # 关闭 PyAudio
    p.terminate()
def Monitor():
    recording=0
    start=1
    end=2
    CHUNK = 128
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "cache.wav"
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("开始缓存录音")
    frames = []
    status=recording
    while (True):
        print ('begin ')
        for i in range(0, 10):
            data = stream.read(CHUNK)
            frames.append(data)
        audio_data = np.fromstring(data, dtype=np.short)
        large_sample_count = np.sum( audio_data > 800 )
        temp = np.max(audio_data)
        if temp > 10000 and status==recording :
            print ("开始录音")
            status=start
            frames.clear()
        if  temp < 1000 and status==start:
            print("结束")
            break
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
if __name__ == '__main__':
    while True:
        Monitor()
        play()