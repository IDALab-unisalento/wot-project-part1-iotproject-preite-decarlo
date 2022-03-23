import asyncio
import logging
import random

from azure.iot.device import MethodResponse
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device.aio import ProvisioningDeviceClient
