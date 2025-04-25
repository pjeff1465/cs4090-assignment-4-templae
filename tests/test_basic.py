import pytest
import json
import os


from datetime import datetime, timedelta
from tasks import *


# test if tasks correctly loads from JSON
# Unit tests
# Does function handle known input correctly?


def test_load_tasks(tmp_path):
   sample_data = [
       {"id": 1, "title": "load_task test", "description": "pytest for load_task", "priority": "high", "category": "school", "due_date": "2025-05-27", "completed": False, "created_at": "2025-04-22 11:03:16"},
       {"id": 2, "title": "invalid JSON"}
   ]


   test_file = tmp_path / "test_tasks.json"
   with open(test_file, "w") as j:
       json.dump(sample_data, j)


   result = load_tasks(file_path=str(test_file))


   assert result == sample_data


   # test empty JSON file
   result = load_tasks("nonexistent_file.json")
   assert result == []


   # test corrupt JSON
   bad_file = tmp_path / "bad.json"
   bad_file.write_text("{ not valid json }")


   assert load_tasks(str(bad_file)) == []


# test function that saves tasks
def test_save_tasks(tmp_path):
   sample_data = [
       {"id": 1, "title": "save_tasks test", "description": "pytest for load_task", "priority": "high", "category": "school", "due_date": "2025-05-27", "completed": False, "created_at": "2025-04-22 11:03:16"}
   ]


   test_file = tmp_path / "save_test.json"


   save_tasks(sample_data, str(test_file))


   assert os.path.exists(test_file)


   with open(test_file, "r") as f:
       loaded_data = json.load(f)


   assert loaded_data == sample_data
  
   # check for unique ID
   # if no tasks result 1
   assert generate_unique_id([]) == 1


   # if task check for unique ID
   assert generate_unique_id(sample_data) == 2
  
# test function that filters tasks by priority
def test_filter_tasks_by_priority(tmp_path):
   sample_data = [
       {"id": 1, "title": "load_task test (high)", "description": "pytest for load_task", "priority": "high", "category": "school", "due_date": "2025-05-27", "completed": False, "created_at": "2025-04-22 11:03:16"},
       {"id": 2, "title": "save_tasks test (low)", "description": "pytest for load_task", "priority": "low", "category": "school", "due_date": "2025-05-27", "completed": False, "created_at": "2025-04-22 11:03:16"},
       {"id": 3, "title": "(medium) ex task", "description": "medium priority", "priority": "medium", "category": "work", "due_date": "2025-04-20", "completed": True, "created_at": "2025-04-22 08:03:16"},
       {"id": 4, "title": "(high) ex task", "description": "high priority", "priority": "high", "category": "work", "due_date": "2025-04-20", "completed": True, "created_at": "2025-04-22 08:03:16"},
       {"id": 5, "title": "load_task test (low)", "description": "pytest for load_task", "priority": "low", "category": "school", "due_date": "2025-05-27", "completed": False, "created_at": "2025-04-22 11:03:16"},  
   ]


   # filter by high priority
   high_priority = filter_tasks_by_priority(sample_data, "high")
   assert len(high_priority) == 2 # hard code check for 2 high priority tasks
   assert all(task["priority"] == "high" for task in high_priority)


   # filter by medium priority
   medium_priority = filter_tasks_by_priority(sample_data, "medium")
   assert len(medium_priority) == 1
   assert medium_priority[0]["priority"] == "medium"


   # filter by low priority
   low_priority = filter_tasks_by_priority(sample_data, "low")
   assert len(low_priority) == 2
   assert low_priority[0]["priority"] == "low"


   no_priority = filter_tasks_by_priority(sample_data, "critical")
   assert len(no_priority) == 0


# test function to search_tasks
def test_search_tasks(tmp_path):
   sample_data = [
       {"id": 1, "title": "CS4090 hw3", "description": "pytest for load_task", "priority": "high", "category": "school", "due_date": "2025-05-27", "completed": False, "created_at": "2025-04-22 11:03:16"},
       {"id": 2, "title": "finish code", "description": "search by description", "priority": "low", "category": "school", "due_date": "2025-05-27", "completed": False, "created_at": "2025-04-22 11:03:16"},
       {"id": 3, "title": "CS5001", "description": "finish hw3", "priority": "medium", "category": "work", "due_date": "2025-04-20", "completed": True, "created_at": "2025-04-22 08:03:16"},
       {"id": 4, "title": "chores", "description": "clean room", "priority": "high", "category": "work", "due_date": "2025-04-20", "completed": True, "created_at": "2025-04-22 08:03:16"},
   ]


   # search tasks by title
   title_results = search_tasks(sample_data, "CS4090")
   assert len(title_results) == 1
   assert title_results[0]["id"] == 1


   # Test search in description
   desc_results = search_tasks(sample_data, "room")
   assert len(desc_results) == 1
   assert desc_results[0]["id"] == 4


  # Test search matching multiple tasks
   multi_results = search_tasks(sample_data, "hw3")
   assert len(multi_results) == 2
   assert sorted([task["id"] for task in multi_results]) == [1, 3]
 
   # Test case insensitive search
   case_results = search_tasks(sample_data, "CODE")
   assert len(case_results) == 1
   assert case_results[0]["id"] == 2


   # Test no results
   no_results = search_tasks(sample_data, "project")
   assert len(no_results) == 0


# test function for getting overdue tasks
def test_get_overdue_tasks(tmp_path):


   # Get current date for testing
   today = datetime.now().strftime("%Y-%m-%d")
   yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
   tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
  
   # Create sample tasks with different due dates
   sample_tasks = [
       {"id": 1, "title": "overdue task", "description": "task already due", "priority": "high", "due_date": yesterday, "completed": False},
       {"id": 2, "title": "current task", "description": "task is due today", "priority": "medium", "due_date": today, "completed": False},
       {"id": 3, "title": "future task", "description": "task is not due yet", "priority": "low", "due_date": tomorrow, "completed": False},
       {"id": 4, "title": "completed overdue", "description": "task is overdue but completed", "priority": "high", "due_date": yesterday, "completed": True}
   ]
  
   # Test getting overdue tasks
   overdue = get_overdue_tasks(sample_tasks)
  
   # Should only include task #1 (overdue and not completed)
   assert len(overdue) == 1
   assert overdue[0]["id"] == 1
   assert overdue[0]["due_date"] == yesterday
   assert overdue[0]["completed"] is False
