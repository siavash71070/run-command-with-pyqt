import os
import subprocess
import threading

from RunCommand.run_command_view import RunCommandView


class RunCommandPresenter:
    def __init__(self):
        self.view = RunCommandView()
        self.current_path = '/'  # Default current path
        self.connections()
        self.start_path_check_thread()
        self.view.set_result_label("")

    def show_window(self):
        self.view.show_dialog()

    def connections(self):
        self.view.get_run_button().clicked.connect(self.run_command)
        self.view.get_path_button().clicked.connect(self.get_current_path)

    def update_path_label(self):
        self.view.set_path_label(f'Current Path: {self.current_path}')

    def get_current_path(self):
        new_path = self.view.get_path_line_edit()
        self.view.set_result_label("")

        address_mapping = self.map_input_path()

        # Check if the provided address is in the mapping
        if new_path in address_mapping:
            self.current_path = address_mapping[new_path]
            self.update_path_label()
        else:
            # Continue with the rest of the logic for handling valid addresses
            if '/' in new_path and '..' not in new_path:
                path_parts = new_path.split(':')
                if len(path_parts) > 1:
                    self.current_path = path_parts[1]
                else:
                    self.current_path = os.path.abspath(os.path.expanduser(new_path))

                if self.is_valid_directory(self.current_path):
                    self.update_path_label()
                else:
                    self.view.set_result_label(f"Error: Path '{self.current_path}' does not exist.")
            else:
                self.view.set_result_label("Error: Invalid path format.")

    def is_valid_directory(self, path):
        for p in path:
            if p in self.map_input_path():
                return True
            else:
                return False
        return bool(path)

    def run_command(self):
        command = self.view.get_command_line_edit()
        result = self.execute_command(command, self.current_path)
        self.view.set_result_label(result)

    @staticmethod
    def execute_command(command, working_directory):
        try:
            expanded_path = os.path.expanduser(working_directory)

            # Check if the specified path exists before executing the command
            if not os.path.exists(expanded_path):
                return f"Error: Path '{expanded_path}' does not exist."

            if isinstance(command, str):
                # If command is a string, use shell=True
                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True,
                                                 cwd=expanded_path)
            elif isinstance(command, list):
                # If command is a list, use shell=False
                result = subprocess.check_output(command, shell=False, stderr=subprocess.STDOUT, text=True,
                                                 cwd=expanded_path)
            else:
                raise ValueError("Invalid command type. Use a string or a list.")

            return result
        except subprocess.CalledProcessError as e:
            return f"Error: {e.output}"

    @staticmethod
    def map_input_path():
        # Mapping of user-friendly names to their corresponding system paths
        address_mapping = {
            'Desktop': os.path.join(os.path.expanduser('~'), 'Desktop'),
            'Documents': os.path.join(os.path.expanduser('~'), 'Documents'),
            'Downloads': os.path.join(os.path.expanduser('~'), 'Downloads'),
            'Pictures': os.path.join(os.path.expanduser('~'), 'Pictures'),
            'Music': os.path.join(os.path.expanduser('~'), 'Music'),
            'Videos': os.path.join(os.path.expanduser('~'), 'Videos'),
        }
        return address_mapping

    def start_path_check_thread(self):
        path_check_thread = threading.Thread(target=self.path_check_thread, daemon=True)
        path_check_thread.start()

    def path_check_thread(self):
        while True:
            try:
                if self.current_path == "/":
                    self.current_path = os.getcwd()
                    self.view.set_path_label(f'Current Path: {self.current_path}')
                    # Add a sleep to avoid constant checking
                    threading.Event().wait(1)
            except:
                pass
