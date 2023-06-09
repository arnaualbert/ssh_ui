from flask import Flask, render_template, request
import paramiko

app = Flask(__name__)

def get_folder_contents(path):
    # SSH connection details
    hostname = '************'
    port = 22
    username = '************'
    password = '***********'

    # Establish SSH connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)

    # Execute command to list folder contents
    _, folders, _ = ssh.exec_command(f'ls -l {path}')

    # Read the output of the command
    folder_list = folders.read().decode('utf-8').splitlines()

    # Close the SSH connection
    ssh.close()

    return folder_list

@app.route('/', methods=['GET', 'POST'])
def index():
    path = '/'
    if 'path' in request.args:
        path = request.args['path']
        if path.startswith('//'):
            path = path[1:] 
    folder_list = get_folder_contents(path)

    if request.method == 'POST':
        selected_file = request.form.get('file')
        if selected_file:
            file_path = path + '/' + selected_file
            if file_path.startswith('//'):
                file_path = file_path[1:]  # Remove duplicate slash
            return f"Selected file path: {file_path}"


        button_clicked = request.form.get('get_files_button')
        if button_clicked:
            file_paths = []
            for folder in folder_list:
                if not folder.startswith('d'):  # Check if it's a file
                    folder_items = folder.split()
                    if len(folder_items) >= 9:
                        file_paths.append(path + '/' + folder_items[8])
            if len(file_paths) > 1:
                return "<br>".join(file_paths)  # Return the file paths with line breaks
    return render_template('index.html', path=path, folders=folder_list)

if __name__ == '__main__':
    app.run()
