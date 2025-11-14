from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem, QFrame, QGroupBox,
                             QHeaderView, QMessageBox, QTextEdit, QDialog,
                             QDialogButtonBox, QDateEdit, QComboBox, QLineEdit)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from utils.formatters import format_currency
from datetime import datetime

class CashModule:
    def __init__(self, db):
        self.db = db
        self.widget = QWidget()
        self.init_ui()

    def get_widget(self):
        return self.widget

    def on_enter(self):
        self.load_cash_data()

    def on_leave(self):
        pass

    def init_ui(self):
        layout = QVBoxLayout(self.widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        # Header
        self.create_header(layout)

        # Acciones rápidas
        self.create_quick_actions(layout)

        # Estado actual de caja
        self.create_current_status(layout)

        # Historial de caja
        self.create_cash_history(layout)

    def create_header(self, layout):
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)

        title = QLabel("💰 Gestión de Caja")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #1e293b; margin-bottom: 5px;")

        subtitle = QLabel("Control y administración del flujo de caja del negocio")
        subtitle.setStyleSheet("font-size: 16px; color: #64748b;")

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addWidget(header_frame)

    def create_quick_actions(self, layout):
        group = QGroupBox("🚀 Acciones Rápidas")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 18px;
                color: #374151;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
            }
        """)

        actions_layout = QHBoxLayout(group)
        actions_layout.setSpacing(15)

        # Botones principales
        actions = [
            ("🔓 Apertura de Caja", "Abrir caja para el día", "#10b981", self.open_cash_dialog),
            ("💸 Cierre de Caja", "Cerrar caja con reporte", "#f59e0b", self.close_cash_dialog),
            ("📊 Reporte Diario", "Ver resumen del día", "#3b82f6", self.show_daily_report),
            ("📈 Historial", "Ver historial completo", "#8b5cf6", self.show_history_dialog)
        ]

        for text, tooltip, color, callback in actions:
            btn = QPushButton(text)
            btn.setToolTip(tooltip)
            btn.setMinimumHeight(70)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {color}, stop:1 {self.lighten_color(color)});
                    color: white;
                    border: none;
                    border-radius: 12px;
                    font-weight: bold;
                    font-size: 14px;
                    padding: 15px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {self.darken_color(color)}, stop:1 {color});
                }}
            """)
            btn.clicked.connect(callback)
            actions_layout.addWidget(btn)

        layout.addWidget(group)

    def create_current_status(self, layout):
        group = QGroupBox("📊 Estado Actual de Caja")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 18px;
                color: #374151;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                margin-top: 10px;
                padding-top: 15px;
            }
        """)

        self.status_layout = QVBoxLayout(group)
        self.status_layout.setSpacing(15)

        # Placeholder para estado actual
        self.status_label = QLabel("Cargando estado de caja...")
        self.status_label.setStyleSheet("font-size: 16px; color: #6b7280; padding: 20px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_layout.addWidget(self.status_label)

        layout.addWidget(group)

    def create_cash_history(self, layout):
        group = QGroupBox("📋 Historial Reciente")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 18px;
                color: #374151;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                margin-top: 10px;
                padding-top: 15px;
            }
        """)

        history_layout = QVBoxLayout(group)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Fecha", "Tipo", "Monto", "Notas"])

        header = self.history_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)

        self.history_table.setAlternatingRowColors(True)
        self.history_table.setMaximumHeight(300)

        history_layout.addWidget(self.history_table)
        layout.addWidget(group)

    def load_cash_data(self):
        """Cargar datos de caja"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")

            # Verificar si hay apertura hoy
            open_records = self.db.get_cash_open_records(today, today)
            close_records = self.db.get_cash_close_records(today, today)

            if open_records:
                opening_amount = open_records[0][2]
                status_text = f"✅ Caja ABIERTA - Monto inicial: {format_currency(opening_amount)}"

                if close_records:
                    closing_amount = close_records[0][2]
                    status_text += f" | Cierre: {format_currency(closing_amount)}"
            else:
                status_text = "❌ Caja CERRADA - No se ha abierto hoy"

            self.status_label.setText(status_text)

            # Cargar historial reciente (últimos 10 registros)
            self.load_recent_history()

        except Exception as e:
            self.status_label.setText(f"Error cargando datos: {str(e)}")
            print(f"Error en load_cash_data: {e}")

    def load_recent_history(self):
        """Cargar historial reciente de caja"""
        try:
            # Obtener aperturas recientes
            opens = self.db.get_cash_open_records()
            closes = self.db.get_cash_close_records()

            # Combinar y ordenar por fecha
            history = []

            for record in opens[-5:]:  # Últimas 5 aperturas
                history.append({
                    'date': record[1],
                    'type': 'Apertura',
                    'amount': record[2],
                    'notes': record[3] or ''
                })

            for record in closes[-5:]:  # Últimas 5 cierres
                history.append({
                    'date': record[1],
                    'type': 'Cierre',
                    'amount': record[2],
                    'notes': record[3] or ''
                })

            # Ordenar por fecha descendente
            history.sort(key=lambda x: x['date'], reverse=True)
            history = history[:10]  # Solo los 10 más recientes

            # Actualizar tabla
            self.history_table.setRowCount(len(history))

            for row, item in enumerate(history):
                self.history_table.setItem(row, 0, QTableWidgetItem(item['date']))
                self.history_table.setItem(row, 1, QTableWidgetItem(item['type']))
                self.history_table.setItem(row, 2, QTableWidgetItem(format_currency(item['amount'])))
                self.history_table.setItem(row, 3, QTableWidgetItem(item['notes']))

        except Exception as e:
            print(f"Error cargando historial: {e}")

    def open_cash_dialog(self):
        """Diálogo para apertura de caja"""
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Verificar si ya existe una apertura para hoy
        try:
            open_records = self.db.get_cash_open_records(current_date, current_date)
            if open_records:
                QMessageBox.warning(self.widget, "Apertura Ya Existente",
                                    f"Ya existe una apertura de caja para la fecha: {current_date}")
                return
        except Exception as e:
            QMessageBox.critical(self.widget, "Error de Base de Datos", f"No se pudo verificar aperturas existentes:\n{e}")
            return

        # Solicitar el monto de apertura
        opening_amount, ok = QInputDialog.getDouble(
            self.widget,
            "🔓 Apertura de Caja",
            f"Ingrese el monto de apertura para la fecha: {current_date}",
            value=0.00,
            decimals=2,
            min=0.00,
            max=999999.99
        )

        if not ok:
            return

        # Confirmar la apertura
        reply = QMessageBox.question(
            self.widget,
            "Confirmar Apertura de Caja",
            f"¿Confirmar apertura de caja para {current_date} con monto inicial de {format_currency(opening_amount)}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                # Llama al método de database.py para insertar el registro de apertura
                self.db.insert_cash_open_record(current_date, opening_amount)
                QMessageBox.information(self.widget, "Éxito", f"Apertura de caja registrada exitosamente.\nMonto inicial: {format_currency(opening_amount)}")
                self.load_cash_data()  # Recargar datos
            except Exception as e:
                QMessageBox.critical(self.widget, "Error de Apertura", f"Error al guardar la apertura de caja:\n{e}")

    def close_cash_dialog(self):
        """Diálogo para cierre de caja con reporte detallado"""
        current_date = datetime.now().strftime("%Y-%m-%d")

        try:
            # Obtener datos para el reporte
            total_income = self.db.get_cash_register_income_summary(current_date)
            sales_summary = self.db.get_sales_summary(current_date, current_date)
            top_products = self.db.get_top_products(current_date, current_date, 5)
            total_products_sold = self.db.get_total_products_sold(current_date, current_date)
            inventory_value = self.db.get_inventory_value()
            total_products = self.db.get_total_products()
            low_stock_count = self.db.get_low_stock_count()
            out_of_stock_count = self.db.get_out_of_stock_count()

            # Extraer datos de ventas
            if sales_summary and len(sales_summary) >= 4:
                total_sales, total_amount, avg_ticket, unique_customers = sales_summary
            else:
                total_sales, total_amount, avg_ticket, unique_customers = 0, 0.0, 0.0, 0

        except Exception as e:
            QMessageBox.critical(self.widget, "Error de Base de Datos", f"No se pudo calcular el resumen de caja:\n{e}")
            return

        # Crear diálogo personalizado para el cierre de caja
        dialog = QDialog(self.widget)
        dialog.setWindowTitle("💸 Cierre de Caja - Reporte Detallado")
        dialog.setModal(True)
        dialog.setFixedSize(700, 600)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Título
        title = QLabel("📊 Reporte de Cierre de Caja")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1e293b;")
        layout.addWidget(title)

        # Fecha
        date_label = QLabel(f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y')}")
        date_label.setStyleSheet("font-size: 14px; color: #6b7280;")
        layout.addWidget(date_label)

        # Área de texto para el reporte
        report_text = QTextEdit()
        report_text.setReadOnly(True)
        report_text.setFont(QFont("Courier New", 10))

        # Generar contenido del reporte
        report_content = f"""
{'='*60}
{'🏪 KIOSCO ARONIUM - CIERRE DE CAJA'.center(60)}
{'='*60}
Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

