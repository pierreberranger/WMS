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
        objects_focused_user_choices = click.Choice(("package", "inBoundshipment",
                               "outBoundshipment", "bundle", "trip", "view", "quit"), case_sensitive=False)
        object_focused = click.prompt("Element you want to focus on", type=objects_focused_user_choices)

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
            view_type_choices = click.Choice(
                ("packages", "shipments", "particular shipment"), case_sensitive=False)
            answer = click.prompt(
                "What do you want to view : ", default="packages", type=view_type_choices)

            if answer == "packages":
                service_layer_display.set_of_packages()
                print("\n")
            if answer == "shipments":
                service_layer_display.set_of_shipments()
                print("\n")
            if answer == "particular shipment":
                shipment_id = prompt.shipment_id()
                service_layer_display.shipment(shipment_id)
                print("\n")

        elif object_focused == "inBoundshipment" :
            declare_update = click.Choice(("declare", "update", "del", "quit"), case_sensitive=False)
            action = click.prompt("Actions ", default="declare", type=declare_update)
            
            if action == "declare" :
                interface_commands.declare_inshipment()

            if action == "update":
                print("Your inshipment is arrived.")
                interface_commands.declare_inshipment_actual_arrival()

            if action == "del":
                interface_commands.del_shipments()
            
            if action == "quit" :
                interface_commands.save_and_quit()
                in_out = False

            print("\n")

        
        elif object_focused == "outBoundshipment" :
            declare_update = click.Choice(("declare", "update", "del", "quit"), case_sensitive=False)
            action = click.prompt("Actions ", default="declare", type=declare_update)
            
            if action == "declare" :
                interface_commands.declare_outshipment()

            if action == "update":
                exit_delivered = click.Choice(("actual_exit", "delivered"), case_sensitive=False)
                answer = click.prompt("New Status ", default="actual_exit", type=exit_delivered)
                
                if answer == "actual_exit" :
                    print("Your outshipment has left the warehouse")
                    interface_commands.declare_outshipment_actual_departure()

                elif answer == "delivered_client" :
                    print("Your outshipment is delivered.")
                    interface_commands.declare_outboundshipment_actual_delivery()

            if action == "del":
                interface_commands.del_shipments()
            
            if action == "quit" :
                interface_commands.save_and_quit()
                in_out = False
        
        elif object_focused == "bundle" :
            answer = click.prompt("Do you want to prompt a bundle already scheduled or choose the automatic bundle ?",
            default="scheduled", type=click.Choice(("scheduled", "automatic", "quit"), case_sensitive=False))

            if answer == "scheduled" :
                interface_commands.declare_bundle()
            
            elif answer == "automatic" :
                print("The function is not ready yet, sorry :(")
            
            elif answer == "quit" :
                interface_commands.save_and_quit()
                in_out = False


        elif object_focused == "trip" :
            answer = click.prompt("Do you want to prompt a trip already scheduled / choose the automatic trip or obtain the Cargo Manifest of a trip ?",
            default="scheduled", type=click.Choice(("scheduled", "automatic", "CargoManifest", "quit"), case_sensitive=False))

            if answer == "scheduled" :
                interface_commands.declare_trip()
            
            elif answer == "automatic" :
                print("The function is not ready yet, sorry :(")
            
            elif answer == "CargoManifest" :
                print("The function is not ready yet, sorry :(")

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