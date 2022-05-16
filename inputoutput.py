from models import SetOfPackages, Dimensions, Package, SetOfSomething

def display(set_of_something: SetOfSomething):
    base = "{:<10}|{:<25}|{:<10}|{:<30}"
    header = base.format('id','description','status',"shipment_ids")
    print(header)
    print ('='*len(header))
    for something in set_of_something:
        print(base.format(something.id, something.description, something.status, str(something.shipment_ids)))