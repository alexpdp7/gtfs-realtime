```
wget https://gtfs.org/documentation/realtime/gtfs-realtime.proto
```

```
curl https://gtfsrt.renfe.com/vehicle_positions.pb | protoc --decode=transit_realtime.FeedMessage gtfs-realtime.proto
```
