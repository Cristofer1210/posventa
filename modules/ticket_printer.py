import win32print
import win32ui
import win32con
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QComboBox,
                             QPushButton, QHBoxLayout, QTextEdit, QLineEdit,
                             QGroupBox, QFormLayout, QMessageBox, QCheckBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import os

class TicketPrinter:
    """Clase para manejar la impresión física de tickets"""

    def __init__(self):
        self.default_printer = None
        self.update_default_printer()

    def update_default_printer(self):
        """Actualizar impresora por defecto"""
        try:
            self.default_printer = win32print.GetDefaultPrinter()
        except:
            self.default_printer = None

    def get_available_printers(self):
        """Obtener lista de impresoras disponibles"""
        try:
            printers = []
            for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS):
                printers.append(printer[2])  # Nombre de la impresora
            return printers
        except Exception as e:
            print(f"Error obteniendo impresoras: {e}")
            return []

    def print_ticket(self, ticket_text, printer_name=None):
        """Imprimir ticket físicamente"""
        if not printer_name:
            printer_name = self.default_printer

        if not printer_name:
            raise Exception("No hay impresora configurada")

        try:
            # Crear contexto de impresión
            hprinter = win32print.OpenPrinter(printer_name)
            try:
                # Obtener información de la impresora
                printer_info = win32print.GetPrinter(hprinter, 2)

                # Crear contexto de dispositivo
                hdc = win32ui.CreateDC()
                hdc.CreatePrinterDC(printer_name)

                # Iniciar documento
                hdc.StartDoc("Ticket de Venta")
                hdc.StartPage()

                # Configurar fuente para tickets térmicos (fuente monoespaciada pequeña)
                font = win32ui.CreateFont({
                    "name": "Courier New",
                    "height": 20,  # Altura pequeña para tickets
                    "weight": 400,
                })

                hdc.SelectObject(font)

                # Dividir el texto en líneas e imprimir
                lines = ticket_text.split('\n')
                y_position = 100  # Posición Y inicial

                for line in lines:
                    if line.strip():  # Solo imprimir líneas no vacías
                        hdc.TextOut(50, y_position, line)  # Posición X=50, Y variable
                        y_position += 25  # Espacio entre líneas

                # Finalizar página y documento
                hdc.EndPage()
                hdc.EndDoc()

            finally:
                win32print.ClosePrinter(hprinter)

            return True

        except Exception as e:
            raise Exception(f"Error al imprimir: {str(e)}")


