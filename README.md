# DataDog & Akamai Custom Integration

Akamai has an out of the box solution that integrates with DataDog called [DataStream](https://www.akamai.com/products/datastream). However, sometimes a more custom approach is needed based on different use cases such as aggregated metrics from real-time Akamai's Media Delivery Reports for [AMD](https://www.akamai.com/products/adaptive-media-delivery).

The purpose of this Python script is to collect metrics by running API calls to Akamai's Media Delivery Reports for AMD (any other API endpoint for any other product can be used) and send them to DataDog by using their agent. 

## Requirements
1. Akamai API credentials with all the required access
2. Datadog account with access to metrics and logs
3. [Datadog Agent](https://docs.datadoghq.com/agent/) installed and configured
4. Python and all the dependencies

## Datadog Agent
The Datadog Agent is a software that runs on any host. It collects logs, events and metrics from the host and sends them to Datadog. 
We use the Agent in this integration to forward the metrics obtained from the Akamai API response to Datadog’s “Metrics” endpoint.
The usage of the Agent also ensures that the integration will include built-in resilience techniques to connect to the Datadog endpoint. [More information available here](https://docs.datadoghq.com/agent/)

## Datadog Metrics Endpoint
The metrics end-point allows you to post time-series data that can be graphed on Datadog’s dashboards.
It is expected that all the metrics available with the Akamai Media Delivery API’s will be tagged and posted to the metrics endpoint for building "Dashboards" for visualization. [More information available here](https://docs.datadoghq.com/api/latest/metrics/)

## Datadog Logs Endpoint
Additionally, it is highly recommended to format and save the API responses for logging. The logs end-point allows you to post logs which can be monitored in the Datadog Dashboards. [More information here](https://docs.datadoghq.com/logs/log_collection/?tabs=host)


## Configuration (Specific to the Media Reporting API)
1. Edit the cpcodes variable value to your own. The type of the value must be an array. For example:
```
    cpcodes = ["00000", "11111"]
```
2. Edit the dimension and metrics IDs by modifying the `dimensions` and `metrics` variable values.


## Cron Job
You want the metrics to be collected periodically. For AMD's Media Delivery Report the maximum granularity if 5 minutes. Therefore a cron job that runs every 5 minutes must be installed.
```
*/5 * * * * /apps/datadog-akamai-metrics-and-logs.py
```