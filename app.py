import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, 
    QGroupBox, QFormLayout, QComboBox, QFileDialog, QMessageBox, QTableWidget, 
    QTableWidgetItem, QProgressBar, QFrame, QSplitter, QTabWidget, QScrollArea, QSlider
)
from PyQt5.QtCore import Qt
from fuzzy_engine import FuzzyFloodEngine
from ui.styles import STYLESHEET
from ui.widgets import PlotCanvas
import os

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistem Deteksi Banjir Fuzzy - Muhammad Iqbal Ramadhan (231011400285)")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(STYLESHEET)
        self.engine = FuzzyFloodEngine()
        self._build_ui()

    def _build_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # --- Sidebar (Inputs) ---
        sidebar = self._create_sidebar()
        main_layout.addWidget(sidebar, 1)

        # --- Main Dashboard ---
        dashboard = self._create_dashboard()
        main_layout.addWidget(dashboard, 3)

    def _create_sidebar(self):
        group = QGroupBox("Panel Kontrol")
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Presets
        layout.addWidget(QLabel("Muat Preset:"))
        self.preset = QComboBox()
        self.preset.addItems([
            "Kustom",
            "Sampel 1 (Risiko Rendah)",
            "Sampel 2 (Risiko Sedang)",
            "Sampel 3 (Risiko Tinggi)",
            "Sampel 4 (Campuran)"
        ])
        self.preset.currentIndexChanged.connect(self.load_preset)
        layout.addWidget(self.preset)

        # Inputs Form with Sliders
        form = QVBoxLayout()
        
        # Curah Hujan (0-300 mm/jam)
        layout.addWidget(QLabel("Curah Hujan (mm/jam):"))
        cr_row = QHBoxLayout()
        self.cr_input = QLineEdit("10")
        self.cr_input.setFixedWidth(70)
        self.cr_input.setToolTip("Curah Hujan dalam mm/jam (0-300)")
        self.cr_slider = QSlider(Qt.Horizontal)
        self.cr_slider.setRange(0, 300)
        self.cr_slider.setValue(10)
        self.cr_slider.setToolTip("Geser untuk mengatur curah hujan")
        cr_row.addWidget(self.cr_slider)
        cr_row.addWidget(self.cr_input)
        layout.addLayout(cr_row)
        
        # Ketinggian Air (0-5 m, step 0.01)
        layout.addWidget(QLabel("Ketinggian Air Sungai (m):"))
        wl_row = QHBoxLayout()
        self.wl_input = QLineEdit("0.25")
        self.wl_input.setFixedWidth(70)
        self.wl_input.setToolTip("Ketinggian Air dalam meter (0-5)")
        self.wl_slider = QSlider(Qt.Horizontal)
        self.wl_slider.setRange(0, 500)  # 0.00 to 5.00 (x100)
        self.wl_slider.setValue(25)  # 0.25
        self.wl_slider.setToolTip("Geser untuk mengatur ketinggian air")
        wl_row.addWidget(self.wl_slider)
        wl_row.addWidget(self.wl_input)
        layout.addLayout(wl_row)
        
        # Durasi (0-24 jam)
        layout.addWidget(QLabel("Durasi (jam):"))
        du_row = QHBoxLayout()
        self.du_input = QLineEdit("5")
        self.du_input.setFixedWidth(70)
        self.du_input.setToolTip("Durasi Hujan dalam jam (0-24)")
        self.du_slider = QSlider(Qt.Horizontal)
        self.du_slider.setRange(0, 24)
        self.du_slider.setValue(5)
        self.du_slider.setToolTip("Geser untuk mengatur durasi")
        du_row.addWidget(self.du_slider)
        du_row.addWidget(self.du_input)
        layout.addLayout(du_row)
        
        # Connect sliders and inputs for synchronization
        self.cr_slider.valueChanged.connect(self._on_cr_slider_changed)
        self.cr_input.textChanged.connect(self._on_cr_input_changed)
        self.wl_slider.valueChanged.connect(self._on_wl_slider_changed)
        self.wl_input.textChanged.connect(self._on_wl_input_changed)
        self.du_slider.valueChanged.connect(self._on_du_slider_changed)
        self.du_input.textChanged.connect(self._on_du_input_changed)

        # Buttons
        btn_layout = QVBoxLayout()
        self.btn_calc = QPushButton("HITUNG ANALISIS")
        self.btn_calc.setCursor(Qt.PointingHandCursor)
        self.btn_calc.setMinimumHeight(40)
        self.btn_calc.clicked.connect(self.calculate)
        
        self.btn_export = QPushButton("Ekspor Laporan (CSV)")
        self.btn_export.setCursor(Qt.PointingHandCursor)
        self.btn_export.clicked.connect(self.export_csv)
        
        btn_layout.addWidget(self.btn_calc)
        btn_layout.addWidget(self.btn_export)
        layout.addLayout(btn_layout)

        layout.addStretch()
        
        # Footer / Info
        footer_layout = QVBoxLayout()
        footer_layout.setSpacing(5)
        
        # Logos
        logo_layout = QHBoxLayout()
        logo_layout.setAlignment(Qt.AlignCenter)
        
        logo_unpam = QLabel()
        pix_unpam = QtGui.QPixmap("logo_unpam.png").scaledToHeight(50, Qt.SmoothTransformation)
        logo_unpam.setPixmap(pix_unpam)
        
        logo_ku = QLabel()
        pix_ku = QtGui.QPixmap("logoku.png").scaledToHeight(50, Qt.SmoothTransformation)
        logo_ku.setPixmap(pix_ku)
        
        logo_layout.addWidget(logo_unpam)
        logo_layout.addSpacing(10)
        logo_layout.addWidget(logo_ku)
        footer_layout.addLayout(logo_layout)

        # Text Info
        info_label = QLabel("Tugas Matkul Kecerdasan Buatan Semester 5\nDosen Pengampu: Bapak NURJAYA S.Kom, M.Kom")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: #4c4f69; font-size: 11px; font-weight: bold;")
        footer_layout.addWidget(info_label)

        copyright_label = QLabel("© Muhammad Iqbal Ramadhan - NIM 231011400285")
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet("color: #9ca0b0; font-size: 10px;")
        footer_layout.addWidget(copyright_label)

        layout.addLayout(footer_layout)
        group.setLayout(layout)
        return group

    def _create_dashboard(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # 1. Result Cards (Top Row)
        cards_layout = QHBoxLayout()
        
        # Flood Card
        self.flood_card = self._create_result_card("Risiko Banjir", "N/A", "Menunggu...")
        self.flood_bar = QProgressBar()
        self.flood_bar.setRange(0, 100)
        self.flood_bar.setValue(0)
        self.flood_bar.setTextVisible(False)
        self.flood_bar.setStyleSheet("QProgressBar::chunk { background-color: #1e66f5; }")
        self.flood_card.layout().addWidget(self.flood_bar)
        
        # Depth Card
        self.depth_card = self._create_result_card("Kedalaman Air", "N/A", "Menunggu...")
        self.depth_bar = QProgressBar()
        self.depth_bar.setRange(0, 300) # 0 to 3.00 m mapped to 0-300
        self.depth_bar.setValue(0)
        self.depth_bar.setTextVisible(False)
        self.depth_bar.setStyleSheet("QProgressBar::chunk { background-color: #fe640b; }")
        self.depth_card.layout().addWidget(self.depth_bar)

        cards_layout.addWidget(self.flood_card)
        cards_layout.addWidget(self.depth_card)
        layout.addLayout(cards_layout)

        # 2. Recommendation Box
        self.rec_box = QGroupBox("Rekomendasi Sistem")
        self.rec_box.setFixedHeight(100)
        rec_layout = QVBoxLayout()
        self.rec_label = QLabel("Silakan masukkan data dan klik tombol hitung.")
        self.rec_label.setWordWrap(True)
        self.rec_label.setStyleSheet("font-size: 16px; color: #4c4f69;")
        rec_layout.addWidget(self.rec_label)
        self.rec_box.setLayout(rec_layout)
        layout.addWidget(self.rec_box)

        # 3. Tabs for Details (Plots & Rules)
        self.tabs = QTabWidget()
        
        # Tab 1: Visualizations
        plot_tab = QWidget()
        plot_layout = QHBoxLayout(plot_tab)
        self.plot1 = PlotCanvas(self, width=5, height=3)
        self.plot2 = PlotCanvas(self, width=5, height=3)
        plot_layout.addWidget(self.plot1)
        plot_layout.addWidget(self.plot2)
        self.tabs.addTab(plot_tab, "Visualisasi")

        # Tab 2: Rule Inference
        rule_tab = QWidget()
        rule_layout = QVBoxLayout(rule_tab)
        self.rule_table = QTableWidget(0, 4)
        self.rule_table.setHorizontalHeaderLabels(["ID", "Anteseden (CR, WL, DU)", "Kekuatan Firing", "Konsekuen"])
        self.rule_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        rule_layout.addWidget(self.rule_table)
        self.tabs.addTab(rule_tab, "Mesin Inferensi Aturan")

        layout.addWidget(self.tabs, 1)

        return container

    def _create_result_card(self, title, value, status):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #e6e9ef;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        layout = QVBoxLayout(frame)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #5c5f77; font-size: 14px;")
        
        lbl_value = QLabel(value)
        lbl_value.setObjectName("ResultValue")
        
        lbl_status = QLabel(status)
        lbl_status.setObjectName("ResultTitle") # Reusing style
        
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_value)
        layout.addWidget(lbl_status)
        return frame

    def load_preset(self, idx):
        # 0: Custom, 1: Sample 1, etc.
        # Block signals to prevent recursive updates
        self.cr_slider.blockSignals(True)
        self.wl_slider.blockSignals(True)
        self.du_slider.blockSignals(True)
        
        if idx == 1:
            self.cr_input.setText("10"); self.wl_input.setText("0.25"); self.du_input.setText("5")
            self.cr_slider.setValue(10); self.wl_slider.setValue(25); self.du_slider.setValue(5)
        elif idx == 2:
            self.cr_input.setText("140"); self.wl_input.setText("2.20"); self.du_input.setText("8")
            self.cr_slider.setValue(140); self.wl_slider.setValue(220); self.du_slider.setValue(8)
        elif idx == 3:
            self.cr_input.setText("260"); self.wl_input.setText("4.20"); self.du_input.setText("18")
            self.cr_slider.setValue(260); self.wl_slider.setValue(420); self.du_slider.setValue(18)
        elif idx == 4:
            self.cr_input.setText("73"); self.wl_input.setText("1.55"); self.du_input.setText("2")
            self.cr_slider.setValue(73); self.wl_slider.setValue(155); self.du_slider.setValue(2)
        
        self.cr_slider.blockSignals(False)
        self.wl_slider.blockSignals(False)
        self.du_slider.blockSignals(False)

    # Slider-Input synchronization handlers
    def _on_cr_slider_changed(self, value):
        self.cr_input.blockSignals(True)
        self.cr_input.setText(str(value))
        self.cr_input.blockSignals(False)

    def _on_cr_input_changed(self, text):
        try:
            val = int(float(text))
            val = max(0, min(val, 300))
            self.cr_slider.blockSignals(True)
            self.cr_slider.setValue(val)
            self.cr_slider.blockSignals(False)
        except ValueError:
            pass

    def _on_wl_slider_changed(self, value):
        self.wl_input.blockSignals(True)
        self.wl_input.setText(f"{value / 100:.2f}")
        self.wl_input.blockSignals(False)

    def _on_wl_input_changed(self, text):
        try:
            val = int(float(text) * 100)
            val = max(0, min(val, 500))
            self.wl_slider.blockSignals(True)
            self.wl_slider.setValue(val)
            self.wl_slider.blockSignals(False)
        except ValueError:
            pass

    def _on_du_slider_changed(self, value):
        self.du_input.blockSignals(True)
        self.du_input.setText(str(value))
        self.du_input.blockSignals(False)

    def _on_du_input_changed(self, text):
        try:
            val = int(float(text))
            val = max(0, min(val, 24))
            self.du_slider.blockSignals(True)
            self.du_slider.setValue(val)
            self.du_slider.blockSignals(False)
        except ValueError:
            pass

    def calculate(self):
        try:
            cr = float(self.cr_input.text())
            wl = float(self.wl_input.text())
            du = float(self.du_input.text())
        except ValueError:
            QMessageBox.warning(self, "Kesalahan Input", "Harap masukkan nilai numerik yang valid.")
            return

        # Fuzzy Computation
        mu_cr, mu_wl, mu_du = self.engine.fuzzify_sample(cr, wl, du)
        active = self.engine.evaluate_rules(mu_cr, mu_wl, mu_du)
        agg = self.engine.aggregate_and_defuzz(active)
        
        flood_val = agg["flood_val"]
        depth_val = agg["depth_val"]

        # Update UI
        self._update_results(flood_val, depth_val)
        self._update_plots(agg)
        self._update_rules(active)

    def _update_results(self, flood_val, depth_val):
        # Flood
        f_val_str = f"{flood_val:.2f}" if flood_val is not None else "N/A"
        f_status, f_color = self._get_flood_status(flood_val)
        
        self.flood_card.findChild(QLabel, "ResultValue").setText(f_val_str)
        self.flood_card.findChild(QLabel, "ResultTitle").setText(f_status)
        self.flood_card.findChild(QLabel, "ResultTitle").setStyleSheet(f"color: {f_color}; font-size: 18px; font-weight: bold;")
        
        if flood_val is not None:
            self.flood_bar.setValue(int(flood_val))
            self.flood_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {f_color}; border-radius: 3px; }}")

        # Depth
        d_val_str = f"{depth_val:.2f} m" if depth_val is not None else "N/A"
        d_status, d_color = self._get_depth_status(depth_val)
        
        self.depth_card.findChild(QLabel, "ResultValue").setText(d_val_str)
        self.depth_card.findChild(QLabel, "ResultTitle").setText(d_status)
        self.depth_card.findChild(QLabel, "ResultTitle").setStyleSheet(f"color: {d_color}; font-size: 18px; font-weight: bold;")
        
        if depth_val is not None:
            # Map 0-3m to 0-300 for progress bar
            val_mapped = min(int(depth_val * 100), 300)
            self.depth_bar.setValue(val_mapped)
            self.depth_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {d_color}; border-radius: 3px; }}")

        # Recommendation
        rec_text = self._recommendation(flood_val, depth_val)
        self.rec_label.setText(rec_text)

    def _get_flood_status(self, val):
        if val is None: return "Tidak Diketahui", "#9ca0b0"
        if val < 30: return "AMAN", "#40a02b" # Green
        if val < 60: return "WASPADA", "#df8e1d" # Yellow
        return "BAHAYA", "#d20f39" # Red

    def _get_depth_status(self, val):
        if val is None: return "Tidak Diketahui", "#9ca0b0"
        if val < 1.0: return "RENDAH", "#40a02b"
        if val < 2.0: return "SEDANG", "#df8e1d"
        return "TINGGI", "#d20f39"

    def _recommendation(self, flood_val, depth_val):
        if flood_val is None: return "Data tidak mencukupi."
        if flood_val < 30:
            return "✅ Status Aman. Tidak diperlukan tindakan evakuasi. Tetap pantau informasi cuaca."
        if flood_val < 60:
            return "⚠️ Status Waspada. Siapkan barang berharga dan pantau terus ketinggian air. Hindari area rendah."
        return "🚨 BAHAYA BANJIR! Segera lakukan evakuasi ke tempat tinggi. Matikan aliran listrik dan ikuti arahan petugas."

    def _update_plots(self, agg):
        # Plot Flood
        ax1 = self.plot1.axes
        ax1.clear()
        ax1.set_title("Agregasi Risiko Banjir", color='#4c4f69')
        ax1.plot(self.engine.x_flood, agg["agg_flood"], label="Teragregasi", color='#d20f39', linewidth=2)
        for k, v in self.engine.flood_mfs.items():
            ax1.plot(self.engine.x_flood, v, '--', alpha=0.3, label=k)
        
        if agg["flood_val"] is not None:
            ax1.axvline(x=agg["flood_val"], color='#40a02b', linestyle='-', linewidth=2, label='Hasil')
            
        ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=3, fontsize='small', facecolor='#e6e9ef', edgecolor='#bcc0cc')
        self.plot1.figure.tight_layout()
        self.plot1.draw()

        # Plot Depth
        ax2 = self.plot2.axes
        ax2.clear()
        ax2.set_title("Agregasi Kedalaman Air", color='#4c4f69')
        ax2.plot(self.engine.x_depth, agg["agg_depth"], label="Teragregasi", color='#1e66f5', linewidth=2)
        for k, v in self.engine.depth_mfs.items():
            ax2.plot(self.engine.x_depth, v, '--', alpha=0.3, label=k)
            
        if agg["depth_val"] is not None:
            ax2.axvline(x=agg["depth_val"], color='#40a02b', linestyle='-', linewidth=2, label='Hasil')
            
        ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=3, fontsize='small', facecolor='#e6e9ef', edgecolor='#bcc0cc')
        self.plot2.figure.tight_layout()
        self.plot2.draw()

    def _update_rules(self, active):
        self.rule_table.setRowCount(0)
        for r in active:
            row = self.rule_table.rowCount()
            self.rule_table.insertRow(row)
            
            ant = f"CH:{r['antecedent'][0]}, KA:{r['antecedent'][1]}, DR:{r['antecedent'][2]}"
            cons = f"Banjir:{r['flood']} / Kedalaman:{r['depth']}"
            
            self.rule_table.setItem(row, 0, QTableWidgetItem(str(r['id'])))
            self.rule_table.setItem(row, 1, QTableWidgetItem(ant))
            self.rule_table.setItem(row, 2, QTableWidgetItem(f"{r['firing']:.3f}"))
            self.rule_table.setItem(row, 3, QTableWidgetItem(cons))

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Simpan Analisis", os.getcwd(), "File CSV (*.csv)")
        if not path: return
        
        try:
            with open(path, "w") as f:
                f.write("ID,Antecedent,Firing,Consequent\n")
                for r in range(self.rule_table.rowCount()):
                    rid = self.rule_table.item(r, 0).text()
                    ant = self.rule_table.item(r, 1).text()
                    firing = self.rule_table.item(r, 2).text()
                    cons = self.rule_table.item(r, 3).text()
                    f.write(f"{rid},{ant},{firing},{cons}\n")
            QMessageBox.information(self, "Berhasil", f"Data tersimpan di {path}")
        except Exception as e:
            QMessageBox.critical(self, "Kesalahan", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set global font
    font = QtGui.QFont("Segoe UI", 10)
    app.setFont(font)
    
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())