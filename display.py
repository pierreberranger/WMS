from models import DropOff, TypedSet, Shipment, Package, Trip, Groupage, Container
import datetime, time
from service_layer import database
from fpdf import FPDF
from pdfrw import PageMerge, PdfWriter, PdfReader
import os


def set_of_packages(set_of_packages: TypedSet(Package) = None) -> None:
    if set_of_packages is None:
        set_of_packages = database.set_of_packages
    base = "{:<10}|{:<25}|{:<10}|{:<30}"
    header = base.format('id', 'description', 'status', "shipment_id")
    print(header)
    print('='*len(header))
    for package in set_of_packages:
        print(base.format(package.id, package.description,
              package.status, str(package.shipment_id)))


def set_of_shipments(set_of_shipments: TypedSet(Shipment) = None) -> None:
    if set_of_shipments is None:
        set_of_shipments = database.set_of_shipments
    base = "{:<10}|{:<25}|{:<10}|{:<20}"
    header = base.format('id', 'description', 'status', "adressee")
    print(header)
    print('='*len(header))
    for shipment in set_of_shipments:
        print(base.format(shipment.id, shipment.description,
              shipment.status, shipment.adressee))

def set_of_dropoffs(set_of_dropoffs: TypedSet(DropOff) = None) -> None:
    if set_of_dropoffs is None:
        set_of_dropoffs = database.set_of_dropoffs
    base = "{:<10}|{:<25}|{:<10}|{:<10}|{:<20}"
    header = base.format('id', "description", 'sender', 'status', "arrival_date")
    print(header)
    print('='*len(header))
    for dropoff in set_of_dropoffs:
        print(base.format(dropoff.id, dropoff.description, dropoff.sender,
              dropoff.status, dropoff.arrival_date))

def set_of_trips(set_of_trips: TypedSet(Trip) = None) -> None:
    if set_of_trips is None:
        set_of_trips = database.set_of_trips
    base = "{:<10}|{:<25}"
    header = base.format('id', 'ship_name')
    print(header)
    print('='*len(header))
    for trip in set_of_trips:
        print(base.format(trip.id, trip.ship_name))

def set_of_groupages(set_of_groupages: TypedSet(Groupage) = None) -> None:
    if set_of_groupages is None:
        set_of_groupages = database.set_of_groupages
    base = "{:<10}|{:<25}"
    header = base.format('id', 'freight_forwarder')
    print(header)
    print('='*len(header))
    for groupage in set_of_groupages:
        print(base.format(groupage.id, groupage.freight_forwarder))

def set_of_containers(set_of_containers: TypedSet(Container) = None) -> None:
    if set_of_containers is None:
        set_of_containers = database.set_of_containers
    base = "{:<10}|{:<25}"
    header = base.format('id', 'groupage_id')
    print(header)
    print('='*len(header))
    for container in set_of_containers:
        print(base.format(container.id, container.groupage_id))

def shipment(shipment_id: str) -> None:
    shipment = database.set_of_shipments[shipment_id]
    shipment_informations = shipment.__dict__
    print(f"{shipment_informations}")
    print("\n")
    shipment_packages = shipment.set_of_packages
    print(
        f"The shipment {shipment_id} contains {len(shipment_packages)} packages, which are : ")
    print("\n")
    set_of_packages(shipment_packages)

def groupage(groupage_id: str) -> None:
    groupage = database.set_of_groupages[groupage_id]
    groupage_informations = groupage.__dict__
    print(f"{groupage_informations}")
    print("\n")
    groupage_shipments = groupage.set_of_shipments
    print(
        f"The groupage {groupage_id} contains {len(groupage_shipments)} shipments, which are : ")
    print("\n")
    set_of_shipments(groupage_shipments)

def dropoff(dropoff_id: str) -> None:
    dropoff = database.set_of_dropoffs[dropoff_id]
    dropoff_informations = dropoff.__dict__
    print(f"{dropoff_informations}")
    print("\n")
    dropoff_packages = dropoff.set_of_packages
    print(
        f"The dropoff {dropoff_id} contains {len(dropoff_packages)} packages, which are : ")
    print("\n")
    set_of_packages(dropoff_packages)

def container(container_id: str) -> None:
    container = database.set_of_containers[container_id]
    container_informations = container.__dict__
    print(f"{container_informations}")
    print("\n")
    container_packages = container.set_of_packages
    print(
        f"The container {container_id} contains {len(container_packages)} packages, which are : ")
    print("\n")
    set_of_packages(container_packages)

def trip_packages(trip_id: str) -> None:
    trip = database.set_of_trips[trip_id]
    trip_informations = trip.__dict__
    print(f"{trip_informations}")
    print("\n")
    trip_packages = TypedSet(Package)
    for groupage in trip.set_of_groupages:
        for shipment in groupage.set_of_shipments:
            for package in shipment.set_of_packages:
                trip_packages.add(package)
    set_of_packages(trip_packages)

