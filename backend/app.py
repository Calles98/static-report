from flask import Flask, request, send_file, render_template
import os 
from flask_cors import CORS
import subprocess
import shutil 

PYTHON_PATH = os.getenv("PYTHON_ENV_PATH", "/Users/josecalles/Desktop/IMEx_Projects/Report-App/backend/venv/bin/python3")

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'analysisType' not in request.form:
        return "Missing file or analysis type", 400
    
    file = request.files['file']
    filename = request.form['filename']
    analysis_type = request.form['analysisType']
    
    
    if not file or filename == '':
        return 'No selected file', 400
    
    if file and file.filename != '':
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
    # Notebook to proecess
    notebook_filename = select_notebook(analysis_type)
    
    # Call Jupyter notebook processing function 
    result_filepath = process_notebook(filepath, filename, notebook_filename)
    
    return send_file(result_filepath, as_attachment=True)

def select_notebook(type): 
    notebook_mapping = {
        'aba': 'Notebooks/aba2_notebook.ipynb',
        'boxes': 'Notebooks/boxes_notebook.ipynb',
        'elemental': 'Notebooks/elemental_notebook.ipynb'
    }
    return notebook_mapping.get(type, 'Notebooks/default_notebook.ipynb')

def process_notebook(filepath, filename, notebook_filename):
    result_html = os.path.join(RESULT_FOLDER, 'report.html')
    temp_notebook = 'temp_notebook.ipynb'

    print(result_html)

    # Copy the selected notebook to a temporary file to modify
    shutil.copy(notebook_filename, temp_notebook)

    # Open and modify the notebook to include the file path
    with open(temp_notebook, 'r') as file:
        notebook_content = file.read()

    # Update the notebook content with the file path
    notebook_content = notebook_content.replace('FILE_PATH_PLACEHOLDER', filepath)
    notebook_content = notebook_content.replace('FILE_NAME', filename)


    with open(temp_notebook, 'w') as file:
        file.write(notebook_content)

    # Run the Jupyter notebook with the updated file path
    #command = f'{PYTHON_PATH} -m jupyter nbconvert --to html --no-input --execute --output {result_pdf} {temp_notebook}'
    command = f"{PYTHON_PATH} -m jupyter nbconvert --to html --execute --ExecutePreprocessor.kernel_name=flask_env  --no-input --output {result_html} {temp_notebook}"
   
    print("Running command:", command)  # Debug print statement
    subprocess.run(command, shell=True, check=True)
    
    # Clean up
    os.remove(temp_notebook)
    
    return result_html
    
    
            
if __name__ == '__main__':
    app.run(debug=True)
        
    
    
    
