from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
import datetime

class PdfReport:
    def __init__(self, domain, target_keywords, domain_urls, not_domain_urls, three_first_words, three_first_words_in_keywords, alt_tags, all_imgs):
        self.domain = domain
        self.target_keywords = target_keywords
        self.domain_urls = domain_urls
        self.not_domain_urls = not_domain_urls
        self.three_first_words = three_first_words
        self.three_first_words_in_keywords = three_first_words_in_keywords
        self.alt_tags = alt_tags
        self.all_imgs = all_imgs
        self.date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.filename = f"Report-SEO-{self.date}.pdf"
        self.padding = 15

        self.createReport()
        self.open()

    def createReport(self):
        report = SimpleDocTemplate(self.filename, pagesize=letter)
        content = []

        styles = getSampleStyleSheet()
        title_style = styles['Title']
        subtitle_style = styles['Heading2']
        normal_style = styles['Normal']

        content.append(Paragraph("mySeo Report", title_style))
        content.append(Paragraph(f"URL Analysée:", subtitle_style))
        content.append(Paragraph(self.domain, normal_style))
        content.append(Paragraph(f"Mots clés recherchés: ", subtitle_style))
        content.append(Paragraph(', '.join(self.target_keywords), normal_style))
        
        for word in self.three_first_words:
            content.append(Paragraph(f"Mot clé pertinent : {word[0]} ({word[1]} fois)", normal_style))

        content.append(Paragraph(f"Mots clés recherchés dans les plus pertinents : { 'Oui' if self.three_first_words_in_keywords else 'Non'}", normal_style))

        content.append(Paragraph(f"Nombre d'images avec alt : ", subtitle_style))
        content.append(Paragraph(f"{len(self.alt_tags)} / {len(self.all_imgs)} soit {round(len(self.alt_tags) / len(self.all_imgs) * 100)}% d'images avec attribut alt", normal_style))

        content.append(Paragraph(" ", title_style))

        content.append(self.createTable("Liens internes", self.domain_urls))
        content.append(self.createTable("Liens externes", self.not_domain_urls))

        
        report.build(content)

    def createTable(self, title, data):
        table_data = [[title]]
        for item in data:
            table_data.append([item])

        table = Table(table_data, colWidths=[400], rowHeights=15, style=[
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#885eff')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#885eff')),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ])

        return table
    
    def open(self):
        import os
        os.startfile(self.filename)

