import click

import confirm, prompt, service_layer, echo


def load() -> None:
    """
    Loads the database
    """
    service_layer.load()

def save_and_quit() -> None:
    """
    Saves the database then quits
    """
    service_layer.save_and_quit()

# Package 

def add_one_package() -> None:
    """
    Adds one package to the database by asking its information 
    to the user then echos the new package id.
    """

    keep_looping = True
    while keep_looping:
        package_informations = prompt.package_information("package")
        if confirm.package(package_informations):
            new_package_id = service_layer.add_one_package(package_informations)
            echo.id_package(new_package_id)
            keep_looping = False
    print("\n")

def add_packages_to_database() -> None:
    """
    Adds packages to the database by two possible ways :
    - Adds the packages one by one by asking their information 
        to the user then echos the new package id
    - Adds N times packages sharing the same informations then echos all the new packages id
    """

    if confirm.enter_one_by_one():
        for _ in range(prompt.number_packages()):
            add_one_package()
    else:
        # we have to separate the register of the informations about the package
        # and the creation of the nb same packages 
        for _ in range(prompt.number_references()):
            keep_looping = True
            while keep_looping:
                packages_informations = prompt.package_information("package")
                nb_packages = prompt.number_packages()
                packages_id_of_this_reference = set()

                if confirm.package_reference_and_amount(packages_informations, nb_packages):
                    
                    keep_looping = False 

                    for _ in range(nb_packages):
                        new_package_id = service_layer.add_one_package(packages_informations)
                        packages_id_of_this_reference.add(new_package_id)

                    echo.ids(packages_id_of_this_reference)   

def del_packages_from_database() -> None:
    """Deletes N packages from the database by asking their id to the user.
        N : an input asked to the user""" 

    for _ in range(prompt.number_packages()):
        keep_looping = True
        while keep_looping:
            package_id = prompt.package_id()
            if confirm.del_objects():
                service_layer.del_one_package(package_id)
                keep_looping = False
        print("\n")

def change_status_package() -> None:
    """
    Changes the status of a package by asking the user 
    its id and its new status.
    """ 
    
    keep_looping = True
    while keep_looping:
        package_id = prompt.package_id()
        new_status = prompt.new_package_status()
        if confirm.change_status(package_id, new_status):
            service_layer.change_package_status(package_id, new_status)
            keep_looping = False
    print("\n")

# DropOff 
def declare_dropoff() -> None: # fonction destinée aux DropOffs dans le sens où on rentre les packages par id
    """
    Adds a new dropoff to the database by asking the user 
    its informations and the packages to add to this dropoff.
    """
    
    keep_looping = True
    while keep_looping:
        dropoff_informations = prompt.dropoff_information()
        if confirm.dropoff(dropoff_informations):
            keep_looping = False
    dropoff_id = service_layer.declare_dropoff(dropoff_informations)
    echo.id_dropoff(dropoff_id)
    register_packages_in_an_dropoff(dropoff_id)

def register_packages_in_an_dropoff(dropoff_id: str) -> None: # fonction destinée aux DropOffs dans le sens où on rentre les packages par id
    """
    Adds packages to an dropoff one by one by asking their id
    to the user.
    
    Parameters :
        dropoff_id (str) : The id of the dropoff to add packages to
    """
    
    for _ in range(prompt.number_packages()):
        keep_looping = True  
        while keep_looping:
            package_id = prompt.package_id()
            if confirm.pick_package(package_id):
                service_layer.register_package_in_a_dropoff_by_id(package_id, dropoff_id)
                click.echo("Package added")
                keep_looping = False
            else:
                click.echo("Aborted")

def declare_dropoff_actual_arrival() -> None: # fonction destinée aux futurs DropOffs et potentiellement aux dropoff
    """
    - Changes the arrival date of an dropoff by asking the user 
    its id and the actual arrival date to the warehouse. 
    - Updates the status of the packages of the given dropoff to `"warehouse"`.
    """
    
    keep_looping = True 
    while keep_looping:
        id_dropoff = prompt.dropoff_id()
        actual_arrival_date = prompt.datetime("Arrival date ")
        if confirm.update_dropoff(id_dropoff, actual_arrival_date):
            service_layer.declare_dropoff_actual_arrival(id_dropoff, actual_arrival_date)
            keep_looping = False

def del_dropoffs() -> None:
    """
    Deletes N dropoffs from the database by asking their id to the user.
        N : an input asked to the user
    """
    for _ in range(prompt.number_dropoffs()):
        keep_looping = True
        while keep_looping:
            dropoff_id = prompt.dropoff_id()
            if confirm.del_objects():
                service_layer.del_dropoff(dropoff_id)
                keep_looping = False
        print("\n")

# Shipment

def declare_shipment() -> None: # fonction destinée aux Shipments
    """
    Adds a new shipment to the database by asking the user 
    its informations and the packages to add to this shipment.
    """ 

    keep_looping = True
    while keep_looping:
        shipment_informations = prompt.shipment_information()
        keep_looping = not confirm.shipment(shipment_informations)
    shipment_id = service_layer.declare_shipment(shipment_informations)
    echo.id_shipment(shipment_id)
    register_packages_in_an_shipment(shipment_id)

