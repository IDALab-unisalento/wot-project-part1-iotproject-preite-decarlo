# Progetto IoT Preite - De Carlo (Azure)
Programma in Python utilizzato per la connessione di Raspberry Pi ad un applicazione Azure IoT Central realizzata sulla piattaforma Microsoft Azure.

## Prerequisiti
Per il corretto funzionamento è necessario aver installato sul dispositivo:
- Python 3.8 o superiore (testato con Python 3.9.5);
- Libreria Azure IoT Device installata nell'ambiente Python;
- Libreria Python AdaFruitDHT.
Inoltre è necessario aver creato correttamente un'applicazione Azure IoT Central che abbia il modello di dispositivo "Tracking controller" definito correttamente (come definito dal file [Tracking Controller.json](Modelli%20Azure/Tracking%20Controller.json)) e aver creato un dispositivo da associare al dispositivo.

## Configurazioni
Per utiizzare lo script è necessario modificare alcune variabili nel file [azure_tracking_controller.py](azure_tracking_controller.py) che sono l'input del programma:
- [Variabili connessione Azure](https://github.com/IDALab-unisalento/wot-project-part1-iotproject-preite-decarlo/blob/77245edcce3badb07878bc312a039b8f3c645c20/azure_tracking_controller.py#L16): fornire i dati di connessione reperibili dalla schermata di connessione dispositivo dall'applicazione Azure IoT Central;
- [Variabili del sensore di temperatura DHT](https://github.com/IDALab-unisalento/wot-project-part1-iotproject-preite-decarlo/blob/77245edcce3badb07878bc312a039b8f3c645c20/azure_tracking_controller.py#L33): fornire il modello del sensore DHT utilizzato ed il pin GPIO al quale è stato collegato sul raspberry.

## Utilizzo
Per eseguire è sufficiente eseguire con la corretta versione di Python lo script [azure_tracking_controller.py](azure_tracking_controller.py):
```
python3 azure_tracking_controller.py
```
Dato che spesso su Raspberry ci sono il comando `python` è riferito ad una versione 2.X è necessario usare `python3`.
Dopo l'avvio, se tutto è stato configurato correttamente, dovrebbero apparire messaggi che confermano la il provisioning del dispositivo e si dovrebbero inziare a vedere l'invio dei messaggi di telemetria al cloud Azure.
Per fermare l'esecuzione digitare `q` oppure `Q` e dare invio.


## File nel repository
Sono presenti i seguenti file:
- [Modelli Azure](Modelli%20Azure): cartella contenente i modelli in formato DTDL da importare nell'applicazione Azure IoT Central per creare correttamente il modello del dispositivo con il quale interagire;
- [azure_tracking_controller.py](azure_tracking_controller.py): script principale utilizzato per eseguire tutte le operazioni necessarie per la comunicazione con l'applicazione cloud di Azure IoT Central;
- [adafruit.py](adafruit.py): utilizzato per esporre la funzione “read_temperature_humidity” della libreria Adafruit, necessaria per la lettura delle misure effettuate dal sensore di temperatura utilizzato;
- [handlers.py](handlers.py): utilizzato per raccogliere le funzioni utilizzate per la gestione della ricezione dei comandi dall’applicazione cloud;
- [pnp_helper.py](pnp_helper.py): fornito da Microsoft, utilizzato per convertire gli oggetti creati tramite l’SDK Python in oggetti pronti all’invio all’applicazione cloud.
