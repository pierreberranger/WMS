from  fpdf import FPDF
from pdfrw import PageMerge, PdfWriter, PdfReader
import os



def generate_validated_pdf_loading_plan(id_trip):

    _DATE_FORMATS = click.DateTime(["%d%m%y","%d%m%Y", "%d/%m/%Y","%d/%m/%y"])


    y = FPDF()
    y.add_page()

    y.set_font('Arial','B',16)
    y.cell(200, 20, txt = 'Plan de chargement', ln = 2, align = 'C')

    y.set_font('Arial','B',16)
    y.cell(200, 20, txt = '', ln = 2)

    y.set_font('Arial','B',12)
    y.cell(200, 20, txt = f'Trip : {id_trip} ', ln = 2)

    #y.set_font('Arial','B',12)
    #y.cell(200, 20, txt = f'Date de chargement des contanaires : {date_loading} ', ln = 2)

    y.set_font('Arial','B',18)
    y.cell(200, 20, txt = 'Description du plan de chargement ', ln = 2, align = 'C')

    for filename in os.listdir(id_trip):
        if filename.endswith(".png"):
            y.image(filename)

    y.output("output/Plan_chargement" + f'_{id_trip}.pdf', 'F')
