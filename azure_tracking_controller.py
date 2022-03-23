import asyncio
import logging
import random

from azure.iot.device import MethodResponse
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device.aio import ProvisioningDeviceClient

import pnp_helper
import handlers

# VARIABILI PER LA CONNESSIONE CON AZURE (INPUT)
security_type = "DPS"
id_scope = "0ne005457FD"
device_key = "4eRyI/FGYlEoirEXRU/Z3Jyz5BqNG7ldkvJLy7OXW2g="
device_id = "2kv7cqlfibe"
dps_endpoint = "global.azure-devices-provisioning.net"

# PROPRIETA' SENSORE
# ID
identifier = 001
# Temperatura
thermostat = {'name': "Thermostat", 'temperature': 0, 'humidity': 0}
# Gps
gps = {'name': "Gps", 'lat': 0.0, 'lon': 0.0, 'alt': 0.0}

# FUNZIONE PRINCIPALE
async def main():

    # Provisioning
    if security_type == "DPS":
        registration_result = await provision_device(dps_endpoint, id_scope, device_id, device_key)
        if registration_result.status == "assigned":
            print("Device was assigned")
            print(registration_result.registration_state.assigned_hub)
            print(registration_result.registration_state.device_id)
            device_client = IoTHubDeviceClient.create_from_symmetric_key(
                symmetric_key=device_key,
                hostname=registration_result.registration_state.assigned_hub,
                device_id=registration_result.registration_state.device_id
            )
        else:
            raise RuntimeError("Could not provision device. Aborting Plug and Play device connection.")
    else:
        raise RuntimeError("Can't use different security type from DPS")

    await device_client.connect()

    # Scrittura proprietà di sola lettura
    properties_root = pnp_helper.create_reported_properties(Identifier=identifier)
    property_updates = asyncio.gather(device_client.patch_twin_reported_properties(properties_root), )

     # Attivazione listeners
    listeners = asyncio.gather(
        execute_command_listener(device_client, method_name="Reboot", user_command_handler=handlers.reboot_handler), )

# ALTRE FUNZIONI
# Provisioning dispositivo
async def provision_device(provisioning_host, scope, registration_id, symmetric_key):
    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=provisioning_host,
        registration_id=registration_id,
        id_scope=scope,
        symmetric_key=symmetric_key,
    )
    return await provisioning_device_client.register()

# listeners (per lettura comandi e standard input)
async def execute_command_listener(
        device_client,
        component_name=None,
        method_name=None,
        user_command_handler=None,
        create_user_response_handler=None):
    while True:
        if component_name and method_name:
            command_name = component_name + "*" + method_name
        elif method_name:
            command_name = method_name
        else:
            command_name = None

        command_request = await device_client.receive_method_request(command_name)
        print("Command request received with payload")
        values = command_request.payload
        print(values)

        if user_command_handler:
            await user_command_handler(values)
        else:
            print("No handler provided to execute")

        (response_status, response_payload) = pnp_helper.create_response_payload_with_status(
            command_request, method_name, create_user_response=create_user_response_handler
        )

        command_response = MethodResponse.create_from_method_request(
            command_request, response_status, response_payload
        )

        try:
            await device_client.send_method_response(command_response)
        except Exception:
            print("responding to the {command} command failed".format(command=method_name))


def stdin_listener():
    """
    Listener for quitting the sample
    """
    while True:
        selection = input("Press Q to quit\n")
        if selection == "Q" or selection == "q":
            print("Quitting...")
            break
