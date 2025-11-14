from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class CustomersModule:
    def __init__(self, db):
        self.db = db
        self.widget = QWidget()
        self.init_ui()
        
    def get_widget(self):
        return self.widget
        
    def on_enter(self):
        pass
        
    def on_leave(self):
        pass
        
    def init_ui(self):
        layout = QVBoxLayout(self.widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("👥 Gestión de Clientes")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        content = QLabel("Módulo de clientes - En desarrollo")
        content.setAlignment(Qt.AlignCenter)
        content.setStyleSheet("font-size: 16px; color: #7f8c8d; margin: 50px;")
        layout.addWidget(content)