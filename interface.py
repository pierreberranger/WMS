from dateutil import parser
from datetime import datetime
import os

from models import SetOfPackages, Package, Dimensions, InBoundShipment, Shipment, OutBoundShipment
from inputoutput import set_of_packages_to_txt, txt_to_set_of_packages, display_packages

import click

""" import numpy as np """

""" Attention du code est écrit en commentaire car nous n'avons merge les fichiers et les fonctions sont donc encore indisponibles"""

# créer la variable globale
package_database = txt_to_set_of_packages()
# attention : préciser le fichier dans lequel la datebase est gardée en memoire
shipment_database = ...

statuses_package = click.Choice(Package.statuses, case_sensitive=False)
statuses_inshipment = click.Choice(InBoundShipment.statuses, case_sensitive=False)
statuses_outshipment = click.Choice(OutBoundShipment.statuses, case_sensitive=False)
types = click.Choice(Package.types, case_sensitive=False)

def package_id_prompt():
    return int(click.prompt("package id ",type=click.Choice(list((str(p.id) for p in package_database))), show_choices=False))

def shipment_id_prompt():
    return int(click.prompt("shipment id ",type=click.Choice(list((str(p.id) for p in shipment_database))), show_choices=False))

def default_date() :
    today_date = datetime.now()
    year = str(today_date.year)
    month = str(today_date.month)
    day = str(today_date.day)
    hour = str(today_date.hour)
    minute = str(today_date.minute)
    if 0<=today_date.month<=9 :
        month = "0" + month
    if 0<=today_date.day<=9 :
        year = "0"+year
    if 0<=today_date.hour<=9 :
        hour = "0" + hour
    if 0<=today_date.minute<=9 :
        minute = "0"+minute
    return year+'-'+month+'-'+day+' '+hour+":"+minute

def parse(value: str) :
    try:
        date = parser.parse(value)
    except:
        raise click.BadParameter("Couldn't understand date.", param=value)
    return value

def register_many_packages(one_by_one: bool, shipment_packages: SetOfPackages(), type_of_shipment: str) :
    if type_of_shipment == "inshipment" :
        default_package_status = Package.statuses[1]
    if type_of_shipment == "outshipment" :
        default_package_status = Package.statuses[2]
    if one_by_one : 
        number_of_packages = click.prompt(f"Number of packages ", type=int)
        for j in range(number_of_packages) :
            # Features
            name = click.prompt("Description of the package")
            length = click.prompt("Length",type=float)
            width = click.prompt("Width",type=float)
            height = click.prompt("Height",type=float)
            dimensions = Dimensions(length, width, height)
            status = default_package_status
            package_type = click.prompt("Package Type", default=Package.types[0], type=types)
            
            click.echo(f"You entered the package : {name}, {length}, {width}, {height}, {status}, {package_type}")
            sure = click.confirm("Do you want to add the package ?",default=True)
            if sure:
                new_package = Package(dimensions, status, package_type, name) 
                shipment_packages.add(new_package)
                package_database.add(new_package)
                click.echo(f'You added your package with the id : {new_package.id}')
            print("\n")
    else :
        number_of_references = click.prompt(f"How much references do you have ?", type=int)
        for i in range(number_of_references) :
            number_of_packages = click.prompt(f"How much packages do you have for the {i+1}ème reference ?", type=int)
            packages_id_per_reference = []
            # Packages form in the reference number i
            name = click.prompt("Description of the package (reference)")
            length = click.prompt("Length",type=float)
            width = click.prompt("Width",type=float)
            height = click.prompt("Height",type=float)
            dimensions = Dimensions(length, width, height)
            status = default_package_status
            package_type = click.prompt("Package Type", default=Package.types[0], type=types)
            
            click.echo(f"You entered for this reference the package form : {name}, {length}, {width}, {height}, {status}, {package_type}")
            sure = click.confirm(f"Do you want to add these packages in number of {number_of_packages} ?",default=True)
            if sure :
                for j in range(number_of_packages) :
                    new_package = Package(dimensions, status, package_type, name) 
                    shipment_packages.add(new_package)
                    package_database.add(new_package)
                    packages_id_per_reference.append(new_package.id)
            click.echo(f'The packages for the reference n°{i} have the id : {packages_id_per_reference}')
        print("\n")

