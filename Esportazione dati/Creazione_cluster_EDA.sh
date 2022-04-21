# VARIABILI INPUT
clustername="preiteclustertest"
centralurlprefix="iot-preite-decarlo-tracciabilita"
databasename="preitedbtest"
location="westeurope"
resourcegroup="test"

# ESTENSIONE NECESSARIA PER ESECUZIONE
echo "Aggiunta estensione kusto"
az extension add -n kusto

# CREAZIONE GRUPPO DI RISORSE PER ARCHIVIAZIONE
echo "Creazione gruppo di risorse"
az group create --location $location \
    --name $resourcegroup

# CREAZIONE CLUSTER AZURE ESPLORA DATI
echo "Creazione cluster esplora dati"
az kusto cluster create --cluster-name $clustername \
    --sku name="Standard_D11_v2"  tier="Standard" \
    --enable-streaming-ingest=true \
    --enable-auto-stop=true \
    --resource-group $resourcegroup --location $location

# CREAZIONE DATABASE NEL CLUSTER
echo "Creazione database"
az kusto database create --cluster-name $clustername \
    --database-name $databasename \
    --read-write-database location=$location soft-delete-period=P365D hot-cache-period=P31D \
    --resource-group $resourcegroup


# CREAZIONE E ASSEGNAZIONE IDENTITA' GESTITA
# Creazione
echo "Creazione identità gestita"
MI_JSON=$(az iot central app identity assign --name $centralurlprefix \
    --resource-group IOTC --system-assigned)

## Assegnazione
echo "Assegnazione identità gestita"
az kusto database-principal-assignment create --cluster-name $clustername \
                                              --database-name $databasename \
                                              --principal-id $(jq -r .principalId <<< $MI_JSON) \
                                              --principal-assignment-name $centralurlprefix \
                                              --resource-group $resourcegroup \
                                              --principal-type App \
                                              --tenant-id $(jq -r .tenantId <<< $MI_JSON) \
                                              --role Admin

# STAMPA URL AZURE DATA EXPLORER
echo "Azure Data Explorer URL: $(az kusto cluster show --name $clustername --resource-group $resourcegroup --query uri -o tsv)"
