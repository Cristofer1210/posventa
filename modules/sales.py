from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QTableWidget, QTableWidgetItem, QLineEdit, QComboBox,
                             QHeaderView, QMessageBox, QFrame, QGroupBox, QSpinBox,
                             QScrollArea, QGridLayout, QSizePolicy, QInputDialog, QDialog, 
                             QDialogButtonBox, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from utils.formatters import format_currency
import random
from datetime import datetime 

# Clase para el botón de producto rápido (se mantiene)
class QuickProductButton(QPushButton):
    def __init__(self, name, price, code, parent=None):
        super().__init__(parent)
        self.code = code
        self.price = price
        self.setText(f"{name}\n{format_currency(price)}")
        self.setFont(QFont("Arial", 10))
        self.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6; 
                color: white; 
                border-radius: 8px; 
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        self.setMinimumHeight(60)

# Clase principal del Módulo de Ventas
class SalesModule:
    def __init__(self, db):
        self.db = db
        self.cart_items = []
        self.widget = QWidget()
        self.init_ui()
        
    def get_widget(self):
        return self.widget
        
    def on_enter(self):
        self.load_products()
        # Asegurarse de que el foco esté en el campo de código de barras al entrar
        self.barcode_input.setFocus()
        
    def on_leave(self):
        pass
        
    def init_ui(self):
        layout = QHBoxLayout(self.widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Panel izquierdo - Carrito de compras (60%)
        self.create_cart_panel(layout)
        
        # Panel derecho - Productos y búsqueda (40%)
        self.create_products_panel(layout)
        
    def create_cart_panel(self, layout):
        cart_frame = QFrame()
        cart_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_cart_layout = QVBoxLayout(cart_frame) 
        
        # --- Contenido superior con Scroll ---
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(16)

        # Header del carrito
        header_layout = QHBoxLayout()
        title = QLabel("🛒 Venta en Curso")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1e293b;")
        
        self.clear_btn = QPushButton("🗑️ Limpiar Todo")
        self.clear_btn.setProperty("class", "danger")
        self.clear_btn.clicked.connect(self.clear_cart)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.clear_btn)
        scroll_layout.addLayout(header_layout) 
        
        # Información de la venta
        info_group = QGroupBox("📋 Información de Venta")
        info_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        info_layout = QGridLayout(info_group)
        info_layout.setVerticalSpacing(12)
        info_layout.setHorizontalSpacing(12)
        
        info_layout.addWidget(QLabel("Cliente:"), 0, 0)
        self.client_combo = QComboBox()
        self.client_combo.addItems(["🧑 Consumidor Final", "⭐ Cliente Habitual", "🏢 Cliente Empresa"])
        info_layout.addWidget(self.client_combo, 0, 1)
        
        info_layout.addWidget(QLabel("Pago:"), 1, 0)
        self.payment_combo = QComboBox()
        self.payment_combo.addItems(["💵 Efectivo", "📱 Mercado Pago", "💳 Débito"])
        info_layout.addWidget(self.payment_combo, 1, 1)
        
        scroll_layout.addWidget(info_group)
        
        # Tabla del carrito
        cart_table_group = QGroupBox("📦 Productos en el Carrito")
        cart_table_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        cart_table_layout = QVBoxLayout(cart_table_group)
        
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(5)
        self.cart_table.setHorizontalHeaderLabels(["Producto", "Precio", "Cantidad", "Subtotal", ""])
        
        header = self.cart_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        self.cart_table.setAlternatingRowColors(True)
        self.cart_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        cart_table_layout.addWidget(self.cart_table)
        scroll_layout.addWidget(cart_table_group)

        # Envolver el contenido con ScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_content)
        main_cart_layout.addWidget(scroll_area, 1) # Peso 1 para que ocupe espacio variable
        
        # --- Footer Fijo (Totales y Botones) ---
        footer_frame = QFrame()
        footer_layout = QVBoxLayout(footer_frame)
        footer_layout.setContentsMargins(0, 10, 0, 0)
        footer_layout.setSpacing(12)
        
        # Panel de totales
        totals_frame = QFrame()
        totals_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #059669, stop:1 #10b981);
                border-radius: 12px;
                padding: 0px;
            }
        """)
        totals_layout = QVBoxLayout(totals_frame)
        totals_layout.setContentsMargins(24, 20, 24, 20)
        totals_layout.setSpacing(8)
        
        # Subtotal
        subtotal_widget = QWidget()
        subtotal_widget.setStyleSheet("background: transparent;")
        subtotal_layout = QHBoxLayout(subtotal_widget)
        subtotal_layout.setContentsMargins(0, 0, 0, 0)
        
        subtotal_label = QLabel("Subtotal:")
        subtotal_label.setStyleSheet("color: white; font-size: 16px; font-weight: 600;")
        self.subtotal_value = QLabel("$ 0.00")
        self.subtotal_value.setStyleSheet("color: white; font-size: 16px; font-weight: 600;")
        
        subtotal_layout.addWidget(subtotal_label)
        subtotal_layout.addStretch()
        subtotal_layout.addWidget(self.subtotal_value)
        
        # Total
        total_widget = QWidget()
        total_widget.setStyleSheet("background: transparent;")
        total_layout = QHBoxLayout(total_widget)
        total_layout.setContentsMargins(0, 0, 0, 0)
        
        total_label = QLabel("TOTAL A PAGAR:")
        total_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        self.total_value = QLabel("$ 0.00")
        self.total_value.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        
        total_layout.addWidget(total_label)
        total_layout.addStretch()
        total_layout.addWidget(self.total_value)
        
        totals_layout.addWidget(subtotal_widget)
        totals_layout.addWidget(total_widget)
        footer_layout.addWidget(totals_frame)
        
        # Botones de acción
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        self.cancel_btn = QPushButton("❌ Cancelar")
        self.cancel_btn.setProperty("class", "danger")
        self.cancel_btn.clicked.connect(self.clear_cart)
        
        # Botón de Apertura de Caja (Añadido)
        self.open_cash_btn = QPushButton("🔓 Apertura de Caja")
        self.open_cash_btn.setProperty("class", "primary")
        self.open_cash_btn.setStyleSheet("font-size: 14px; padding: 10px;")
        self.open_cash_btn.clicked.connect(self.open_cash_open_dialog)

        # Botón de Cierre de Caja (Añadido)
        self.close_cash_btn = QPushButton("💸 Cierre de Caja")
        self.close_cash_btn.setProperty("class", "secondary")
        self.close_cash_btn.setStyleSheet("font-size: 14px; padding: 10px;")
        self.close_cash_btn.clicked.connect(self.open_cash_close_dialog)

        self.process_btn = QPushButton("✅ COBRAR VENTA")
        self.process_btn.setProperty("class", "success")
        self.process_btn.setStyleSheet("font-size: 16px; font-weight: bold; padding: 14px;")
        self.process_btn.clicked.connect(self.process_sale)

        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.open_cash_btn) # Posición accesible
        button_layout.addWidget(self.close_cash_btn) # Posición accesible
        button_layout.addStretch()
        button_layout.addWidget(self.process_btn)
        
        footer_layout.addLayout(button_layout)
        
        main_cart_layout.addWidget(footer_frame) # Añadido al layout principal
        layout.addWidget(cart_frame, 3)

        # Conectar doble click para editar precios
        self.cart_table.cellDoubleClicked.connect(self.on_cart_item_double_click)
        
    def on_cart_item_double_click(self, row, column):
        """Permitir editar precios con doble click - CUMPLIDO"""
        if column == 1 and 0 <= row < len(self.cart_items): 
            item = self.cart_items[row]
            current_price = item['price']
        
            new_price, ok = QInputDialog.getDouble(
                self.widget, 
                "💰 Cambiar Precio", 
                f"Nuevo precio para:\n{item['name']}", 
                value=current_price, 
                decimals=2, 
                min=0.01,
                max=999999.99
            )
        
            if ok and new_price != current_price:
                item['price'] = new_price
                item['subtotal'] = item['quantity'] * new_price
                self.update_cart_display()
                self.show_quick_notification(f"✅ Precio actualizado: {format_currency(new_price)}")
    
    def open_cash_open_dialog(self):
        """Abre un diálogo para ejecutar la apertura de caja."""

        current_date = datetime.now().strftime("%Y-%m-%d")

        # Verificar si ya existe una apertura para hoy
        try:
            open_records = self.db.get_cash_open_records(start_date=current_date, end_date=current_date)
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
            except Exception as e:
                QMessageBox.critical(self.widget, "Error de Apertura", f"Error al guardar la apertura de caja:\n{e}")

    def open_cash_close_dialog(self):
        """Abre un diálogo para ejecutar el cierre de caja con reporte detallado."""

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
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QPushButton, QFrame, QGroupBox

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

        except Exception as e:
            QMessageBox.critical(dialog, "Error de Cierre",
                               f"Error al guardar el cierre de caja:\n{e}")


    def show_quick_notification(self, message):
        """Mostrar notificación rápida sin interrumpir el flujo"""
        print(f"📢 {message}") 

    def create_products_panel(self, layout):
        products_frame = QFrame()
        products_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        products_layout = QVBoxLayout(products_frame)
        products_layout.setSpacing(16)
        
        # Búsqueda rápida
        search_group = QGroupBox("🔍 Buscar Productos")
        search_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        search_layout = QVBoxLayout(search_group)
        search_layout.setSpacing(12)
        
        # Búsqueda por código de barras
        barcode_layout = QHBoxLayout()
        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("Escanear código de barras...")
        self.barcode_input.returnPressed.connect(self.search_by_barcode)
        barcode_btn = QPushButton("Buscar")
        barcode_btn.clicked.connect(self.search_by_barcode)
        
        barcode_layout.addWidget(self.barcode_input)
        barcode_layout.addWidget(barcode_btn)
        search_layout.addLayout(barcode_layout)
        
        # Búsqueda por nombre
        name_search_layout = QHBoxLayout()
        self.name_search_input = QLineEdit()
        self.name_search_input.setPlaceholderText("Buscar producto por nombre...")
        self.name_search_input.textChanged.connect(self.filter_products)
        clear_search_btn = QPushButton("X")
        clear_search_btn.setFixedWidth(30)
        clear_search_btn.setToolTip("Limpiar búsqueda")
        clear_search_btn.clicked.connect(self.clear_search)
        
        name_search_layout.addWidget(self.name_search_input)
        name_search_layout.addWidget(clear_search_btn)
        search_layout.addLayout(name_search_layout)
        
        products_layout.addWidget(search_group)
        

        
        # Lista de productos
        products_list_group = QGroupBox("📦 Todos los Productos")
        products_list_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        products_list_layout = QVBoxLayout(products_list_group)
        products_list_layout.setSpacing(12)
        
        # Filtros de categoría
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Categoría:"))
        self.category_filter = QComboBox()
        self.category_filter.addItems(["Todas", "Bebidas", "Snacks", "Cigarrillos", "Golosinas", "Lácteos", "Otros"])
        self.category_filter.currentTextChanged.connect(self.filter_products)
        filter_layout.addWidget(self.category_filter)
        filter_layout.addStretch()
        
        products_list_layout.addLayout(filter_layout)
        
        # Tabla de productos
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(4)
        self.products_table.setHorizontalHeaderLabels(["Producto", "Precio", "Stock", "Agregar"])
        
        header = self.products_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.resizeSection(3, 100)
        
        self.products_table.setAlternatingRowColors(True)
        self.products_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.products_table.setSortingEnabled(False)
        
        self.products_table.verticalHeader().setDefaultSectionSize(45)
        
        products_list_layout.addWidget(self.products_table)
        products_layout.addWidget(products_list_group)
        
        layout.addWidget(products_frame, 2)
        
    def load_products(self):
        """Cargar productos desde la base de datos REAL"""
        try:
            products_from_db = self.db.get_products()
        
            # Asumimos que la tupla de productos es: 
            # (id, code, name, category, buy_price, sell_price, stock, min_stock)
            self.all_products = []
            for product in products_from_db:
                product_id, code, name, category, buy_price, sell_price, stock, min_stock = product
                self.all_products.append((
                    product_id, name, sell_price, stock, code, category
                ))
        
            self.filter_products()
            
        except Exception as e:
            QMessageBox.critical(self.widget, "Error", f"Error al cargar productos:\n{str(e)}")
            self.all_products = []
            
    def filter_products(self):
        """Filtrar productos por categoría y búsqueda"""
        try:
            if not hasattr(self, 'all_products'):
                return
                
            category_filter = self.category_filter.currentText()
            search_text = self.name_search_input.text().strip().lower()
            
            filtered_products = []
            for product in self.all_products:
                product_id, name, price, stock, code, category = product
                
                if category_filter != "Todas" and category != category_filter:
                    continue
                    
                if search_text and search_text not in name.lower():
                    continue
                    
                filtered_products.append(product)
            
            # Actualizar tabla
            self.products_table.setRowCount(len(filtered_products))
            
            for row, product in enumerate(filtered_products):
                product_id, name, price, stock, code, category = product
                
                # Producto
                name_item = QTableWidgetItem(name)
                name_item.setData(Qt.UserRole, product_id)
                self.products_table.setItem(row, 0, name_item)
                
                # Precio
                price_item = QTableWidgetItem(format_currency(price))
                price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.products_table.setItem(row, 1, price_item)
                
                # Stock con indicador visual
                if stock == 0:
                    stock_text = "❌ Agotado"
                    stock_style = "color: #ef4444; font-weight: bold;"
                elif stock <= 5:
                    stock_text = f"⚠️ {stock}"
                    stock_style = "color: #f59e0b; font-weight: bold;"
                else:
                    stock_text = f"✅ {stock}"
                    stock_style = "color: #10b981; font-weight: bold;"
                
                stock_item = QTableWidgetItem(stock_text)
                stock_item.setTextAlignment(Qt.AlignCenter)
                stock_item.setData(Qt.UserRole, stock_style)
                self.products_table.setItem(row, 2, stock_item)
                
                # Botón agregar
                add_btn = QPushButton("➕ Agregar")
                add_btn.setFixedHeight(35)
                add_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #10b981;
                        color: white;
                        border: none;
                        border-radius: 6px;
                        font-weight: 600;
                        font-size: 12px;
                        padding: 8px;
                    }
                    QPushButton:hover {
                        background-color: #059669;
                    }
                    QPushButton:disabled {
                        background-color: #9ca3af;
                        color: #6b7280;
                    }
                """)
                add_btn.setEnabled(stock > 0)
                add_btn.clicked.connect(lambda checked, pid=product_id, n=name, p=price, s=stock: 
                                            self.add_to_cart(pid, n, p, s))
                self.products_table.setCellWidget(row, 3, add_btn)
                
        except Exception as e:
            print(f"Error filtrando productos: {e}")
            
    def clear_search(self):
        """Limpiar búsqueda"""
        self.name_search_input.clear()
        self.filter_products()
        
    def search_by_barcode(self):
        """Buscar producto por código de barras - MANTIENE EL FOCO - CUMPLIDO"""
        barcode = self.barcode_input.text().strip()
    
        if not barcode:
            QMessageBox.warning(self.widget, "Búsqueda vacía", "Ingresa un código de barras para buscar.")
            self.barcode_input.setFocus() 
            return
    
        product_found = False
        for product in self.all_products: 
            product_id, name, price, stock, code, category = product
            if code == barcode:
                self.add_to_cart(product_id, name, price, stock)
                self.barcode_input.clear()
                self.barcode_input.setFocus() # CLAVE: MANTENER EL FOCO
                product_found = True
                break
    
        if not product_found:
            QMessageBox.warning(self.widget, "Producto no encontrado", 
                                f"❌ No se encontró ningún producto con el código:\n{barcode}")
            self.barcode_input.selectAll() 
            self.barcode_input.setFocus() # CLAVE: MANTENER EL FOCO
            
    def add_to_cart(self, product_id, name, price, stock):
        """Agregar producto al carrito"""
        for item in self.cart_items:
            if item['product_id'] == product_id:
                if item['quantity'] >= stock:
                    QMessageBox.warning(self.widget, "Stock insuficiente", 
                                        f"❌ No hay suficiente stock de {name}\n\nStock disponible: {stock}")
                    return
                    
                item['quantity'] += 1
                item['subtotal'] = item['quantity'] * item['price']
                self.update_cart_display()
                return
                
        if stock <= 0:
            QMessageBox.warning(self.widget, "Sin stock", 
                                f"❌ El producto {name} está agotado")
            return
            
        self.cart_items.append({
            'product_id': product_id,
            'name': name,
            'price': price,
            'quantity': 1,
            'subtotal': price,
            'stock': stock
        })
        
        self.update_cart_display()
        
    def add_quick_product(self, name, price, code):
        """Agregar producto rápido al carrito"""
        for product in self.all_products:
            product_id, p_name, p_price, stock, p_code, category = product
            if p_code == code:
                self.add_to_cart(product_id, name, price, stock) 
                return
                
        QMessageBox.warning(self.widget, "Producto no disponible", 
                            f"El producto {name} no está disponible en este momento")
        
    def update_cart_display(self):
        """Actualizar la visualización del carrito"""
        self.cart_table.setRowCount(len(self.cart_items))
        
        for row, item in enumerate(self.cart_items):
            # Producto
            name_item = QTableWidgetItem(item['name'])
            self.cart_table.setItem(row, 0, name_item)
            
            # Precio unitario
            price_item = QTableWidgetItem(format_currency(item['price']))
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.cart_table.setItem(row, 1, price_item)
            
            # Cantidad con controles
            qty_widget = QWidget()
            qty_layout = QHBoxLayout(qty_widget)
            qty_layout.setContentsMargins(4, 2, 4, 2)
            qty_layout.setSpacing(4)
            
            minus_btn = QPushButton("-")
            minus_btn.setFixedSize(28, 28)
            minus_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ef4444; 
                    color: white; 
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #dc2626;
                }
            """)
            minus_btn.clicked.connect(lambda checked, r=row: self.decrease_quantity(r))
            
            qty_label = QLabel(str(item['quantity']))
            qty_label.setAlignment(Qt.AlignCenter)
            qty_label.setStyleSheet("font-weight: bold; padding: 0 8px; min-width: 30px;")
            qty_label.setMinimumWidth(30)
            
            plus_btn = QPushButton("+")
            plus_btn.setFixedSize(28, 28)
            plus_btn.setStyleSheet("""
                QPushButton {
                    background-color: #10b981; 
                    color: white; 
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #059669;
                }
            """)
            plus_btn.clicked.connect(lambda checked, r=row: self.increase_quantity(r))
            
            qty_layout.addWidget(minus_btn)
            qty_layout.addWidget(qty_label)
            qty_layout.addWidget(plus_btn)
            qty_layout.addStretch()
            
            self.cart_table.setCellWidget(row, 2, qty_widget)
            
            # Subtotal
            subtotal_item = QTableWidgetItem(format_currency(item['subtotal']))
            subtotal_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.cart_table.setItem(row, 3, subtotal_item)
            
            # Botón eliminar
            remove_btn = QPushButton("🗑️")
            remove_btn.setToolTip("Eliminar del carrito")
            remove_btn.setFixedSize(32, 32)
            remove_btn.setStyleSheet("""
                QPushButton {
                    background-color: #6b7280; 
                    color: white; 
                    border-radius: 6px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #4b5563;
                }
            """)
            remove_btn.clicked.connect(lambda checked, r=row: self.remove_from_cart(r))
            self.cart_table.setCellWidget(row, 4, remove_btn)
            
        self.update_totals()
        
    def increase_quantity(self, row):
        """Aumentar cantidad de un producto en el carrito"""
        if 0 <= row < len(self.cart_items):
            item = self.cart_items[row]
            if item['quantity'] < item['stock']:
                item['quantity'] += 1
                item['subtotal'] = item['quantity'] * item['price']
                self.update_cart_display()
            else:
                QMessageBox.warning(self.widget, "Stock insuficiente", 
                                    f"❌ No hay suficiente stock de {item['name']}\n\nStock disponible: {item['stock']}")
                
    def decrease_quantity(self, row):
        """Disminuir cantidad de un producto en el carrito"""
        if 0 <= row < len(self.cart_items):
            item = self.cart_items[row]
            if item['quantity'] > 1:
                item['quantity'] -= 1
                item['subtotal'] = item['quantity'] * item['price']
                self.update_cart_display()
            else:
                self.remove_from_cart(row)
                
    def remove_from_cart(self, row):
        """Eliminar producto del carrito"""
        if 0 <= row < len(self.cart_items):
            self.cart_items.pop(row)
            self.update_cart_display()
            
    def clear_cart(self):
        """Limpiar todo el carrito"""
        if self.cart_items:
            reply = QMessageBox.question(
                self.widget, 
                "Limpiar Carrito",
                "¿Estás seguro de que quieres limpiar todo el carrito?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.cart_items = []
                self.update_cart_display()
                
    def update_totals(self):
        """Actualizar totales de la venta - SIMPLIFICADO"""
        total = sum(item['subtotal'] for item in self.cart_items)
        
        self.subtotal_value.setText(format_currency(total))
        self.total_value.setText(format_currency(total))
        
    def process_sale(self):
        """Procesar la venta - VERSIÓN CORREGIDA y lista para Cuenta Corriente"""
        if not self.cart_items:
            QMessageBox.warning(self.widget, "Carrito Vacío", 
                                "🛒 No hay productos en el carrito.\n\nAgrega algunos productos antes de cobrar.")
            return
        
        # Verificar stock
        for item in self.cart_items:
            if item['quantity'] > item['stock']:
                QMessageBox.warning(self.widget, "Stock Insuficiente",
                                    f"❌ No hay suficiente stock de:\n{item['name']}\n\nStock disponible: {item['stock']}")
                return
            
        total = sum(item['subtotal'] for item in self.cart_items)
    
        # Mostrar resumen de venta
        items_summary = "\n".join([f"• {item['name']} x{item['quantity']} = {format_currency(item['subtotal'])}" 
                                    for item in self.cart_items])
    
        summary_text = f"""
