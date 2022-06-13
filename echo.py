import click
from typing import Union

def id_package(id_package) -> None :
    click.echo(
        f'You added your package with the id : {id_package}')

def ids(ids: Union[set, list, tuple]) -> None :
    click.echo(
        f'The packages for the reference have the id : {ids}')

def id_dropoff(id_dropoff) -> None :
    click.echo(f'Your DropOff id is {id_dropoff}')

def id_shipment(id_shipment) -> None :
    click.echo(f'Your Shipment id is {id_shipment}')

def id_groupage(groupage_id) -> None :
    click.echo(f'Your Groupage id is {groupage_id}')

def id_trip(id) -> None :
    click.echo(f'Your Tripe id is {id}')