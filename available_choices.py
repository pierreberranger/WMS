from models import Package, InBoundShipment, OutBoundShipment

import click
from collections import namedtuple

# Informations from the structure

# Packages 
    # statuses
Statuses_package = namedtuple("PackageStatuses", Package.statuses)
statuses_package_namedtuple = Statuses_package(*Package.statuses) 

statuses_package_choices = click.Choice(Package.statuses, case_sensitive=False)

    # types 
Types_package = namedtuple("PackageTypes", Package.types)
package_types_namedtuple = Types_package(*Package.types) 

package_types_choices = click.Choice(Package.types, case_sensitive=False)

# InBoundshipments
Statuses_inshipment = namedtuple("InBoundshipmentStatuses", InBoundShipment.statuses)
statuses_inshipment_namedtuple = Statuses_package(*InBoundShipment.statuses) 

statuses_inshipment_choices = click.Choice(
    InBoundShipment.statuses, case_sensitive=False)

# OutBoundshipments
Statuses_outshipment = namedtuple("OutBoundshipmentStatuses", OutBoundShipment.statuses)
statuses_outshipment_namedtuple = Statuses_package(*OutBoundShipment.statuses) 

statuses_outshipment_choices = click.Choice(
    OutBoundShipment.statuses, case_sensitive=False)