STYLESHEET = """
QMainWindow, QWidget {
    background-color: #eff1f5;
    color: #4c4f69;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
}

QGroupBox {
    border: 2px solid #bcc0cc;
    border-radius: 8px;
    margin-top: 1.5em;
    font-weight: bold;
    color: #1e66f5;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center;
    padding: 0 10px;
    background-color: #eff1f5;
}

QLineEdit, QComboBox {
    background-color: #ffffff;
    border: 1px solid #ccd0da;
    border-radius: 4px;
    padding: 5px;
    color: #4c4f69;
}

QLineEdit:focus, QComboBox:focus {
    border: 1px solid #1e66f5;
}

QPushButton {
    background-color: #1e66f5;
    color: #eff1f5;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #7287fd;
}

QPushButton:pressed {
    background-color: #179299;
}

QTableWidget {
    background-color: #ffffff;
    gridline-color: #ccd0da;
    border: 1px solid #ccd0da;
    border-radius: 8px;
    color: #4c4f69;
}

QHeaderView::section {
    background-color: #e6e9ef;
    color: #4c4f69;
    padding: 5px;
    border: none;
}

QProgressBar {
    border: 1px solid #ccd0da;
    border-radius: 4px;
    text-align: center;
    background-color: #e6e9ef;
    color: #4c4f69;
}

QProgressBar::chunk {
    background-color: #40a02b;
    border-radius: 3px;
}

QTabWidget::pane {
    border: 1px solid #bcc0cc;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #e6e9ef;
    color: #4c4f69;
    padding: 8px 12px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #1e66f5;
    color: #eff1f5;
}

QLabel#ResultTitle {
    font-size: 18px;
    font-weight: bold;
    color: #d20f39;
}

QLabel#ResultValue {
    font-size: 24px;
    font-weight: bold;
    color: #40a02b;
}
"""