📋 RESUMEN DE VENTA
    
👤 Cliente: {self.client_combo.currentText()}
💳 Pago: {self.payment_combo.currentText()}
    
🛒 Productos:
{items_summary}
    
💰 Total: {format_currency(total)}
"""
    
        reply = QMessageBox.question(
            self.widget, 
            "✅ Confirmar Venta",
            summary_text,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
    
        if reply == QMessageBox.Yes:
            try:
                # Usar el método de pago completo con emoji para mejor visualización en reportes
                payment_method = self.payment_combo.currentText()

                # Definir estado de pago
                if "Cuenta Corriente" in payment_method:
                    payment_status = "cuenta_corriente"
                else:
                    payment_status = "pagado"
                    
                sale_data = {
                    'total': total,
                    'payment_method': payment_method,
                    'payment_status': payment_status, # Añadido
                    'customer_type': self.client_combo.currentText()
                }
            
                # GUARDAR EN BASE DE DATOS
                sale_id = self.db.save_sale(sale_data, self.cart_items) 
            
                # Mostrar ticket
                ticket_text = self.print_ticket(sale_id, sale_data, self.cart_items, total)
            
                # Limpiar carrito y recargar productos
                self.clear_cart()
                self.load_products()
            
                current_time = datetime.now().strftime("%H:%M")

                QMessageBox.information(
                    self.widget, 
                    "✅ Venta Exitosa", 
                    f"Venta #{sale_id} procesada correctamente\n\nHora: {current_time}\nTotal: {format_currency(total)}"
                )
            
            except Exception as e:
                QMessageBox.critical(self.widget, "❌ Error", 
                                     f"Error al procesar la venta:\n{str(e)}")
                
    def print_ticket(self, sale_id, sale_data, items, total):
        """Generar y mostrar ticket de venta con opciones de personalización e impresión física"""

        # Importar el módulo de impresión de tickets
        from modules.ticket_printer import TicketCustomizationDialog

        # Crear diálogo de personalización e impresión
        dialog = TicketCustomizationDialog("", sale_data, items, total, self.widget)
        dialog.sale_data['id'] = sale_id  # Agregar ID de venta

        result = dialog.exec_()

        if result == dialog.Accepted:
            # El ticket ya fue procesado (impreso o solo vista previa)
            pass

        return ""
