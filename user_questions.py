from datetime import datetime

from models import SetOfPackages, Package, Dimensions, InBoundShipment, OutBoundShipment

import click

# choices and informations from the structure
statuses_package = click.Choice(Package.statuses, case_sensitive=False)

statuses_inshipment = click.Choice(
    InBoundShipment.statuses, case_sensitive=False)

statuses_outshipment = click.Choice(
    OutBoundShipment.statuses, case_sensitive=False)

types = click.Choice(Package.types, case_sensitive=False)

objects_concerned_user = click.Choice(("package", "inBoundshipment",
                               "outBoundshipment", "view", "quit"), case_sensitive=False)

view_type = click.Choice(
                ("package_database", "shipment_database", "particular shipment"), case_sensitive=False)

def default_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

# informations given by the user
def package_id_prompt(database) -> int :
    return click.prompt("package id ", 
    type=click.Choice(list((str(p.id) for p in database.set_of_packages))), 
    show_choices=False)

def shipment_id_prompt(database) -> int :
    return click.prompt("shipment id ", 
    type=click.Choice(list((str(p.id) for p in database.set_of_shipments))), 
    show_choices=False)

def datetime_prompt(name_date) -> str :
    in_out = True
    today = default_date()
    while in_out :
        in_out = False
        date = input( name_date + "[" + today + "]: ")
        
        if len(date) == 0 :
            print(today)
            return today
        try :
            datetime.strptime(date, "%Y-%m-%d %H:%M")
        except :
            in_out = True
            print("Couldn't read the date, respect the format YYYY-MM-DD HH:mm")
    return date

def package_information_prompt() -> Package :
    name = click.prompt("Description of the package")
    length = click.prompt("Length", type=float)
    width = click.prompt("Width", type=float)
    height = click.prompt("Height", type=float)
    dimensions = Dimensions(length, width, height)
    status = click.prompt(
        "status", default=Package.statuses[0], type=statuses_package)
    package_type = click.prompt(
        "Package Type", default=Package.types[0], type=types)
    return (dimensions, status, package_type, name)

def new_package_status() -> str :
    return click.prompt(
        "New status", default=Package.statuses[2], type=statuses_package)

def enter_packages_one_by_one() -> bool :
    return click.confirm(
        "Do you want to add the package one by one ? (else you will register them by grouping them under a number of references")

# check before actions

def confirm_package(name, dimensions, status, package_type) -> bool :
    click.echo(
        f"You entered the package : {name}, {dimensions[0]}, {dimensions[1]}, {dimensions[2]}, {status}, {package_type}")
    return click.confirm("Do you want to add the package ?", default=True)

def confirm_package_reference(name, dimensions, status, package_type, number_of_packages) -> bool :
    click.echo(
        f"You entered for this reference the package form : {name},  {dimensions[0]}, {dimensions[1]}, {dimensions[2]}, {status}, {package_type}")
    return click.confirm(
        f"Do you want to add these packages in number of {number_of_packages} ?", default=True)

def confirm_change_status(identity, newstatus) :
    return click.confirm(
        f"You want to change the status of package {identity} to {newstatus}")

def confirm_del_objects(identity) :
    return click.confirm(
            "Are you sure to delete the data ?", default=False)

# Others

def save_id_package(id_package) -> None :
    click.echo(
        f'You added your package with the id : {id_package}')

def save_id_list_packages(list_id) -> None :
    click.echo(
        f'The packages for the reference have the id : {list_id}')

def save_id_shipment(id_shipment) -> None :
    click.echo(f'Your Shipment id is {id_shipment}')

def number_packages() -> int :
    return click.prompt("Number of packages ", type=int)

def number_references() -> int :
    return click.prompt("How many references do you have ?", type=int)

