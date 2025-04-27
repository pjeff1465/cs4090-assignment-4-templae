import pytest
import os
import json


from tasks import *
from datetime import datetime, timedelta


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

    print(f"New unqiue id: {unique_id}")

    assert unique_id == 3

def test_tdd_get_overdue_tasks_proper_date_parsing():
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    sample_data = [
       {"id": 1, "title": "load_task test (high)", "due_date": yesterday, "completed": False}, # should return overdue
       {"id": 2, "title": "save_tasks test (low)", "due_date": tomorrow, "completed": False}, # should NOT return overdue
       {"id": 3, "title": "(medium) ex task", "due_date": "01/01/2020", "completed": False}, # should return overdue
       {"id": 4, "title": "(high) ex task", "due_date": "yesterday", "completed": True}, # should NOT return overdue
       {"id": 5, "title": "(high) ex task", "due_date": "not a date", "completed": False}, # should NOT return overdue
       {"id": 6, "title": "(high) ex task", "completed": False} # no due date
    ]

    overdue_tasks = get_overdue_tasks(sample_data)

    print(f"Overdue tasks (should be task 1 and 3): {overdue_tasks}")
    assert len(overdue_tasks) == 2
    assert overdue_tasks[0]["id"] == 1
    assert overdue_tasks[1]["id"] == 3

def test_tdd_filter_tasks_by_completion():
    # order should 3, 4 are completed. 5 is empty 
    sample_data = [
        {"id": 1, "title": "load_task test (high)", "description": "pytest for load_task", "priority": "high", "category": "school", "due_date": "2025-05-05", "completed": False, "created_at": "2025-04-22 11:03:16"},
        {"id": 2, "title": "save_tasks test (low)", "description": "pytest for load_task", "priority": "low", "category": "school", "due_date": "05/03/2025", "completed": False, "created_at": "2025-04-22 11:03:16"},
        {"id": 3, "title": "(medium) ex task", "description": "medium priority", "priority": "medium", "category": "work", "due_date": "Apr 02, 2025", "completed": True, "created_at": "2025-04-22 08:03:16"},
        {"id": 4, "title": "(high) ex task", "description": "high priority", "priority": "high", "category": "work", "due_date": "No date", "completed": True, "created_at": "2025-04-22 08:03:16"},
        {"id": 5, "title": "load_task test (low)", "description": "pytest for load_task", "priority": "low", "category": "school", "due_date": "2025-05-01", "created_at": "2025-04-22 11:03:16"},  
    ]

    sorted_tasks = filter_tasks_by_completion(sample_data)

    print(f"\nCompleted Tasks: {sorted_tasks}")

    assert len(sorted_tasks) == 2
    assert sorted_tasks[0]["id"] == 3
    assert sorted_tasks[1]["id"] == 4  

# Test to make sure marking a task as complete is persistent
def test_tdd_mark_task_complete():
    sample_data = [
        {"id": 1, "description": "hw3", "completed": False},
        {"id": 2, "description": "Quantum hw", "completed": False}
    ]

    updated_tasks = mark_task_complete(sample_data, 2) # mark task 2 has complete

    assert updated_tasks[1]["completed"] is True

    assert updated_tasks[0]["completed"] is False

# delete task by unique id
def test_tdd_delete_task():
    sample_data = [
        {"id": 1, "description": "hw3", "completed": False},
        {"id": 2, "description": "Quantum hw", "completed": False}
    ]

    updated_tasks = delete_task(sample_data, 2)

    assert len(updated_tasks) == (len(sample_data) - 1)

# mark test as incomplete based on ID
def test_tdd_incomplete():
    sample_data = [
        {"id": 1, "description": "hw3", "completed": True},
        {"id": 2, "description": "Quantum hw", "completed": True},
        {"id": 3, "description": "hw3", "completed": False}
    ]

    updated_tasks = mark_task_incomplete(sample_data, 2)

    updated_tasks = mark_task_incomplete(sample_data, 1)

    print(f"\n{updated_tasks}")
    
    assert updated_tasks[0]["completed"] is False # task 1 is changed to incomplete

    assert updated_tasks[1]["completed"] is False # task 2 is changed to incomplete

    assert updated_tasks[2]["completed"] is False # task 3 is unchanged