from baidu_api import BaiduRest
from pyaudio import PyAudio,paInt16
from chatbot import tuling_chatbot
import pyaudio
import numpy as np
import wave
""" 你的 APPID AK SK """
APP_ID = '10362955'
API_KEY = ''
SECRET_KEY = ''
framerate=16000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=1
def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()
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
def my_record():
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    my_buf=[]
    count=0
    while count<TIME*20:#控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        count+=1
        print('.')
    save_wave_file('01.wav',my_buf)
    stream.close()
chunk=1024
def play():
    f=wave.open(r"02.wav",'rb')
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
if __name__ == '__main__':
    while True:
        #my_record()
        Monitor()
        print('Over!')
        bdr = BaiduRest("test_python", API_KEY, SECRET_KEY)
        a=bdr.getText('cache.wav')
        print(type(a))
        response=tuling_chatbot(a['result'])
        print(response)
        bdr.getVoice(response,"out.mp3")
        bdr.ConvertToWav("out.mp3", "02.wav")
        play()