class TicketCustomizationDialog(QDialog):
    """Diálogo para personalizar y imprimir tickets"""

    def __init__(self, ticket_text, sale_data, items, total, parent=None):
        super().__init__(parent)
        self.ticket_text = ticket_text
        self.sale_data = sale_data
        self.items = items
        self.total = total
        self.printer = TicketPrinter()

        self.setWindowTitle("🖨️ Personalizar e Imprimir Ticket")
        self.setModal(True)
        self.setFixedSize(600, 700)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Título
        title = QLabel("🎫 Personalización del Ticket")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e293b;")
        layout.addWidget(title)

        # Grupo de personalización
        customization_group = QGroupBox("✏️ Personalizar Ticket")
        customization_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        customization_layout = QVBoxLayout(customization_group)

        # Campo para nombre del cliente
        customer_layout = QHBoxLayout()
        customer_layout.addWidget(QLabel("👤 Nombre del Cliente:"))
        self.customer_name_input = QLineEdit()
        self.customer_name_input.setPlaceholderText("Opcional - aparecerá en el ticket")
        customer_layout.addWidget(self.customer_name_input)
        customization_layout.addLayout(customer_layout)

        # Campo para observaciones
        notes_layout = QHBoxLayout()
        notes_layout.addWidget(QLabel("📝 Observaciones:"))
        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Opcional - notas adicionales")
        notes_layout.addWidget(self.notes_input)
        customization_layout.addLayout(notes_layout)

        # Checkbox para mostrar precio unitario
        self.show_unit_price = QCheckBox("Mostrar precio unitario de cada producto")
        self.show_unit_price.setChecked(True)  # Por defecto activado
        customization_layout.addWidget(self.show_unit_price)

        layout.addWidget(customization_group)

        # Vista previa del ticket
        preview_group = QGroupBox("👁️ Vista Previa del Ticket")
        preview_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        preview_layout = QVBoxLayout(preview_group)

        self.preview_text = QTextEdit()
        self.preview_text.setFont(QFont("Courier New", 10))
        self.preview_text.setReadOnly(True)
        self.preview_text.setMaximumHeight(300)
        preview_layout.addWidget(self.preview_text)

        layout.addWidget(preview_group)

        # Grupo de impresión
        print_group = QGroupBox("🖨️ Opciones de Impresión")
        print_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        print_layout = QVBoxLayout(print_group)

        # Selector de impresora
        printer_layout = QHBoxLayout()
        printer_layout.addWidget(QLabel("Impresora:"))
        self.printer_combo = QComboBox()
        self.update_printer_list()
        printer_layout.addWidget(self.printer_combo)

        refresh_btn = QPushButton("🔄")
        refresh_btn.setToolTip("Actualizar lista de impresoras")
        refresh_btn.clicked.connect(self.update_printer_list)
        printer_layout.addWidget(refresh_btn)

        print_layout.addLayout(printer_layout)

        layout.addWidget(print_group)

        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        # Botón actualizar vista previa
        update_preview_btn = QPushButton("🔄 Actualizar Vista Previa")
        update_preview_btn.clicked.connect(self.update_preview)
        buttons_layout.addWidget(update_preview_btn)

        # Botón solo vista previa
        preview_only_btn = QPushButton("👁️ Solo Vista Previa")
        preview_only_btn.clicked.connect(self.preview_only)
        buttons_layout.addWidget(preview_only_btn)

        # Botón imprimir
        self.print_btn = QPushButton("🖨️ Imprimir Ticket")
        self.print_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #059669, stop:1 #10b981);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #047857, stop:1 #065f46);
            }
        """)
        self.print_btn.clicked.connect(self.print_ticket)
        buttons_layout.addWidget(self.print_btn)

        # Botón cancelar
        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        layout.addLayout(buttons_layout)

        # Actualizar vista previa inicial
        self.update_preview()

    def update_printer_list(self):
        """Actualizar lista de impresoras disponibles"""
        self.printer_combo.clear()
        printers = self.printer.get_available_printers()

        if printers:
            self.printer_combo.addItems(printers)
            # Seleccionar impresora por defecto si está disponible
            default_printer = self.printer.default_printer
            if default_printer in printers:
                self.printer_combo.setCurrentText(default_printer)
        else:
            self.printer_combo.addItem("No hay impresoras disponibles")
            self.print_btn.setEnabled(False)

    def update_preview(self):
        """Actualizar la vista previa del ticket con las personalizaciones"""
        # Generar ticket personalizado
        custom_ticket = self.generate_custom_ticket()
        self.preview_text.setPlainText(custom_ticket)

    def generate_custom_ticket(self):
        """Generar ticket con personalizaciones"""
        from datetime import datetime

        current_time = datetime.now()
        line_width = 42

        # Encabezado premium
        ticket_text = f"""
{'*' * line_width}
{'🏪 KIOSCO ARONIUM'.center(line_width)}
{'*' * line_width}
{'TICKET DE VENTA'.center(line_width)}
{'Nº: {:06d}'.format(self.sale_data.get('id', 0)).center(line_width)}
{'FECHA: ' + current_time.strftime('%d/%m/%Y %H:%M')}
"""

        # Agregar nombre del cliente si se especificó
        customer_name = self.customer_name_input.text().strip()
        if customer_name:
            ticket_text += f"{'CLIENTE: ' + customer_name}\n"

        ticket_text += f"{'PAGO: ' + self.sale_data.get('payment_method', 'N/A')}\n"
        ticket_text += f"{'-' * line_width}\n"
        ticket_text += f"{'DESCRIPCIÓN'.ljust(25)} {'CANT'.ljust(6)} {'TOTAL'.ljust(8)}\n"
        ticket_text += f"{'-' * line_width}\n"

        # Productos
        for item in self.items:
            product_name = item['name']
            if len(product_name) > 22:
                product_name = product_name[:19] + "..."

            # Formato de tabla alineada
            line = f"{product_name:<22} {item['quantity']:>2}   {format_currency(item['subtotal']):>10}"
            ticket_text += line + "\n"

            # Mostrar precio unitario si está activado
            if self.show_unit_price.isChecked():
                unit_price_line = f"{'@ ' + format_currency(item['price']):>38}"
                ticket_text += unit_price_line + "\n"

        # Sección de totales
        ticket_text += f"""
{'-' * line_width}
{'TOTAL A PAGAR:':<30} {format_currency(self.total):>10}
"""

        # Agregar observaciones si existen
        notes = self.notes_input.text().strip()
        if notes:
            ticket_text += f"\n{'OBSERVACIONES:'.center(line_width)}\n{notes.center(line_width)}\n"

        ticket_text += f"""
{'*' * line_width}
{'¡GRACIAS POR SU COMPRA!'.center(line_width)}
{'*' * line_width}
{'Conserve este ticket'.center(line_width)}
{'*' * line_width}
"""

        return ticket_text

    def preview_only(self):
        """Solo mostrar vista previa y cerrar"""
        self.accept()

    def print_ticket(self):
        """Imprimir el ticket físicamente"""
        try:
            # Generar ticket personalizado
            custom_ticket = self.generate_custom_ticket()

            # Obtener impresora seleccionada
            selected_printer = self.printer_combo.currentText()
            if not selected_printer or selected_printer == "No hay impresoras disponibles":
                QMessageBox.warning(self, "Impresora no válida",
                                  "Por favor selecciona una impresora válida.")
                return

            # Imprimir
            self.printer.print_ticket(custom_ticket, selected_printer)

            QMessageBox.information(self, "✅ Impresión Exitosa",
                                  f"Ticket impreso correctamente en:\n{selected_printer}")

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "❌ Error de Impresión",
                               f"Error al imprimir el ticket:\n{str(e)}")


def format_currency(amount):
    """Formatear monto como moneda"""
    return f"${amount:,.2f}"
