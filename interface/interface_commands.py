import click

from interface import confirm, prompt, service_layer, echo, display


import container_optimisation.container_loading as container_loading

def home(prompt_function):
    def decorated_function(* args, ** kwargs):
        try :
            return prompt_function(* args, ** kwargs)
        except (click.exceptions.Abort, KeyboardInterrupt):
            click.echo("\nBack to the menu")
            print("\n")
            return
    return decorated_function
        

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

@home
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
                    print()
@home
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

@home
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

@home
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
    register_packages_in_a_dropoff(dropoff_id)

@home
def register_packages_in_a_dropoff(dropoff_id: str) -> None: # fonction destinée aux DropOffs dans le sens où on rentre les packages par id
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

@home
def declare_dropoff_actual_arrival() -> None: # fonction destinée aux futurs DropOffs et potentiellement aux dropoff
    """
    - Changes the arrival date of an dropoff by asking the user 
    its id and the actual arrival date to the warehouse. 
    - Updates the status of the packages of the given dropoff to `"warehouse"`.
    """
    
    keep_looping = True 
    while keep_looping:
        id_dropoff = prompt.dropoff_id()
        actual_arrival_date = prompt.date("Arrival date ")
        if confirm.update_dropoff(id_dropoff, actual_arrival_date):
            service_layer.declare_dropoff_actual_arrival(id_dropoff, actual_arrival_date)
            keep_looping = False

@home
def change_arrival_date() -> None:
    """ Update the arrival date of a dropoff """

    keep_looping = True 
    while keep_looping:
        dropoff_id = prompt.dropoff_id()
        actual_arrival_date = prompt.date("Arrival date ")
        if confirm.update_dropoff(dropoff_id, actual_arrival_date):
            service_layer.update_dropoff_arrival_date(dropoff_id, actual_arrival_date)
            keep_looping = False

@home
def add_packages_to_a_dropoff() -> None:
    """ Add packages to a dropoff after its declaration """
    dropoff_id = prompt.dropoff_id()
    register_packages_in_a_dropoff(dropoff_id)

@home
def del_packages_of_a_dropoff() -> None:
    """ Del Packages of a Dropoff after its declaration """
    dropoff_id = prompt.dropoff_id()
    package_id = prompt.package_id()
    confirm.remove_package_from_dropoff(package_id, dropoff_id)
    service_layer.remove_package_from_dropoff(package_id, dropoff_id)

@home
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

@home
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

@home
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
                if confirm.enter_packages_by_id():
                    print("Prompt the id of the package you want to use as reference")
                    package_id = prompt.package_id()
                    nb_packages = prompt.number_packages()
                    packages_id_of_this_reference = set()

                    if confirm.package_reference_by_id_and_amount(package_id, nb_packages): 
                        keep_looping = False 
                        for _ in range(nb_packages):
                            new_package_id = service_layer.add_one_package_by_id(package_id)
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
                            service_layer.register_package_in_a_shipment_by_id(new_package_id, shipment_id)
                            packages_id_of_this_reference.add(new_package_id)
            echo.ids(packages_id_of_this_reference)
            print("\n")

@home

def update_status_shipment() -> None:
    """ Change the status of a given shipment"""
    keep_looping = True
    while keep_looping:
        shipment_id = prompt.shipment_id()
        new_status = prompt.new_shipment_status()
        if confirm.change_status(shipment_id, new_status):
            service_layer.change_shipment_status(shipment_id, new_status)
            keep_looping = False
        print("\n")
    
@home
def add_packages_to_a_shipment() -> None:
    """ Add packages to a shipment """
    shipment_id = prompt.shipment_id()
    register_packages_in_an_shipment(shipment_id)

@home
def del_packages_to_a_shipment() -> None:
    """ Del packages to a shipment """
    del_packages_from_database()

@home
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
        actual_departure_date_from_warehouse = prompt.date("Departure date from warehouse ")
        if confirm.exit_shipment(shipment_id):
            service_layer.declare_shipment_actual_departure_from_warehouse(actual_departure_date_from_warehouse, shipment_id)
            keep_looping = False

