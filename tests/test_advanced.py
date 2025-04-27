import pytest
from tasks import *
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

   unique_id = generate_unique_id(sample_data)
   print(f"Next unqiue id: {unique_id}")
   
   assert unique_id == 7
   # both tests pass

# test for get overdue task but with invalid date format
def test_edge_get_overdue_task():
    # different date formats, 1=correct, 2=MM/DD/YYYY, 3- Month Day, Year, 4='Not a date'
    sample_data = [
       {"id": 1, "title": "load_task test (high)", "description": "pytest for load_task", "priority": "high", "category": "school", "due_date": "2025-01-01", "completed": False, "created_at": "2024-04-22 11:03:16"},
       {"id": 2, "title": "save_tasks test (low)", "description": "pytest for load_task", "priority": "low", "category": "school", "due_date": "01/01/2025", "completed": False, "created_at": "2024-04-22 11:03:16"},
       {"id": 3, "title": "(medium) ex task", "description": "medium priority", "priority": "medium", "category": "work", "due_date": "Apr 1, 2025", "completed": False, "created_at": "2024-04-22 08:03:16"},
       {"id": 4, "title": "(high) ex task", "description": "high priority", "priority": "high", "category": "work", "due_date": "Not a date", "completed": False, "created_at": "2024-04-22 08:03:16"}
    ]

    overdue_tasks = get_overdue_tasks(sample_data)

    print(overdue_tasks)

    assert len(overdue_tasks) == 3
   
# mark task complete that does not exist
def test_edge_mark_complete():
   sample_data = [
         {"id": 1, "title": "Task 1", "description": "pytest for load_task", "completed": False}
   ]

   updated_tasks = mark_task_complete(sample_data, task_id=1313)

   print(f"\nUpdated Task: {updated_tasks}")

   assert sample_data == updated_tasks 
   # expecte no change if id doesnt exist

# Test handling of non-string search query
def test_search_tasks_non_string():
   """Test if search_tasks handles non-string queries properly."""
   tasks = [
      {"id": 1, "title": "Task 1", "description": "Description 1"},
      {"id": 2, "title": "Task 2", "description": "Description 2"}
   ]

   result = search_tasks(tasks, 1)
   assert len(result) == 1
   assert result[0]["id"] == 1


# tests for complete/incomplete to raise error if no task with ID found

def test_mark_task_complete_bad_id():
   sample_data = [{"id": 1, "completed": False}]

   mark_task_complete(sample_data, 13)

   assert all(not task["completed"] for task in sample_data)

def test_mark_task_incomplete_bad_id():
   sample_data = [{"id": 1, "completed": True}]

   mark_task_incomplete(sample_data, 13)

   assert all(task["completed"] for task in sample_data)

def test_edge_updated_id():
   sample_data = [
      {"id": 1, "title": "load_task test (high)", "description": "pytest for load_task", "priority": "high", "category": "school", "due_date": "2025-01-01", "completed": False, "created_at": "2024-04-22 11:03:16"},
      {"id": 2, "title": "save_tasks test (low)", "description": "pytest for load_task", "priority": "low", "category": "school", "due_date": "01/01/2025", "completed": False, "created_at": "2024-04-22 11:03:16"},
      {"id": 3, "title": "(medium) ex task", "description": "medium priority", "priority": "medium", "category": "work", "due_date": "Apr 1, 2025", "completed": False, "created_at": "2024-04-22 08:03:16"},
      {"id": 4, "title": "(high) ex task", "description": "high priority", "priority": "high", "category": "work", "due_date": "Not a date", "completed": False, "created_at": "2024-04-22 08:03:16"}
   ]
   # delete task 2 and update 3, 4 ids to -1

   updated_tasks = delete_task(sample_data, 2) # delete task 2

   #print(f"task 2 id == " u)
   assert (len(sample_data) - 1) == len(updated_tasks)

   assert updated_tasks[1]["id"] == 2 # since task 2 was deleted task with id 3 should move to spot 2 in list

   assert updated_tasks[2]["id"] == 3 # task id 4 should change to id 3