def register_packages_in_an_shipment(shipment_id: str) -> None: # fonction destinée aux Shipments
    """
    Adds packages to an shipment by two different ways :
    - Adds the packages one by one by asking their information or their id
    to the user. Then echos the new package id of newly created packages.
    - Adds N times packages sharing the same informations. 
    The package informations used as reference can be entered by the user
    or determined thanks to the id of an existing package
    
    Parameters :
        shipment_id (str) : The id of the shipment to add packages to
    """


    if confirm.enter_one_by_one():
        for _ in range(prompt.number_packages()):

            if confirm.enter_packages_by_id():
                keep_looping = True
                while keep_looping:
                    package_id = prompt.package_id()
                    if confirm.pick_package(package_id):
                        service_layer.register_package_in_a_shipment_by_id(package_id, shipment_id)
                        click.echo("Package added to the shipment")
                        keep_looping = False
                    else:
                        click.echo("Aborted")
                    print("\n")
            else:
                keep_looping = True
                while keep_looping:
                    package_informations = prompt.package_information("shipment")
                    if confirm.package(package_informations):
                        new_package_id = service_layer.add_one_package(package_informations)
                        service_layer.register_package_in_a_shipment_by_id(new_package_id, shipment_id)
                        echo.id_package(new_package_id)
                        keep_looping = False
                print("\n")

    else:
        for _ in range(prompt.number_references()):
            keep_looping = True
            while keep_looping:

                if confirm.enter_packages_by_id:
                    print("Prompt the id of the package you want to use as reference")
                    package_id = prompt.package_id()
                    packages_informations = service_layer.access_to_the_package_informations_by_id(package_id) # passer par un constructeur de copies permet de s'affranchir de cette étape
                    nb_packages = prompt.number_packages()
                    packages_id_of_this_reference = set()

                    if confirm.package_reference_and_amount(packages_informations, nb_packages): 
                        keep_looping = False 
                        for _ in range(nb_packages):
                            new_package_id = service_layer.add_one_package(packages_informations)
                            service_layer.register_package_in_a_shipment_by_id(new_package_id, shipment_id)
                            packages_id_of_this_reference.add(new_package_id)

                else: 
                    packages_informations = prompt.package_information("shipment")
                    nb_packages = prompt.number_packages()
                    packages_id_of_this_reference = set()

                    if confirm.package_reference_and_amount(packages_informations, nb_packages):
                        keep_looping = False 
                        for _ in range(nb_packages):
                            new_package_id = service_layer.add_one_package(packages_informations)
                            service_layer.register_package_in_a_shipment_by_id(new_package_id)
                            packages_id_of_this_reference.add(new_package_id)
            echo.ids(packages_id_of_this_reference)


def declare_shipment_actual_departure_from_warehouse() -> None:
    """
    - Changes the departure date of an shipment by asking the user 
    its id and the actual departure date from the warehouse. 
    - Updates the status of the given shipment to `"outbound"`.
    - Updates the status of the packages of the given shipment to `"shipbound"`.
    """

    keep_looping = True
    while keep_looping:
        shipment_id = prompt.shipment_id()
        actual_departure_date_from_warehouse = prompt.datetime("Departure date from warehouse ")
        if confirm.exit_shipment(shipment_id):
            service_layer.declare_shipment_actual_departure_from_warehouse(actual_departure_date_from_warehouse, shipment_id)
            keep_looping = False
    
def declare_shipment_actual_delivery() -> None:
    """
    - Changes the delivery date of an shipment by asking the user 
    its id and the actual delivery date from the warehouse. 
    - Updates the status of the given shipment to `"delivered"`.
    - Updates the status of the packages of the given shipment to `"delivered"`.
    """

    keep_looping = True
    while keep_looping:
        shipment_id = prompt.shipment_id()
        actual_delivery_date = prompt.datetime("Delivered date ")
        if confirm.delivered_shipment(shipment_id, actual_delivery_date):
            service_layer.declare_shipment_actual_delivery(shipment_id, actual_delivery_date)
            keep_looping = False

def del_shipments() -> None:
    """
    Deletes N shipments from the database by asking their id to the user.
        N : an input asked to the user
    """
    for _ in range(prompt.number_shipments()):
        keep_looping = True
        while keep_looping:
            shipment_id = prompt.shipment_id()
            if confirm.del_objects():
                service_layer.del_shipment(shipment_id)
                keep_looping = False
        print("\n")

# groupage

def declare_groupage() -> None:
    """
    Adds a new groupage to the database by asking the user 
    its informations and the shipments to add to this groupage.
    """

    freight_forwarder = prompt.freight_forwarder()
    groupage_id = service_layer.declare_groupage(freight_forwarder)
    for _ in range(prompt.number_shipments()):
        keep_looping = True
        while keep_looping:
            shipment_id = prompt.shipment_id()
            if confirm.shipment_to_add(shipment_id):
                service_layer.add_shipment_to_a_groupage(groupage_id, shipment_id)
                keep_looping = False
            else:
                print("Aborted")
    echo.id_groupage(groupage_id)

def declare_trip(): # Fonction à modifier après avoir modifié la logique
    print("Fonction à modifier après avoir modifié la logique ")
    pass 
    
    ship_name = prompt.ship_name()
    trip_id = service_layer.declare_trip(ship_name)
    for _ in range(prompt.number_groupages()):
        keep_looping = True
        while keep_looping:
            groupage_to_add_id = prompt.groupage_id()
            if confirm.groupage_to_add(groupage_to_add_id):
                service_layer.add_groupage_to_a_trip(trip_id, groupage_to_add_id)
                keep_looping = False
            else:
                print("Canceled, enter the right groupage")
    echo.id_trip(trip_id)