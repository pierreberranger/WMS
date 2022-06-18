import click

import prompt, interface_commands
import service_layer_display

interface_commands.load()

def interactive():
    in_out = True
    print("Welcome ! \n")
    print("This plateform allows you to manage your packages within many actions")
    print("If you want to quit, input [quit] \n")

    while (in_out):
        objects_focused_user_choices = click.Choice(("package", "shipment", "dropoff",
                                "groupage", "trip", "view", "quit"), case_sensitive=False)
        object_focused = click.prompt("Element you want to focus on", default="shipment", type=objects_focused_user_choices)

        if object_focused == "package":
            action = click.prompt("Action you want to do :", default='add', type=click.Choice(
                ("add", "del", "status", "quit")))

            if action == "add":
                interface_commands.add_packages_to_database()

            elif action == "quit":
                interface_commands.save_and_quit()
                in_out = False

            elif action == "del":
                interface_commands.del_packages_from_database()

            elif action == "status":
                interface_commands.change_status_package()

        elif object_focused == "view":
            list_or_details = click.Choice(
                ("list", "details", "pdf"), case_sensitive=False)
            action = click.prompt("Type of view you want ", default="list", type=list_or_details)

            if action == "list":
                view_type_choices = click.Choice(
                    ("packages",  "dropoffs", "shipments","groupages", "trips",), case_sensitive=False)
                answer = click.prompt(
                    "What do you want to view : ", default="packages", type=view_type_choices)

                if answer == "packages":
                    service_layer_display.set_of_packages()
                    print("\n")
                elif answer =="dropoffs" :
                    service_layer_display.set_of_dropoffs()
                    print("\n")
                elif answer == "shipments":
                    service_layer_display.set_of_shipments()
                    print("\n")
                elif answer == "trips":
                    service_layer_display.set_of_trips()
                    print("\n")
                elif answer == "groupages":
                    service_layer_display.set_of_groupages()
                    print("\n")
            
            if action == "details":
                view_type_choices = click.Choice(
                    ("dropoff", "shipment", "groupage", "trip", "container"), case_sensitive=False)
                answer = click.prompt(
                    "What do you want to view ", default="shipment", type=view_type_choices)

                if answer == "shipment":
                    shipment_id = prompt.shipment_id()
                    service_layer_display.shipment(shipment_id)
                    print("\n")
                elif answer == "groupage":
                    groupage_id = prompt.groupage_id ()
                    service_layer_display.groupage(groupage_id)
                    print("\n")
                elif answer == "dropoff":
                    dropoff_id = prompt.dropoff_id ()
                    service_layer_display.dropoff(dropoff_id)
                    print("\n")
                elif answer == "trip" :
                    choice = click.prompt(
                    "What do you want to view ", default="shipment", type=
                    click.Choice(
                    ("packages", "shipments", "groupages", "containers"), case_sensitive=False))
                    trip_id = prompt.trip_id()

                    if choice == "packages" :
                        service_layer_display.trip_packages(trip_id)
                    elif choice == "shipments" :
                        service_layer_display.trip_shipments(trip_id)
                    elif choice == "groupages" :
                        service_layer_display.trip_groupages(trip_id)
                    elif choice == "containers":
                        service_layer_display.trip_containers(trip_id)
                elif answer == "container":
                    container_id = prompt.container_id ()
                    service_layer_display.container(container_id)
                    print("\n")
            if action == "pdf":
                documents = click.Choice(
                ("CargoManifest", "Incoming", "Outputs"), case_sensitive=False)
                document_generated = click.prompt("Document you want to generate ", default="Incoming")

                if document_generated == "CargoManifest":
                    pass
                elif document_generated == "Incoming":
                    service_layer_display.planning_incoming()

                elif document_generated == "Outputs":
                    pass

        elif object_focused == "dropoff" :
            declare_update = click.Choice(("declare", "update", "del", "quit"), case_sensitive=False)
            action = click.prompt("Actions ", default="declare", type=declare_update)
            
            if action == "declare" :
                interface_commands.declare_dropoff()

            if action == "update":
                options_update_dropoff = click.Choice(("arrival_date", "add_packages", "del_packages", "actual_arrival"), case_sensitive=False)
                answer = click.prompt("Update ", default="actual_arrival", type=options_update_dropoff)
                
                if answer == "actual_arrival":
                    print("Your dropoff is arrived.")
                    interface_commands.declare_dropoff_actual_arrival()
                
                elif answer == "arrival_date":
                    interface_commands.change_arrival_date()
                
                elif answer == "add_packages":
                    interface_commands.add_packages_to_a_dropoff()
                
                elif answer == "del_packages":
                    interface_commands.del_packages_of_a_dropoff()

            if action == "del":
                interface_commands.del_dropoffs()
            
            if action == "quit" :
                interface_commands.save_and_quit()
                in_out = False

            print("\n")

        
        elif object_focused == "shipment" :
            declare_update = click.Choice(("declare", "update", "del", "quit", "home"), case_sensitive=False)
            action = click.prompt("Actions ", default="declare", type=declare_update)
            
            if action == "declare" :
                interface_commands.declare_shipment()
            
            if action == "home" :
                print("\n")

            if action == "update":
                exit_delivered = click.Choice(("actual_exit", "add_packages", "del_packages", "delivered"), case_sensitive=False)
                answer = click.prompt("Update ", default="actual_exit", type=exit_delivered)
                
                if answer == "actual_exit" :
                    print("Your shipment has left the warehouse")
                    interface_commands.declare_shipment_actual_departure_from_warehouse()
                
                elif answer == "add_packages":
                    interface_commands.add_packages_to_a_shipment()

                elif answer == "del_packages":
                    interface_commands.del_packages_to_a_shipment()

                elif answer == "delivered" :
                    print("Your shipment is delivered.")
                    interface_commands.declare_shipment_actual_delivery()

            if action == "del":
                interface_commands.del_shipments()
            
            if action == "quit" :
                interface_commands.save_and_quit()
                in_out = False
        
        elif object_focused == "groupage" :
            answer = click.prompt("Actions ",
            default="declare", type=click.Choice(("declare", "del", "quit"), case_sensitive=False))

            if answer == "declare" :
                interface_commands.declare_groupage()
            
            if answer == "del" :
                interface_commands.del_groupages()
            
            elif answer == "quit" :
                interface_commands.save_and_quit()
                in_out = False


        elif object_focused == "trip" :
            answer = click.prompt("Actions ",
            default="declare", type=click.Choice(("declare", "del", "load", "quit"), case_sensitive=False))

            if answer == "declare" :
                interface_commands.declare_trip()
            
            elif answer == "del" :
                interface_commands.del_trip()
            
            elif answer == "load":
                interface_commands.load_trip()

            elif answer == "quit" :
                interface_commands.save_and_quit()
                in_out = False

        elif object_focused == "quit":
            interface_commands.save_and_quit()
            in_out = False

        else:
            print("The action doesn't exit yet")


if __name__ == "__main__":
    interactive()