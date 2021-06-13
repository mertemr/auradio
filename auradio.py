#!/usr/bin/python3
from os import system, name
from time import sleep
import weakref
import pafy
import vlc
import os

os.environ["VLC_VERBOSE"] = str("-1")  # thanks to rickie95

def auradio():
    print('''                              
                                _ _        
       __ _ _   _ _ __ __ _  __| (_) ___   
      / _` | | | | '__/ _` |/ _` | |/ _ \  
     | (_| | |_| | | | (_| | (_| | | (_) | 
      \__,_|\__,_|_|  \__,_|\__,_|_|\___/  
                                           
    ''')                                   
    sleep(0.4)


class radio:
    instances = []

    def __init__(self, number, radioname, url):
        self.__class__.instances.append(weakref.proxy(self))
        self.number = number
        self.radioname = radioname
        self.url = url

    def __str__(self):
        return self.number + ' ~ ' + self.radioname


CRFlorida =   radio('1' , 'Classic Rock Florida' ,'https://cutt.ly/AvFrd9g')
Megaton =     radio('2' , 'Megaton Cafe Radio'   ,'https://cutt.ly/SvFro84')
Palnostalji = radio('3' , 'Pal Nostalji'         ,'https://cutt.ly/TvFrupx')
Bakaradio =   radio('4' , 'Bakaradio'            ,'https://cutt.ly/fvFreAS')
Metrofm =     radio('5' , 'Metro FM'             ,'https://cutt.ly/wvFe7Pm')
FAkustik =    radio('6' , 'Fenomen Akustik'      ,'https://cutt.ly/YvFe9Qn')
Fenomen =     radio('7' , 'Fenomen'              ,'https://cutt.ly/3vFeBXO')
Jakustik =    radio('8' , 'Joytürk Akustik'      ,'https://cutt.ly/BvD7r2Q')

def radiochan():
    while True:
        system('cls')
        for instance in radio.instances:
            print(instance)

        print('\nYou can return to the previous menu by typing "back".')
        print('You can close the program by typing "exit".')
        radioin = input('\n$ ')
        if radioin == 'back':
            system('cls')
            return
        elif radioin == 'exit':
            system('cls')
            bye()

        try:
            url, radioname = urlsearch(radioin)
            if url:
                break
        except:
            pass
    radioplayer(url, radioname)

def urlsearch(radioin):
    for instance in radio.instances:
        if instance.number == radioin:
            return instance.url, instance.radioname

def getinfo(player):
    media = player.get_media()
    info = str(media.get_meta(12))
    info = info.split("-")
    artist = info[0]
    track = info[1]
    return artist, track

def radiomenu():
    print('1 ~ Show current playing track')
    print('2 ~ Go back to the list')
    print('3 ~ Volume up')
    print('4 ~ Volume down')
    print('0 ~ Disconnect\n')

def radioplayer(url, radioname):
    system('cls')

    vlc_instance = vlc.Instance('-q')
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(url)
    player.set_media(media)

    ses = 30
    player.audio_set_volume(ses)
    player.play()

    radiomenu()
    while player.play:

        cat = input('$ ')
        if (cat.lower() == '1'):

            system('cls')
            radiomenu()
            try:
                print('Radio ~ ' + radioname)
                artist, track = getinfo(player)
                print('Song ~'+track+' by '+artist+'\n')
            except:
                pass
        elif (cat.lower() == '2'):
            player.stop()
            break
        elif (ses < 100 and cat.lower() == '3'):

            ses = ses + 5
            player.audio_set_volume(ses)
            system('cls')
            radiomenu()
            print('V ~ Current volume is:', ses)

        elif (ses > 0 and cat.lower() == "4"):

            ses = ses - 5
            player.audio_set_volume(ses)
            system('cls')
            radiomenu()
            print('V ~ Current volume is:', ses)
        elif (cat.lower() == '0'):
            system('cls')
            bye()
        else:
            system('cls')
            radiomenu()
    radiochan()

def youtubechan():
    youtubeurl = ''
    while True:
        system('cls')
        print('You can return to the previous menu by typing "back".')
        print('You can close the program by typing "exit".')
        vid = input('\nEnter url $ ')

        if vid == "back":
            system('cls')
            return

        elif vid == 'exit':
            bye()

        try:
            audio = pafy.new(vid)
            best = audio.getbestaudio()
            youtubeurl = best.url
            if youtubeurl:
                break
        except:
            pass
        
    youtubeplayer(youtubeurl,audio)

def youtubemenu():
    print('1 ~ Show current playing track')
    print('2 ~ Take another url')
    print('3 ~ Volume up')
    print('4 ~ Volume down')
    print('0 ~ Disconnect\n')

def youtubeplayer(url,audio):
    system('cls')

    vlc_instance = vlc.Instance('-q')
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(url)
    player.set_media(media)
    
    ses = 30
    player.audio_set_volume(ses)
    player.play()
    youtubemenu()
    
    #while player.is_playing() == 1:
    #print(player.is_playing())
    
    while player.play:

        
        
        cat = input()

        if (cat.lower() == '1'):

            system('cls')
            youtubemenu()
            
            try:
                print('Title ~ ' + audio.title)
                print('Rating ~ ' + str(audio.rating))
                print('Author ~ ' + audio.author)
                print('Duration ~ ' + audio.duration + "\n")   
            except:
                pass
        elif (cat.lower() == '2'):
            player.stop()
            break
        elif (ses < 100 and cat.lower() == '3'):

            ses = ses + 5
            player.audio_set_volume(ses)
            system('cls')
            youtubemenu()
            print('V ~ Current volume is:', ses)

        elif (ses > 0 and cat.lower() == '4'):
            ses = ses - 5
            player.audio_set_volume(ses)
            system('cls')
            youtubemenu()
            print('V ~ Current volume is:', ses)
        elif (cat.lower() == "0"):
            system('cls')
            bye()
    youtubechan()

def bye():
    print("\nI don't like goodbyes ~\n")
    exit()

def chanplayer(path):

    vlc_instance = vlc.Instance('-q')
    chanplayer = vlc_instance.media_player_new()
    media = vlc_instance.media_new(path)
    chanplayer.set_media(media)

    chanplayer.audio_set_volume(75)
    chanplayer.play()
    return

def chan():
    system('cls')
    while True:

        auradio()
        print("1 ~ Radio")
        print("2 ~ Youtube")

        inpm = input("\n$ ")
        
        if(inpm.lower() == "1"):
            radiochan()
        
        elif(inpm.lower() == "2"):
            youtubechan()
        
        elif (inpm.lower() == "radioactive"):
            system('cls')
            chanplayer("files/radioahhtive.mp3")

        elif (inpm.lower() == "yamete"):
            system('cls')
            chanplayer("files/yametekudasai.mp3")

        elif (inpm.lower() == "taylor"):
            taylor()      

        else:
            system('cls')
            chanplayer("files/wtf.mp3")

def taylor():
    system('cls')
    print('''
        My friends: You okay?
        Me: Yeah, I’m fine.

        My headphones:

        Taylor Swift - All Too Well
        0:35 ━❍──────── -5:32
        ↻     ⊲  Ⅱ  ⊳     ↺
        VOLUME: ▲ 200%
        
        ''')
    sleep(2)
    system('cls')

if __name__ == "__main__":
    system('cls')
    chan()
