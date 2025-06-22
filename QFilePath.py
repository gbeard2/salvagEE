from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QFileDialog


class QFilePath(QWidget):
    def __init__(self, path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._filePath_lbl = QLineEdit(path)
        self._filePath_lbl.setFrame(False)

        self._browse_btn = QPushButton('📂')
        self._browse_btn.setFixedWidth(40)
        self._browse_btn.setFlat(True)
        self._browse_btn.clicked.connect(self._onBrowse_clicked)

        layout.addWidget(self._filePath_lbl)
        layout.addWidget(self._browse_btn)
        self.setLayout(layout)

    def text(self):
        return self._filePath_lbl.text()

    def _onBrowse_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select datasheet")
        if file_path:
            self._filePath_lbl.setText(file_path)
