import json
import random
from tkinter import *
import requests


class HangManGame():
    def __init__(self, guessCounter):
        self.mysteryWord = ""
        self.lettersInWord = ""
        self.guessCounter = guessCounter
        self.lettersUsed = ""

    def GenerateWord(self):
        '''with open("wordbook.txt", "r") as file: 
            fileData = file.read()
            wordList = json.loads(fileData)'''
        #//https://raw.githubusercontent.com/redbo/scrabble/master/dictionary.txt
        #//https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt
        rawWords = requests.get('https://raw.githubusercontent.com/redbo/scrabble/master/dictionary.txt')
        fomratedWords = str(rawWords.content)
        wordList = fomratedWords.split("\\n")
        self.mysteryWord = wordList[random.randint(0, len(wordList) -1)]
        while len(self.mysteryWord) > 7:
            self.mysteryWord = wordList[random.randint(0, len(wordList) -1)]
        self.lettersInWord = ["-" for _ in range(len(self.mysteryWord))]

    
    def PlayerGuess(self, playerGuess):
        if self.guessCounter > 0 and "-" in self.lettersInWord and len(playerGuess) == 1:
            if str(playerGuess).lower() in self.mysteryWord and str(playerGuess).lower() not in self.lettersUsed: #Check if the player has guessed a correct letter and congratulate them.
                length = len(self.mysteryWord)
                count = 0
                while(count < length):
                    if self.mysteryWord[count] == playerGuess:
                        #print(self.lettersInWord[count])
                        self.lettersInWord[count] = playerGuess
                    count += 1 
                self.lettersUsed += playerGuess
            elif str(playerGuess).lower() in self.lettersUsed:
                pass
            else:
                self.lettersUsed += playerGuess #Update the list of used letters
                self.guessCounter -= 1 #Update Guess counter
        elif len(playerGuess) > 1:
            print("How the hell did you manage that fam?")
        #Win or loose

    def DisplayStats(self):
        global GuessDisplay
        GuessDisplay["text"] = newHangManGame.guessCounter
        global LettersUsed
        LettersUsed["text"] = newHangManGame.lettersUsed
        if "-" not in self.lettersInWord and self.guessCounter > 0: #If the player has correctly guessed the word
            global Display
            Display["font"] = ("arial", 13, "bold")
            Display["text"] = "You guessed the word congrats!"
        elif self.guessCounter == 0: #If the player has run out of guesses
            Display["font"] = ("arial", 11, "bold")
            Display["text"] = "You ran out of guesses \n the word was " + self.mysteryWord.upper()
        else:
            Display["text"]=self.lettersInWord

newHangManGame = HangManGame(10)
newHangManGame.GenerateWord()

window = Tk()
window.title("Hang-man Game")
window.config(bg="paleturquoise1")

#The pain beggings
#Display
Display = Label(text=newHangManGame.lettersInWord, fg="black", bg="paleturquoise2", font=('arial', 20, "bold"))
Display.grid(row=0, column=0, columnspan=10)

Stats = Label(text="STATISTICS", fg="black", bg="paleturquoise2", font=('calibri', 14, "bold"))
Stats.grid(row=0, column=11)

GuessCount = Label(text="GUESSES LEFT", fg="black", bg="paleturquoise2", font=('calibri', 14, "bold"))
GuessCount.grid(row=1, column=11)

GuessDisplay = Label(text=newHangManGame.guessCounter, fg="black", bg="paleturquoise2", font=('arial', 14, "bold"))
GuessDisplay.grid(row=2, column=11)

LettersUsed = Label(text=newHangManGame.lettersUsed, fg="black", bg="paleturquoise2", font=('arial', 12, "bold"))
LettersUsed.grid(row=3, column=11)

def Clicked(key):
    keyEntered = str(key).lower()
    newHangManGame.PlayerGuess(keyEntered)
    newHangManGame.DisplayStats()

def EnterNew():
    global NewWordInput
    NewWordInput = Entry(window, borderwidth=3, width=26, font=('calibre',14,'bold'), bg="paleturquoise2")
    NewWordInput.grid(row=0, column=0, columnspan=14)
    global EnterBut
    EnterBut = Button(window, width=3, height=6, relief="raised", text="E\nN\nT\nE\nR", bg="paleturquoise2", fg="black", 
                font=('calibri', 8, "bold"), activebackground="slateblue1", command=Confirm)
    EnterBut.grid(row=2, column=0, rowspan=2)
    
    GuessCount.grid_forget()
    GuessDisplay.grid_forget()
    Stats.grid_forget()
    LettersUsed.grid_forget()
    Display.grid_forget()
    NewWordBut.grid_forget()

