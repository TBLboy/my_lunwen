from __future__ import annotations

from PyQt6.QtWidgets import (
    QWidget,
    QFormLayout,
    QDoubleSpinBox,
    QPushButton,
    QMessageBox,
    QLabel,
    QLineEdit,
)


class KoopmanLQRSettingsWidget(QWidget):
    def __init__(self, algorithm, title: str, path_key: str = "model_path", path_label: str = "Model checkpoint:"):
        super().__init__()
        self.algo = algorithm
        self.title = title
        self.path_key = path_key
        self.path_label = path_label
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)
        layout.addRow(QLabel(self.title))

        self.model_path_edit = QLineEdit()
        self.model_path_edit.setText(str(self.algo.config.get(self.path_key, "")))
        layout.addRow(self.path_label, self.model_path_edit)

        self.spin_qx1 = QDoubleSpinBox()
        self.spin_qx1.setRange(0.0, 100000.0)
        self.spin_qx1.setSingleStep(50.0)
        self.spin_qx1.setValue(float(self.algo.config.get("Q_x1", 10.0)))

        self.spin_qx2 = QDoubleSpinBox()
        self.spin_qx2.setRange(0.0, 100000.0)
        self.spin_qx2.setSingleStep(50.0)
        self.spin_qx2.setValue(float(self.algo.config.get("Q_x2", 10.0)))

        self.spin_alpha = QDoubleSpinBox()
        self.spin_alpha.setRange(0.0, 0.999)
        self.spin_alpha.setDecimals(4)
        self.spin_alpha.setSingleStep(0.01)
        self.spin_alpha.setValue(float(self.algo.config.get("alpha", 0.01)))

        self.spin_r = QDoubleSpinBox()
        self.spin_r.setRange(0.001, 1000.0)
        self.spin_r.setDecimals(4)
        self.spin_r.setSingleStep(0.1)
        self.spin_r.setValue(float(self.algo.config.get("R_control", 0.4)))

        self.spin_ff = QDoubleSpinBox()
        self.spin_ff.setRange(0.0, 5.0)
        self.spin_ff.setDecimals(3)
        self.spin_ff.setSingleStep(0.1)
        self.spin_ff.setValue(float(self.algo.config.get("ff_gain", 0.5)))

        self.spin_ulimit = QDoubleSpinBox()
        self.spin_ulimit.setRange(1.0, 1000.0)
        self.spin_ulimit.setSingleStep(5.0)
        self.spin_ulimit.setValue(float(self.algo.config.get("u_limit", 100.0)))

        layout.addRow("Q_x1  (state weight):", self.spin_qx1)
        layout.addRow("Q_x2  (state weight):", self.spin_qx2)
        layout.addRow("alpha (feature weight):", self.spin_alpha)
        layout.addRow("R     (control weight):", self.spin_r)
        layout.addRow("ff_gain:", self.spin_ff)
        layout.addRow("u_limit:", self.spin_ulimit)

        btn_save = QPushButton("Save & Re-design LQR")
        btn_save.clicked.connect(self.save_params)
        layout.addRow(btn_save)

        btn_reload = QPushButton("Re-load Model")
        btn_reload.clicked.connect(self.reload_model)
        layout.addRow(btn_reload)

    def save_params(self):
        self.algo.config["Q_x1"] = self.spin_qx1.value()
        self.algo.config["Q_x2"] = self.spin_qx2.value()
        self.algo.config["alpha"] = self.spin_alpha.value()
        self.algo.config["R_control"] = self.spin_r.value()
        self.algo.config["ff_gain"] = self.spin_ff.value()
        self.algo.config["u_limit"] = self.spin_ulimit.value()
        self.algo.save_config()
        self.algo.design_lqr()
        QMessageBox.information(self, "OK", "Parameters saved. LQR re-designed.")

    def reload_model(self):
        self.algo.config[self.path_key] = self.model_path_edit.text()
        self.algo.save_config()
        self.algo.load_model_and_design_lqr()
        if self.algo.lifter is not None:
            QMessageBox.information(self, "OK", "Model re-loaded.")
        else:
            QMessageBox.warning(self, "Error", "Model load failed - check console.")
