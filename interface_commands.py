import confirm, prompt, service_layer

from display import display_set_of_packages, display_set_of_shipments, display_shipment

from user_questions import *

# Package 

def add_one_package():
    keep_looping = True
    while keep_looping:
        package_informations = prompt.package_information("package")
        if confirm.package(package_informations):
            new_package_id = service_layer.add_one_package(package_informations)
            echo_id_package(new_package_id)
            keep_looping = False
    print("\n")

def add_packages_to_database():
    if choose_enter_one_by_one():
        for i in range(prompt.number_packages()):
            add_one_package()
    else:
        # we have to separate the register of the informations about the package
        # and the creation of the nb same packages 
        for i in range(prompt.number_references()):
            keep_looping = True
            while keep_looping:
                packages_informations = prompt.package_information("package")
                nb_packages = prompt.number_packages()
                packages_id_of_this_reference = set()

                if confirm.package_reference_and_amount(packages_informations, nb_packages):
                    
                    keep_looping = False 

                    for j in range(prompt.number_packages()):
                        new_package_id = service_layer.add_one_package(packages_informations)
                        packages_id_of_this_reference.add(new_package_id)

                    echo_ids(packages_id_of_this_reference)   

def del_packages_from_database():
    for i in range(prompt.number_packages()):
        keep_looping = True
        while keep_looping:
            identity = prompt.package_id()
            if confirm.del_objects():
                service_layer.del_one_package(identity)
                keep_looping = False
        print("\n")

def change_status_package():
    keep_looping = True
    while keep_looping:
        package_id = prompt.package_id()
        new_status = prompt.new_package_status()
        if confirm.change_status(package_id, new_status):
            service_layer.change_package_status(package_id, new_status)
            keep_looping = False
    print("\n")

# Inshipment 

def declare_inshipment():
    keep_looping = True
    while keep_looping:
        inshipment_informations = prompt.inshipment_information()
        keep_looping = not confirm.inshipment(inshipment_informations)
    inshipment_id = service_layer.declare_inshipment(inshipment_informations)
    echo_id_shipment(inshipment_id)
    register_packages_in_a_inshipment(inshipment_id)

def register_packages_in_a_inshipment(inshipment_id: str):

    if choose_enter_one_by_one():
        for j in range(prompt.number_packages()):

            if choose_enter_packages_by_id():
                keep_looping = True
                while keep_looping:
                    package_id = prompt.package_id()
                    if confirm.pick_package(package_id):
                        service_layer.register_package_in_a_inshipment_by_id(package_id, inshipment_id)
                        click.echo("Package added to the inshipment")
                        keep_looping = False
                    else:
                        click.echo("Aborted")
                    print("\n")
            else :
                keep_looping = True
                while keep_looping:
                    package_informations = prompt.package_information("inshipment")
                    if confirm.package(package_informations):
                        new_package_id = service_layer.add_one_package(packages_informations)
                        service_layer.register_package_in_a_inshipment_by_id(new_package_id, inshipment_id)
                        echo_id_package(new_package_id)
                        keep_looping = False
                print("\n")

    else:
        for i in range(prompt.number_references()):
            keep_looping = True
            while keep_looping :

                if choose_enter_packages_by_id :
                    print("Prompt the id of the package you want to use as reference")
                    package_id = prompt.package_id()
                    package_informations = service_layer.access_to_the_package_informations_by_id(package_id)
                    nb_packages = prompt.number_packages()
                    packages_id_per_reference = set()

                    if confirm.package_reference_and_amount(package_informations, nb_packages) :
                        keep_looping = False 
                        for j in range(nb_packages):
                            new_package_id = service_layer.add_one_package(package_informations)
                            service_layer.register_package_in_a_inshipment_by_id(new_package_id, inshipment_id)
                            packages_id_per_reference.add(new_package_id)

                else : 
                    packages_informations = prompt.package_information("inshipment")
                    nb_packages = prompt.number_packages()
                    packages_id_per_reference = set()

                    if confirm.package_reference_and_amount(packages_informations, nb_packages):
                        keep_looping = False 
                        for j in range(nb_packages):
                            new_package_id = service_layer.add_one_package(packages_informations)
                            service_layer.register_package_in_a_inshipment_by_id(new_package_id)
                            packages_id_per_reference.add(new_package_id)
            echo_ids(packages_id_per_reference)


