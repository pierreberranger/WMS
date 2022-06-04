from datetime import datetime

from models import SetOfPackages, Package, Dimensions, InBoundShipment, OutBoundShipment
import pickle_data as database

import click

from typing import Union

# choices and informations from the structure
statuses_package = click.Choice(Package.statuses, case_sensitive=False)

statuses_inshipment = click.Choice(
    InBoundShipment.statuses, case_sensitive=False)

statuses_outshipment = click.Choice(
    OutBoundShipment.statuses, case_sensitive=False)

package_types = click.Choice(Package.types, case_sensitive=False)

objects_focused_user = click.Choice(("package", "inBoundshipment",
                               "outBoundshipment", "bundle", "trip", "view", "quit"), case_sensitive=False)

view_type = click.Choice(
                ("packages", "shipments", "particular shipment"), case_sensitive=False)

def default_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def choose_enter_one_by_one() -> bool :
    return click.confirm(
        "Do you want to add the package one by one ? (else you will register them by grouping them under a number of references")

def choose_enter_package_by_id() -> bool:
    return click.confirm(
        "Do you want to add the packages to your inshipment by their ids ? (else you will have enter the all informations about the packages.")

# Others

def echo_id_package(id_package) -> None :
    click.echo(
        f'You added your package with the id : {id_package}')

def echo_ids(ids: Union[set, list, tuple]) -> None :
    click.echo(
        f'The packages for the reference have the id : {ids}')

def echo_id_shipment(id_shipment) -> None :
    click.echo(f'Your Shipment id is {id_shipment}')

def echo_id_bundle(bundle_id) -> None :
    click.echo(f'Your Bundle id is {bundle_id}')

def echo_id_trip(id) -> None :
    click.echo(f'Your Tripe id is {id}')




