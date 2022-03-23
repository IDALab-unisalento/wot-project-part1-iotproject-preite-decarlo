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
