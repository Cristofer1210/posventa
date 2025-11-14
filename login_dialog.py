from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QHBoxLayout, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔐 Inicio de Sesión")
        self.setModal(True)
        self.setFixedSize(450, 550)  # Mantenemos la altura aumentada
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowTitleHint)

        # Credenciales correctas
        self.correct_username = "usuario"
        self.correct_password = "usuario123"

        self.init_ui()

    def init_ui(self):
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 30)
        layout.setSpacing(30)
        layout.setAlignment(Qt.AlignCenter)

        # Header con logo
        self.create_header(layout)
        
        # Formulario de login
        self.create_login_form(layout)
        
        # Footer
        self.create_footer(layout)

    def create_header(self, layout):
        logo_frame = QFrame()
        logo_frame.setFixedHeight(120)
        logo_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e40af, stop:1 #3b82f6);
                border-radius: 12px;
            }
        """)
        
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setAlignment(Qt.AlignCenter)
        logo_layout.setSpacing(8)

        title = QLabel("🏪 SISTEMA POS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 22px;
                font-weight: bold;
            }
        """)

        subtitle = QLabel("Punto de Venta")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                opacity: 0.9;
            }
        """)

        logo_layout.addWidget(title)
        logo_layout.addWidget(subtitle)
        layout.addWidget(logo_frame)

    def create_login_form(self, layout):
        form_frame = QFrame()
        # ELIMINAMOS cualquier estilo que pueda limitar el tamaño
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
            }
        """)
        
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(35, 35, 35, 35)
        form_layout.setSpacing(25)
        form_layout.setAlignment(Qt.AlignCenter)

        # Campo Usuario
        user_container = QVBoxLayout()
        user_container.setSpacing(8)  # Reducido ligeramente para mejor ajuste
        
        user_label = QLabel("👤 Usuario:")
        user_label.setStyleSheet("""
            font-weight: bold; 
            color: #374151; 
            font-size: 14px;
        """)
        user_label.setMinimumWidth(200)  # Aseguramos ancho mínimo para el texto
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ingrese su usuario")
        self.username_input.setMinimumHeight(45)
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 15px;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                font-size: 14px;
                background-color: #f8fafc;
                color: #1f2937;
                font-family: Arial;
                min-width: 250px;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
                background-color: white;
            }
        """)

        user_container.addWidget(user_label)
        user_container.addWidget(self.username_input)

        form_layout.addLayout(user_container)

        # Campo Contraseña
        pass_container = QVBoxLayout()
        pass_container.setSpacing(8)
        
        pass_label = QLabel("🔒 Contraseña:")
        pass_label.setStyleSheet("""
            font-weight: bold; 
            color: #374151; 
            font-size: 14px;
        """)
        pass_label.setMinimumWidth(200)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingrese su contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(45)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 15px;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                font-size: 14px;
                background-color: #f8fafc;
                color: #1f2937;
                font-family: Arial;
                min-width: 250px;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
                background-color: white;
            }
        """)

        pass_container.addWidget(pass_label)
        pass_container.addWidget(self.password_input)

        form_layout.addLayout(pass_container)

        # Botón de login
        login_btn = QPushButton("🚀 Ingresar al Sistema")
        login_btn.setMinimumHeight(50)
        login_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #059669, stop:1 #10b981);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
                font-family: Arial;
                min-width: 200px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #047857, stop:1 #065f46);
            }
            QPushButton:pressed {
                background: #064e3b;
            }
        """)
        login_btn.clicked.connect(self.attempt_login)

        form_layout.addWidget(login_btn)

        layout.addWidget(form_frame)

        # Conectar Enter para login
        self.username_input.returnPressed.connect(self.attempt_login)
        self.password_input.returnPressed.connect(self.attempt_login)

    def create_footer(self, layout):
        footer_label = QLabel("© 2024 Mi Kiosco - Sistema POS v1.0")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("color: #6b7280; font-size: 11px; margin-top: 15px;")
        layout.addWidget(footer_label)

    def attempt_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Campos Vacíos", 
                              "Por favor ingrese usuario y contraseña.")
            return

        if username == self.correct_username and password == self.correct_password:
            self.accept()
        else:
            QMessageBox.critical(self, "Credenciales Incorrectas",
                               "Usuario o contraseña incorrectos.\n\nIntente nuevamente.")
            self.password_input.clear()
            self.password_input.setFocus()