import streamlit as st
import pandas as pd
import subprocess
import webbrowser
import os


from datetime import datetime
from src.tasks import load_tasks, save_tasks, filter_tasks_by_priority, filter_tasks_by_category


def main():
   st.title("To-Do Application")
  
   # Load existing tasks
   tasks = load_tasks()
  
   # Sidebar for adding new tasks
   st.sidebar.header("Add New Task")
  
   # Task creation form
   with st.sidebar.form("new_task_form"):
       task_title = st.text_input("Task Title")
       task_description = st.text_area("Description")
       task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
       task_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"])
       task_due_date = st.date_input("Due Date")
       submit_button = st.form_submit_button("Add Task")
      
       if submit_button and task_title:
           new_task = {
               "id": len(tasks) + 1,
               "title": task_title,
               "description": task_description,
               "priority": task_priority,
               "category": task_category,
               "due_date": task_due_date.strftime("%Y-%m-%d"),
               "completed": False,
               "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           }
           tasks.append(new_task)
           save_tasks(tasks)
           st.sidebar.success("Task added successfully!")
  
   # Main area to display tasks
   st.header("Your Tasks")
  
   # Filter options
   col1, col2 = st.columns(2)
   with col1:
       filter_category = st.selectbox("Filter by Category", ["All"] + list(set([task["category"] for task in tasks])))
   with col2:
       filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
  
   show_completed = st.checkbox("Show Completed Tasks")
  
   # Apply filters
   filtered_tasks = tasks.copy()
   if filter_category != "All":
       filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
   if filter_priority != "All":
       filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
   if not show_completed:
       filtered_tasks = [task for task in filtered_tasks if not task["completed"]]
  
   # Display tasks
   for task in filtered_tasks:
       col1, col2 = st.columns([4, 1])
       with col1:
           if task["completed"]:
               st.markdown(f"~~**{task['title']}**~~")
           else:
               st.markdown(f"**{task['title']}**")
           st.write(task["description"])
           st.caption(f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}")
       with col2:
           if st.button("Complete" if not task["completed"] else "Undo", key=f"complete_{task['id']}"):
               for t in tasks:
                   if t["id"] == task["id"]:
                       t["completed"] = not t["completed"]
                       save_tasks(tasks)
                       st.rerun()
           if st.button("Delete", key=f"delete_{task['id']}"):
               tasks = [t for t in tasks if t["id"] != task["id"]]
               save_tasks(tasks)
               st.rerun()


   st.sidebar.divider()
   st.sidebar.header("Developer Tools")
  
   if st.sidebar.button("Run Unit Tests"):
       with st.spinner("Running tests with coverage.."):
           process = subprocess.Popen(
               ["pytest", "tests/", "--cov=tasks", "--cov-report=term", "--cov-report=html:coverage_html"],
               stdout=subprocess.PIPE,
               stderr=subprocess.PIPE,
               text=True
           )
           stdout, stderr = process.communicate()
           combined_output = stdout + stderr


           with st.expander("Test Results", expanded = True):
               st.code(combined_output)


               if process.returncode == 0:
                   st.success("All tests passed successfully!")
               else:
                   st.error("Some tests failed! Check output for details.")


               if os.path.exists("coverage_html/index.html"):
                   st.write("## Coverage Report")
                   try:
                       coverage_line = [line for line in combined_output.split('\n') if "TOTAL" in line][0]
                       coverage_percentage = coverage_line.split()[-1]
                       st.metric("Code Coverage", coverage_percentage)
                   except:
                       st.write("Coverage data not available")
                  
                   # Button to open in browser
                   if st.button("Open Coverage Report"):
                       try:
                           webbrowser.open_new_tab(f"file://{os.path.abspath('coverage_html/index.html')}")
                       except Exception as e:
                           st.error(f"Could not open browser: {e}")
               else:
                   st.warning("Coverage report not generated.")                     
          
if __name__ == "__main__":
   main()
