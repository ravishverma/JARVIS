import speech_recognition as sr
import os

r = sr.Recognizer()
m = sr.Microphone()

os.system('sudo jack_control start')

try:
    print("A moment of silence, please...")
    with m as source:
        r.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(r.energy_threshold))
        os.system('espeak -v en "Jarvis is active. Say something!"')
        while True:
            print("Listening...")
            try:
                audio = r.listen(source)
                print("Recognizing...")

                try:
                    # recognize speech using Google Speech Recognition
                    value = r.recognize_google(audio)
                    print 'You said ', value

                    # Voice commands
                    cstr = value.upper()
                    response = '.'

                    if cstr == 'HELLO JARVIS':
                        os.system('echo "Hello " $USER')
                        os.system('espeak -v en "Hello",$USER')
                    elif cstr == 'JARVIS RECALIBRATE':
                        r.adjust_for_ambient_noise(source)
                        response = "Set minimum energy threshold to " + str(int(format(r.energy_threshold)))
                    elif cstr == 'JARVIS USERNAME':
                        os.system('echo $USER')
                    elif cstr[:19] == 'JARVIS SHUTDOWN IN ':
                        response = 'Shutting down in '+cstr[19:21]+' minute(s)'
                        os.system('gnome-terminal -x sh -c "shutdown -h %0d; bash" &' % (int(cstr[19:21])))
                    elif cstr[:18] == 'JARVIS RESTART IN ':
                        response = 'Restarting in '+cstr[18:+20]+' minute(s)'
                        os.system('gnome-terminal -x sh -c "shutdown -r %0d; bash" &' % (int(cstr[18:20])))
                    elif cstr[:15] == 'JARVIS WEBSITE ':
                        os.system('google-chrome %s &' % (cstr[15:]))
                    elif cstr[:18] == 'JARVIS WEB SEARCH ':
                        os.system('firefox -new-tab -search "%s" &' % (cstr[18:]))
                    elif cstr == 'JARVIS UPDATE SYSTEM':
                        os.system('gnome-terminal -x sh -c "sudo apt-get update && sudo apt-get upgrade && sudo apt-get dist-upgrade -y; bash" &')
                        response = 'System update started!'
                        print response
                        os.system('espeak -v en "%s"' % (response))
                    elif cstr[:14] == 'JARVIS LOCATE ':
                        os.system('gnome-terminal -x sh -c "locate %s; bash" &' % (cstr[14:]))
                        response = 'Check the search results!'
                    elif cstr == 'JARVIS LOCK SESSION':
                        os.system('gnome-screensaver-command --lock &')
                        response = 'System locked!'

                    print response
                    os.system('espeak -v en "%s"' % (response))

                except sr.UnknownValueError:
                    response = "Oops! Didn't catch that"
                    print response
                    #os.system('espeak -v en "%s"' % (response))
                except sr.RequestError as e:
                    response = "Uh oh! Couldn't request results from Google Speech Recognition service"
                    print response
                    #os.system('espeak -v en "%s"' % (response))
            except IOError:
                source = None
                source = m
                print 'IOError: Try again!'
            except ValueError:
                print 'ValueError: Try again!'
            except AttributeError:
                print 'AttributeError: Try again!'
except KeyboardInterrupt:
    pass