def update_inshipment():
    keep_looping = True 
    while keep_looping:
        id_inshipment = prompt.inshipment_id()
        inshipment = database.set_of_shipments[id_inshipment]
        arrival_date = prompt.datetime("Arrival date ")
        if confirm.update_inshipment(id_inshipment, arrival_date):
            inshipment.status = InBoundShipment.statuses[0] 
            inshipment.arrival_date = arrival_date 
            inshipment_packages = inshipment.set_of_packages
            for package in inshipment_packages: 
                package.status = Package.statuses[1]
            keep_looping = False

def del_shipments():
    for i in range(prompt.number_packages()):
        keep_looping = True
        while keep_looping:
            identity = prompt.shipment_id()
            if confirm.del_objects():
                database.set_of_shipments.remove(identity)
                keep_looping = False
        print("\n")

# Outshipment 

def register_packages_outshipment():
    shipment_packages = SetOfPackages() 
    for j in range(prompt.number_packages()):
        keep_looping = True
        while keep_looping:
            identity = prompt.package_id()
            if confirm.pick_package(identity):
                package_picked = database.set_of_packages[identity]
                shipment_packages.add(package_picked)
                click.echo("Package picked")
                keep_looping = False
            else:
                click.echo("Aborted")
    return shipment_packages

def declare_outshipment():
    keep_looping = True
    while keep_looping:
        outshipment_information = prompt.outshipment_information()
        if confirm.outshipment(outshipment_information):
            keep_looping = False
    outshipment = OutBoundShipment(outshipment_information[0], outshipment_information[1], 
    outshipment_information[2], 
    register_packages_outshipment(),
    outshipment_information[3],
    outshipment_information[4],
    outshipment_information[5])
    database.set_of_shipments.add(outshipment)
    echo_id_shipment(outshipment.id)

def actual_exit_outboundshipment():
    keep_looping = True
    while keep_looping:
        id_outshipment = prompt.outshipment_id()
        outshipment = database.set_of_shipments[id_outshipment]
        if confirm.exit_outshipment(id_outshipment):
            outshipment.status = OutBoundShipment.statuses[0]
            outshipment_packages = outshipment.set_of_packages
            for package in outshipment_packages:
                package.status = Package.statuses[2]
            keep_looping = False
    
def delivered_outboundshipment():
    keep_looping = True
    while keep_looping:
        id_outshipment = prompt.outshipment_id()
        outshipment = database.set_of_shipments[id_outshipment]
        arrival_date = prompt.datetime("Delivered date ")
        if confirm.delivered_outshipment(id_outshipment, arrival_date):
            outshipment.expected_arrival_date = arrival_date
            outshipment.status = OutBoundShipment.statuses[2]
            outshipment_packages = outshipment.set_of_packages
            for package in outshipment_packages:
                package.status = Package.statuses[5]
            keep_looping = False

# Bundle

def declare_bundle():
    transporter = prompt.transporter()
    shipments = SetOfShipments()
    for i in range(prompt.number_shipments()):
        keep_looping = True
        while keep_looping:
            shipment_to_add = database.set_of_shipments[prompt.outshipment_id()]
            if confirm.shipment_to_add(shipment_to_add.id):
                shipments.add(shipment_to_add)
                keep_looping = False
            else:
                print("Aborted")
    new_bundle = Bundle(transporter, shipments)
    database.set_of_bundles.add(new_bundle)
    echo_id_bundle(new_bundle.id)

def declare_trip():
    ship_name = prompt.ship_name()
    bundles = SetOfBundles()
    for i in range(prompt.number_bundles()):
        keep_looping = True
        while keep_looping:
            bundle_to_add = database.set_of_bundles[prompt.bundle_id()]
            if confirm.bundle_to_add(bundle_to_add.id):
                bundles.add(bundle_to_add)
                keep_looping = False
            else:
                print("Canceled, enter the right bundle")
    new_trip = Trip(ship_name, bundles)
    database.set_of_trips.add(new_trip)
    echo_id_trip(new_trip.id)


    