def Reset():
    newHangManGame.lettersUsed = ""
    print(newHangManGame.lettersUsed)
    newHangManGame.guessCounter = 10
    newHangManGame.GenerateWord()
    Display["font"] = ('arial', 20, "bold")
    Display["text"] = newHangManGame.lettersInWord
    LettersUsed["text"] = newHangManGame.lettersUsed
    GuessDisplay["text"] = newHangManGame.guessCounter
    GuessCount.grid(row=1, column=11)
    LettersUsed.grid(row=3, column=11)
    Stats.grid(row=0, column=11)
    GuessDisplay.grid(row=2, column=11)
    Display.grid(row=0, column=0, columnspan=10)
    NewWordBut.grid(row=2, column=0, rowspan=2)
    try:
        NewWordInput.grid_forget()
    except NameError:
        pass
    try:
        EnterBut.grid_forget()
    except NameError:
        pass

    
def Confirm():
    newWord = NewWordInput.get()
    with open("wordbook.txt", "r") as file: 
            fileData = file.read()
            wordList = json.loads(fileData)
    if newWord == "":
        pass
    elif newWord not in wordList:
        wordin = {"word": newWord}
        wordList.append(wordin)

    with open("wordbook.txt", "w") as file:
            json.dump(wordList, file)
    NewWordInput.delete(0,END)

#Buttons
A = Button(window, width=3, height=2, relief="raised", text="A", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="A": Clicked(Key))
A.grid(row=1, column=0)
B = Button(window, width=3, height=2, relief="raised", text="B", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="B": Clicked(Key))
B.grid(row=1, column=1)
C = Button(window, width=3, height=2, relief="raised", text="C", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="C": Clicked(Key))
C.grid(row=1, column=2)
D = Button(window, width=3, height=2, relief="raised", text="D", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="D": Clicked(Key))
D.grid(row=1, column=3)
E = Button(window, width=3, height=2, relief="raised", text="E", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="E": Clicked(Key))
E.grid(row=1, column=4)
F = Button(window, width=3, height=2, relief="raised", text="F", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="F": Clicked(Key))
F.grid(row=1, column=5)
G = Button(window, width=3, height=2, relief="raised", text="G", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="G": Clicked(Key))
G.grid(row=1, column=6)
H = Button(window, width=3, height=2, relief="raised", text="H", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="H": Clicked(Key))
H.grid(row=1, column=7)
I = Button(window, width=3, height=2, relief="raised", text="I", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="I": Clicked(Key))
I.grid(row=1, column=8)
J = Button(window, width=3, height=2, relief="raised", text="J", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="J": Clicked(Key))
J.grid(row=1, column=9)
K = Button(window, width=3, height=2, relief="raised", text="K", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="K": Clicked(Key))
K.grid(row=2, column=1)
L = Button(window, width=3, height=2, relief="raised", text="L", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="L": Clicked(Key))
L.grid(row=2, column=2)
M = Button(window, width=3, height=2, relief="raised", text="M", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="M": Clicked(Key))
M.grid(row=2, column=3)
N = Button(window, width=3, height=2, relief="raised", text="N", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="N": Clicked(Key))
N.grid(row=2, column=4)
O = Button(window, width=3, height=2, relief="raised", text="O", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="O": Clicked(Key))
O.grid(row=2, column=5)
P = Button(window, width=3, height=2, relief="raised", text="P", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="P": Clicked(Key))
P.grid(row=2, column=6)
Q = Button(window, width=3, height=2, relief="raised", text="Q", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="Q": Clicked(Key))
Q.grid(row=2, column=7)
R = Button(window, width=3, height=2, relief="raised", text="R", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="R": Clicked(Key))
R.grid(row=2, column=8)
S = Button(window, width=3, height=2, relief="raised", text="S", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="S": Clicked(Key))
S.grid(row=3, column=1)
T = Button(window, width=3, height=2, relief="raised", text="T", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="T": Clicked(Key))
T.grid(row=3, column=2)
U = Button(window, width=3, height=2, relief="raised", text="U", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="U": Clicked(Key))
U.grid(row=3, column=3)
V = Button(window, width=3, height=2, relief="raised", text="V", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="V": Clicked(Key))
V.grid(row=3, column=4)
W = Button(window, width=3, height=2, relief="raised", text="W", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="W": Clicked(Key))
W.grid(row=3, column=5)
X = Button(window, width=3, height=2, relief="raised", text="X", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="X": Clicked(Key))
X.grid(row=3, column=6)
Y = Button(window, width=3, height=2, relief="raised", text="Y", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="Y": Clicked(Key))
Y.grid(row=3, column=7)
Z = Button(window, width=3, height=2, relief="raised", text="Z", bg="paleturquoise2", fg="black", justify="left",
                font=('arial', 9, "bold"), activebackground="slateblue1", command=lambda Key="Z": Clicked(Key))
Z.grid(row=3, column=8)

ResetBut = Button(window, width=3, height=5, relief="raised", text="R\nE\nS\nE\nT", bg="paleturquoise2", fg="black", 
                font=('calibri', 10, "bold"), activebackground="slateblue1", command=Reset)
ResetBut.grid(row=2, column=9, rowspan=2)

NewWordBut = Button(window, width=5, height=8, relief="raised", text="N\nE\nW\n\nW\nO\nR\nD", bg="paleturquoise2", fg="black", 
                font=('calibri', 6, "bold"), activebackground="slateblue1", command=EnterNew)
NewWordBut.grid(row=2, column=0, rowspan=2)

window.mainloop()
