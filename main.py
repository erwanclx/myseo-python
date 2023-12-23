from pathlib import Path

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, OptionMenu, ttk, StringVar, Menu, Toplevel, Listbox, Frame
from ttkthemes import ThemedTk
from tkextrafont import Font

import csv
import requests
from requests.exceptions import RequestException, ConnectionError

from process import WebPageAnalyzer
from pdfReport import PdfReport

def init():

    default_stop_words = [
        "le", "la", "les", "de", "du", "des", "un", "une", "deux", "trois", 
        "quatre", "cinq", "six", "sept", "huit", "neuf", "dix", "et", "ou", "car", 
        "avec", "pour", "dans", "sur", "sous", "par", "entre", "vers", "ainsi", "mais", 
        "donc", "or", "ni", "si", "que", "qui", "quoi", "où", "quand", "comment", "en", 
        "ça", "ce", "cela", "cette", "ces", "ceux", "mon", "ma", "mes", "ton", "ta",  "à",
        "tes", "son", "sa", "ses", "est", "sont", 
        "je", "tu", "il", "elle", "nous", "vous", "ils", "elles", "on", "lui", "leur", "eux",
        "-", "–", "—", "!", "?", ".", ",", "|", "«", "»", ":", ";", "(", ")", "[", "]", "{", "}", "’", "“", "”", "…", "•", "€", "°", "£", ">", "<",
    ]

    filename = "parasite.csv"

    try: 
        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
    except FileNotFoundError:
        with open(filename, 'w', newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([[word] for word in default_stop_words])
class app:
    def __init__(self, master):
        self.filename = "parasite.csv"
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

        self.settingsMenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Paramètres", menu=self.settingsMenu)
        self.settingsMenu.add_command(label="Modifier les mots parasites..", command=self.changeWords)

        self.settingsMenu.add_separator()
        self.settingsMenu.add_command(label="Quitter", command=self.master.quit)

    def popup(self, text_content):
        popup = Toplevel(self.master)
        popup.title("Aide")
        popup.geometry("400x200")
        popup.resizable(False, False)
        popup.iconbitmap("./assets/frame0/favicon.ico")

        popupCanvas = Canvas(
            popup,
            bg = "#885EFF",
            height = 200,
            width = 400,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        popupCanvas.place(x = 0, y = 0)

        popupCanvas.create_text(
            40,
            40.0,
            anchor="nw",
            text="Aide",
            fill="#FCFCFC",
            font=("Roboto Bold", 24 * -1)
        )

        popupCanvas.create_rectangle(
            40,
            73.0,
            100,
            78.0,
            fill="#FCFCFC",
            outline="")

        popupCanvas.create_text(
            40,
            107.0,
            anchor="nw",
            text=text_content,
            fill="#FCFCFC",
            font=("Roboto Regular", 16 * -1)
        )

    def handle_button_click(self):

        analyzed_keywords = []

        URL = app.input_URL.get()
        KEYWORDS = app.input_KEYWORDS.get()

        analyzed_keywords = KEYWORDS.split(" ")

        try :
            response = requests.get(URL)
            analyzed_url = URL
            analyzer = WebPageAnalyzer(URL, analyzed_keywords)
            firsts_words, incoming_links, outgoing_links, alt_tags, all_imgs, keywords = analyzer.main().values()


            self.changePage(self.resultsPage(
                URL,
                analyzed_keywords,
                firsts_words,
                incoming_links,
                outgoing_links,
                alt_tags,
                all_imgs,
                keywords
            ))
                 

        except ConnectionError as e:
            print(f"Une erreur s'est produite lors de la requête HTTP : {e}")
            app.errorPage()
            return

        except RequestException as e:
            print(f"Une erreur s'est produite : {e}")
            app.errorPage()
            return

    def getParasiteWords(self):
        with open(self.filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            return [word[0] for word in csvreader]

    def changeWords(self):
        parasite_words = self.getParasiteWords()
        print(parasite_words)
        modal = Toplevel(self.master)
        modal.title("Modifier les mots parasites")

        modal.geometry("400x600")
        modal.resizable(False, False)
        modal.iconbitmap("./assets/frame0/favicon.ico")

        modalCanvas = Canvas(
            modal,
            bg = "#885EFF",
            height = 600,
            width = 400,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        modalCanvas.place(x = 0, y = 0)

        modalCanvas.create_text(
            40,
            40.0,
            anchor="nw",
            text="Modifier les mots parasites",
            fill="#FCFCFC",
            font=("Roboto Bold", 24 * -1)
        )

        modalCanvas.create_rectangle(
            40,
            73.0,
            100,
            78.0,
            fill="#FCFCFC",
            outline="")
        
        listboxFrame = Frame(modal, bg="#885eff", bd=0, highlightthickness=0, borderwidth=0)
        listboxFrame.place(x=40, y=100, width=320, height=400)
        style=ttk.Style()
        style.configure("Vertical.TScrollbar", background="#885eff", bordercolor="#885eff")
        scrollbar = ttk.Scrollbar(listboxFrame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.listbox = Listbox(listboxFrame, yscrollcommand=scrollbar.set, font=("Roboto Regular", 20 * -1), bg="#885eff", fg="white", highlightthickness=0, borderwidth = 0)
        self.listbox.style = ttk.Style()
        self.listbox.pack(side="left", fill="both", expand=True)

        for word in parasite_words:
            self.listbox.insert("end", word)

        # Add delete button
            
        self.deleteImg = PhotoImage(
            file="./assets/edit_page/delete_btn.png"
        )
        
        delete = Button(
            modal,
            image=self.deleteImg,
            command=lambda: self.deleteWord(),
            borderwidth=0,
            highlightthickness=0,
            activebackground="#885eff",
            background="#885eff",
            relief="sunken",
        )

        delete.place(
            x=40,
            y=510.0,
            width=180.0,
            height=55.0
        )

        # Add add button

        self.addImg = PhotoImage(
            file="./assets/edit_page/add_btn.png"
        )

        add = Button(
            modal,
            image=self.addImg,
            command=lambda: self.addWord(),
            borderwidth=0,
            highlightthickness=0,
            activebackground="#885eff",
            background="#885eff",
            relief="sunken",
        )

        add.place(
            x=220,
            y=510.0,
            width=180.0,
            height=55.0
        )

        return
            
    def deleteWord(self):
        selected_word = self.listbox.get(self.listbox.curselection())
        self.listbox.delete(self.listbox.curselection())
        with open(self.filename, 'w', newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([[word] for word in self.listbox.get(0, "end")])
        self.popup(f"Le mot parasite {selected_word} a bien été supprimé !")

    def addWord(self):
        modal = Toplevel(self.master)
        modal.title("Ajouter un mot parasite")

        modal.geometry("400x200")
        modal.resizable(False, False)
        modal.iconbitmap("./assets/frame0/favicon.ico")

        modalCanvas = Canvas(
            modal,
            bg = "#885EFF",
            height = 200,
            width = 400,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        modalCanvas.place(x = 0, y = 0)

        modalCanvas.create_text(
            40,
            40.0,
            anchor="nw",
            text="Ajouter un mot parasite",
            fill="#FCFCFC",
            font=("Roboto Bold", 24 * -1)
        )

        modalCanvas.create_rectangle(
            40,
            73.0,
            100,
            78.0,
            fill="#FCFCFC",
            outline="")

        self.input_parasite = ttk.Entry(
            modal,
            style="TEntry",
            font=("Roboto Regular", 20 * -1)
        )

        self.input_parasite.place(
            x=40,
            y=107.0,
            width=241.0,
            height=59.0
        )

        self.addImg = PhotoImage(
            file="./assets/edit_page/add_btn.png"
        )

        add = Button(
            modal,
            image=self.addImg,
            command=lambda: self.addWordToCSV(),
            borderwidth=0,
            highlightthickness=0,
            activebackground="#885eff",
            background="#885eff",
            relief="sunken",
        )

        add.place(
            x=290,
            y=107.0,
            width=60.0,
            height=60.0
        )
        

    def addWordToCSV(self):
        with open(self.filename, 'a', newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([self.input_parasite.get()])
        self.listbox.insert("end", self.input_parasite.get())
        self.popup(f"Le mot parasite {self.input_parasite.get()} a bien été ajouté !")
        self.input_parasite.delete(0, "end")

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

        ## Default URL
        self.input_URL.insert(0, "https://www.lemonde.fr/afrique/article/2023/12/23/loi-immigration-des-etudiants-africains-toujours-plus-entraves-dans-leur-mobilite_6207430_3212.html")

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

        ## Default Keywords
        self.input_KEYWORDS.insert(0, "Testez moi maintenant")

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
            command=lambda: self.handle_button_click(),
            relief="sunken",
        )

        self.launchAnalysis.place(
            x=557,
            y=401.0,
            width=180.0,
            height=55.0
        )

        self.master.mainloop()

    def resultsPage(self, url, target_keywords, url_keywords, incoming_links, outgoing_links, alt_tags, all_imgs, keywords):
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
            text="Mots clés analysés : \n 👉 " + ", ".join(target_keywords[:3]),
            fill="#FCFCFC",
            font=("Roboto Bold", 20 * -1)
        )

        # Right Side

        ## Header

        dropdown_var = StringVar(value=url)
        dropdown = ttk.Combobox(
            self.master,
            textvariable=dropdown_var,
            values=incoming_links,
            state="readonly",
            style="TCombobox",
            font=("Roboto Regular", 20 * -1),
        )
        dropdown.place(x=470, y=30.0, width=321.0, height=59.0)
        dropdown.bind("<<ComboboxSelected>>", lambda event: self.handle_dropdown_click(event, target_keywords))
        
        
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
            text="Entrants : \n 🔘 " + str(len(incoming_links)),
            fill="#505485",
            font=("Roboto Bold", 16 * -1)
        )

        self.rightCanvas.create_text(
            200,
            150.0,
            anchor="nw",
            text="Sortants : \n 🔘 " + str(len(outgoing_links)),
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
            text=f"{round(len(alt_tags) / len(all_imgs) * 100)}% d'images avec attribut alt ({len(alt_tags)} / {len(all_imgs)})",
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

        for keyword in url_keywords:
            index = url_keywords.index(keyword)
            self.rightCanvas.create_text(
                40,
                282.0 + index * 28,
                anchor="nw",
                text=f"🔘 {keyword[0]} - {keyword[1]} fois",
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
            text="Oui" if keywords else "Non",
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
            command=lambda: PdfReport(
                url,
                target_keywords,
                incoming_links,
                outgoing_links,
                url_keywords,
                keywords,
                alt_tags,
                all_imgs
            )
            ,
            # command=lambda: self.changePage(self.homePage),
            relief="sunken"
        )

        self.export.place(
            x=557,
            y=441.0,
            width=180.0,
            height=55.0
        )



        self.master.mainloop()

    def handle_dropdown_click(self, event, analyzed_keywords):
                
                URL = event.widget.get()
                analyzer = WebPageAnalyzer(URL, analyzed_keywords)
                firsts_words, incoming_links, outgoing_links, alt_tags, all_imgs, keywords = analyzer.main().values()
                self.changePage(self.resultsPage(
                    URL,
                    analyzed_keywords,
                    firsts_words,
                    incoming_links,
                    outgoing_links,
                    alt_tags,
                    all_imgs,
                    keywords
                ))

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
