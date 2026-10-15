#!/usr/bin/env python3

import sys

current_key = None
employees = []
departments = []


def emit_join():
    for emp_id, name in employees:
        for dept_name in departments:
            print(f"{emp_id}\t{name}\t{dept_name}")


for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    key, value = line.split("\t", 1)

    if current_key is not None and key != current_key:
        emit_join()
        employees = []
        departments = []

    current_key = key

    parts = value.split(",")

    if parts[0] == "E":
        employees.append((parts[1], parts[2]))

    elif parts[0] == "D":
        departments.append(parts[1])


if current_key is not None:
    emit_join()