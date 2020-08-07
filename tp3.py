# Neha Choudhari: PyGarageBand
# 15-112 S20

# PyGarageband has two main classes: FirstScreen and Second. These two control
# the different screens by having two separate TkInter canvases. In each
# class, there are buttons, labels, and other objects that are on the canvas 
# that the user can interact with. Each class also has specific functions that 
# represent features of that particular screen.


import pygame
from threading import Thread
import wave
import math, copy, random
from os import path
import wave
from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import normalize
from pydub.playback import play
from pydub.generators import Sine
import decimal
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import time
from time import time

pygame.mixer.init()

# almostEqual and roundHalfUp were taken from 112 course website: 
# https://www.cs.cmu.edu/~112/notes/notes-variables-and-functions.html

def almostEqual(d1, d2, epsilon=10**-7): 
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

def roundHalfUp(d): 
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

fileNames = []
originalTuneCount = 0

# code for the class SampleApp taken from:
# https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter

class SampleApp(Frame):
    def __init__(self):
        super().__init__()
        self._frame = None
        self.switch_frame(FirstScreen)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class FirstScreen(Frame):
    def __init__(self, master):
        super().__init__()
        self.pack(fill = Y, side = LEFT)
        self.canvas = Canvas(self, bg = "black", height = 750, 
                width = 1000)
        self.title = self.canvas.create_text(25, 50, 
            text = "PyGarageBand", font = ("Courier", 50), anchor = "w", fill = "white")
        self.step1title = self.canvas.create_text(25, 100, 
            text = "Step 1: Gathering Audios", font = ("Courier", 20), anchor = "w", 
            fill = "white")
        # helpButton is from http://pixelartmaker.com/art/de557e157e6bb26
        self.buttonImage = PhotoImage(file = "helpButton.png")
        self.buttonImage2 = self.buttonImage.subsample(4,4)
        self.helpButton = Button(self, image = self.buttonImage2,
            command = self.helpScreen)
        self.canvas.create_window(920, 100, window = self.helpButton)
        self.helpDoneButton = Button(self, text = "Exit Help Screen", font = ("Courier", 10),
            command = self.helpDone)
        # image from: http://www.pngall.com/xylophone-png
        self.step1 = PhotoImage(file = "instrument2.png")
        self.step2 = self.step1.subsample(2,2)
        self.guitarPic = self.canvas.create_image(450,100, 
            image = self.step2)
        self.moveToEditor = Button(self, text = "Move to Editor", font = ("Courier", 15),
            command = lambda: master.switch_frame(Second))
        self.canvas.create_window(920, 50, window = self.moveToEditor)
        self.addFileButton = Button(self, 
        text = "Import a .wav file!", command = self.beginMakingMusic, font = ("Courier", 15))
        self.doneButton = Button(self, text = "Done!", 
            command = self.getBack, font = ("Courier", 15))
        self.combineButton = Button(self, text = "Combine Audios!", 
            command = self.combineAudiosEntry, font = ("Courier", 15))
        self.makeTuneButton = Button(self, text = "Make a Tune!", 
            command = self.drawKeyboard, font = ("Courier", 15))
        self.startRecordingButton = Button(self, text = "Start Recording", 
            command = self.startRecording, font = ("Courier, 10"))
        self.startRecordingButtonItem = None
        self.fileEntry = Entry(self, bd = 5)
        self.fileEntryLabel = Label(self, text = "Enter File Name:",
            font = ("Courier", 15))
        self.canvas.create_window(100, 200, window = self.addFileButton)
        self.canvas.create_window(270, 200, window = self.combineButton)
        self.canvas.create_window(410, 200, window = self.makeTuneButton)
        self.combineInputLabel = Label(self, text = "Which 2 audios (#)?",
            font = ("Courier", 10))
        self.combineEntry1 = Entry(self, bd = 5)
        self.combineEntry2 = Entry(self, bd = 5) 
        self.canvas.pack(side = LEFT)
        self.item = None
        self.item2 = None
        self.item3 = None
        self.item4 = None
        self.item5 = None
        self.item6 = None
        self.item7 = None
        self.songButton = None
        self.cButton = Button(self, text = "C", height = 10, width = 3, 
            compound = "c", command = lambda: self.addNote("C"))
        self.cButton2 = Button(self, text = "C", height = 10, width = 3, 
            compound = "c", command = lambda: self.addNote("C+"))
        self.cButtonItem = None
        self.cButtonItem2 = None
        self.dButton = Button(self, text = "D", height = 10, width = 3, 
            compound = "c", command = lambda: self.addNote("D"))
        self.dButtonItem = None
        self.eButton = Button(self, text = "E", height = 10, width = 3, 
            compound = "c", command = lambda: self.addNote("E"))
        self.eButtonItem = None
        self.fButton = Button(self, text = "F", height = 10, width = 3, 
            compound = "c", command = lambda: self.addNote("F"))
        self.fButtonItem = None
        self.gButton = Button(self, text = "G", height = 10, width = 3, 
            compound = "c", command = lambda: self.addNote("G"))
        self.gButtonItem = None
        self.aButton = Button(self, text = "A", height = 10, width = 3, 
            compound = "c", command = lambda: self.addNote("A"))
        self.aButtonItem = None
        self.bButton = Button(self, text = "B", height = 10, width = 3, 
            compound = "c", command = lambda: self.addNote("B"))
        self.bButtonItem = None
        self.cSharpButton = Button(self, text = "C#", height = 4, width = 2, 
            compound = "c", bg = "red", command = lambda: self.addNote("C1"), 
            highlightbackground = '#3E4149')
        self.cSharpButtonItem = None
        self.dSharpButton = Button(self, text = "D#", height = 4, width = 2, 
            compound = "c", command = lambda: self.addNote("D1"), 
            highlightbackground = '#3E4149')
        self.dSharpButtonItem = None
        self.fSharpButton = Button(self, text = "F#", height = 4, width = 2, 
            compound = "c", command = lambda: self.addNote("F1"),
            highlightbackground = '#3E4149')
        self.fSharpButtonItem = None
        self.gSharpButton = Button(self, text = "G#", height = 4, width = 2, 
            compound = "c", command = lambda: self.addNote("G1"),
            highlightbackground = '#3E4149')
        self.gSharpButtonItem = None
        self.aSharpButton = Button(self, text = "A#", height = 4, width = 2, 
            compound = "c", command = lambda: self.addNote("A1"),
            highlightbackground = '#3E4149')
        self.aSharpButtonItem = None
        self.currentOctaveNumber = 5
        self.currentOctave = Label(self, 
            text = f'CURRENT OCTAVE = {self.currentOctaveNumber}',
            font = ("Courier", 10)) 
        self.currentOctaveItem = None
        self.raiseOctave = Button(self, text = "Raise Octave", 
            command = self.raiseOctave)
        self.raiseOctaveItem = None
        self.lowerOctave = Button(self, text = "Lower Octave", 
            command = self.lowerOctave)
        self.lowerOctaveItem = None
        self.makingMusicDone = Button(self, text = "Stop Recording", 
            command = self.doneMakingMusic)
        self.exitKeyboardItem = None
        self.exitKeyboard = Button(self, text = "Exit MakingMusic", 
            command = self.exitKeyboard, highlightbackground = '#e12016')
        self.currentDurationNumber = 250
        self.currentDuration = Label(self, 
            text = f'CURRENT DURATION ={self.currentDurationNumber} ms',
            font = ("Courier", 10))
        self.currentDurationItem = None
        self.raiseDurationItem = None 
        self.lowerDurationItem = None
        self.raiseDurationButton = Button(self, 
            text = "Raise Duration by 100ms", command = self.raiseDuration)
        self.lowerDuration = Button(self, text = "Lower Duration by 100 ms", 
            command = self.lowerDuration)
        self.makingMusicDoneItem = None
        self.madeNotes = []
        self.currentlyRecording = False
        self.refreshButton = Button(self, text = "Refresh", font = ("Courier", 15),
            command = self.refreshMusic)
        self.addAutomatedTuneButton = Button(self, text = "Built-In Tunes!", 
            font = ("Courier", 15), command = self.addAutomatedTunes)
        self.canvas.create_window(550, 200, window = self.addAutomatedTuneButton)
        self.addPianoButton = Button(self, text = "Add Piano", font = ("Courier", 10),
            command = self.addPiano)
        self.addPianoItem = None
        self.addDrumsButton = Button(self, text = "Add Drums", font = ("Courier", 10),
            command = self.addDrums)
        self.addDrumsItem = None
        self.addGuitarButton = Button(self, text = "Add Guitar", font = ("Courier", 10),
            command = self.addGuitar)
        self.automatedTuneDoneButton = Button(self, text = "Done", font = ("Courier", 10),
            command = self.automatedTuneDone)
        self.automatedTuneDoneItem = None
        self.helpImageStep1 = PhotoImage(file = "helpImage1.png")
        self.helpImageStep2 = self.helpImageStep1.subsample(3,3)
        self.helpImage = Button(self, image = self.helpImageStep2,
            command = self.helpDone)
        self.stopAllMusicButton = Button(self, text = "Stop All Music",
            font = ("Courier", 15), command = self.stopAllMusic)
        self.canvas.create_window(100,150, window = self.stopAllMusicButton)
        self.helpImageItem = None
        self.drawSongs()

    def beginMakingMusic(self):
        self.item = (self.canvas.create_window(130, 250, 
            window = self.fileEntryLabel))
        self.item2 = self.canvas.create_window(320, 250, 
            window = self.fileEntry)
        self.item3 = self.canvas.create_window(450, 250, 
            window = self.doneButton)

    def stopAllMusic(self):
        pygame.mixer.music.stop()


    def getBack(self):
        if self.item != None and self.item != '':
            fileName = self.fileEntry.get()
            global fileNames
            if fileName not in fileNames:
                fileNames.append(fileName)
            self.canvas.delete(self.item)
            self.canvas.delete(self.item2)
            self.canvas.delete(self.item3)
            self.fileEntry.delete(0, 'end')
            self.item = None
        if self.item5 and self.item6 and self.item5 != '' and self.item6 != '':
            firstSong = self.combineEntry1.get()
            secSong = self.combineEntry2.get()
            self.canvas.delete(self.item4)
            self.canvas.delete(self.item5)
            self.canvas.delete(self.item6)
            self.canvas.delete(self.item7)
            self.combineEntry1.delete(0, 'end')
            self.combineEntry2.delete(0, 'end')
            self.combineAudios(firstSong, secSong)
        self.drawSongs()

    def drawSongs(self):
        colors = ["red", "blue", "green", "yellow", "brown"]
        global fileNames
        for numSong in range(len(fileNames)):
            x = (numSong * 100)
            y = (numSong * 23) + 300
            song = AudioSegment.from_file(file = fileNames[numSong])
            self.canvas.create_rectangle(x+100, y, x, y + 150, 
                fill = colors[(numSong % 5)])
            self.songButton = Button(self, text = "Press to play!", 
                command = lambda numSong=numSong: self.playSong(numSong),
                font = ("Courier", 10))
            self.canvas.create_window(x+50, y+50, window = self.songButton)
            self.canvas.create_text(x+25, y+25, text = numSong +1,
                font = ("Courier", 15))
            self.canvas.create_text(x+50, y+75, text = fileNames[numSong],
                anchor = "c", font = ("Courier", 10))

    def playSong(self, numSong):
        global fileNames
        song = AudioSegment.from_file(file = fileNames[numSong])
        #print("firstWidth:", song.sample_width)
        #print("firstChannels", song.channels)
        if fileNames[numSong][:4] != "Orig":
            song = song.set_sample_width(1)
        #print("width:", song.sample_width)
        #print("channels", song.channels)

        pygame.mixer.music.load(fileNames[numSong])
        pygame.mixer.music.play()
    
    # matchAmplitude function taken from stack overflow: 
    # https://stackoverflow.com/questions/
    # 42492246/how-to-normalize-the-volume-of-an-audio-file-in-python-
    # any-packages-currently-a

    def matchAmplitude(self, sound, target_dBFS): 
        change_in_dBFS = target_dBFS - sound.dBFS
        return sound.apply_gain(change_in_dBFS)
    
    def combineAudiosEntry(self):
        self.item4 = (self.canvas.create_window(550, 250, 
            window = self.combineInputLabel))
        self.item5 = (self.canvas.create_window(550, 300, 
            window = self.combineEntry1))
        self.item6 = (self.canvas.create_window(550, 400, 
            window = self.combineEntry2))
        self.item7 = (self.canvas.create_window(600, 350, 
            window = self.doneButton))

    def addAutomatedTunes(self):
        self.addPianoItem = self.canvas.create_window(500, 230,
            window = self.addPianoButton)
        self.addGuitarItem = self.canvas.create_window(580, 230,
            window = self.addGuitarButton)
        self.addDrumsItem = self.canvas.create_window(530, 255, 
            window = self.addDrumsButton)
        self.automatedTuneDoneItem = self.canvas.create_window(530, 280,
            window = self.automatedTuneDoneButton)
        return 42


