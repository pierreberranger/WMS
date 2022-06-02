from datetime import datetime
from email.policy import default

from models import SetOfPackages, Package, Dimensions, InBoundShipment, OutBoundShipment
from display import display_set_of_packages, display_set_of_shipments, display_shipment
import pickle_data as database

from service_layer import *

import click

load()

def interactive():
    in_out = True
    print("Welcome ! \n")
    print("This plateform allows you to manage your packages within many actions")
    print("If you want to quit, input [quit] \n")

    while (in_out):
        
        object_focused = click.prompt("Element you want to focus on", type=objects_focused_user)

        if object_focused == "package":
            action = click.prompt("Action you want to do : (add,del,status)", default='add', type=click.Choice(
                ("add", "del", "status", "quit")), show_choices=False)

            if action == "add":
                add_packages_to_database()

            elif action == "quit":
                quit_and_save()
                in_out = False

            elif action == "del":
                del_packages_from_database()

            elif action == "status":
                change_status_package()

        elif object_focused == "view":
            
            answer = click.prompt(
                "What do you want to view : ", default="package_database", type=view_type)
            if answer == "package_database":
                display_set_of_packages(database.set_of_packages)
                print("\n")
            if answer == "shipment_database":
                display_set_of_shipments(database.set_of_shipments)
                print("\n")
            if answer == "particular shipment":
                shipment_id = shipment_id_prompt()
                display_shipment(database.set_of_shipments[shipment_id])
                print("\n")

        elif object_focused == "inBoundshipment" :
            declare_update = click.Choice(("declare", "update", "del"), case_sensitive=False)
            action = click.prompt("Actions ", default="declare", type=declare_update)
            
            if action == "declare" :
                declare_inshipment()

            if action == "update":
                print("Your inshipment is arrived.")
                update_inshipment()

            if action == "del":
                del_shipments()

            print("\n")

        
        elif object_focused == "outBoundshipment" :
            declare_update = click.Choice(("declare", "update", "del"), case_sensitive=False)
            answer = click.prompt("Actions ", default="declare", type=declare_update)
            
            if answer == "declare" :
                declare_outshipment()

            if answer == "update":
                exit_delivered = click.Choice(("actual_exit", "delivered"), case_sensitive=False)
                answer = click.prompt("New Status ", default="actual_exit", type=exit_delivered)
                
                if answer == "actual_exit" :
                    print("Your outshipment has left the warehouse")
                    actual_exit_outboundshipment()

                elif answer == "delivered_client" :
                    print("Your outshipment is delivered.")
                    delivered_outboundshipment()

            if answer == "del":
                del_shipments()

        elif object_focused == "quit":
            quit_and_save()
            in_out = False

        else:
            print("The action doesn't exit yet")


if __name__ == "__main__":
    interactive()
