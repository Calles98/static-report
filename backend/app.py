from flask import Flask, request, send_file, render_template
import os 
from flask_cors import CORS
import subprocess
import shutil 

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
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    
    if not file or file.filename == '':
        return 'No selected file', 400
    
    if file and file.filename != '':
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
    # Notebook to proecess
    notebook_filename = select_notebook(request.form.get('type'))
    
    # Call Jupyter notebook processing function 
    result_filepath = process_notebook(filepath, notebook_filename)
    
    return send_file(result_filepath, as_attachment=True)

def select_notebook(type): 
    notebook_mapping = {
        'aba': 'Notebooks/aba2_notebook.ipynb',
        'boxes': 'Notebooks/boxes_notebook.ipynb',
        'elemental': 'Notebooks/elemental_notebook.ipynb'
    }
    return notebook_mapping.get(type, 'Notebooks/default_notebook.ipynb')

def process_notebook(filepath, notebook_filename):
    result_html = os.path.join(RESULT_FOLDER, 'report.html')
    temp_notebook = 'temp_notebook.ipynb'
    
    # Copy the original notebook to a temporay file
    shutil.copy(notebook_filename, temp_notebook)
    
    # open and modify the notebook to include the filepath
    with open(temp_notebook, 'r') as file: 
        notebook_content = file.read()
        
    # Update the notebook conten with the file path
    filepath_str = repr(filepath) # to ensure proper string formatting
    print("file paths to insert into noteboook", filepath_str)
    notebook_content = notebook_content.replace('FILEPATH_PLACEHOLDER', filepath_str)
    
    with open(temp_notebook, 'w') as file:
        file.write(notebook_content)
        
    # Run the Jupyter notebook with the updated file path
    command = f'jupyter nbconvert --to html --no-input --execute --output {result_html} {temp_notebook}'
    print("Running command:", command)  # Debug print statement
    subprocess.run(command, shell=True, check=True)
    
    # Clean up
    os.remove(temp_notebook)
    
    return result_html
    
    
            
if __name__ == '__main__':
    app.run(debug=True)
        
    
    
    