def trip_shipments(trip_id: str) -> None:
    trip = database.set_of_trips[trip_id]
    trip_informations = trip.__dict__
    print(f"{trip_informations}")
    print("\n")
    trip_groupages = trip.set_of_groupages
    for trip_groupage in trip_groupages:
        groupage(trip_groupage.id)
        print("\n")

def trip_groupages(trip_id: str) -> None:
    trip = database.set_of_trips[trip_id]
    trip_informations = trip.__dict__
    print(f"{trip_informations}")
    print("\n")
    trip_groupages = trip.set_of_groupages
    print(
        f"The trip {trip_id} contains {len(trip_groupages)} groupages, which are : ")
    print("\n")
    set_of_groupages(trip_groupages)

def trip_containers(trip_id: str) -> None:
    trip = database.set_of_trips[trip_id]
    trip_informations = trip.__dict__
    print(f"{trip_informations}")
    print("\n")
    trip_groupages = trip.set_of_groupages
    trip_containers = TypedSet(Container)
    for groupage in trip_groupages:
        for container in groupage.set_of_containers:
            trip_containers.add(container)
    print(
        f"The trip {trip_id} contains {len(trip_containers)} containers, which are : ")
    print("\n")
    set_of_containers(trip_containers)

def incoming_dates_list() -> list:
    incoming_dates = []
    for dropoff in database.set_of_dropoffs:
        incoming_dates.append(dropoff.arrival_date)
    incoming_dates.sort(key=lambda x: time.mktime(time.strptime(x,"%Y-%m-%d %H:%M")))
    return incoming_dates

def planning_incoming() -> None:
    print("\n")
    base = "{:<30}|{:<10}|{:<10}|{:<20}"
    header = base.format('Date', 'Dropoff id', 'Sender', "Description")
    print(header)
    print('='*len(header))
    incoming_dates = incoming_dates_list()
    for date in incoming_dates :
        for dropoff in database.set_of_dropoffs :
            
            if dropoff.arrival_date == date :
                print(base.format(date, dropoff.id, dropoff.sender,
                    dropoff.description))
    print("\n")

def cargomanifest(id_trip):

    # recovery of the packages, containers
    trip = database.set_of_trips[id_trip]
    containers_trip = trip.set_of_containers

    trip_weight = trip.weight

    data = ( ("Référence des conteneurs", "Description des conteneurs") )
    
    for container in containers_trip:
        container_description = ""
        container_packages = container.set_of_packages
        for package in container_packages:
            container_description += " " + package.description
        data += (container.id, container_description)
    
    # Writing
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('Arial','B',16)
    pdf.cell(200, 20, txt = 'Cargo Manifest', ln = 2, align = 'C')

    pdf.set_font('Arial','B',12)
    pdf.cell(200, 20, txt = f'La référence du voyage est : {trip.id}', ln = 2)

    pdf.set_font('Arial','B',12)
    pdf.cell(200, 20, txt = f'Poids total du voyage : {trip_weight}', ln = 2)


    line_height = pdf.font_size * 2.5
    col_width = pdf.epw / 4.5

    lh_list = [] #list with proper line_height for each row
    use_default_height = 0 #flag

    #create lh_list of line_heights which size is equal to num rows of data
    for row in data:
        for datum in row:
            word_list = datum.split()
            number_of_words = len(word_list) #how many words
            if number_of_words>2: #names and cities formed by 2 words like Los Angeles are ok)
                use_default_height = 1
                new_line_height = pdf.font_size * (number_of_words/2) #new height change according to data 
        if not use_default_height:
            lh_list.append(line_height)
        else:
            lh_list.append(new_line_height)
            use_default_height = 0

    #create your fpdf table ..passing also max_line_height!
    for j,row in enumerate(data):
        for datum in row:
            line_height = lh_list[j] #choose right height for current row
            pdf.multi_cell(col_width, line_height, datum, border=1,align='L',ln=3, 
            max_line_height=pdf.font_size)
        pdf.ln(line_height)

    pdf.output(f'cargo_manifest{id_trip}.pdf')

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

def planning_incoming() :
    """ 
    Make a pdf describing the dates of the arrival of dropoffs 
    by chronological order
    """

    pdf = FPDF()
    
    # Adding a page
    pdf.add_page()
    pdf.set_margins(10, 10, 10)

    # Title
    pdf.set_font("Arial", size = 15)
    pdf.cell(100, 10, txt = "Planning of the arrivals of droppoffs", ln = 1, align ='C', border=1)

    # Subtitle
    pdf.set_font("Arial", size = 13, style="B")
    pdf.cell(200, 20, txt = "Date : id, sender, description", ln = 2)
    incoming_dates = incoming_dates_list()
    for date in incoming_dates :
        for dropoff in database.set_of_dropoffs :
            
            if dropoff.arrival_date == date :
                pdf.set_font("Arial", size = 9) 
                pdf.cell(200, 10, txt = f"{date} : {dropoff.id}, {dropoff.sender}, {dropoff.description}", ln = 2)

    # save the pdf
    pdf.output("output/planning.pdf")