{'='*60}
{'📈 RESUMEN DE VENTAS'.center(60)}
{'='*60}

• Total de Ventas: {total_sales}
• Monto Total de Ventas: {format_currency(total_amount)}
• Ticket Promedio: {format_currency(avg_ticket)}
• Clientes Atendidos: {unique_customers}
• Productos Vendidos: {total_products_sold}

{'='*60}
{'💰 INGRESOS MONETARIOS'.center(60)}
{'='*60}

• Total de Ingresos (Efectivo/Transferencias/Abonos): {format_currency(total_income)}

{'='*60}
{'🏆 PRODUCTOS MÁS VENDIDOS'.center(60)}
{'='*60}
"""

        if top_products:
            for i, (name, qty, amount) in enumerate(top_products[:5], 1):
                report_content += f"{i}. {name:<30} {qty:>3} unidades  {format_currency(amount):>10}\n"
        else:
            report_content += "No hay datos de productos vendidos.\n"

        report_content += f"""
{'='*60}
{'📦 ESTADO DEL INVENTARIO'.center(60)}
{'='*60}

• Total de Productos: {total_products}
• Valor Total del Inventario: {format_currency(inventory_value)}
• Productos con Stock Bajo (≤5): {low_stock_count}
• Productos Agotados: {out_of_stock_count}

