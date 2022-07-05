import click
import pickle_data as database
from datetime import datetime

from models import Dimensions
from available_choices import statuses_package_choices, statuses_shipment_choices, statuses_dropoff_choices, package_types_choices, statuses_package_namedtuple, statuses_shipment_namedtuple, statuses_dropoff_namedtuple, package_types_namedtuple

# informations given by the user

def package_id() -> str:
    return click.prompt("package id ", 
    type=click.Choice(list((str(p.id) for p in database.set_of_packages))), 
    show_choices=False)


def dropoff_id() -> str:
    return click.prompt("dropoff id ", 
    type=click.Choice(list((str(d.id) for d in database.set_of_dropoffs))), 
    show_choices=False)


def shipment_id() -> str:
    return click.prompt("shipment id ", 
    type=click.Choice(list((str(s.id) for s in database.set_of_shipments))), 
    show_choices=False)


def groupage_id() -> str:
    return click.prompt("groupage id ", 
    type=click.Choice(list((str(g.id) for g in database.set_of_groupages))), 
    show_choices=False)

def trip_id() -> str:
    return click.prompt("trip id ", 
    type=click.Choice(list((str(t.id) for t in database.set_of_trips))), 
    show_choices=False)


def container_id() -> str:
    return click.prompt("container id ", 
    type=click.Choice(list((str(c.id) for c in database.set_of_containers))), 
    show_choices=False)

# Date

def date(name_date: str) -> datetime:
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

# Informations on object 

def package_information(object) -> dict:
    description = click.prompt("Description of the package")
    length = click.prompt("Length", type=float)
    width = click.prompt("Width", type=float)
    height = click.prompt("Height", type=float)
    dimensions = Dimensions(width, length, height)
    weight = click.prompt("Weight", type=float)
    if object == "package":
        status = click.prompt(
            "Status", default=statuses_package_namedtuple.warehouse, type=statuses_package_choices)
    elif object == "shipment":
        status = click.prompt(
            "Status", default=statuses_shipment_namedtuple.inbound, type=statuses_shipment_choices)
    package_type = click.prompt(
        "Package Type", default=package_types_namedtuple.EPAL, type=package_types_choices)
    return {"dimensions": dimensions, "weight": weight, "status": status, "package_type": package_type, "description": description}

def dropoff_information() -> dict:
    status = statuses_dropoff_namedtuple.inbound
    sender = click.prompt("Sender ", type=str)
    arrival_date = date("Arrival date ")
    description = click.prompt("Description of the dropoff")
    return {"status": status, "sender": sender, "arrival_date": arrival_date, "description": description}

def shipment_information() -> dict:
    status = statuses_shipment_namedtuple.inbound
    adressee = click.prompt("Adressee ", type=str)
    departure_date_from_warehouse = date("Departure date from warehouse ")
    delivery_date = date("Delivery date ")
    description = click.prompt("Description of the shipment")
    return {"status": status, "adressee": adressee, "departure_date_from_warehouse" : departure_date_from_warehouse,  "delivery_date": delivery_date,  "description": description}

def new_package_status() -> str:
    return click.prompt(
        "New status", default=statuses_package_namedtuple.shipbound, type=statuses_package_choices)

def freight_forwarder() -> str:
    return click.prompt(
        "Freight_forwarder ", type=str)

def ship_name() -> str:
    return click.prompt(
        "Ship Name ", default="Southern Liner", type=str)

def departure_date() -> datetime:
    return date("Departure date")

def number_packages() -> int:
    return click.prompt("Number of packages ", type=int)

def number_references() -> int:
    return click.prompt("Number of references you have ?", type=int)

def number_dropoffs() -> int:
    return click.prompt("Number of dropoffs ", type=int)

def number_shipments() -> int:
    return click.prompt("Number of shipments ", type=int)

def number_groupages() -> int:
    return click.prompt("Number of groupages ", type=int)

def number_trips() -> int:
    return click.prompt("Number of trips ", type=int)

def number_containers() -> int:
    return click.prompt("Number of containers ", type=int)

def number_containers_available() -> int:
    nb_available_containers = len(list((str(c.id) for c in database.set_of_containers if c.groupage_id is None)))
    nb_available_containers_standard = len(list((str(c.id) for c in database.set_of_containers if (c.groupage_id is None) and (c.dimensions == (235, 589, 239) ))))
    nb_available_containers_wide = nb_available_containers - nb_available_containers_standard
    print(f"There are {nb_available_containers} available with {nb_available_containers_standard} standard containers and {nb_available_containers_wide} wide containers")
    return int(click.prompt("Number of containers ", type=click.Choice([str(i) for i in range(nb_available_containers+1)])))

def available_container() -> set[str]:
    return click.prompt(" available container id ", 
    type=click.Choice(list((str(c.id) for c in database.set_of_containers if c.groupage_id is None))), 
    show_choices=False)

def number_containers_wide() -> int:
    nb_available_containers_wide = len(list((str(c.id) for c in database.set_of_containers if (c.groupage_id is None) and (c.dimensions == (241, 589, 239) ))))
    return int(click.prompt("Number of wide containers ", type=click.Choice(list(str(i) for i in range(nb_available_containers_wide+1)))))

