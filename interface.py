from datetime import datetime

from models import SetOfPackages, Package, Dimensions, InBoundShipment, OutBoundShipment
from inputoutput import display_set_of_packages, display_set_of_shipments, display_shipment
import pickle_data as database

from service_layer import *

import click

filename = "database.txt"
database.load(filename)

def register_many_packages(one_by_one: bool, shipment_packages: SetOfPackages):
    default_package_status = Package.statuses[1]

    if one_by_one:
        number_of_packages = click.prompt("Number of packages ", type=int)
        for j in range(number_of_packages):
            # Features
            name = click.prompt("Description of the package")
            length = click.prompt("Length", type=float)
            width = click.prompt("Width", type=float)
            height = click.prompt("Height", type=float)
            dimensions = Dimensions(length, width, height)
            status = default_package_status
            package_type = click.prompt(
                "Package Type", default=Package.types[0], type=types)

            click.echo(
                f"You entered the package : {name}, {length}, {width}, {height}, {status}, {package_type}")
            sure = click.confirm(
                "Do you want to add the package ?", default=True)
            if sure:
                new_package = Package(dimensions, status, package_type, name)
                shipment_packages.add(new_package)  # ?
                database.set_of_packages.add(new_package)
                click.echo(
                    f'You added your package with the id : {new_package.id}')
            print("\n")
    else:
        number_of_references = click.prompt(
            "How many references do you have ?", type=int)
        for i in range(number_of_references):
            number_of_packages = click.prompt(
                f"How many packages do you have for the {i+1}ème reference ?", type=int)
            packages_id_per_reference = []
            # Packages form in the reference number i
            name = click.prompt("Description of the package (reference)")
            length = click.prompt("Length", type=float)
            width = click.prompt("Width", type=float)
            height = click.prompt("Height", type=float)
            dimensions = Dimensions(length, width, height)
            status = default_package_status
            package_type = click.prompt(
                "Package Type", default=Package.types[0], type=types)

            click.echo(
                f"You entered for this reference the package form : {name}, {length}, {width}, {height}, {status}, {package_type}")
            sure = click.confirm(
                f"Do you want to add these packages in number of {number_of_packages} ?", default=True)
            if sure:
                for j in range(number_of_packages):
                    new_package = Package(
                        dimensions, status, package_type, name)
                    shipment_packages.add(new_package)  # ?
                    database.set_of_packages.add(new_package)
                    packages_id_per_reference.append(new_package.id)
            click.echo(
                f'The packages for the reference n°{i} have the id : {packages_id_per_reference}')
        print("\n")
        


def pick_many_packages_from_warehouse(shipment_packages: SetOfPackages):
    number_of_packages = click.prompt(
        "Number of packages to pick from the warehouse", type=int)
    for j in range(number_of_packages):
        identity = package_id_prompt()
        answer = click.confirm(
            f"Are you sure to pick the package with id :{identity} ?", default=False)
        if answer:
            shipment_packages.add(database.set_of_packages[identity])
            click.echo("Package picked")
        else:
            click.echo("Aborted")


