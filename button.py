import streamlit as lit
import webbrowser
import subprocess
import time
import os


lit.title("Steamlit Button")


if lit.button("Run All Unit Tests"):
   lit.write("Running unit tests with coverage...")


   output_placeholder = lit.empty()


   process = subprocess.Popen(
       ["pytest", "tests/", "--cov=tasks", "--cov-report=term", "--cov-report=html:coverage_html"],
       stdout=subprocess.PIPE,
       stderr=subprocess.PIPE,
       text=True)
  
   full_output = ""
   for line in iter(process.stdout.readline, ''):
       if not line:
           break
       full_output += line
       output_placeholder.code(full_output)


   process.wait()


   if process.returncode == 0:
       lit.success("All tests were passed successfully!")
   else:
       lit.error("Tests have failed! Check output for details.")


   if os.path.exists("coverage_html/index.html"):
       lit.write(" ## Coverage Report")
       lit.write("Coverage report generated")
       lit.code(full_output.split("----")[-1] if "----" in full_output else "coverage not available")


       if lit.button("Open coverage report in browser"):
           try:
               webbrowser.open_new_tab(f"file://{os.path.abspath('coverage_html/index.html')}")
               lit.write("Opening browser..")
           except Exception as e:
               lit.error(f"Browser could not open: {e}")


       else:
           lit.warning("Coverage report not generated")
