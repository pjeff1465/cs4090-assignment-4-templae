import pytest
from tasks import generate_unique_id
# Test complex interactions
# test multiple features together
# add task, load it, check if it appears in filters
# Integration level


# test edge cases of unqiue id
# what will it do if id numbers are somehow not sequential?
# what will it do if input is empty list?
def test_edge_generate_unique_id():
   assert generate_unique_id([]) == 1 # empty list should return 1


   sample_data = [
       {"id": 1, "title": "Quantum hw"},
       {"id": 6, "title": "Capstone hw4"}
   ]


   assert generate_unique_id(sample_data) == 7
   # both tests pass