
# Interface commands
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

# service layer
def declare_inshipment_actual_arrival(inshipment_id, actual_arrival_date) -> None:
    inshipment = database.set_of_shipments[inshipment_id]
    inshipment.status = InBoundShipment.statuses[0] 
    inshipment.arrival_date = actual_arrival_date 
    inshipment_packages = inshipment.set_of_packages
    for package in inshipment_packages: 
        package.status = Package.statuses[1]

def declare_outshipment(outshipment_informations) -> str:
    outshipment = OutBoundShipment(**outshipment_informations)
    database.set_of_shipments.add(outshipment)
    return outshipment.id