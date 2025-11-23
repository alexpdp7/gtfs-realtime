import dataclasses
import datetime
import pathlib

import gtfs_realtime_pb2


def all_files(path: pathlib.Path) -> list[pathlib.Path]:
    return sorted(path.glob("*/*/*/*"))


@dataclasses.dataclass
class DateMessage:
    date: datetime.datetime
    message: gtfs_realtime_pb2.FeedMessage


def parse(path: pathlib.Path) -> DateMessage:
    message = gtfs_realtime_pb2.FeedMessage()
    message.ParseFromString(path.read_bytes())
    return DateMessage(datetime.datetime.fromtimestamp(message.header.timestamp), message)


def parse_all_files(path: pathlib.Path) -> list[DateMessage]:
    return list(map(parse, all_files(path)))


@dataclasses.dataclass
class Stop:
    stop_id: str
    trip_id: str
    date: datetime.datetime


def first_stopped_ats(dms: list[DateMessage]):
    found = set()
    for dm in dms:
        date = dm.date
        for entity in dm.message.entity:
            vehicle = entity.vehicle
            if vehicle.current_status != vehicle.STOPPED_AT:
                continue
            key = vehicle.trip.trip_id, vehicle.stop_id
            if key in found:
                continue
            found.add(key)
            yield Stop(vehicle.stop_id, vehicle.trip.trip_id, date)