@home   
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
        actual_delivery_date = prompt.date("Delivered date ")
        if confirm.delivered_shipment(shipment_id, actual_delivery_date):
            service_layer.declare_shipment_actual_delivery(actual_delivery_date, shipment_id)
            keep_looping = False

@home
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

@home
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

@home
def del_groupages() :
    """
    Deletes N groupages from the database by asking their id to the user.
        N : an input asked to the user
    """
    for _ in range(prompt.number_groupages()):
        keep_looping = True
        while keep_looping:
            groupage_id = prompt.groupage_id()
            if confirm.del_objects():
                service_layer.del_groupage(groupage_id)
                keep_looping = False
        print("\n")

# Trip

@home
def declare_trip(): 
    ship_name = prompt.ship_name()
    departure_date = prompt.departure_date()
    trip_id = service_layer.declare_trip(ship_name, departure_date)
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

@home
def del_trip():
    """
    Deletes N trips from the database by asking their id to the user.
        N : an input asked to the user
    """
    for _ in range(prompt.number_trips()):
        keep_looping = True
        while keep_looping:
            trip_id = prompt.trip_id()
            if confirm.del_objects():
                service_layer.del_trip(trip_id)
                keep_looping = False
        print("\n")

@home
def load_trip() -> None:
    """Change the statuses of the packages """

    trip_id = prompt.trip_id()
    service_layer.load_packages_in_trip(trip_id)
    print("Packages and Shipments status changed")
    
    print("\n")

@home
def select_available_containers():
    nb_container_available = prompt.number_containers_available()
    nb_container_wide = prompt.number_containers_wide()
    nb_container_standard = nb_container_available - nb_container_wide
    return service_layer.available_containers(nb_container_wide, nb_container_standard)

@home
def plan_loading() -> None:
    """
    Proposes a plan to load a particular trip 
    Generates the associated pdf
    """
    
    trip_id = prompt.trip_id()
    available_containers = select_available_containers()
    groupage_placements = container_loading.trip_loading(trip_id, available_containers)
    display.plot_trip_loading_proposal(groupage_placements)
    click.echo(f"We propose the following plannification to load the trip n°{trip_id}")
    if confirm.plan_loading():
        display.save_trip_loading_proposal(groupage_placements, trip_id)
        display.generate_validated_pdf_loading_plan(trip_id)
        container_loading.validate_trip_loading_proposal(groupage_placements)
    else :
        print("You can update the trip to have a new loading proposal. '\n'")

@home
def add_groupage_to_a_trip():
    trip_id = prompt.trip_id()
    for _ in range(prompt.number_groupages()):
        keep_looping = True
        while keep_looping:
            groupage_id = prompt.groupage_id()
            if confirm.add_objects():
                service_layer.add_groupage_to_trip(trip_id, groupage_id)
                keep_looping = False
        print("\n")
@home
def del_groupage_from_a_trip():
    trip_id = prompt.trip_id()
    for _ in range(prompt.number_groupages()):
        keep_looping = True
        while keep_looping:
            groupage_id = prompt.groupage_id()
            if confirm.del_objects():
                service_layer.del_groupage_from_trip(trip_id, groupage_id)
                keep_looping = False
        print("\n")

# Containers

@home
def add_containers():
    for _ in range(prompt.number_containers()):
        type_container = click.prompt("Type of container ", 
        default="standard", type=click.Choice(("palet_wide","standard"), case_sensitive=False))
        container_id = service_layer.add_container_to_database(type_container)
        echo.id_container(container_id)
        print("\n")

@home
def del_containers():
    for _ in range(prompt.number_containers()):
        keep_looping = True
        while keep_looping:
            container_id = prompt.container_id()
            if confirm.del_objects():
                service_layer.del_container_from_database(container_id)
                keep_looping = False
        print("\n")
    

        