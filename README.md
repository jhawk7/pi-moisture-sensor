# Pi Moisture Sensor ![Raspberry Pi](https://img.shields.io/badge/-Raspberry_Pi-C51A4A?style=for-the-badge&logo=Raspberry-Pi) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white) ![Grafana](https://img.shields.io/badge/grafana-%23F46800.svg?style=for-the-badge&logo=grafana&logoColor=white)
Raspberry Pi Moisture Sensor w/ OpenTelemetry Reporting

This project uses a [capacative soil moisture sensor](https://www.amazon.com/AITRIP-Capacitive-Corrosion-Resistant-Electronic/dp/B094J8XD83/ref=asc_df_B094J8XD83?mcid=f36789f1b52d313ca55c0ddd806aee81&hvocijid=11206063840108402844-B094J8XD83-&hvexpln=73&tag=hyprod-20&linkCode=df0&hvadid=721245378154&hvpos=&hvnetw=g&hvrand=11206063840108402844&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9010835&hvtargid=pla-2281435177858&th=1) to calculate the moisture percentage of the soil and publishes that metric, along with a message if the soil needs to be watered, to an `MQTT Server` to be processes by an [MQTT subscriber client](https://github.com/jhawk7/mqtt-sub-client) that will send alerts and forward metrics to a `prometheus backend`. Te data from the prometheus instance is collected in visualized via `grafana` to keep track of the plants watering cycles.

## Local Development (pi-zero only)
* install `pyenv`, use python 3.9.2 `pyenv install 3.9.2` and set it to be global or local `pyenv local 3.9.2`
* install `pipenv` with `pip3 install pipenv`
* create requirements.txt file with `pipenv run pip freeze > requirements.txt`
