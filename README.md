![NOTIFIER](./docs/notifier_logo.png)
# NOTIFIER - Earthquake Precursors Alerting Framework

Python flask application that constantly scans data for thresholds values and sends an alert as an email.

This service is part of our [Earthquake Data Assimilation System](https://github.com/encresearch/data-assimilation-system).

## API Overview
Notifier works by recieving JSON Objects in the following structure:
~~~
{
  'topic': ____,
  'location': ____,
  'time_init: ____',
  'time_duration': ____
}
~~~
With this object, Notifier queries a database containing subscribers (and the topics they are subscribed to), and sends an email to the subscribers of the respective topic specified in the JSON objecct. The other information in the JSON Object is included in the email.

Notifier will recieve its data from the Inspector container (once it is operational) over MQTT.


## Getting Started
These instructions are to get notifier up and running in your local development environment.

### Install and Run Locally

Pending.

**Run Locally**

Pending.

**Run Local Tests**

Pending.


## Contributing
Pull requests and stars are always welcome. To contribute, please fetch, create an issue explaining the bug or feature request, create a branch off this issue and submit a pull request.
