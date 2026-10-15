#!/usr/bin/env python3

import sys

for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    fields = line.split(",")

    if len(fields) == 3:
        # Employee: emp_id,name,dept_id
        emp_id, name, dept_id = fields
        print(f"{dept_id}\tE,{emp_id},{name}")

    elif len(fields) == 2:
        # Department: dept_id,dept_name
        dept_id, dept_name = fields
        print(f"{dept_id}\tD,{dept_name}")