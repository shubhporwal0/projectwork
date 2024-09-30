import os

# Get the path to the current project directory
project_dir = os.path.dirname(os.path.abspath(__file__))

# Generate the requirements.txt file using pip freeze
os.system(f'pip freeze > {project_dir}/requirements.txt')

print(f'requirements.txt file has been created in {project_dir}')
