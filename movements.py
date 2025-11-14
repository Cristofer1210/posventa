from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QTableWidget, QTableWidgetItem, QDateEdit, QComboBox,
                             QHeaderView, QFrame, QMessageBox)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QColor
from utils.formatters import format_currency
from datetime import datetime, timedelta

class MovementsModule:
    def __init__(self, db):
        self.db = db
        self.widget = QWidget()
        self.init_ui()
        
    def get_widget(self):
        return self.widget
        
    def on_enter(self):
        self.load_movements()
        
    def on_leave(self):
        pass
        
    def init_ui(self):
        layout = QVBoxLayout(self.widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("📋 Registro de Movimientos")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1e293b;")
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Filtros
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Fecha:"))
        
        self.date_filter = QDateEdit()
        self.date_filter.setDate(QDate.currentDate())
        self.date_filter.setCalendarPopup(True)
        self.date_filter.dateChanged.connect(self.load_movements)
        
        self.type_filter = QComboBox()
        self.type_filter.addItems(["Todos", "Ventas", "Abonos", "Cuentas Corrientes"])
        self.type_filter.currentTextChanged.connect(self.load_movements)
        
        filter_layout.addWidget(self.date_filter)
        filter_layout.addWidget(QLabel("Tipo:"))
        filter_layout.addWidget(self.type_filter)
        filter_layout.addStretch()
        
        layout.addLayout(header_layout)
        layout.addLayout(filter_layout)
        
        # Tabla de movimientos
        self.create_movements_table(layout)
        
    def create_movements_table(self, layout):
        self.movements_table = QTableWidget()
        self.movements_table.setColumnCount(6)
        self.movements_table.setHorizontalHeaderLabels([
            "Hora", "Cliente", "Productos", "Total", "Método Pago", "Estado"
        ])
        
        header = self.movements_table.horizontalHeader()
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Productos más ancho
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        self.movements_table.setAlternatingRowColors(True)
        layout.addWidget(self.movements_table)
        
    def load_movements(self):
        """Cargar movimientos con detalle completo"""
        try:
            date = self.date_filter.date().toString("yyyy-MM-dd")
            movements = self.db.get_detailed_movements(date)
            
            self.movements_table.setRowCount(len(movements))
            
            for row, movement in enumerate(movements):
                # movement: (id, hora, cliente, productos, total, metodo_pago, estado)
                hora, cliente, productos, total, metodo_pago, estado = movement
                
                # Color según el estado
                color = "#10b981" if estado == "pagado" else "#ef4444"
                
                self.movements_table.setItem(row, 0, QTableWidgetItem(hora))
                self.movements_table.setItem(row, 1, QTableWidgetItem(cliente))
                self.movements_table.setItem(row, 2, QTableWidgetItem(productos))
                self.movements_table.setItem(row, 3, QTableWidgetItem(format_currency(total)))
                
                metodo_item = QTableWidgetItem(metodo_pago)
                self.movements_table.setItem(row, 4, metodo_item)
                
                estado_item = QTableWidgetItem("✅ " + estado if estado == "pagado" else "⏳ " + estado)
                estado_item.setForeground(QColor(color))
                self.movements_table.setItem(row, 5, estado_item)
                
        except Exception as e:
            QMessageBox.critical(self.widget, "Error", f"Error al cargar movimientos:\n{str(e)}")