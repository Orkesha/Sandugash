import openai, time, json, requests
import speech_recognition as sr
from pygame import mixer

mixer.init()
inp = False


def saveurl(url):
 r = requests.get(url)
 file_extension = ".mp3"
 if file_extension not in url.split("/")[-1]:
        filename = f'{last_url_path}{file_extension}'
 else:
        filename = url.split("/")[-1]

 with open("response.mp3", 'wb') as f:
        # You will get the file in base64 as content
        f.write(r.content)

def plays():
 mixer.music.load("response.mp3")
 mixer.music.play()
 while mixer.music.get_busy():  # wait for music to finish playing
    time.sleep(1)

# Устанавливаем ваш API-ключ
openai.api_key = "ТОКЕН ОТ CHATGPT"   #platform.openai.com
def gpttext(text):
 completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[{"role": "system", "content": 
              "Please, answer shortly and in kazakh language"},
    {"role": "user", "content": text}
    ]
 )
 otv = completion.choices[0].message.content
 return otv


headers = {"Authorization": "Bearer ТОКЕН ОТ EDENAI"}  #edenai.co
def tts(text):
 url ="https://api.edenai.run/v2/audio/text_to_speech"
 payload={"providers": "microsoft", "language": "kk-KZ", "option":"FEMALE", "text": text}
 response = requests.post(url, json=payload, headers=headers)
 result = json.loads(response.text)
 r = requests.get(result['microsoft']['audio_resource_url'])
 url = result['microsoft']['audio_resource_url']
 return url



def record_volume():
    r = sr.Recognizer()
    with sr.Microphone(device_index = 1) as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    global inp
    try:
        query = r.recognize_google(audio, language = 'kk-KZ')
        text = query.lower()
        if inp == True:
          inp = False
          otv = gpttext(text)
          saveurl(tts(otv))
          plays()
        if text == 'сандуғаш' and inp == False:
          mixer.music.load("suc.mp3")
          mixer.music.play()
          while mixer.music.get_busy():  # wait for music to finish playing
              time.sleep(1)
          inp = True
        
    except:
        pass


print("Басталды")
while True:
    record_volume()
