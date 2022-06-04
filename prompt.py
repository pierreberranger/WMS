import click
from user_questions import *
import pickle_data as database

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

def datetime(name_date) -> str:
    in_out = True
    today = default_date()
    while in_out:
        in_out = False
        date = input( name_date + "[" + today + "]: ")
        
        if len(date) == 0:
            print(today)
            return today
        try:
            datetime.strptime(date, "%Y-%m-%d %H:%M")
        except:
            in_out = True
            print("Couldn't read the date, respect the format YYYY-MM-DD HH:mm")
    return date

def package_information(object) -> dict:
    description = click.prompt("Description of the package")
    length = click.prompt("Length", type=float)
    width = click.prompt("Width", type=float)
    height = click.prompt("Height", type=float)
    dimensions = Dimensions(length, width, height)
    weight = click.prompt("Weight", type=float)
    if object == "package":
        status = click.prompt(
            "status", default=Package.statuses[1], type=statuses_package)
    elif object == "inshipment":
        status = click.prompt(
            "status", default=Package.statuses[0], type=statuses_package)
    package_type = click.prompt(
        "Package Type", default=Package.types[0], type=package_types)
    return {"dimensions": dimensions, "weight": weight, "status": status, "package_type": package_type, "description": description}

def inshipment_information() -> dict:
    arrival_date = datetime("Arrival date ")
    status = InBoundShipment.statuses[0]
    sender = click.prompt("Sender ", type=str)
    # On pourrait ensuit imaginer une liste de fournisseur qu'on passerait en type avec un click.Choice ?
    adressee = click.prompt("Adressee ", type=str)
    description = click.prompt("Description of the inshipment")
    return {"arrival_date": arrival_date, "status": status, "sender": sender, "adressee": adressee, "description": description}

def outshipment_information() -> dict:
    departure_date = datetime("Departure date ")
    expected_arrival_date = datetime("Expected delivered date")
    status = Package.statuses[2]
    sender = click.prompt("Sender ", type=str)
    adressee = click.prompt("Adressee ", type=str)
    description = click.prompt("Description of the outshipment")
    return {"departure_date": departure_date, "expected_arrival_date": expected_arrival_date, "status": status, "adressee": adressee, "sender": sender, "description": description}

def new_package_status() -> str:
    return click.prompt(
        "New status", default=Package.statuses[2], type=statuses_package)

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