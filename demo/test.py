from fpdf import FPDF
import pickle_data as database
from models import *
database.load("database.txt")
import os

def cargomanifest(id_trip):

    # recovery of the packages, containers
    trip = database.set_of_trips[id_trip]
    containers_trip = trip.set_of_containers

    trip_weight = trip.weight
    data = []

    for container in containers_trip:
        container_description = []
        container_packages = container.set_of_packages
        for package in container_packages:
            container_description.append(package.description)
        data.append([container.id, container_description])
    print(data)
    # Writing
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('Arial','B',16)
    pdf.cell(200, 20, txt = 'Cargo Manifest', ln = 2, align = 'C')

    pdf.set_font('Arial','B',12)
    pdf.cell(200, 20, txt = f'The trip ID is : {trip.id}', ln = 2)

    pdf.set_font('Arial','B',12)
    pdf.cell(200, 20, txt = f'Total weight of the trip : {trip_weight}', ln = 2)

    line_height = pdf.font_size * 2.5
    col_width = pdf.epw / 4.5

    for j in range(len(data)):
        pdf.multi_cell(w=0, h = pdf.font_size * 2.5, txt=f"Container ID : {data[j][0]}", border=1)
        pdf.ln(0)
        container_description = "Description of the container :"
        line_height = 2.5 * (len(data[j][1]) + 1)
        for i in range(len(data[j][1])):
            containor_description += f"\n - {data[j][1][i]}"
        pdf.multi_cell(w=0, h = line_height, txt=container_description, border=1)
        pdf.ln(20)
    if os.path.isfile(f'output/cargo_manifest{id_trip}.pdf'):
        os.remove(f'output/cargo_manifest{id_trip}.pdf')
    pdf.output(f'output/cargo_manifest{id_trip}.pdf')

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

    for filename in os.listdir(f"trips/{id_trip}"):
        if filename.endswith(".png"):
            y.image(f"trips/{id_trip}/{filename}")

    y.output("output/Plan_chargement" + f'_{id_trip}.pdf', 'F')
#cargomanifest("T299")

print([container.groupage_id for container in database.set_of_trips["T299"].set_of_containers])