import sys
import os
import stat


python_exec_path = sys.executable

with open("tedge_cli.py", "r") as file_ptr:
    content = file_ptr.read()

content = f"#!{python_exec_path}\n" + content

with open("tedge_cli", "w") as file_ptr:
    file_ptr.write(content)

st = os.stat('tedge_cli')
os.chmod('tedge_cli', st.st_mode | stat.S_IEXEC)

