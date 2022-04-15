# LIBRERIA PER INSERIMENTO GESTORI DI COMANDI RICEVUTI DA AZURE
async def reboot_handler(values):
    # Simula il riavvio del dispositivo dopo un certo numero di secondi passanti in input da interfaccia Azure)
    if values:
        print("Rebooting after delay of {delay} secs".format(delay=values))
    print("Done rebooting")