def interactive():
    in_out = True
    print("Welcome ! \n")
    print("This plateform allows you to manage your packages within many actions")
    print("If you want to quit, input [quit] \n")


    while (in_out) :
            
        element = click.Choice(("package", "inBoundshipment", "outBoundShipment", "view", "quit"), case_sensitive=False)
        action = click.prompt("Element you want to focus on", type=element)

        if action ==  "package" :
            action2 = click.prompt("Action you want to do : (add,del,status)", default='add', type=click.Choice(("add","del","status", "quit")), show_choices=False)
            
            if action2 == "add" :
                # Features
                name = click.prompt("Description of the package")
                length = click.prompt("Length",type=float)
                width = click.prompt("Width",type=float)
                height = click.prompt("Height",type=float)
                dimensions = Dimensions(length, width, height)
                status = click.prompt("status", default=Package.statuses[0], type=statuses_package)
                package_type = click.prompt("Package Type", default=Package.types[0], type=types)
                
                click.echo(f"You entered the package : {name}, {length}, {width}, {height}, {status}, {package_type}")
                sure = click.confirm("Do you want to add the package ?",default=True)
                
                if sure:
                    new_package = Package(dimensions, status, package_type) 
                    package_database.add(new_package)
                    click.echo(f'You added your package with the id : {new_package.id}')
                print("\n")

            elif action2 == "quit" :
                #save the data in a text file
                set_of_packages_to_txt(package_database)
                in_out = False
                

            elif action2 == "del" :
                identity =  package_id_prompt()
                answer = click.confirm("Are you sure to delete the data ?", default=False)
                if answer:
                    package_database.remove(identity) 
                print("\n")

            elif action2 == "sta" :
                identity = package_id_prompt()
                newstatus = click.prompt("New status", default=Package.statuses[2], type=statuses_package)
                answer = click.confirm(f"You want to change the status of package {identity} to {newstatus}")
                if answer:
                    package_database[identity].status = newstatus
                print("\n")
        
        elif action == "view" :
            display_packages(package_database)
            print("\n")

        elif action == "inBoundshipment" :
            declare_update = click.Choice(("declare", "update", "del"), case_sensitive=False)
            answer = click.prompt("Actions ", default="declare", type=declare_update)
            
            if answer == "declare" :
                arrival_date = click.prompt("Enter the arrival date YYYY-MM-DD HH:MM", value_proc=parse, default=default_date())
                status =Package.statuses[1]
                inshipment_packages = SetOfPackages()
                sender = click.prompt("Sender ", type=str) 
                #On pourrait ensuit imaginer une liste de fournisseur qu'on passerait en type avec un click.Choice ?
                adressee = click.prompt("Adressee ", type=str)

                one_by_one = click.confirm("Do you want to add the package one by one ? (else you will register them by grouping them under a number of references")
                register_many_packages(one_by_one, inshipment_packages, "inshipment")

                new_inshipment = InBoundShipment(arrival_date, status, inshipment_packages, sender, adressee)
                #shipment_database.add(new_inshipment)
                #Why not create a set of shipment like with the set of packages ? To have a data base with the shipment
                id_shipment = new_inshipment.id 
                for package in inshipment_packages:
                    package.shipment_id = id_shipment
                
                click.echo(f'Your Inshipment id is {id_shipment}')

            if answer == "update" :
                print("Your inshipment is arrived.")
                id_inshipment = shipment_id_prompt()
                inshipment = shipment_database[id_inshipment]
                arrival_date = click.prompt("Enter the actual arrival date YYYY-MM-DD HH:MM", value_proc=parse, default=default_date())
                inshipment.status = InBoundShipment.statuses[1] # InBoundShipment.statuses[0] ?
                inshipment.arrival_date = arrival_date 
                for package in inshipment.set_of_packages : 
                    package.status = Package.statuses[0]

            if answer == "del" :
                id_inshipment = shipment_id_prompt()
                shipment_database.remove(id_inshipment)

            print("\n")
        
        elif action == "outBoundShipment" :
            declare_update = click.Choice(("declare", "update", "del"), case_sensitive=False)
            answer = click.prompt("Actions ", default="declare", type=declare_update)
            
            if answer == "declare" :
                departure_date = click.prompt("Enter the departure date YYYY-MM-DD HH:MM", value_proc=parse, default=default_date())
                expected_arrival_date = click.prompt("Enter the expected arrival date YYYY-MM-DD HH:MM", value_proc=parse, default=default_date())
                status = Package.statuses[2]
                outshipment_packages = SetOfPackages()
                sender = click.prompt("Sender ", type=str) 
                adressee = click.prompt("Adressee ", type=str)

                one_by_one = click.confirm("Do you want to add the package one by one ? (else you will register them by grouping them under a number of references")
                register_many_packages(one_by_one, outshipment_packages, "outshipment")
                
                new_outshipment = OutBoundShipment(departure_date, expected_arrival_date, status, id, set_of_packages, adressee, sender)
                #new_outshipment = OutBoundShipment(outshipment_packages, receiver,status, expected_dispatch_date ,dispatch_date, expected_delivery_date, delivery_date) #
                #Why not create a set of shipment like with the set of packages ? To have a data base with the shipment
                #shipment_database.add(new_outshipment)
                id_shipment = new_outshipment.id 
                for package in outshipment_packages :
                    package.shipment_id = id_shipment

            if answer == "update" :
                #answer2 = input("Do you want to declare the actual exist of the outshipment [e] or to declare its actual arrival ? [a] ")
                # cas retiré du cas d'usage
                print("Your outshipment is delivered.")
                id_outshipment = shipment_id_prompt()
                outshipment = shipment_database[id_outshipment]
                arrival_date = click.prompt("Enter the actual arrival date YYYY-MM-DD HH:MM", value_proc=parse, default=default_date())
                outshipment.expected_arrival_date = arrival_date
                outshipment.status = OutBoundShipment.statuses[1]
                for package in shoutipment.set_of_packages : 
                    package.status = Package.statuses[3]
                
            if answer == "del" :
                id_inshipment = shipment_id_prompt()
                shipment_database.remove(id_inshipment)
            print("\n")

        

        elif action == "quit" :
            #save the data in a text file
            set_of_packages_to_txt(package_database)
            in_out = False
        
        else :
            print("The action doesn't exit yet")

if __name__ == "__main__":
    interactive()