# pianoChords3 audio: 
# https://mega.nz/folder/NGZGmJgQ#9fslXqj5T0Eov8WVeBBirQ/folder/YORVQKrR

    def addPiano(self):
        global fileNames
        if 'pianoChords3.wav' not in fileNames:
            fileNames.append("pianoChords3.wav")
            self.drawSongs()

# guitarChords3 audio:
# https://drive.google.com/drive/folders/1D0hKdlVkl6kIIBuuNtZ1GnmWaWhEo9k7

    def addGuitar(self):
        global fileNames
        if 'guitarChords3.wav' not in fileNames:
            fileNames.append("guitarChords3.wav")
            self.drawSongs()

# drumbeatFinal audio: 
# http://www.orangefreesounds.com/category/loops/drum-loops/

    def addDrums(self):
        global fileNames
        if "drumbeatFinal.wav" not in fileNames:
            fileNames.append("drumbeatFinal.wav")
            self.drawSongs()

    def helpScreen(self):
        self.helpImageItem = self.canvas.create_window(500,450,
            window = self.helpImage)

    def helpDone(self):
        self.canvas.delete(self.helpImageItem)
        
    def automatedTuneDone(self):
        self.canvas.delete(self.addPianoItem)
        self.canvas.delete(self.addGuitarItem)
        self.canvas.delete(self.addDrumsItem)
        self.canvas.delete(self.automatedTuneDoneItem)

    def combineAudios(self, song1, song2):
        global fileNames
        if int(song1) <= len(fileNames) and int(song2) <= len(fileNames):
            name1 = fileNames[int(song1)-1]
            name2 = fileNames[int(song2)-1]
            song1 = AudioSegment.from_file(name1)
            song2 = AudioSegment.from_file(name2)
            if song1.sample_width != song2.sample_width:
                minWidth = min(song1.sample_width, song2.sample_width)
                song1 = song1.set_sample_width(minWidth)
                song2 = song2.set_sample_width(minWidth)
            song1 = self.matchAmplitude(song1, -20)
            song2 = self.matchAmplitude(song2, -20)
            newSong = song1.overlay(song2)
            newSongName = str(name1[:-4]) + str(name2[:-4]) + "combined.wav"
            newSong.export(out_f=str(newSongName), format = 'wav')
            if newSongName not in fileNames:
                fileNames.append(newSongName)
    
    def refreshMusic(self):
        self.drawSongs()

    def raiseOctave(self):
        self.currentOctaveNumber +=1
        self.currentOctave.configure(text = f'CURRENT OCTAVE = {self.currentOctaveNumber}')

    def lowerOctave(self):
        self.currentOctaveNumber -=1
        self.currentOctave.configure(text = f'CURRENT OCTAVE = {self.currentOctaveNumber}')

    def addNote(self, note):
        tempNote = note
        sine = self.freqFromNote(note, self.currentOctaveNumber, self.currentDurationNumber)
        play(sine)
        if self.currentlyRecording:
            self.madeNotes.append([tempNote, time(), self.currentDurationNumber, self.currentOctaveNumber])

    def drawKeyboard(self):
        self.currentOctaveItem = self.canvas.create_window(730, 175, 
            window = self.currentOctave)
        self.raiseOctaveItem = self.canvas.create_window(680, 200, 
            window = self.raiseOctave)
        self.lowerOctaveItem = self.canvas.create_window(780, 200, 
            window = self.lowerOctave)
        self.makingMusicDoneItem = self.canvas.create_window(910, 300, 
            window = self.makingMusicDone)
        self.currentDurationItem = self.canvas.create_window(730, 425,
            window = self.currentDuration)
        self.startRecordingButtonItem = self.canvas.create_window(910, 250, 
            window = self.startRecordingButton)
        self.madeNotes = []
        self.cButtonItem = self.canvas.create_window(630, 300, 
            window = self.cButton)
        self.dButtonItem = self.canvas.create_window(660, 300, 
            window = self.dButton)
        self.eButtonItem = self.canvas.create_window(690, 300, 
            window = self.eButton)
        self.fButtonItem = self.canvas.create_window(720, 300, 
            window = self.fButton)
        self.gButtonItem = self.canvas.create_window(750, 300, 
            window = self.gButton)
        self.aButtonItem = self.canvas.create_window(780, 300, 
            window = self.aButton)
        self.bButtonItem = self.canvas.create_window(810, 300, 
            window = self.bButton)
        self.cSharpButtonItem = self.canvas.create_window(645, 252, 
            window = self.cSharpButton)
        self.dSharpButtonItem = self.canvas.create_window(675, 252, 
            window = self.dSharpButton)   
        self.fSharpButtonItem = self.canvas.create_window(735, 252, 
            window = self.fSharpButton)    
        self.gSharpButtonItem = self.canvas.create_window(765, 252, 
            window = self.gSharpButton)
        self.aSharpButtonItem = self.canvas.create_window(795, 252, 
            window = self.aSharpButton)
        self.cButtonitem2 = self.canvas.create_window(840, 300, 
            window = self.cButton2)
        self.raiseDurationItem = self.canvas.create_window(655, 400, 
            window = self.raiseDurationButton)
        self.lowerDurationItem = self.canvas.create_window(840, 400, 
            window = self.lowerDuration)
        self.exitKeyboarditem = self.canvas.create_window(900, 180, 
            window = self.exitKeyboard)


    def exitKeyboard(self):
        self.canvas.delete(self.currentOctaveItem)
        self.canvas.delete(self.raiseOctaveItem)
        self.canvas.delete(self.lowerOctaveItem)
        self.canvas.delete(self.makingMusicDoneItem)
        self.canvas.delete(self.currentDurationItem)
        self.canvas.delete(self.startRecordingButtonItem)
        self.canvas.delete(self.cButtonItem)
        self.canvas.delete(self.dButtonItem)
        self.canvas.delete(self.eButtonItem)
        self.canvas.delete(self.fButtonItem)
        self.canvas.delete(self.gButtonItem)
        self.canvas.delete(self.aButtonItem)
        self.canvas.delete(self.bButtonItem)
        self.canvas.delete(self.cSharpButtonItem)
        self.canvas.delete(self.dSharpButtonItem)
        self.canvas.delete(self.fSharpButtonItem)
        self.canvas.delete(self.gSharpButtonItem)
        self.canvas.delete(self.aSharpButtonItem)
        self.canvas.delete(self.cButtonitem2) 
        self.canvas.delete(self.raiseDurationItem)
        self.canvas.delete(self.lowerDurationItem) 
        self.canvas.delete(self.exitKeyboarditem)

    def startRecording(self):
        self.currentlyRecording = True
        self.startRecordingButton.configure(text = "Currently Recording")

        self.madeNotes = [time()]

    def raiseDuration(self):
        self.currentDurationNumber += 100
        self.currentDuration.configure(text = f'CURRENT DURATION ={self.currentDurationNumber} ms')

    def lowerDuration(self):
        self.currentDurationNumber -= 100
        self.currentDuration.configure(text = f'CURRENT DURATION ={self.currentDurationNumber} ms')

    def doneMakingMusic(self):
        if self.currentlyRecording:
            self.currentlyRecording = False
            self.startRecordingButton.configure(text = "Start Recording")
            note = self.madeNotes[1][0]
            pauseb4first = (self.madeNotes[1][1] - self.madeNotes[0]) * 1000
            # in ms
            result = AudioSegment.silent(duration= pauseb4first)
            duration = self.madeNotes[1][2] # ms
            octave = self.madeNotes[1][3]
            currentTime = (pauseb4first + duration) / 1000 + self.madeNotes[0] # seconds
            note1 = self.freqFromNote(note, octave, duration)
            result+= note1
            # add first note
            for i in range(2, len(self.madeNotes)):
                note = self.madeNotes[i][0]
                startTime = self.madeNotes[i][1] # seconds
                duration = self.madeNotes[i][2]
                octave = self.madeNotes[i][3]
                if startTime > currentTime:
                    pauseBefore = startTime - currentTime # seconds
                    result += AudioSegment.silent(duration = pauseBefore * 1000)
                    currentTime = currentTime + pauseBefore +(duration/1000)
                else:
                    currentTime = currentTime + (duration / 1000)
                result+= self.freqFromNote(note, octave, duration)
            
            global originalTuneCount
            originalTuneCount +=1

            result.export(out_f=f'OriginalTune{originalTuneCount}.wav', format = 'wav')

            global fileNames
            fileNames.append(f'OriginalTune{originalTuneCount}.wav')
            self.drawSongs()

    def freqFromNote(self, note, octave, duration):
        tempNote = note
        scale = []
        if octave == 5:
            for i in range(3, 16):
                freq = 440 * ((1.059463094359) ** i)
                freq = roundHalfUp(freq)
                scale.append(freq)
        else:
            diff = octave - 5
            for i in range(3, 16):
                temp = i + (diff * 12)
                freq = 440 * ((1.059463094359) ** temp)
                freq = roundHalfUp(freq)
                scale.append(freq)
        newScale = scale[9:12:2] + scale[0:5:2] + [scale[5]] + [scale[7]]
        if len(note) == 1:
            i = ord(note) - ord("A")
            note = Sine(newScale[i])
        elif note[1] == "1":
            i = ord(note[0]) - ord("A")
            index = scale.index(newScale[i])
            noteFreq = scale[index + 1]
            note = Sine(noteFreq)
        else:
            note = Sine(scale[12])
        sine = note.to_audio_segment(duration=duration).apply_gain(-3)
        sine = sine.fade_in(50).fade_out(100)
        return sine



