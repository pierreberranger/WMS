import click

# check before actions

def package(package_informations: dict) -> bool:
    click.echo(
        f"You entered the package: {package_informations}")
    return click.confirm("Do you want to add the package ?", default=True)

def package_reference_and_amount(package_informations: dict, number_of_packages: int) -> bool:
    click.echo(
        f"You entered for this reference the package form: {package_informations}")
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
            f"Are you sure to pick the package with id:{identity} ?", default=False)

def inshipment(shipment_informations) -> bool:
    return click.confirm(
            f"Are the information of the inshipment right:arrival_date: {shipment_informations} ?", default=False)

def update_inshipment(id_inshipment, arrival_date) -> bool:
    return click.confirm(
            f"The Indhipment {id_inshipment} arrived on the: {arrival_date}", default=False)

def outshipment(outshipment_informations) -> bool:
    return click.confirm(
            f"Are the information of the Outshipment right: departure_date: {outshipment_informations} ?", default=False)

def exit_outshipment(id_outshipment) -> bool:
    return click.confirm(f"The Outshipment {id_outshipment} has left the warehouse.", default = False)

def delivered_outshipment(id, date) -> bool:
    return click.confirm(f"The Outshipment {id} has been delivered on the {date}.", default = False)

def shipment_to_add(identity) -> bool:
    return click.confirm(
            f"Are you sure to add the shipment with id:{identity} ?", default=False)

def bundle_to_add(id) -> bool:
    return click.confirm(
            f"Are you sure to add the bundle with id:{id} ?", default=False)
