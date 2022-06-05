import click
import pickle_data as database
from datetime import datetime

from service_layer import Dimensions
from available_choices import statuses_package_choices, statuses_inshipment_choices, statuses_outshipment_choices, package_types_choices, statuses_package_namedtuple, statuses_inshipment_namedtuple, statuses_outshipment_namedtuple, package_types_namedtuple


# informations given by the user
def package_id() -> str:
    return click.prompt("package id ", 
    type=click.Choice(list((str(p.id) for p in database.set_of_packages))), 
    show_choices=False)

def shipment_id() -> str:
    return click.prompt("shipment id ", 
    type=click.Choice(list((str(s.id) for s in database.set_of_shipments))), 
    show_choices=False)

def inshipment_id() -> str:
    return click.prompt("shipment id ", 
    type=click.Choice(list((str(s.id) for s in database.set_of_shipments if s.id[0] == "I"))), 
    show_choices=False)

def outshipment_id() -> str:
    return click.prompt("shipment id ", 
    type=click.Choice(list((str(s.id) for s in database.set_of_shipments if s.id[0] == "O"))), 
    show_choices=False)

def bundle_id() -> str:
    return click.prompt("shipment id ", 
    type=click.Choice(list((str(b.id) for b in database.set_of_bundles))), 
    show_choices=False)

def datetime(name_date: str) -> datetime:
    in_out = True
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    while in_out:
        in_out = False
        date = input( name_date + "[" + today + "]: ")
        
        if len(date) == 0:
            print(today)
            return today
        try:
            date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        except:
            in_out = True
            print("Couldn't read the date, respect the format YYYY-MM-DD HH:mm")
    return date

def package_information(object) -> dict:
    description = click.prompt("Description of the package")
    length = click.prompt("Length", type=float)
    width = click.prompt("Width", type=float)
    height = click.prompt("Height", type=float)
    dimensions = Dimensions(width, length, height)
    weight = click.prompt("Weight", type=float)
    if object == "package":
        status = click.prompt(
            "status", default=statuses_package_namedtuple.warehouse, type=statuses_package_choices)
    elif object == "inshipment":
        status = click.prompt(
            "status", default=statuses_inshipment_namedtuple.inbound, type=statuses_inshipment_choices)
    package_type = click.prompt(
        "Package Type", default=package_types_namedtuple.EPAL, type=package_types_choices)
    return {"dimensions": dimensions, "weight": weight, "status": status, "package_type": package_type, "description": description}

def inshipment_information() -> dict:
    arrival_date = datetime("Arrival date ")
    status = statuses_inshipment_namedtuple.inbound
    sender = click.prompt("Sender ", type=str)
    # On pourrait ensuit imaginer une liste de fournisseur qu'on passerait en type avec un click.Choice ?
    adressee = click.prompt("Adressee ", type=str)
    description = click.prompt("Description of the inshipment")
    return {"arrival_date": arrival_date, "status": status, "sender": sender, "adressee": adressee, "description": description}

def outshipment_information() -> dict:
    departure_date = datetime("Departure date ")
    expected_arrival_date = datetime("Expected delivered date")
    status = statuses_package_namedtuple.warehouse
    sender = click.prompt("Sender ", type=str)
    adressee = click.prompt("Adressee ", type=str)
    description = click.prompt("Description of the outshipment")
    return {"departure_date": departure_date, "expected_arrival_date": expected_arrival_date, "status": status, "adressee": adressee, "sender": sender, "description": description}

def new_package_status() -> str:
    return click.prompt(
        "New status", default=statuses_package_namedtuple.shipbound, type=statuses_package_choices)

def transporter() -> str:
    return click.prompt(
        "Transporter ", type=str)

def ship_name() -> str:
    return click.prompt(
        "Ship Name ", default="Nostos Marine Ship", type=str)

def number_packages() -> int:
    return click.prompt("Number of packages ", type=int)

def number_references() -> int:
    return click.prompt("How many references do you have ?", type=int)

def number_shipments() -> int:
    return click.prompt("Number of shipments ", type=int)

def number_bundles() -> int:
    return click.prompt("Number of bundles ", type=int)