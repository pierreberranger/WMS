from models import SetOfPackages, Dimensions, Package, SetOfSomething, SetOfShipments, Shipment

def display_set_of_packages(set_of_packages: SetOfPackages):
    
    base = "{:<10}|{:<25}|{:<10}|{:<30}"
    header = base.format('id','description','status',"shipment_ids")
    print(header)
    print ('='*len(header))
    for package in set_of_packages:
        print(base.format(package.id, package.description, package.status, str(package.shipment_ids)))

def display_set_of_shipments(set_of_shipments: SetOfShipments):
    
    base = "{:<10}|{:<25}|{:<10}|{:<20}|{:<20}"
    header = base.format('id','description','status',"adressee", "sender")
    print(header)
    print ('='*len(header))
    for shipment in set_of_shipments:
        print(base.format(shipment.id, shipment.description, shipment.status, shipment.adressee, shipment.sender))

def display_shipment(shipment: Shipment):
    
    print(f"id : {shipment.id}, description : {shipment.description}, status : {shipment.status}, adressee : {shipment.adressee}, sender : {shipment.sender}")
    print("\n")
    print(f"The shipment {shipment.id} contains {len(shipment.set_of_packages)}packages, which are : ")
    print("\n")
    display_set_of_packages(shipment.set_of_packages)
    