{'='*60}
{'✅ CIERRE DE CAJA COMPLETADO'.center(60)}
{'='*60}
"""

        report_text.setPlainText(report_content)
        layout.addWidget(report_text)

        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        cancel_btn.clicked.connect(dialog.reject)

        close_btn = QPushButton("✅ Cerrar Caja y Guardar Reporte")
        close_btn.setStyleSheet("""
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
        close_btn.clicked.connect(lambda: self.confirm_cash_close(dialog, current_date, total_income, report_content))

        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(close_btn)
        layout.addLayout(buttons_layout)

        dialog.exec_()

    def confirm_cash_close(self, dialog, date, total_income, report_content):
        """Confirmar cierre de caja y guardar reporte"""
        try:
            # Guardar el registro de cierre en la base de datos
            self.db.insert_cash_close_record(date, total_income, report_content)

            QMessageBox.information(dialog, "✅ Caja Cerrada",
                                  f"Caja cerrada exitosamente para la fecha {date}.\n\n"
                                  f"Ingreso total registrado: {format_currency(total_income)}\n\n"
                                  f"El reporte detallado ha sido guardado.")

            dialog.accept()
            self.load_cash_data()  # Recargar datos

        except Exception as e:
            QMessageBox.critical(dialog, "Error de Cierre",
                               f"Error al guardar el cierre de caja:\n{e}")

    def show_daily_report(self):
        """Mostrar reporte diario"""
        current_date = datetime.now().strftime("%Y-%m-%d")

        try:
            # Obtener datos del día
            sales_summary = self.db.get_sales_summary(current_date, current_date)
            total_income = self.db.get_cash_register_income_summary(current_date)
            open_records = self.db.get_cash_open_records(current_date, current_date)

            # Crear diálogo de reporte
            dialog = QDialog(self.widget)
            dialog.setWindowTitle("📊 Reporte Diario")
            dialog.setModal(True)
            dialog.setFixedSize(600, 500)

            layout = QVBoxLayout(dialog)
            layout.setContentsMargins(20, 20, 20, 20)

            title = QLabel("📊 Reporte del Día")
            title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1e293b;")
            layout.addWidget(title)

            date_label = QLabel(f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y')}")
            date_label.setStyleSheet("font-size: 14px; color: #6b7280;")
            layout.addWidget(date_label)

            # Área de contenido
            content_text = QTextEdit()
            content_text.setReadOnly(True)
            content_text.setFont(QFont("Courier New", 10))

            report = f"""
{'='*50}
{'🏪 KIOSCO ARONIUM - REPORTE DIARIO'.center(50)}
{'='*50}
Fecha: {datetime.now().strftime('%d/%m/%Y')}

"""

            if open_records:
                report += f"🔓 Caja Abierta: {format_currency(open_records[0][2])}\n\n"
            else:
                report += "❌ Caja No Abierta\n\n"

            if sales_summary and len(sales_summary) >= 4:
                total_sales, total_amount, avg_ticket, unique_customers = sales_summary
                report += f"""📈 VENTAS DEL DÍA:
• Total de Ventas: {total_sales}
• Monto Total: {format_currency(total_amount)}
• Ticket Promedio: {format_currency(avg_ticket)}
• Clientes Atendidos: {unique_customers}

💰 INGRESOS MONETARIOS: {format_currency(total_income)}
"""
            else:
                report += "📈 No hay ventas registradas para hoy.\n"

            content_text.setPlainText(report)
            layout.addWidget(content_text)

            # Botón cerrar
            close_btn = QPushButton("✅ Cerrar")
            close_btn.clicked.connect(dialog.accept)
            layout.addWidget(close_btn)

            dialog.exec_()

        except Exception as e:
            QMessageBox.critical(self.widget, "Error", f"Error generando reporte:\n{str(e)}")

    def show_history_dialog(self):
        """Mostrar diálogo con historial completo"""
        dialog = QDialog(self.widget)
        dialog.setWindowTitle("📈 Historial Completo de Caja")
        dialog.setModal(True)
        dialog.setFixedSize(800, 600)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("📈 Historial Completo de Caja")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1e293b;")
        layout.addWidget(title)

        # Filtros
        filters_layout = QHBoxLayout()

        date_from_label = QLabel("Desde:")
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addMonths(-1))
        self.date_from.setCalendarPopup(True)

        date_to_label = QLabel("Hasta:")
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setCalendarPopup(True)

        type_combo = QLabel("Tipo:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Todos", "Aperturas", "Cierres"])

        filter_btn = QPushButton("🔍 Filtrar")
        filter_btn.clicked.connect(self.filter_history)

        filters_layout.addWidget(date_from_label)
        filters_layout.addWidget(self.date_from)
        filters_layout.addWidget(date_to_label)
        filters_layout.addWidget(self.date_to)
        filters_layout.addWidget(type_combo)
        filters_layout.addWidget(self.type_combo)
        filters_layout.addWidget(filter_btn)
        filters_layout.addStretch()

        layout.addLayout(filters_layout)

        # Tabla de historial
        self.full_history_table = QTableWidget()
        self.full_history_table.setColumnCount(5)
        self.full_history_table.setHorizontalHeaderLabels(["Fecha", "Tipo", "Monto", "Notas", "Hora"])

        header = self.full_history_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        self.full_history_table.setAlternatingRowColors(True)

        layout.addWidget(self.full_history_table)

        # Botón cerrar
        close_btn = QPushButton("✅ Cerrar")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        # Cargar datos iniciales
        self.filter_history()

        dialog.exec_()

    def filter_history(self):
        """Filtrar historial según criterios"""
        try:
            date_from = self.date_from.date().toString("yyyy-MM-dd")
            date_to = self.date_to.date().toString("yyyy-MM-dd")
            type_filter = self.type_combo.currentText()

            # Obtener datos
            opens = []
            closes = []

            if type_filter in ["Todos", "Aperturas"]:
                opens = self.db.get_cash_open_records(date_from, date_to)

            if type_filter in ["Todos", "Cierres"]:
                closes = self.db.get_cash_close_records(date_from, date_to)

            # Combinar y ordenar
            history = []

            for record in opens:
                history.append({
                    'date': record[1],
                    'type': 'Apertura',
                    'amount': record[2],
                    'notes': record[3] or '',
                    'time': record[4].split(' ')[1] if record[4] else ''
                })

            for record in closes:
                history.append({
                    'date': record[1],
                    'type': 'Cierre',
                    'amount': record[2],
                    'notes': record[3] or '',
                    'time': record[4].split(' ')[1] if record[4] else ''
                })

            # Ordenar por fecha y hora descendente
            history.sort(key=lambda x: (x['date'], x['time']), reverse=True)

            # Actualizar tabla
            self.full_history_table.setRowCount(len(history))

            for row, item in enumerate(history):
                self.full_history_table.setItem(row, 0, QTableWidgetItem(item['date']))
                self.full_history_table.setItem(row, 1, QTableWidgetItem(item['type']))
                self.full_history_table.setItem(row, 2, QTableWidgetItem(format_currency(item['amount'])))
                self.full_history_table.setItem(row, 3, QTableWidgetItem(item['notes']))
                self.full_history_table.setItem(row, 4, QTableWidgetItem(item['time']))

        except Exception as e:
            print(f"Error filtrando historial: {e}")

    def lighten_color(self, hex_color, factor=0.3):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        lighter = tuple(min(255, int(c + (255 - c) * factor)) for c in rgb)
        return f"#{lighter[0]:02x}{lighter[1]:02x}{lighter[2]:02x}"

    def darken_color(self, hex_color, factor=0.2):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darker = tuple(max(0, int(c * (1 - factor))) for c in rgb)
        return f"#{darker[0]:02x}{darker[1]:02x}{darker[2]:02x}"
