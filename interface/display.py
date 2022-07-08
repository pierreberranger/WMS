from models import DropOff, TypedSet, Shipment, Package, Trip, Groupage, Container
import time
from interface.service_layer import database

from fpdf import FPDF
import os
from matplotlib import pyplot as plt
import click
from datetime import datetime


def set_of_packages(set_of_packages: TypedSet(Package) = None) -> None:
    if set_of_packages is None:
        set_of_packages = database.set_of_packages
    base = "{:<10}|{:<25}|{:<10}|{:<30}"
    header = base.format('id', 'description', 'status', "shipment_id")
    print(header)
    print('='*len(header))
    for package in set_of_packages:
        print(base.format(str(package.id), str(package.description),
              str(package.status), str(package.shipment_id)))


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
              dropoff.status, dropoff.arrival_date.strftime("%Y-%m-%d %H:%M")))

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
    header = base.format('id', 'container_id')
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


# Plot and save trip and container loading proposal

def create_fig_container_load_output(container_ids: set, package_placements: list, groupage_id: str = None):
    nb_containers = len(container_ids)
    fig = plt.figure(figsize=(5*nb_containers, 7))
    plt.rc('font', **{'size': 5})

    for container_idx, container_id in enumerate(container_ids): 
        ax = fig.add_subplot(1, nb_containers, (container_idx+1))
        container_dimensions = database.set_of_containers[container_id].dimensions[:2]

        # Draw the container limits 
        plt.plot([0, container_dimensions[0], container_dimensions[0], 0, 0], 
                [0, 0, container_dimensions[1], container_dimensions[1], 0], '--r')

        for package_placement in package_placements:
            if package_placement[0] == container_id:
                container_id, x, y, w, l, package_id = package_placement
                x1, x2, x3, x4, x5 = x, x+w, x+w, x, x
                y1, y2, y3, y4, y5 = y, y, y+l, y+l,y

                plt.plot([x1,x2,x3,x4,x5],[y1,y2,y3,y4,y5], '--k')

                package = database.set_of_packages[package_id]
                plt.annotate(f"{package_id} ({package.shipment_id})", (x+w/3, y+l/2), color='b')

        ax.set_aspect('equal')
        ax.set_title(f"{container_id}", size=15, weight='bold')
        plt.axis('off')

    # espacement entre les subplots
    fig.tight_layout(pad=10.0)
    if not(groupage_id is None):
        plt.suptitle(f"{groupage_id}", size=20)

    return fig

def show_fig(container_ids: set, package_placements: list, groupage_id: str = None) -> None:
    _ = create_fig_container_load_output(container_ids, package_placements, groupage_id)
    plt.show()

def plot_trip_loading_proposal(groupage_placements: dict) -> None:
    for groupage_id, groupage_placement in groupage_placements.items():
        _ = create_fig_container_load_output(*groupage_placement, groupage_id)
        plt.show()

def save_trip_loading_proposal(groupage_placements: dict, trip_id: str) -> None:
    if os.path.isdir(f"output/trips/{trip_id}"):
        raise KeyError("This trip has already been loaded, please delete the corresponding directory if you want to load it again")
    os.mkdir(f"output/trips/{trip_id}")
    for groupage_id, (containers_id, package_placements) in groupage_placements.items():
        for container_id in containers_id:
            _ = create_fig_container_load_output(set([container_id]), package_placements, groupage_id)
            plt.savefig(f"output/trips/{trip_id}/{container_id}.png", dpi=300)



def incoming_dates_list() -> list:
    incoming_dates = []
    for dropoff in database.set_of_dropoffs:
        incoming_dates.append(dropoff.arrival_date)
    incoming_dates.sort()
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
    trip: Trip = database.set_of_trips[id_trip]
    containers: TypedSet(Container) = trip.set_of_containers

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('courier','B', 20)
    pdf.cell(190, 30, txt = 'Cargo Manifest', ln=2, align = 'C')

    pdf.set_font('courier','B', 13)
    pdf.cell(100, 10, txt = f'Référence du voyage : {trip.id}', ln=0)
    pdf.cell(90, 10, txt = f'Date de départ : {str(trip.departure_date)}', align='R', ln=1)

    pdf.cell(90, 10, txt = f'Port de départ : {trip.departure_port}', align='L', ln=0)
    pdf.cell(90, 10, txt = f"Port d'arrivée : {trip.arrival_port}", align='R', ln=1)

    pdf.cell(190, 10, txt = f'Poids total du voyage : {trip.weight} kg', align='L', ln=2)

    pdf.cell(190, 5 , txt = f'', align='L', border='B', ln=2)


    pdf.set_font('courier','B', 16)
    pdf.cell(190, 20, txt = f'Contenu du voyage :', border='B', ln=1)

    for container in containers:
        pdf.set_font('courier','B', 13)
        pdf.cell(190, 10, txt = f'  Conteneur {container.id} ({container.weight} kg)', ln=1)

        pdf.set_font('courier', '', 12)
        for package in container.set_of_packages:
            pdf.cell(190, 5, txt = f'      - {package.description} ({package.weight} kg)', ln=1)
        pdf.cell(5, 5, txt = f' ', ln=0)
        pdf.cell(185, 5, txt = f' ', border='B', ln=1)

    pdf.cell(190, 5, txt = f' ', border='T', ln=1)

    pdf.output(f'output/trips/{id_trip}/cargo_manifest{id_trip}.pdf')

