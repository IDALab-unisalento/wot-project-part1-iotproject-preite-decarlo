import asyncio
import logging
import random

from azure.iot.device import MethodResponse
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device.aio import ProvisioningDeviceClient

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