def interactive():
    in_out = True
    print("Welcome ! \n")
    print("This plateform allows you to manage your packages within many actions")
    print("If you want to quit, input [quit] \n")

    while (in_out):
        
        object_focused = click.prompt("Element you want to focus on", type=objects_concerned_user)

        if object_focused == "package":
            action = click.prompt("Action you want to do : (add,del,status)", default='add', type=click.Choice(
                ("add", "del", "status", "quit")), show_choices=False)

            if action == "add":
                add_packages_to_database(database)

            elif action == "quit":
                database.save()
                in_out = False

            elif action == "del":
                del_packages_from_database(database)

            elif action == "status":
                change_status_package(database)

        elif object_focused == "view":
            
            answer = click.prompt(
                "What do you want to view : ", default="package_database", type=view_type)
            if answer == "package_database":
                display_set_of_packages(database.set_of_packages)
                print("\n")
            if answer == "shipment_database":
                display_set_of_shipments(database.set_of_shipments)
                print("\n")
            if answer == "particular shipment":
                shipment_id = shipment_id_prompt()
                display_shipment(database.set_of_shipments[shipment_id])
                print("\n")

        elif object_focused == "inBoundshipment" :
            declare_update = click.Choice(("declare", "update", "del"), case_sensitive=False)
            answer = click.prompt("Actions ", default="declare", type=declare_update)
            
            if answer == "declare" :
                #arrival_date = click.prompt("Enter the arrival date YYYY-MM-DD HH:MM", value_proc=parse, default=default_date())
                arrival_date = datetime_prompt("Arrival date ")
                status =Package.statuses[1]
                inshipment_packages = SetOfPackages()
                sender = click.prompt("Sender ", type=str)
                # On pourrait ensuit imaginer une liste de fournisseur qu'on passerait en type avec un click.Choice ?
                adressee = click.prompt("Adressee ", type=str)

                one_by_one = click.confirm(
                    "Do you want to add the package one by one ? (else you will register them by grouping them under a number of references")
                register_many_packages(one_by_one, inshipment_packages)

                new_inshipment = InBoundShipment(
                    arrival_date, status, inshipment_packages, sender, adressee)
                database.set_of_shipments.add(new_inshipment)

                id_shipment = new_inshipment.id
                for package in inshipment_packages:
                    # ce serait plutot :
                    package.shipment_ids.append(id_shipment)

                click.echo(f'Your Inshipment id is {id_shipment}')

            if answer == "update":
                print("Your inshipment is arrived.")
                id_inshipment = shipment_id_prompt()
                inshipment = database.set_of_shipments[id_inshipment]

                #arrival_date = click.prompt("Enter the actual arrival date YYYY-MM-DD HH:MM", value_proc=parse, default=default_date())
                arrival_date = datetime_prompt("Arrival date ")
                inshipment.status = InBoundShipment.statuses[1] # InBoundShipment.statuses[0] ?
                inshipment.arrival_date = arrival_date 
                for package in inshipment.set_of_packages : 
                    package.status = Package.statuses[0]

            if answer == "del":
                id_inshipment = shipment_id_prompt()
                database.set_of_shipments.remove(id_inshipment)

            print("\n")

        
        elif object_focused == "outBoundshipment" :
            declare_update = click.Choice(("declare", "update", "del"), case_sensitive=False)
            answer = click.prompt("Actions ", default="declare", type=declare_update)
            
            if answer == "declare" :
                #departure_date = click.prompt("Enter the departure date YYYY-MM-DD HH:MM", value_proc=parse, default=default_date())
                departure_date = datetime_prompt("Departure date ")
                #expected_arrival_date = click.prompt("Enter the expected arrival date YYYY-MM-DD HH:MM", value_proc=parse, default=default_date())
                expected_arrival_date = datetime_prompt("Expected delivered date")
                status = Package.statuses[2]
                outshipment_packages = SetOfPackages()
                sender = click.prompt("Sender ", type=str)
                adressee = click.prompt("Adressee ", type=str)

                pick_many_packages_from_warehouse(outshipment_packages)

                new_outshipment = OutBoundShipment(
                    departure_date, expected_arrival_date, status, id, outshipment_packages, adressee, sender)
                database.set_of_shipments.add(new_outshipment)
                id_shipment = new_outshipment.id

                for package in outshipment_packages:
                    package.shipment_ids.append(id_shipment)  # non implémenté
                    # ce serait plutot :
                    # package.shipment_id.append(id_shipment)
            click.echo(f'Your OutBoundshipment id is {id_shipment}')

            if answer == "update":
                # answer2 = input("Do you want to declare the actual exit of the outshipment [e] or to declare its actual arrival ? [a] ")
                # cas retiré du cas d'usage
                print("Your outshipment is delivered.")
                id_outshipment = shipment_id_prompt()
                outshipment = database.set_of_shipments[id_outshipment]
                arrival_date = datetime_prompt("Delivered date ")
                outshipment.expected_arrival_date = arrival_date
                # 'delivered'
                outshipment.status = OutBoundShipment.statuses[2]
                for package in outshipment.set_of_packages:
                    package.status = Package.statuses[3]

            if answer == "del":
                id_inshipment = shipment_id_prompt()
                database.set_of_shipments.remove(id_inshipment)
            print("\n")

        elif object_focused == "quit":
            # save the data in a text file
            database.save()
            in_out = False

        else:
            print("The action doesn't exit yet")


if __name__ == "__main__":
    interactive()
