import "iotc" as iotc;
{
    Timestamp: .enqueuedTime,
    IdDispositivoAzure: .device.id,
    IdDispositivoFisico: .device.properties.reported | iotc::find(.name == "Identifier").value,
    NomeDispositivo: .device.name,
    Temperatura: .telemetry | iotc::find(.name == "Temperature").value,
    Umidita: .telemetry | iotc::find(.name == "Humidity").value
}
