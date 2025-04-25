import pytest
import os
import json


from tasks import generate_unique_id, save_tasks
from datetime import datetime


# TDD = test-driven development
# write the test before the actual function exists
# fail test -> write code -> pass




# generate new id, returns NEXT unique ID based on exisiting ones
def test_tdd_generate_new_id():
   sample_data = [
       {"id": 1, "title": "load_task test (high)"},
       {"id": 2, "title": "save_tasks test (low)"}
   ]


   unique_id = generate_unique_id(sample_data)


   assert unique_id == 3
