## Copyright 2023 David Lario
__author__ = 'David Lario'
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

## Revision History
## October 27, 2023 - David James Lario - Created

from pypdf import PdfWriter, PdfReader
import time
import datetime

from os import popen
import subprocess

from sqlalchemy import or_, func

from reportlab.platypus import SimpleDocTemplate, FrameBreak, Table, TableStyle, Paragraph, Frame, Spacer, Image, PageTemplate, BaseDocTemplate, NextPageTemplate, PageBreak
from reportlab.lib import colors
from reportlab.lib.units import cm, inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter, A3, A4, landscape, portrait
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfgen import canvas

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class MyPrint:
    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize

    @staticmethod
    def _header_footer(canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()

        # Header
        header = Paragraph('This is a multi-line header.  It goes on every page.   ' * 5, styles['Normal'])
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

        # Footer
        footer = Paragraph('This is a multi-line footer.  It goes on every page.   ' * 5, styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)

        # Release the canvas
        canvas.restoreState()


    def print_users(self):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=72,
                                leftMargin=72,
                                topMargin=72,
                                bottomMargin=72,
                                pagesize=self.pagesize)

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        users = User.objects.all()
        elements.append(Paragraph('My User Names', styles['Heading1']))
        for i, user in enumerate(users):
            elements.append(Paragraph(user.get_full_name(), styles['Normal']))

        doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer,
                  canvasmaker=NumberedCanvas)

        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        return pdf


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.drawRightString(211 * mm, 15 * mm + (0.2 * inch),
                             "Page %d of %d" % (self._pageNumber, page_count))


def PageLayout1(canvas, doc):
    canvas.saveState()
    canvas.setFont('Calibri', 8)
    canvas.setFillColor(colors.darkblue)

    logo = r"C:\Users\d_lar\OneDrive\Enigma Design Solutions\Document Control\Logo\Enigma Gear - Full Logo - Color2.png"
    qrcode = r"C:\Users\d_lar\OneDrive\Enigma Design Solutions\Document Control\Logo\Enigma - QRCode.png"
    bottomlogo = r"C:\Users\d_lar\OneDrive\Enigma Design Solutions\Document Control\Logo\Enigma Footer Gear.png"

    canvas.drawImage(logo, doc.leftMargin, doc.height, width=2 * inch, height=0.75 * inch, mask='auto')
    canvas.drawImage(qrcode, doc.width + doc.rightMargin/2, doc.height, width=0.75 * inch, height=0.75 * inch, mask='auto')
    canvas.drawImage(bottomlogo, 0, 0, width=8.5 * inch, height= 2.5 * inch, mask='auto')

    # canvas.drawString(inch, 0.75 * inch, "Page %d" % doc.page)
    canvas.restoreState()

def PageLayout2(canvas, doc):
    canvas.saveState()
    canvas.setFont('Calibri', 8)
    form_id = 3
    parent_id = 3

    CompanyName = self.GetRecord(form_id, "18 0-42", 0, parent_id)
    CompanyMailing = self.GetRecord(form_id, "18 15-368 0-47", 0, parent_id)
    CompanyCity = self.GetRecord(form_id, "18 15-368 58-48", 0, parent_id)
    CompanyProvince = self.GetRecord(form_id, "18 15-368 103-49 93-49", 2, parent_id)
    CompanyPostalCode = self.GetRecord(form_id, "18 15-368 103-49 93-49", 3, parent_id)
    CompanyPhone = self.GetRecord(form_id, "18 17-351 0-856", 0, parent_id)
    CompanyEmail = self.GetRecord(form_id, "18 17-351 0-856", 2, parent_id)

    ContactInfo = "CONTACT INFO: " + CompanyMailing + ", " + CompanyCity + " " + CompanyProvince
    ContactInfo = ContactInfo + ", " + CompanyPostalCode + " P:" + CompanyPhone + " E:" + CompanyEmail

    canvas.drawString(2 * inch, 0.5 * inch, ContactInfo)

    canvas.drawString(inch, 0.75 * inch, "Page %d" % doc.page)
    canvas.restoreState()

def background(canvas, doc):
    canvas.saveState()
    canvas.setFont('Calibri', 8)
    canvas.drawString(inch, 0.75 * inch, "Page %d" % doc.page)
    canvas.restoreState()


def static_title(canvas,doc):
    canvas.saveState()
    logo = r"C:\Users\d_lar\OneDrive\Enigma Design Solutions\Document Control\Logo\Enigma Gear - Full Logo - Color2.png"
    canvas.drawImage(logo,doc.width-2.5*inch,doc.height, width=4*inch, preserveAspectRatio=True)
    canvas.setFont('Times-Roman',48)
    canvas.drawString(inch, doc.height - 1*inch, "TITLE")
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch, 0.75 * inch, "Title - Page %d" % doc.page)
    canvas.restoreState()