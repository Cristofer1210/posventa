from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
                             QPushButton, QLineEdit, QListWidget, QListWidgetItem,
                             QFrame, QScrollArea, QWidget)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor
from datetime import datetime

class ChatDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("💬 Chat de Soporte - Mi Emprendimiento")
        self.setModal(False)
        self.setFixedSize(500, 600)

        # Simular mensajes de ejemplo
        self.messages = [
            {"sender": "Sistema", "message": "¡Hola! Soy el asistente de Mi Emprendimiento. ¿En qué puedo ayudarte?", "time": "10:00"},
            {"sender": "Tú", "message": "Necesito ayuda con el inventario", "time": "10:05"},
            {"sender": "Sistema", "message": "Claro, puedo ayudarte con eso. ¿Qué específicamente necesitas saber?", "time": "10:05"}
        ]

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Header
        header = QLabel("💬 Chat de Soporte Técnico")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e293b; margin-bottom: 10px;")
        layout.addWidget(header)

        # Área de mensajes con scroll
        messages_frame = QFrame()
        messages_frame.setStyleSheet("""
            QFrame {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
            }
        """)

        messages_layout = QVBoxLayout(messages_frame)

        self.messages_area = QScrollArea()
        self.messages_area.setWidgetResizable(True)
        self.messages_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.messages_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.messages_widget = QWidget()
        self.messages_vlayout = QVBoxLayout(self.messages_widget)
        self.messages_vlayout.setSpacing(10)
        self.messages_vlayout.setContentsMargins(10, 10, 10, 10)

        self.load_messages()

        self.messages_area.setWidget(self.messages_widget)
        messages_layout.addWidget(self.messages_area)

        layout.addWidget(messages_frame)

        # Área de entrada
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
            }
        """)

        input_layout = QVBoxLayout(input_frame)
        input_layout.setContentsMargins(10, 10, 10, 10)

        # Campo de mensaje
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Escribe tu mensaje aquí...")
        self.message_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
            }
        """)
        self.message_input.returnPressed.connect(self.send_message)

        input_layout.addWidget(self.message_input)

        # Botones
        buttons_layout = QHBoxLayout()

        self.send_btn = QPushButton("📤 Enviar")
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        self.send_btn.clicked.connect(self.send_message)

        self.close_btn = QPushButton("❌ Cerrar")
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        self.close_btn.clicked.connect(self.close)

        buttons_layout.addWidget(self.send_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.close_btn)

        input_layout.addLayout(buttons_layout)

        layout.addWidget(input_frame)

    def load_messages(self):
        """Cargar mensajes en el área de chat"""
        # Limpiar mensajes anteriores
        while self.messages_vlayout.count():
            child = self.messages_vlayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for msg in self.messages:
            self.add_message_to_ui(msg)

        # Scroll al final
        QTimer.singleShot(100, lambda: self.messages_area.verticalScrollBar().setValue(
            self.messages_area.verticalScrollBar().maximum()))

    def add_message_to_ui(self, msg):
        """Agregar un mensaje a la UI"""
        message_frame = QFrame()
        if msg["sender"] == "Tú":
            message_frame.setStyleSheet("""
                QFrame {
                    background-color: #3b82f6;
                    border-radius: 12px;
                    padding: 8px 12px;
                    margin-left: 50px;
                    margin-right: 10px;
                }
            """)
        else:
            message_frame.setStyleSheet("""
                QFrame {
                    background-color: #e2e8f0;
                    border-radius: 12px;
                    padding: 8px 12px;
                    margin-right: 50px;
                    margin-left: 10px;
                }
            """)

        message_layout = QVBoxLayout(message_frame)
        message_layout.setContentsMargins(8, 6, 8, 6)

        # Sender y hora
        header_layout = QHBoxLayout()
        sender_label = QLabel(f"{msg['sender']}")
        sender_label.setStyleSheet("font-weight: bold; font-size: 12px; color: #374151;")
        time_label = QLabel(msg['time'])
        time_label.setStyleSheet("font-size: 10px; color: #6b7280;")

        header_layout.addWidget(sender_label)
        header_layout.addStretch()
        header_layout.addWidget(time_label)

        message_layout.addLayout(header_layout)

        # Mensaje
        message_label = QLabel(msg['message'])
        message_label.setWordWrap(True)
        message_label.setStyleSheet("font-size: 14px; color: #1e293b; line-height: 1.4;")
        message_layout.addWidget(message_label)

        self.messages_vlayout.addWidget(message_frame)

    def send_message(self):
        """Enviar un mensaje"""
        message_text = self.message_input.text().strip()
        if not message_text:
            return

        # Agregar mensaje del usuario
        current_time = datetime.now().strftime("%H:%M")
        user_message = {
            "sender": "Tú",
            "message": message_text,
            "time": current_time
        }
        self.messages.append(user_message)
        self.add_message_to_ui(user_message)

        # Limpiar input
        self.message_input.clear()

        # Simular respuesta automática
        QTimer.singleShot(1000, self.send_auto_response)

        # Scroll al final
        QTimer.singleShot(100, lambda: self.messages_area.verticalScrollBar().setValue(
            self.messages_area.verticalScrollBar().maximum()))

    def send_auto_response(self):
        """Enviar respuesta automática del sistema"""
        responses = [
            "Entiendo tu consulta. Déjame verificar eso para ti.",
            "Gracias por la información. ¿Hay algo más en lo que pueda ayudarte?",
            "Perfecto, voy a revisar el sistema y te doy una respuesta en breve.",
            "Si tienes alguna otra pregunta sobre Mi Emprendimiento, estoy aquí para ayudar.",
            "He registrado tu solicitud. Un administrador se pondrá en contacto contigo pronto."
        ]

        import random
        response_text = random.choice(responses)

        current_time = datetime.now().strftime("%H:%M")
        system_message = {
            "sender": "Sistema",
            "message": response_text,
            "time": current_time
        }
        self.messages.append(system_message)
        self.add_message_to_ui(system_message)

        # Scroll al final
        QTimer.singleShot(100, lambda: self.messages_area.verticalScrollBar().setValue(
            self.messages_area.verticalScrollBar().maximum()))
