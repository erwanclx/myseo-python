from pathlib import Path

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkextrafont import Font

import csv

def handle_button_click():
    URL = app.input_URL.get()
    KEYWORDS = app.input_KEYWORDS.get()
    print(f"URL: {URL}\nKEYWORDS: {KEYWORDS}")
    app.resultsPage()



def init():

    default_stop_words = [
        "mot", "le", "la", "les", "de", "du", "des", "un", "une", "deux", "trois", 
        "quatre", "cinq", "six", "sept", "huit", "neuf", "dix", "et", "ou", "car", 
        "avec", "pour", "dans", "sur", "sous", "par", "entre", "vers", "ainsi", "mais", 
        "donc", "or", "ni", "si", "que", "qui", "quoi", "où", "quand", "comment", "en", 
        "ça", "ce", "cela", "cette", "ces", "ceux", "mon", "ma", "mes", "ton", "ta", 
        "tes", "son", "sa", "ses", "est", "sont"
    ]

    filename = "parasite.csv"

    try: 
        with open(filename, 'r') as csvfile:
            print("File found")
            csvreader = csv.reader(csvfile)
    except FileNotFoundError:
        print("File not found")
        with open(filename, 'w', newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["mot"])
            writer.writerows([[word] for word in default_stop_words])
class app:
    def __init__(self, master):
        self.master = master
        self.master.geometry("862x519")
        self.master.configure(bg = "#885EFF")
        self.master.resizable(False, False)
        self.master.title("mySeo")
        self.master.iconbitmap("./assets/frame0/favicon.png")

    def homePage(self):
        self.robotoClassic = Font(file="assets/fonts/Roboto-Regular.ttf", family="Roboto")
        self.robotoBold = Font(file="assets/fonts/Roboto-Bold.ttf", family="Roboto", weight="bold")

        # Canvas init

        self.mainCanvas = Canvas(
            self.master,
            bg = "#885EFF",
            height = 519,
            width = 862,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.mainCanvas.place(x = 0, y = 0)

        self.rightCanvas = Canvas(
            self.master,
            bg = "#FCFCFC",
            height = 519,
            width = 431,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.rightCanvas.place(x = 431, y = 0)

        # Left Side

        self.mainCanvas.create_text(
            39.999999999999886,
            127.0,
            anchor="nw",
            text="Bienvenue dans mySeo",
            fill="#FCFCFC",
            font=("Roboto Bold", 24 * -1)
        )

        self.mainCanvas.create_rectangle(
            39.999999999999886,
            160.0,
            99.99999999999989,
            165.0,
            fill="#FCFCFC",
            outline="")

        self.mainCanvas.create_text(
            39.999999999999886,
            191.0,
            anchor="nw",
            text="Entrez une URL à analyser\npour en découvrir un\ncompte-rendu SEO ! ",
            fill="#FCFCFC",
            font=("Roboto Regular", 24 * -1)
        )

        # Right Side

        self.rightCanvas.create_text(
            40,
            97.0,
            anchor="nw",
            text="Entrez l’URL à analyser",
            fill="#505485",
            font=("Roboto Bold", 24 * -1)
        )


        self.input_URL = Entry(
            bd=0,
            bg="#f5f2f2",
            fg="#505485",
            highlightthickness=0,
            font=("Roboto Regular", 20 * -1)
        )
        self.input_URL.place(
            x=470,
            y=137.0,
            width=321.0,
            height=59.0
        )

        # ------ Keywords ------

        self.rightCanvas.create_text(
            40,
            228.0,
            anchor="nw",
            text="Entrez trois mots clés à\nréférencer",
            fill="#505485",
            font=("Roboto Bold", 24 * -1),
        )

        self.input_KEYWORDS = Entry(
            bd=0,
            bg="#f5f2f2",
            fg="#505485",
            highlightthickness=0,
            font=("Roboto Regular", 20 * -1)
        )

        self.input_KEYWORDS.place(
            x=470,
            y=296.0,
            width=321.0,
            height=59.0
        )

        # ------ Launch ------

        self.launchAnalysisImg = PhotoImage(
            file="./assets/frame0/button_1.png"
        )

        self.launchAnalysis = Button(
            image=self.launchAnalysisImg,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: handle_button_click(),
            relief="sunken"
        )

        self.launchAnalysis.place(
            x=557,
            y=401.0,
            width=180.0,
            height=55.0
        )

        self.master.mainloop()

    def resultsPage(self):
        self.mainCanvas = Canvas(
            self.master,
            bg = "#885EFF",
            height = 519,
            width = 862,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.mainCanvas.place(x = 0, y = 0)

        self.mainCanvas.create_text(
            39.999999999999886,
            127.0,
            anchor="nw",
            text="Résultats",
            fill="#FCFCFC",
            font=("Roboto Bold", 24 * -1)
        )

        self.master.mainloop()

init()        
root = Tk()
app = app(root)
app.homePage()