class Second(Frame):
    def __init__(self, master):
        super().__init__()
        self.pack(fill = Y, side = LEFT)
        self.canvas = Canvas(self, bg = "black", height = 800, width = 1250)
        self.canvas.pack(side = LEFT)
        global fileNames
        self.fileNames = fileNames
        self.lengths = dict()
        # lilbutton is from: https://toppng.com/red-button-icon-PNG-free-PNG-Images_85275
        self.resultStep1 = PhotoImage(file = "lilbutton.png")
        self.resultStep2 = self.resultStep1.subsample(2,2)
        self.resultButton = Button(self, image = self.resultStep2, 
            command = self.exportInput, text = "DONE")
        # helpButton is from http://pixelartmaker.com/art/de557e157e6bb26
        self.buttonImage = PhotoImage(file = "helpButton.png")
        self.buttonImage2 = self.buttonImage.subsample(4,4)
        self.helpButton = Button(self, image = self.buttonImage2,
            command = self.helpScreen)
        self.canvas.create_window(1150, 100, window = self.helpButton)
        self.helpDoneButton = Button(self, text = "Exit Help Screen", font = ("Courier", 10),
            command = self.helpDone)
        self.canvas.create_window(950, 100, window = self.resultButton)
        self.highestLength = 0
        self.chunkWidth = 0
        self.title = self.canvas.create_text(25, 50, 
            text = "PyGarageBand", font = ("Courier", 50), anchor = "w", fill = "white")
        self.step2title = self.canvas.create_text(25, 100, 
            text = "Step 2: Compiling Audios", font = ("Courier", 20), anchor = "w", 
            fill = "white")
        self.button = Button(self, text = "Go Back (Reset)", font = ("Courier", 15),
            command = lambda: master.switch_frame(FirstScreen))
        self.canvas.create_window(1150, 50, window = self.button)
        # playFinal from https://www.iconsdb.com/blue-icons/play-5-icon.html
        self.playImg = PhotoImage(file = "playFinal.png")
        self.playAllButton = Button(self, image = self.playImg, 
            text = "Play", font = ("Courier", 10), command = self.playAll)
        self.canvas.create_window(480, 70, window = self.playAllButton)
        self.currentlyPlaying = False
        heightOfSongs = len(self.fileNames) * 60
        # image from https://www.iconsdb.com/blue-icons/pause-icon.html
        self.pauseImg = PhotoImage(file = "pauseFinal.png")
        self.pauseButton = Button(self, image = self.pauseImg,
            text = "Pause", font = ("Courier", 10), command = self.pause)
        self.canvas.create_window(520, 70, window = self.pauseButton)
        self.timeLabel = Label(self, text = "0:00", font = ("Courier", 20))
        self.timeLabelObject = self.canvas.create_window(500, 100, 
            window = self.timeLabel)
        self.playingSongs = copy.copy(self.fileNames)
        self.count = 0
        self.startingTime = 0
        self.currentlyPlaying = False
        self.pauseLabel = Label(self, text = "0:00", font = ("Courier", 20))
        self.pauseLabelItem = None
        self.muteButton = Button(self, text = "Mute/Unmute", command = self.muteInput,
            font = ("Courier", 10))
        self.canvas.create_window(850, 100, window = self.muteButton)
        self.muteEntry = Entry(self, width = 8)
        self.muteEntryItem = None
        self.muteLabelItem = None
        self.muteLabel = Label(self, text = "Muted:", font = ("Courier", 10))
        self.canvas.create_window(820, 70, window = self.muteLabel) 
        self.muteDoneButton = Button(self, text = "Done", font = ("Courier", 10),
            command = self.muteSong)
        self.muteDoneItem = None
        self.splitButton = Button(self, text = "Split", 
            command = self.splitAudiosEntry, font = ("Courier", 10))
        self.canvas.create_window(583, 100, window = self.splitButton)
        self.loopButton = Button(self, text = "Loop", 
            command = self.loopAudiosEntry, font = ("Courier", 10))
        self.canvas.create_window(620, 100, window = self.loopButton)
        self.split1EntryItem = None
        self.split2EntryItem = None
        self.split3EntryItem = None
        self.split1Entry = Entry(self, bd = 2, width = 3)
        self.split2Entry = Entry(self, bd = 2, width = 8)
        self.split3Entry = Entry(self, bd =2, width = 15)
        self.splitDoneButton = Button(self, text = "Done", 
            command = self.splitDone)
        self.splitDoneButtonItem = None
        self.split1Label = Label(self, text = "Audio #", font = ("Courier", 10))
        self.split2Label = Label(self, text = "TimeStamp Split (secs)", 
            font = ("Courier", 10))
        self.split3Label = Label(self, text = "New File Name",
            font = ("Courier", 10))
        self.split1LabelItem = None
        self.split2LabelItem = None
        self.split3LabelItem = None
        self.deleteButton = Button(self, command = self.deleteAudio, 
            text = "Delete", font = ("Courier", 10))
        self.delete1Label = Label(self, text = "Audio #", font = ("Courier", 10))
        self.delete1LabelItem = None
        self.delete1Entry = Entry(self, bd = 2, width = 3)
        self.delete1EntryItem = None
        self.deleteDoneButton = Button(self, command = self.deleteDone,
            text = "Done", font = ("Courier", 10))
        self.deleteDoneButtonItem = None
        self.canvas.create_window(660, 100, window = self.deleteButton)
        self.delayButton = Button(self, text = "Delay", command = self.delayAudioInput,
            font = ("Courier", 10))
        self.canvas.create_window(750, 100, window = self.delayButton)
        self.delay1EntryItem = None
        self.delay1Entry = Entry(self, bd = 2, width = 10)
        self.delay2EntryItem = None
        self.delay2Label = Label(self, text = "Delay (secs)", font = ("Courier", 10))
        self.delay2Entry = Entry(self, bd = 2, width = 5)
        self.delayDoneButton = Button(self, text = "Done", command = self.delayDone,
            font = ("Courier", 10))
        self.delayDoneButtonItem = None
        self.loop1Entry = Entry(self, bd = 2, width = 3)
        self.loop2Label = Label(self, text = "How many loops?", font =("Courier", 10))
        self.loop2Entry = Entry(self, bd = 2, width = 3)
        self.loopDoneButton = Button(self, text = "Done", font = ("Courier", 15),
            command = self.loopDone)
        self.loop1EntryItem = None
        self.loop2EntryItem = None
        self.loopDoneButtonItem = None
        self.loop1LabelItem = None
        self.loop2LabelItem = None
        self.loop3Entry = Entry(self, bd = 2, width = 10)
        self.loop3EntryItem = None
        self.loop3Labelitem = None
        self.chunkLabel = Label(self, text = "Box width: 0 secs", font = ("Courier", 12))
        self.canvas.create_window(660,70, window = self.chunkLabel)
        self.completedAudio1Entry = Entry(self, bd = 2, width = 10)
        self.completedAudio1EntryItem = None
        self.completedAudio1LabelItem = None
        self.completedAudioDoneButton = Button(self, 
            text = "Thanks!", font = ("Courier", 15),
            command = self.exportResult, bg = 'green')
        self.completedAudioDoneButtonItem = None
        self.changeVolumeButton = Button(self, text = "Volume", 
            command = self.changeVolumeInput, font = ("Courier", 10))
        self.canvas.create_window(706, 100, window = self.changeVolumeButton)
        self.volumeChangeLabel = Label(self, text = "Change (db)", 
            font = ("Courier", 10))
        self.volumeChangeEntry1 = Entry(self, bd = 2, width = 10)
        self.volumeChangeEntry2 = Entry(self, bd = 2, width = 5)
        self.volumeChangeDoneButton = Button(self, command = self.volumeChangeDone,
            text = "Done", font = ("Courier", 10))
        self.volumeChangeEntry1Item  = None
        self.volumeChangeEntry2Item = None
        self.volumeChangeDoneButtomItem = None
        self.volumeChangeLabel1Item = None
        self.volumeChangeLabel2Item = None
        self.helpImageStep1 = PhotoImage(file = "helpImage2.png")
        self.helpImageStep2 = self.helpImageStep1.subsample(2,2)
        self.helpImage = Button(self, image = self.helpImageStep2, 
            command = self.helpDone)
        self.helpImageItem = None
        self.redBlockItem = None
        self.redBlock = None
        self.refreshButton = Button(self, text = "Refresh", font = ("Courier", 15),
            command = self.refresh)
        self.canvas.create_window(950, 50, window = self.refreshButton)
        self.organizeBlocks()

    def organizeBlocks(self):
        print("self.fileNames:", self.fileNames)
        self.lengths = dict()
        background = self.canvas.create_rectangle(0, 130, 1250, 750, fill = "black")
        self.canvas.tag_raise(background)
        highestLength = 0
        for numSong in range(len(self.fileNames)):
            song = AudioSegment.from_file(file = fileNames[numSong])
            self.lengths[fileNames[numSong]] = [numSong, len(song)/1000]
            if len(song) > highestLength:
                highestLength = len(song)
        self.highestLength = roundHalfUp(highestLength / 1000)
        self.chunkWidth = highestLength / 10 # chunk in ms 
        print("chunkWidth:", self.chunkWidth)
        startingTimes =[]
        for num in range(11):
            startingTimes.append(num * self.chunkWidth / 1000)
        self.startingTimes = startingTimes
         # added from __init__
        colors = ["peach puff", "rosy brown", "powder blue", "aquamarine2", 
            "khaki1", "lavender", "pink", "LightBlue1", "light coral", "cornsilk2"]
        print("self.lengths:", self.lengths)
        for song in self.lengths:
            songName = song
            numSong = self.lengths[song][0]
            songLength = self.lengths[song][1] / 1000 # in seconds 
            startingHeight = 150 + numSong * 60
            startingWidth = 125
            self.canvas.create_text(startingWidth, startingHeight + 5, text = songName,
                anchor = "e", font = ("Courier", 10), fill = "white")
            self.canvas.create_text(startingWidth, startingHeight + 20, text = numSong +1,
                anchor = "e", font = ("Courier", 15), fill = "white") 
            for i in range(10):
                song = AudioSegment.from_file(file = songName)
                if len(song)/1000 <= self.startingTimes[i]:
                    color = "dim gray"
                else:
                    color  = colors[numSong]
                temp = startingWidth + 100 * i
                self.canvas.create_rectangle(temp, startingHeight, temp + 100, 
                    startingHeight + 60, fill = color)
        self.chunkLabel.config(text = f'Box width: ~ {roundHalfUp(self.chunkWidth/1000)} secs')
        self.currentX = 125
        self.redBlock = self.canvas.create_rectangle(125, 145, 127, 
            155 + len(fileNames) * 60, fill = "red")
        print("highestLength is:", self.highestLength)
        if len(fileNames) != 0:
            self.change = float(str(100 / self.highestLength)[:4])

    def refresh(self):
        self.organizeBlocks()

    # matchAmplitude function taken from stack overflow: 
    # https://stackoverflow.com/questions/
    # 42492246/how-to-normalize-the-volume-of-an-audio-file-in-python-
    # any-packages-currently-a

    def matchAmplitude(self, sound, target_dBFS): 
        change_in_dBFS = target_dBFS - sound.dBFS
        return sound.apply_gain(change_in_dBFS)

    def playAll(self):
        self.canvas.delete(self.pauseLabelItem)
        self.canvas.coords(self.redBlock, 125, 145, 127, 
            155 + len(fileNames) * 60)
        self.currentX = 125
        self.count = 0
        self.startingTime = time()
        self.currentlyPlaying = True
        temp = dict()
        for fileName in self.lengths:
            if fileName in self.playingSongs:
                temp[self.lengths[fileName][1]] = fileName
        times = sorted(temp)
        times.reverse()
        print("times:", times)
        if times != []:
            final = AudioSegment.from_file(temp[times[0]])
            for key in times[1:]:
                fileName = temp[key]
                song = AudioSegment.from_file(fileName)
                if final.sample_width != song.sample_width:
                    minWidth = min(final.sample_width, song.sample_width)
                    final = final.set_sample_width(minWidth)
                    song = song.set_sample_width(minWidth)
                step = final.overlay(song)
                final = step
            # export final as playback
            final.export(out_f='playback.wav', format = 'wav')
            pygame.mixer.music.load('playback.wav')
            pygame.mixer.music.play()
            self.updateLabel()

    def updateLabel(self):
        if self.count <= self.highestLength:
            msg = str(time() - self.startingTime)[:4]
            self.timeLabel.configure(text = msg)
            self.timeLabel.after(100, self.updateLabel)
            self.count+= 0.1
            if self.currentlyPlaying:
                self.canvas.coords(self.redBlock, self.currentX + self.change,
                145, self.currentX + self.change + 2, 155 + len(fileNames) * 60)
                self.currentX = self.currentX + self.change 



    def pause(self):
        if self.currentlyPlaying:
            msg = str(time() - self.startingTime)[:4]
            self.pauseLabel.configure(text = msg)
            self.pauseLabelItem = self.canvas.create_window(500, 100,
                window = self.pauseLabel)
            pygame.mixer.music.stop()
        self.currentlyPlaying = False

    def muteInput(self):
        self.muteLabelItem = self.canvas.create_window(800, 140, 
            window = self.split1Label)
        self.muteEntryItem = self.canvas.create_window(870, 140,
            window = self.muteEntry)
        self.muteDoneItem = self.canvas.create_window(850, 170,
            window = self.muteDoneButton )
        return 42

    def muteSong(self):
        numSongs = self.muteEntry.get()
        for numSong in numSongs.split(','):
            numSong = int(numSong)
            if self.fileNames[numSong-1] in self.playingSongs:
                song = self.fileNames[numSong-1]
                self.playingSongs.remove(song)
            else:
                song = self.fileNames[numSong-1]
                self.playingSongs.append(song)
        msg = ''
        print("selfPlayingSongs:", self.playingSongs)
        for i in range(len(fileNames)):
            if fileNames[i] not in self.playingSongs:
                msg += str(i+1) + ' '
        msg = 'Muted: ' + msg
        self.muteLabel.configure(text = msg)
        self.canvas.delete(self.muteLabelItem)
        self.canvas.delete(self.muteEntryItem)
        self.canvas.delete(self.muteDoneItem)

    def splitAudiosEntry(self):
        self.split1EntryItem = (self.canvas.create_window(650, 150, 
            window = self.split1Entry))
        self.split2EntryItem = (self.canvas.create_window(670, 180, 
            window = self.split2Entry))
        self.split3EntryItem = (self.canvas.create_window(670, 210, 
            window = self.split3Entry))
        self.splitDoneButtonItem = (self.canvas.create_window(650, 240 , 
            window = self.splitDoneButton))
        self.split1LabelItem = (self.canvas.create_window(600, 150, 
            window = self.split1Label))
        self.split2LabelItem = (self.canvas.create_window(545, 180, 
            window = self.split2Label))
        self.split3LabelItem = (self.canvas.create_window(545, 210,
            window = self.split3Label))

    def splitDone(self):
        audioNum = self.split1Entry.get()
        timeStamp = self.split2Entry.get()
        newFileName = self.split3Entry.get()
        self.canvas.delete(self.split1EntryItem)
        self.canvas.delete(self.split2EntryItem)
        self.canvas.delete(self.split3EntryItem)
        self.canvas.delete(self.split1LabelItem)
        self.canvas.delete(self.split2LabelItem)
        self.canvas.delete(self.split3LabelItem)
        self.canvas.delete(self.splitDoneButtonItem)
        if int(audioNum) <= len(fileNames):
            songName = self.fileNames[int(audioNum)-1]
            song = AudioSegment.from_file(file = songName)
            timeStamp = str(timeStamp)
            charIndex = timeStamp.find('-')
            if charIndex == -1:
                return 
            firstNum, secNum = timeStamp[:charIndex], timeStamp[charIndex+1:]
            firstNum = float(firstNum.strip())
            if secNum == "end":
                slicedChunk = song[int(firstNum*1000):]
            else:
                secNum = float(secNum.strip())
                slicedChunk = song[int(firstNum*1000):int(secNum*1000)]
            if firstNum <= len(song):
                slicedChunk.export(out_f=f'{newFileName}.wav', format = 'wav')
                self.fileNames.append(str(newFileName) + '.wav')
                self.playingSongs.append(str(newFileName) + '.wav')
        self.organizeBlocks()
            
    def exportResult(self):
        resultName = self.completedAudio1Entry.get()
        resultName = str(resultName).strip()
        temp = dict()
        for fileName in self.lengths:
            temp[self.lengths[fileName][1]] = fileName
        times = sorted(temp)
        times.reverse()
        final = AudioSegment.from_file(temp[times[0]])
        for key in times[1:]:
            fileName = temp[key]
            song = AudioSegment.from_file(fileName)
            if final.sample_width != song.sample_width:
                minWidth = min(final.sample_width, song.sample_width)
                final = final.set_sample_width(minWidth)
                song = song.set_sample_width(minWidth)
            final = self.matchAmplitude(final, -20)
            song = self.matchAmplitude(song, -20)
            step = final.overlay(song)
            final = step

        final.export(out_f=f'{resultName}.wav', format = 'wav')
        self.canvas.create_text(600,500, text = "You're Done!", font = ("Courier", 100),
            fill = "red")

    def exportInput(self):
        self.completedAudioDoneButtonItem = self.canvas.create_window(1000, 200,
            window = self.completedAudioDoneButton)
        self.completedAudio1EntryItem = self.canvas.create_window(1080, 170, 
            window = self.completedAudio1Entry)
        self.completedAudio1LabelItem = self.canvas.create_window(980, 170,
            window = self.split3Label)

    def loopAudiosEntry(self):
        self.loop1LabelItem = self.canvas.create_window(630, 150,
            window = self.delete1Label)
        self.loop1EntryItem = self.canvas.create_window(680, 150,
            window = self.loop1Entry)
        self.loop2LabelItem = self.canvas.create_window(605, 180, 
            window = self.loop2Label)
        self.loop2EntryItem = self.canvas.create_window(680, 180,
            window = self.loop2Entry)
        self.loop3EntryItem = self.canvas.create_window(712, 210, 
            window = self.loop3Entry)
        self.loop3LabelItem = self.canvas.create_window(613, 210,
            window = self.split3Label)
        self.loopDoneButtonItem = self.canvas.create_window(660, 250,
            window = self.loopDoneButton)


    def loopDone(self):
        audioNum = self.loop1Entry.get()
        numLoops = self.loop2Entry.get()
        newFileName = self.loop3Entry.get()
        print("audioNum:", audioNum, "numLoops:", numLoops)
        self.canvas.delete(self.loop1EntryItem)
        self.canvas.delete(self.loop2EntryItem)
        self.canvas.delete(self.loop3EntryItem)
        self.canvas.delete(self.loop1LabelItem)
        self.canvas.delete(self.loop2LabelItem)
        self.canvas.delete(self.loop3LabelItem)
        self.canvas.delete(self.loopDoneButtonItem)
        index = int(audioNum) - 1
        if index < len(fileNames):
            numLoops = int(numLoops)
            final = AudioSegment.silent(duration=0)
            for i in range(numLoops):
                song = AudioSegment.from_file(file = self.fileNames[index])
                final+= song
            final.export(out_f=f'{newFileName}.wav', format = 'wav')
            self.fileNames.append(str(newFileName) + '.wav')
            self.playingSongs.append(str(newFileName) + '.wav')
        self.organizeBlocks()


        return 42
    
    def deleteAudio(self):
        self.delete1EntryItem = self.canvas.create_window(750, 150, 
            window = self.delete1Entry)
        self.deleteDoneButtonItem = self.canvas.create_window(720, 180, 
            window = self.deleteDoneButton)
        self.delete1LabelItem = self.canvas.create_window(700, 150, 
            window = self.delete1Label)

    def deleteDone(self):
        audioNum = self.delete1Entry.get()
        i = int(audioNum) - 1
        if int(audioNum) <= len(fileNames):
            if self.fileNames[i] in self.playingSongs:
                self.playingSongs.remove(self.fileNames[i])
            self.fileNames.pop(i)
        #print("after deletion,", self.fileNames)
        self.canvas.delete(self.delete1EntryItem)
        self.canvas.delete(self.deleteDoneButtonItem)
        self.canvas.delete(self.delete1LabelItem)
        self.organizeBlocks()

    def delayAudioInput(self):
        self.delay1LabelItem = self.canvas.create_window(
            750, 150, window = self.split1Label)
        self.delay1EntryItem = self.canvas.create_window(835, 150,
            window = self.delay1Entry)
        self.delay2LabelItem = self.canvas.create_window(750, 180,
            window = self.delay2Label)
        self.delay2EntryItem = self.canvas.create_window(825, 180,
            window = self.delay2Entry)
        self.delayDoneButtonItem = self.canvas.create_window(780, 215,
            window = self.delayDoneButton)
        return 42 

    def delayDone(self):
        audioNum = self.delay1Entry.get()
        delaySecs = self.delay2Entry.get()
        delayedAudios = []
        for num in audioNum.split(","):
            delayedAudios.append(int(num) - 1)
        print(delayedAudios)
        for audioNum in delayedAudios:
            result = AudioSegment.silent(duration= float(delaySecs) * 1000)
            song = AudioSegment.from_file(file = fileNames[audioNum])
            result+= song
            newName = str(fileNames[audioNum])[:-4] + f'd{delaySecs}sec'
            result.export(out_f=f'{newName}.wav', format = 'wav')
            self.fileNames.append(str(newName) + '.wav')
    
        self.playingSongs.append(str(newName) + '.wav')
        self.canvas.delete(self.delay1LabelItem)
        self.canvas.delete(self.delay1EntryItem)
        self.canvas.delete(self.delay2LabelItem)
        self.canvas.delete(self.delay2EntryItem)
        self.canvas.delete(self.delayDoneButtonItem)
        self.organizeBlocks()

    def changeVolumeInput(self):
        self.volumeChangeLabel1Item = self.canvas.create_window(650, 150, 
            window = self.split1Label)
        self.volumeChangeEntry1Item = self.canvas.create_window(730, 150,
            window = self.volumeChangeEntry1)
        self.volumeChangeLabel2Item = self.canvas.create_window(650, 180,
            window = self.volumeChangeLabel)
        self.volumeChangeEntry2Item = self.canvas.create_window(720, 180,
            window = self.volumeChangeEntry2)
        self.volumeChangeDoneButtomItem = self.canvas.create_window(680, 215,
            window = self.volumeChangeDoneButton)

    def volumeChangeDone(self):
        audioNum = self.volumeChangeEntry1.get()
        volChange = self.volumeChangeEntry2.get()
        changedAudios = []
        for num in audioNum.split(","):
            changedAudios.append(int(num) - 1)
        for audioNum in changedAudios:
            print("audioNum:", audioNum, "fileNames:", fileNames)
            if int(audioNum) <= len(fileNames):
                song = AudioSegment.from_file(file = fileNames[audioNum])
                currentVol = song.dBFS
                newVol = currentVol + int(volChange)
                result = self.matchAmplitude(song, newVol)
                newName = str(fileNames[audioNum])[:-4] + f'{volChange}dbFS'
                result.export(out_f=f'{newName}.wav', format = 'wav')
                self.fileNames.append(str(newName) + '.wav')
                self.playingSongs.append(str(newName) + '.wav')

        self.canvas.delete(self.volumeChangeLabel1Item)
        self.canvas.delete(self.volumeChangeEntry1Item)
        self.canvas.delete(self.volumeChangeLabel2Item)
        self.canvas.delete(self.volumeChangeEntry2Item)
        self.canvas.delete(self.volumeChangeDoneButtomItem)
        self.organizeBlocks()
    
    def helpScreen(self):
        self.helpImageItem = self.canvas.create_window(600,450,
             window = self.helpImage)

    def helpDone(self):
        self.canvas.delete(self.helpImageItem)

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()


# some extra citations for audio used in the program: 

# hannah montana music (hannahmontana.wav): 
# https://www.youtube.com/watch?v=3ZdiQa2NcF0
