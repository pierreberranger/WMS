from models import Package, Shipment, DropOff

import click
from collections import namedtuple

# Informations from the structure

# Packages 
    # statuses
PackageStatuses = namedtuple("PackageStatuses", Package.statuses)
statuses_package_namedtuple = PackageStatuses(*Package.statuses) 

statuses_package_choices = click.Choice(Package.statuses, case_sensitive=False)

    # types 
PackageTypes = namedtuple("PackageTypes", Package.types)
package_types_namedtuple = PackageTypes(*Package.types) 

package_types_choices = click.Choice(Package.types, case_sensitive=False)

# DropOff
DropOffStatuses = namedtuple("DropOffStatuses", DropOff.statuses)
statuses_dropoff_namedtuple = DropOffStatuses(*DropOff.statuses) 

statuses_dropoff_choices = click.Choice(
    DropOff.statuses, case_sensitive=False)

# Shipments
ShipmentStatuses = namedtuple("ShipmentStatuses", Shipment.statuses)
statuses_shipment_namedtuple = ShipmentStatuses(*Shipment.statuses) 

statuses_shipment_choices = click.Choice(
    Shipment.statuses, case_sensitive=False)
