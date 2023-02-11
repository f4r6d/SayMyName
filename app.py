import pyttsx3, sys, cowsay
import pyaudio
import simpleaudio as sa
import speech_recognition as sr

CHUNK = 882
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
frames = []

r = sr.Recognizer()

def main():
    cowsay.kitty("Please say your name, then I will start listenning to voices around if they say your name, then I will say your message. To exit the program, say exit")

    say_hi("Please say your name, then I will start listenning to voices around if they say your name, then I will say your message. To exit the program, say exit")

    name = get_name("Please say your name?")
    record_audio("What should i say if they call you?")

    while True:
        try:
            if listen_to(name):
                play_audio()
        except KeyboardInterrupt:
            sys.exit(0)


def record_audio(msg):
    print(msg)
    input('press Enter to start recording for 5 seconds')
    global frames 
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("* done recording\n")

    stream.stop_stream()
    stream.close()
    p.terminate()


def play_audio():
    global frames
    play_obj = sa.play_buffer(b''.join(frames), CHANNELS, 2, RATE)
    play_obj.wait_done()


def get_name(q):
    print(q)
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            print("Listenning!")
            audio = r.listen(source)    
            try:
                name = r.recognize_google(audio, language="fa-IR")
                if name.lower() in ["exit", "اگزیت"]:
                    sys.exit(0)
                if name.isalpha():
                    print(f"\nYour name is {name}.\n")
                    return name
                else:
                    print("\nPlease just say your name; One word!")
                    continue
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                pass



def listen_to(name):
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            print("I'm  llistenning if someone calls your name!")
            audio = r.listen(source)    
            try:
                x=r.recognize_google(audio, language="fa-IR")
                print()
                print(x)
                if name.lower() in x.lower():
                    print("They're calling you!")
                    return True
                elif x in ["exit", "اگزیت"]:
                    sys.exit(0)
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                pass


def say_hi(msg):
    engine = pyttsx3.init()
    engine.say(msg)
    engine.runAndWait()


if __name__ == "__main__":
    main()