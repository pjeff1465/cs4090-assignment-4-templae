import json
import os
from datetime import datetime

import streamlit as st


# File path for task storage
DEFAULT_TASKS_FILE = "tasks.json"

def load_tasks(file_path=DEFAULT_TASKS_FILE):
    """
    Load tasks from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file containing tasks
        
    Returns:
        list: List of task dictionaries, empty list if file doesn't exist
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        # Handle corrupted JSON file
        print(f"Warning: {file_path} contains invalid JSON. Creating new tasks list.")
        return []

def save_tasks(tasks, file_path=DEFAULT_TASKS_FILE):
    """
    Save tasks to a JSON file.
    
    Args:
        tasks (list): List of task dictionaries
        file_path (str): Path to save the JSON file
    """
    with open(file_path, "w") as f:
        json.dump(tasks, f, indent=2)

def generate_unique_id(tasks):
    """
    Generate a unique ID for a new task.
    
    Args:
        tasks (list): List of existing task dictionaries
        
    Returns:
        int: A unique ID for a new task
    """
    # save all tasks with id
    tasks_with_id = [task for task in tasks if isinstance(task.get("id"), int)]
    
    # assign no id task as 1
    if not tasks_with_id:
        return 1  
    
    # update all following tasks to make ids sequential
    return max(task["id"] for task in tasks_with_id) + 1 

def filter_tasks_by_priority(tasks, priority):
    """
    Filter tasks by priority level.
    
    Args:
        tasks (list): List of task dictionaries
        priority (str): Priority level to filter by (High, Medium, Low)
        
    Returns:
        list: Filtered list of tasks matching the priority
    """
    return [task for task in tasks if task.get("priority") == priority]

def filter_tasks_by_category(tasks, category):
    """
    Filter tasks by category.
    
    Args:
        tasks (list): List of task dictionaries
        category (str): Category to filter by
        
    Returns:
        list: Filtered list of tasks matching the category
    """
    return [task for task in tasks if task.get("category") == category]

def filter_tasks_by_completion(tasks, completed=True):
    """
    Filter tasks by completion status.
    
    Args:
        tasks (list): List of task dictionaries
        completed (bool): Completion status to filter by
        
    Returns:
        list: Filtered list of tasks matching the completion status
    """
    return [task for task in tasks if task.get("completed") == completed]

def search_tasks(tasks, query):
    """
    Search tasks by a text query in title and description.
    
    Args:
        tasks (list): List of task dictionaries
        query (str): Search query
        
    Returns:
        list: Filtered list of tasks matching the search query
    """
    query_str = str(query).lower()
    return [
        task for task in tasks 
        if query_str in str(task.get("title", "")).lower() or 
           query_str in str(task.get("description", "")).lower()
    ]

def get_overdue_tasks(tasks):
    """
    Get tasks that are past their due date and not completed.
    
    Args:
        tasks (list): List of task dictionaries
        
    Returns:
        list: List of overdue tasks
    """
    today = datetime.now().date() # get todays date to compare later
    overdue = []

    for task in tasks:
        if task.get("completed", False): # first check is not completed
            continue
        due_date_str = task.get("due_date", "") # strip due date from task as string
        
        if not due_date_str: # continue if no date
            print(f"Task has no due date, skipping task: {task}")
            continue

        try: 
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date() # check YYYY-MM-DD format
        except ValueError:
            try:
                due_date = datetime.strptime(due_date_str, "%m/%d/%Y").date() # check MM/DD/YYYY format
            except ValueError:
                try:
                    due_date = datetime.strptime(due_date_str, "%b %d, %Y").date() # check Month Day, Year format
                except ValueError:
                    continue
        
        if due_date < today: # if task overdue add to list
            overdue.append(task)

    return overdue 

def mark_task_complete(tasks, task_id):
    '''
    Mark task as complete by its ID

    Args:
        tasks (list): List of task stored as dictionary
        task_id (int): ID of the task to mark complete

    Returns:
        list: Updated list with given tasks marked as complete    

    '''

    found = False
    for task in tasks:
        if task.get("id") == task_id:
            task["completed"] = True
            found = True
            break

    if not found:
        st.warning(f"Task with ID {task_id} not found.")

    return tasks


def delete_task(tasks, task_id):
   '''
   delete a task by task ID

   Args:
       tasks (list): List of tasks stored as dictionary
       task_id (int): ID of the task to mark complete

   Returns:
       list: Updated list with given tasks deleted
   '''

   updated_tasks = [task for task in tasks if task.get("id") != task_id]

   for i, task in enumerate(updated_tasks, start=1):
       task["id"] = i

   return updated_tasks

def mark_task_incomplete(tasks, task_id):
    '''
    Mark task as incomplete by its ID

    Args:
        tasks (list): List of task stored as dictionary
        task_id (int): ID of the task to mark incomplete

    Returns:
        list: Updated list with given tasks marked as incomplete    

    '''

    found = False
    for task in tasks:
        if task.get("id") == task_id:
            task["completed"] = False
            found = True
            break

    if not found:
        st.warning(f"Task with ID {task_id} not found.")

    return tasks
