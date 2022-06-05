from models import Package, InBoundShipment, OutBoundShipment

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

# InBoundshipments
InBoundshipmentStatuses = namedtuple("InBoundshipmentStatuses", InBoundShipment.statuses)
statuses_inshipment_namedtuple = InBoundshipmentStatuses(*InBoundShipment.statuses) 

statuses_inshipment_choices = click.Choice(
    InBoundShipment.statuses, case_sensitive=False)

# OutBoundshipments
OutBoundshipmentStatuses = namedtuple("OutBoundshipmentStatuses", OutBoundShipment.statuses)
statuses_outshipment_namedtuple = OutBoundshipmentStatuses(*OutBoundShipment.statuses) 

statuses_outshipment_choices = click.Choice(
    OutBoundShipment.statuses, case_sensitive=False)