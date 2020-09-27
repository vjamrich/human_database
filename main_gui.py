from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
# import qtmodern.styles
import json
import sys


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui_layout.ui', self)

        with open(r"config\config.json", "r") as json_config:
            self.config = json.load(json_config)

        self.combo_boxes = {combo_box.objectName(): combo_box for combo_box in self.findChildren(QComboBox)}
        self.check_boxes = {check_box.objectName(): check_box for check_box in self.findChildren(QCheckBox)}
        self.spin_boxes = {spin_boxe.objectName(): spin_boxe for spin_boxe in self.findChildren(QSpinBox)}
        self.tool_buttons = {tool_button.objectName(): tool_button for tool_button in self.findChildren(QToolButton)}
        self.push_buttons = {push_button.objectName(): push_button for push_button in self.findChildren(QPushButton)}
        self.line_edits = {line_edit.objectName(): line_edit for line_edit in self.findChildren(QLineEdit)}
        self.slider = self.findChild(QSlider, "compression_horizontal_slider")
        self.slider_label = self.findChild(QLabel, "compression_label")

        for button_name, button in self.tool_buttons.items():
            button.clicked.connect(self.open_file_dialog)
        self.push_buttons["load_defaults_button"].clicked.connect(self.warning)
        self.push_buttons["run_button"].clicked.connect(self.execute)
        self.slider.valueChanged.connect(self.update_slider_label)

        self.load_config()
        self.update_slider_label()

        self.show()

    def update_slider_label(self):
        self.slider_label.setText(f"Compression {self.slider.value()}%")

    def open_file_dialog(self):
        sending_button = self.sender()
        file_dialog = QFileDialog()

        if sending_button.objectName() == "blender_283_tool_button" or sending_button.objectName() == "blender_279_tool_button":
            path = file_dialog.getOpenFileName()[0]
        else:
            path = file_dialog.getExistingDirectory()

        if sending_button.objectName() == "input_mhm_tool_button":
            self.line_edits["input_mhm_line_edit"].setText(path)
        elif sending_button.objectName() == "output_folder_tool_button":
            self.line_edits["output_folder_line_edit"].setText(path)
        elif sending_button.objectName() == "blender_283_tool_button":
            self.line_edits["blender_283_line_edit"].setText(path)
        elif sending_button.objectName() == "blender_279_tool_button":
            self.line_edits["blender_279_line_edit"].setText(path)
        elif sending_button.objectName() == "cmu_targets_tool_button":
            self.line_edits["cmu_targets_line_edit"].setText(path)
        elif sending_button.objectName() == "hdri_tool_button":
            self.line_edits["hdri_line_edit"].setText(path)

    def save_config(self):
        convert = {"8 bit": "8",
                   "16 bit": "16",
                   "Eevee": "BLENDER_EEVEE",
                   "Cycles": "CYCLES",
                   "Workbench": "BLENDER_WORKBENCH",
                   "RGB": "RGB",
                   "RGBA": "RGBA",
                   "Black & While": "BW"}

        self.config["input path"] = self.line_edits["input_mhm_line_edit"].text()
        self.config["output path"] = self.line_edits["output_folder_line_edit"].text()
        self.config["software"]["blender 2.83 location"] = self.line_edits["blender_283_line_edit"].text()
        self.config["software"]["blender 2.79 location"] = self.line_edits["blender_279_line_edit"].text()
        self.config["data"]["targets"] = self.line_edits["cmu_targets_line_edit"].text()
        self.config["data"]["hdri"] = self.line_edits["hdri_line_edit"].text()

        self.config["render"]["subdivide"] = self.check_boxes["subdivide_check_box"].isChecked()
        self.config["render"]["alpha map"] = self.check_boxes["alpha_check_box"].isChecked()
        self.config["render"]["normal map"] = self.check_boxes["normal_check_box"].isChecked()
        self.config["render"]["depth map"] = self.check_boxes["depth_check_box"].isChecked()
        render = self.check_boxes["render_check_box"].isChecked()

        self.config["render"]["format"] = self.combo_boxes["file_format_combo_box"].currentText()
        self.config["render"]["engine"] = convert[self.combo_boxes["render_engine_combo_box"].currentText()]
        self.config["render"]["colour mode"] = convert[self.combo_boxes["colour_mode_combo_box"].currentText()]
        self.config["render"]["colour depth"] = convert[self.combo_boxes["colour_depth_combo_box"].currentText()]
        self.config["render"]["camera bone anchor"] = self.combo_boxes["camera_anchor_combo_box"].currentText()

        self.config["render"]["x resolution"] = self.spin_boxes["resolution_x_spin_box"].value()
        self.config["render"]["y resolution"] = self.spin_boxes["resolution_y_spin_box"].value()

        self.config["render"]["compression [%]"] = self.slider.value()

        with open(r"config\config.json", "w") as json_config:
            json.dump(self.config, json_config, indent=4)

    def load_config(self):
        convert = {"8": "8 bit",
                   "16": "16 bit",
                   "BLENDER_EEVEE": "Eevee",
                   "CYCLES": "Cycles",
                   "BLENDER_WORKBENCH": "Workbench",
                   "RGB": "RGB",
                   "RGBA": "RGBA",
                   "BW": "Black & While"}

        self.line_edits["input_mhm_line_edit"].setText(self.config["input path"])
        self.line_edits["output_folder_line_edit"].setText(self.config["output path"])
        self.line_edits["blender_283_line_edit"].setText(self.config["software"]["blender 2.83 location"])
        self.line_edits["blender_279_line_edit"].setText(self.config["software"]["blender 2.79 location"])
        self.line_edits["cmu_targets_line_edit"].setText(self.config["data"]["targets"])
        self.line_edits["hdri_line_edit"].setText(self.config["data"]["hdri"])

        self.check_boxes["subdivide_check_box"].setChecked(self.config["render"]["subdivide"])
        self.check_boxes["alpha_check_box"].setChecked(self.config["render"]["alpha map"])
        self.check_boxes["normal_check_box"].setChecked(self.config["render"]["normal map"])
        self.check_boxes["depth_check_box"].setChecked(self.config["render"]["depth map"])
        # self.check_boxes["render_check_box"].setChecked(render)

        self.combo_boxes["file_format_combo_box"].setCurrentText(self.config["render"]["format"])
        self.combo_boxes["render_engine_combo_box"].setCurrentText(convert[self.config["render"]["engine"]])
        self.combo_boxes["colour_mode_combo_box"].setCurrentText(convert[self.config["render"]["colour mode"]])
        self.combo_boxes["colour_depth_combo_box"].setCurrentText(convert[self.config["render"]["colour depth"]])
        self.combo_boxes["camera_anchor_combo_box"].setCurrentText(self.config["render"]["camera bone anchor"])

        self.spin_boxes["resolution_x_spin_box"].setValue(self.config["render"]["x resolution"])
        self.spin_boxes["resolution_y_spin_box"].setValue(self.config["render"]["y resolution"])

        self.slider.setValue(self.config["render"]["compression [%]"])

    def warning(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)

        msg.setText("Are you sure you want to load default settings? This action can't be reverted")
        msg.setWindowTitle("Warning")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.load_defaults)

        msg.exec_()

    def load_defaults(self):
        with open(r"Data\default_config.json", "r") as json_config:
            self.config = json.load(json_config)
        self.load_config()

    def execute(self):
        print("EXECUTE")

    def closeEvent(self, event):
        self.save_config()
        event.accept()


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    # qtmodern.styles.dark(app)
    window = Ui()
    app.exec_()


if __name__ == "__main__":
    main()
