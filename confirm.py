import click

# check before actions

def enter_one_by_one() -> bool:
    return click.confirm(
        "Do you want to add the package one by one ? (else you will register them by grouping them under a number of references")

def enter_packages_by_id() -> bool:
    return click.confirm(
        "Do you want to add the packages to your shipment by their ids ? (else you will have enter the all informations about the packages.")

def package(package_informations: dict) -> bool:
    click.echo(
        f"You entered the package: {package_informations}")
    return click.confirm("Do you want to add the package ?", default=True)

def package_reference_and_amount(package_informations: dict, number_of_packages: int) -> bool:
    click.echo(
        f"You entered for this reference the package form: {package_informations}")
    return click.confirm(
        f"Do you want to add these packages in number of {number_of_packages} ?", default=True)

def package_reference_by_id_and_amount(package_id: str, number_of_packages: int) -> bool:
    click.echo(
        f"You entered for this reference the package id: {package_id}")
    return click.confirm(
        f"Do you want to add these packages in number of {number_of_packages} ?", default=True)

def change_status(identity, newstatus) -> bool:
    return click.confirm(
        f"You want to change the status of package {identity} to {newstatus}")

def del_objects() -> bool:
    return click.confirm(
            "Are you sure to delete the data ?", default=False)

def pick_package(identity) -> bool:
    return click.confirm(
            f"Are you sure to pick the package with id:{identity} ?", default=True)

def dropoff(dropoff_informations) -> bool:
    return click.confirm(
            f"Are the information of the dropoff right:arrival_date: {dropoff_informations} ?", default=True)

def shipment(shipment_informations) -> bool:
    return click.confirm(
            f"Are the information of the shipment right:arrival_date: {shipment_informations} ?", default=True)

def update_dropoff(id_dropoff, arrival_date) -> bool:
    return click.confirm(
            f"The DropOff {id_dropoff} arrived on the: {arrival_date}", default=True)

def remove_package_from_dropoff(package_id, dropoff_id) -> bool:
    return click.confirm(
        f"Do you want to remove the package {package_id} from the dropoff {dropoff_id}",  default=False)

def exit_shipment(id_shipment) -> bool:
    return click.confirm(f"The Shipment {id_shipment} has left the warehouse.", default = True)

def delivered_shipment(id, date) -> bool:
    return click.confirm(f"The Shipment {id} has been delivered on the {date}.", default = True)

def shipment_to_add(identity) -> bool:
    return click.confirm(
            f"Are you sure to add the shipment with id:{identity} ?", default=True)

def groupage_to_add(id) -> bool:
    return click.confirm(
            f"Are you sure to add the groupage with id:{id} ?", default=True)

def plan_loading() -> bool :
    return click.confirm(
        f"Do you confirm you want to use this plan for the load of your trip ?"
    )

def add_objects() -> bool :
    return click.confirm(
        f"Do you confirm you want to add this groupage to your trip ?"
    )