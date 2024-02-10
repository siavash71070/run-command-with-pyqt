from PyQt5.QtWidgets import QWidget, QPushButton

from ui.runcommand_ui import Ui_Form


class RunCommandView(QWidget):
    def __init__(self):
        super(RunCommandView, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def show_dialog(self):
        self.show()

    def get_container_widget(self) -> QWidget:
        return self.ui.widget

    def get_run_button(self) -> QPushButton:
        return self.ui.pushButton_2

    def get_path_button(self) -> QPushButton:
        return self.ui.path_button

    def set_result_label(self, text: str):
        self.ui.resul_lable.setText(text)

    def set_path_label(self, text: str):
        self.ui.path_lable.setText(text)

    def get_command_line_edit(self) -> str:
        return self.ui.command_lineEdit.text()

    def get_path_line_edit(self) -> str:
        return self.ui.path_lineEdit.text()
