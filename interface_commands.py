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

# Inshipment 

def declare_inshipment() -> None: # fonction destinée aux Shipments
    """
    Adds a new shipment to the database by asking the user 
    its informations and the packages to add to this shipment.
    """ 

    keep_looping = True
    while keep_looping:
        inshipment_informations = prompt.inshipment_information()
        keep_looping = not confirm.inshipment(inshipment_informations)
    inshipment_id = service_layer.declare_inshipment(inshipment_informations)
    echo.id_shipment(inshipment_id)
    register_packages_in_an_inshipment(inshipment_id)

def register_packages_in_an_inshipment(inshipment_id: str) -> None: # fonction destinée aux Shipments
    """
    Adds packages to an inshipment by two different ways :
    - Adds the packages one by one by asking their information or their id
    to the user. Then echos the new package id of newly created packages.
    - Adds N times packages sharing the same informations. 
    The package informations used as reference can be entered by the user
    or determined thanks to the id of an existing package
    
    Parameters :
        inshipment_id (str) : The id of the shipment to add packages to
    """


    if confirm.enter_one_by_one():
        for _ in range(prompt.number_packages()):

            if confirm.enter_packages_by_id():
                keep_looping = True
                while keep_looping:
                    package_id = prompt.package_id()
                    if confirm.pick_package(package_id):
                        service_layer.register_package_in_a_shipment_by_id(package_id, inshipment_id)
                        click.echo("Package added to the inshipment")
                        keep_looping = False
                    else:
                        click.echo("Aborted")
                    print("\n")
            else:
                keep_looping = True
                while keep_looping:
                    package_informations = prompt.package_information("inshipment")
                    if confirm.package(package_informations):
                        new_package_id = service_layer.add_one_package(packages_informations)
                        service_layer.register_package_in_a_shipment_by_id(new_package_id, inshipment_id)
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
                    package_informations = service_layer.access_to_the_package_informations_by_id(package_id) # passer par un constructeur de copies permet de s'affranchir de cette étape
                    nb_packages = prompt.number_packages()
                    packages_id_of_this_reference = set()

                    if confirm.package_reference_and_amount(package_informations, nb_packages): 
                        keep_looping = False 
                        for _ in range(nb_packages):
                            new_package_id = service_layer.add_one_package(package_informations)
                            service_layer.register_package_in_a_shipment_by_id(new_package_id, inshipment_id)
                            packages_id_of_this_reference.add(new_package_id)

                else: 
                    packages_informations = prompt.package_information("inshipment")
                    nb_packages = prompt.number_packages()
                    packages_id_of_this_reference = set()

                    if confirm.package_reference_and_amount(packages_informations, nb_packages):
                        keep_looping = False 
                        for _ in range(nb_packages):
                            new_package_id = service_layer.add_one_package(packages_informations)
                            service_layer.register_package_in_a_shipment_by_id(new_package_id)
                            packages_id_of_this_reference.add(new_package_id)
            echo.ids(packages_id_of_this_reference)


def declare_inshipment_actual_arrival() -> None: # fonction destinée aux futurs DropOffs et potentiellement aux Shipments
    """
    - Changes the arrival date of an inshipment by asking the user 
    its id and the actual arrival date to the warehouse. 
    - Updates the status of the packages of the given inshipment to `"warehouse"`.
    """
    
    keep_looping = True 
    while keep_looping:
        id_inshipment = prompt.inshipment_id()
        actual_arrival_date = prompt.datetime("Arrival date ")
        if confirm.update_inshipment(id_inshipment, actual_arrival_date):
            service_layer.declare_inshipment_actual_arrival(id_inshipment, actual_arrival_date)
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
                service_layer.del_inshipment(shipment_id)
                keep_looping = False
        print("\n")

# Outshipment 

def declare_outshipment() -> None: # fonction destinée aux DropOffs dans le sens où on rentre les packages par id
    """
    Adds a new outshipment to the database by asking the user 
    its informations and the packages to add to this outshipment.
    """
    
    keep_looping = True
    while keep_looping:
        outshipment_informations = prompt.outshipment_information()
        if confirm.outshipment(outshipment_informations):
            keep_looping = False
    outshipment_id = service_layer.declare_outshipment(outshipment_informations)
    echo.id_shipment(outshipment_id)
    register_packages_in_an_outshipment(outshipment_id)

def register_packages_in_an_outshipment(outshipment_id: str) -> None: # fonction destinée aux DropOffs dans le sens où on rentre les packages par id
    """
    Adds packages to an outshipment one by one by asking their id
    to the user.
    
    Parameters :
        outshipment_id (str) : The id of the outshipment to add packages to
    """
    
    for _ in range(prompt.number_packages()):
        keep_looping = True  
        while keep_looping:
            package_id = prompt.package_id()
            if confirm.pick_package(package_id):
                service_layer.register_package_in_a_shipment_by_id(package_id, outshipment_id)
                click.echo("Package added")
                keep_looping = False
            else:
                click.echo("Aborted")


def declare_outshipment_actual_departure() -> None:
    """
    - Changes the departure date of an outshipment by asking the user 
    its id and the actual departure date from the warehouse. 
    - Updates the status of the given outshipment to `"outbound"`.
    - Updates the status of the packages of the given outshipment to `"shipbound"`.
    """

    keep_looping = True
    while keep_looping:
        outshipment_id = prompt.outshipment_id()
        actual_departure_date = prompt.datetime("Departure date ")
        if confirm.exit_outshipment(outshipment_id):
            service_layer.declare_outshipment_actual_departure(actual_departure_date, outshipment_id)
            keep_looping = False
    
def declare_outboundshipment_actual_delivery() -> None:
    """
    - Changes the delivery date of an outshipment by asking the user 
    its id and the actual delivery date from the warehouse. 
    - Updates the status of the given outshipment to `"delivered"`.
    - Updates the status of the packages of the given outshipment to `"delivered"`.
    """

    keep_looping = True
    while keep_looping:
        outshipment_id = prompt.outshipment_id()
        actual_delivery_date = prompt.datetime("Delivered date ")
        if confirm.delivered_outshipment(outshipment_id, actual_delivery_date):
            service_layer.declare_inshipment_actual_delivery(outshipment_id, actual_delivery_date)
            keep_looping = False

# Bundle

def declare_bundle() -> None: # Fonction à modifier après avoir modifié la logique
    """
    Adds a new groupage to the database by asking the user 
    its informations and the shipments to add to this groupage.
    """

    print("Fonction à modifier après avoir modifié la logique ")
    pass 

    shipments = SetOfShipments() 

    freight_forwarder = prompt.freight_forwarder()
    for _ in range(prompt.number_shipments()):
        keep_looping = True
        while keep_looping:
            outshipment_id = prompt.outshipment_id()
            if confirm.shipment_to_add(outshipment_id):
                shipment_to_add = database.set_of_shipments[outshipment_id]
                shipments.add(shipment_to_add)
                keep_looping = False
            else:
                print("Aborted")
    new_bundle = Bundle(freight_forwarder, shipments)
    database.set_of_bundles.add(new_bundle)
    echo.id_bundle(new_bundle.id)

def declare_trip(): # Fonction à modifier après avoir modifié la logique
    print("Fonction à modifier après avoir modifié la logique ")
    pass 

    ship_name = prompt.ship_name()
    bundles = SetOfBundles()
    for _ in range(prompt.number_bundles()):
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
    echo.id_trip(new_trip.id)