def cargomanifest1(id_trip):

    # recovery of the packages, containers
    trip = database.set_of_trips[id_trip]
    containers = trip.set_of_containers

    data = [(["Référence des conteneurs"], ["Description des conteneurs"])]
    
    for container in containers:
        packages_descriptions = []
        for package in container.set_of_packages:
            packages_descriptions.append(package.description)
        data += ([container.id], packages_descriptions)
    
    # Writing
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('courier','B',16)
    pdf.cell(200, 20, txt = 'Cargo Manifest', ln=2, align = 'C')

    pdf.set_font('courier','B',12)
    pdf.cell(200, 20, txt = f'La référence du voyage est : {trip.id}', ln=2)

    pdf.set_font('courier','B',12)
    pdf.cell(200, 20, txt = f'Poids total du voyage : {trip.weight}', ln=2)


    line_height = pdf.font_size * 2.5
    col_width = pdf.epw / 4.5

    lh_list = [] #list with proper line_height for each row
    use_default_height = 0 #flag

    #create lh_list of line_heights which size is equal to num rows of data
    for row in data:
        print(row)
        for datum in row:
            print(datum)
            number_of_words = len(datum) #how many words
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
            pdf.multi_cell(col_width, line_height, " ".join(datum), border=1,align='L',ln=3, 
            max_line_height=pdf.font_size)
        pdf.ln(line_height)

    pdf.output(f'output/trips/{id_trip}/cargo_manifest{id_trip}.pdf')

def generate_validated_pdf_loading_plan(id_trip):

    _DATE_FORMATS = click.DateTime(["%d%m%y","%d%m%Y", "%d/%m/%Y","%d/%m/%y"])


    y = FPDF()
    y.add_page()

    y.set_font('courier','B', 16)
    y.cell(200, 20, txt = '', ln=2)

    y.set_font('courier','B', 20)
    y.cell(200, 20, txt = f'Trip : {id_trip} ', ln=2, align='C')

    #y.set_font('courier','B',12)
    #y.cell(200, 20, txt = f'Date de chargement des contanaires : {date_loading} ', ln=2)

    y.set_font('courier','B', 16)
    y.cell(200, 20, txt = '', ln=2)

    y.set_font('courier','B', 16)
    y.cell(200, 20, txt = '', ln=2)

    y.set_font('courier','B', 16)
    y.cell(200, 20, txt = '', ln=2)

    y.set_font('courier','B', 20)
    y.cell(200, 20, txt = 'Détail du plan de chargement', ln=2, align = 'C')

    for filename in os.listdir(f"output/trips/{id_trip}"):
        if filename.endswith(".png"):
            y.image(f"output/trips/{id_trip}/{filename}", w=200)

    if os.path.isfile(f"output/trips/{id_trip}/Plan_chargement_T{id_trip}.pdf"):
        os.remove(f"output/trips/{id_trip}/Plan_chargement_T{id_trip}.pdf")
    y.output(f"output/trips/{id_trip}/Plan_chargement_{id_trip}.pdf", 'F')

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
    pdf.set_font('courier','B',16)
    pdf.cell(200, 20, txt = 'Planning of the arrivals of droppoffs', ln=2, align = 'C')

    incoming_dates = incoming_dates_list()
    pdf.cell(190, 5, txt = f' ', border='T', ln=1)

    for date in incoming_dates :
        for dropoff in database.set_of_dropoffs :
            
            if dropoff.arrival_date == date :
                
                pdf.set_font('courier','B', 13)
                pdf.cell(190, 10, txt = f"  {date.strftime('%Y-%m-%d %H:%M')} | Dropoff {dropoff.id} (from {dropoff.sender}, {dropoff.description})", ln=1)

                pdf.set_font('courier', '', 12)
                for package in dropoff.set_of_packages:
                    pdf.cell(190, 5, txt = f'      - {package.description} ({package.shipment_id})', ln=1)
                pdf.cell(5, 5, txt = f' ', ln=0)
                pdf.cell(185, 5, txt = f' ', border='B', ln=1)


    # save the pdf
    pdf.output("output/planning.pdf")