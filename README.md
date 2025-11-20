# `gtfs-realtime`

Many transit operators publish realtime information about vehicle positions.
You can find [realtime vehicle positions feeds at the Mobility Database](https://mobilitydatabase.org/feeds?gtfs_rt=true).

## Examining the data

Download `gtfs-realtime.proto`, which contains the data definition:

```
wget https://gtfs.org/documentation/realtime/gtfs-realtime.proto
```

Fetch the current status from the feed, decode the data, and print it.

```
curl https://gtfsrt.renfe.com/vehicle_positions.pb | protoc --decode=transit_realtime.FeedMessage gtfs-realtime.proto
```

## Collecting and querying data

This project contains `archiver.py` to collect and store data:

```
while true ; do ./archiver.py https://gtfsrt.renfe.com/vehicle_positions.pb out ; date ; done
```

`lib.py` contains functions to process the data.

The following Python code gets the trip times between Renfe's "MADRID-ATOCHA CERCANÍAS" and "ASAMBLEA DE MADRID-ENTREVÍAS":

```python
import itertools, pathlib, lib
ss = list(lib.first_stopped_ats(lib.parse_all_files(pathlib.Path("out"))))
atocha_stops = dict([(s.trip_id, s) for s in ss if s.stop_id == "18000"])
entrevias_stops = dict([(s.trip_id, s) for s in ss if s.stop_id == "70002"])
trips = [(atocha_stop, entrevias_stop) for trip_id, entrevias_stop in entrevias_stops.items() for trip_id2, atocha_stop in atocha_stops.items() if trip_id == trip_id2 and atocha_stop.date < entrevias_stop.date]
print("\n".join([f"{atocha_stop.date} >> {entrevias_stop.date.time()} travel: {entrevias_stop.date - atocha_stop.date} stop from previous {entrevias_stop.date - previous_entrevias_stop.date}" for ((previous_atocha_stop, previous_entrevias_stop), (atocha_stop, entrevias_stop)) in itertools.pairwise(trips)]))
```

(You can find the stop identifiers [here](https://data.renfe.com/dataset/estaciones-listado-completo "Complete list of Renfe train stops").)

## Alternatives

* https://transsee.ca/ (paid service, can add custom feeds)
