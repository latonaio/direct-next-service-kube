# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

import os
from time import sleep

import simplejson as json
from aion.logger import lprint
from aion.microservice import main_decorator, Options
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

SERVICE_NAME = "direct-next-service"
EXECUTE_INTERVAL = 1
METADATA_KEY = "device_list"


def getext(filename):
    return os.path.splitext(filename)[-1].lower()


def open_json_file(path):
    try:
        with open(path, "r") as f:
            data = json.load(f)
        os.remove(path)
    except json.JSONDecodeError:
        lprint("json file cant decode : + " + path)
        os.remove(path)
        return None
    except FileNotFoundError:
        lprint("json file is not exists : " + path)
        return None

    if not isinstance(data.get("connections"), dict):
        lprint("connection is not set : " + path)
        return None

    return data


class ChangeHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if getext(event.src_path) in ('.json', '.json', '.json'):
            self.direct_next_service(event.src_path)

    def direct_next_service(self, path):
        data = open_json_file(path)
        if data is None:
            return

        connections = data.get("connections")
        if connections is None:
            lprint("error: connections is None")
            return

        for connection_key, connection in connections.items():
            output_data_path = connection["outputDataPath"]
            if output_data_path is None:
                lprint("error: output_data_path is None")
                return
            metadata = connection["metadata"] if connection["metadata"] is not None else dict()
            device_name = connection.get("deviceName") if connection.get("deviceName") else None
            file_list = connection.get("fileList") if connection.get("fileList") else None
            if device_name is None:
                self.conn.output_kanban(
                    result=True,
                    connection_key=connection_key,
                    output_data_path=output_data_path,
                    metadata=metadata,
                    file_list=file_list,
                )
                lprint("send to same device")
                continue

            lprint("send to other device: ", device_name)
            self.conn.output_kanban(
                result=True,
                connection_key=connection_key,
                output_data_path=output_data_path,
                metadata=metadata,
                device_name=device_name,
                file_list=file_list,
                process_number = 1,
            )

        lprint(">>>finish")

    def __init__(self, conn, num):
        self.conn = conn
        self.num = num

    def __del__(self):
        del self.status_obj


@main_decorator(SERVICE_NAME)
def main(opt: Options):
    conn = opt.get_conn()
    num = opt.get_number()
    # get cache kanban
    kanban = conn.set_kanban(SERVICE_NAME, num)
    data_dir = kanban.get_data_path()
    os.makedirs(data_dir, exist_ok=True)
    lprint("watching: " + data_dir)

    event_handler = ChangeHandler(conn, num)
    observer = Observer()
    observer.schedule(event_handler, data_dir, recursive=True)
    observer.start()
    try:
        while True:
            sleep(EXECUTE_INTERVAL)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    del event_handler
