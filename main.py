from pathlib import Path

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, OptionMenu, ttk, StringVar, Menu
from ttkthemes import ThemedTk
from tkextrafont import Font

import csv
import requests

URLs = ['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8']

def handle_button_click():

    analyzed_url = ""
    analyzed_keywords = []

    URL = app.input_URL.get()
    KEYWORDS = app.input_KEYWORDS.get()

    analyzed_url = URL
    analyzed_keywords = KEYWORDS.split(" ")

    print(analyzed_url)
    print(analyzed_keywords)

    try :
        response = requests.get(URL)
        analyzed_url = URL
        app.resultsPage(URL, analyzed_keywords)

    except:
        app.errorPage()
        return

def changeWords():
    print("changeWords")
    return

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
        self.master.iconbitmap("./assets/frame0/favicon.ico")
        self.setMenu()

    def changeTitle(self, title):
        self.master.title(title)

    def setMenu(self):
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)

        self.settingsMenu = Menu(self.menu)
        self.menu.add_cascade(label="Paramètres", menu=self.settingsMenu)
        self.settingsMenu.add_command(label="Modifier les mots parasites..", command=changeWords())

    def changePage(self, page):
        self.master.destroy()
        self.master = Tk()
        self.master.geometry("862x519")
        self.master.configure(bg = "#885EFF")
        self.master.resizable(False, False)
        self.master.title("mySeo")
        self.master.iconbitmap("./assets/frame0/favicon.ico")
        page()
        self.setMenu()

    def homePage(self):
        self.robotoClassic = Font(file="assets/fonts/Roboto-Regular.ttf", family="Roboto")
        self.robotoBold = Font(file="assets/fonts/Roboto-Bold.ttf", family="Roboto", weight="bold")
        self.robotoItalic = Font(file="assets/fonts/Roboto-Italic.ttf", family="Roboto", slant="italic")

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
            40,
            127.0,
            anchor="nw",
            text="Bienvenue dans mySeo",
            fill="#FCFCFC",
            font=("Roboto Bold", 24 * -1)
        )

        self.mainCanvas.create_rectangle(
            40,
            160.0,
            100,
            165.0,
            fill="#FCFCFC",
            outline="")

        self.mainCanvas.create_text(
            40,
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

        self.input_URL = ttk.Entry(
            style="TEntry",
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

        self.input_KEYWORDS = ttk.Entry(
            style="TEntry",
            font=("Roboto Regular", 20 * -1)
        )

        self.input_KEYWORDS.place(
            x=470,
            y=296.0,
            width=321.0,
            height=59.0
        )

        self.rightCanvas.create_text(
            40,
            367.0,
            anchor="nw",
            text="Séparez les mots clés par un espace",
            fill="#505485",
            font=("Roboto Italic", 16 * -1)
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

    def resultsPage(self, url, keywords):

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
            40,
            127.0,
            anchor="nw",
            text="Résultats",
            fill="#FCFCFC",
            font=("Roboto Bold", 24 * -1)
        )

        self.mainCanvas.create_rectangle(
            40,
            160.0,
            100,
            165.0,
            fill="#FCFCFC",
            outline="")
        
        self.mainCanvas.create_text(
            40,
            191.0,
            anchor="nw",
            text="URL analysée : \n 👉 " + url,
            fill="#FCFCFC",
            font=("Roboto Bold", 20 * -1)
        )

        self.mainCanvas.create_text(
            40,
            250.0,
            anchor="nw",
            text="Mots clés analysés : \n 👉 " + ", ".join(keywords[:3]),
            fill="#FCFCFC",
            font=("Roboto Bold", 20 * -1)
        )

        # Right Side

        ## Header

        dropdown_var = StringVar(value=URLs[0])
        dropdown = ttk.Combobox(
            self.master,
            textvariable=dropdown_var,
            values=URLs,
            state="readonly",
            style="TCombobox",
            font=("Roboto Regular", 20 * -1),
        )
        dropdown.place(x=470, y=30.0, width=321.0, height=59.0)

        
        style = ttk.Style()
        style.configure("TCombobox", padding=5, font=("Arial", 12), background="#FCFCFC", foreground="#505485" )
        
        self.rightCanvas.create_text(
            40,
            97.0,
            anchor="nw",
            text="Analyse de la page",
            fill="#885eff",
            font=("Roboto Bold", 24 * -1)
        )

        ## First row - URLs

        self.rightCanvas.create_text(
            40,
            122.0,
            anchor="nw",
            text="Nombres de liens :",
            fill="#505485",
            font=("Roboto Bold", 20 * -1)
        )

        self.rightCanvas.create_text(
            40,
            150.0,
            anchor="nw",
            text="Entrants : \n 🔘 3",
            fill="#505485",
            font=("Roboto Bold", 16 * -1)
        )

        self.rightCanvas.create_text(
            200,
            150.0,
            anchor="nw",
            text="Sortants : \n 🔘 3",
            fill="#505485",
            font=("Roboto Bold", 16 * -1)
        )

        ## Second row

        self.rightCanvas.create_text(
            40,
            200.0,
            anchor="nw",
            text="Attributs :",
            fill="#505485",
            font=("Roboto Bold", 20 * -1)
        )

        self.rightCanvas.create_text(
            40,
            228.0,
            anchor="nw",
            text="87% d'images avec attribut alt",
            fill="#505485",
            font=("Roboto Bold", 16 * -1)
        )
        
        ## Third row - Keywords

        self.rightCanvas.create_text(
            40,
            255.0,
            anchor="nw",
            text="Trois premiers mots clés de la page :",
            fill="#505485",
            font=("Roboto Bold", 20 * -1)
        )

        for keyword in keywords:
            index = keywords.index(keyword)
            self.rightCanvas.create_text(
                40,
                282.0 + index * 28,
                anchor="nw",
                text=f"🔘 {keyword} - 8 fois",
                fill="#505485",
                font=("Roboto Bold", 16 * -1)
            )

        ## Fourth row - Keywords given by the user vs keywords found

        self.rightCanvas.create_text(
            40,
            375.0,
            anchor="nw",
            text="Mots clés trouvés :",
            fill="#505485",
            font=("Roboto Bold", 20 * -1)
        )

        self.rightCanvas.create_text(
            40,
            402.0,
            anchor="nw",
            text="Oui",
            fill="#505485",
            font=("Roboto Bold", 16 * -1)
        )
        
        # Export Button

        self.exportImg = PhotoImage(
            file="./assets/result_page/export_btn.png"
        )

        self.export = Button(
            image=self.exportImg,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.changePage(self.homePage),
            relief="sunken"
        )

        self.export.place(
            x=557,
            y=441.0,
            width=180.0,
            height=55.0
        )

        self.master.mainloop()

    def errorPage(self):
        self.mainCanvas = Canvas(
            self.master,
            bg = "#fcfcfc",
            height = 519,
            width = 862,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.mainCanvas.place(x = 0, y = 0)

        self.mainCanvas.create_text(
            40,
            127.0,
            anchor="nw",
            text="Une erreur est survenue. \nVeuillez vérifier l’URL saisie.",
            fill="#f54242",
            font=("Roboto Bold", 24 * -1)
        )

        # HomePage Button

        self.backHomeImg = PhotoImage(
            file="./assets/error_page/error_btn.png"
        )

        self.backHome = Button(
            image=self.backHomeImg,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.changePage(self.homePage),
            relief="sunken"
        )

        self.backHome.place(
            x=557,
            y=401.0,
            width=180.0,
            height=55.0
        )

        self.master.mainloop()

init()        

root = Tk()
style = ttk.Style(root)
root.tk.call('source', 'azure/azure.tcl')
style.theme_use('azure')
app = app(root)
app.homePage()
# app.resultsPage("https://www.google.com", ["test1", "test2", "test3"])