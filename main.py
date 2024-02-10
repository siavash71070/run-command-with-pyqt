import sys

from PyQt5.QtWidgets import QApplication

from RunCommand.run_command_presenter import RunCommandPresenter


class MainWindow:
    def __init__(self):
        self.command_runner = RunCommandPresenter()

    def run(self):
        self.command_runner.show_window()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.run()
    app.exec_()
