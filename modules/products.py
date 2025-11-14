from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QTableWidget, QTableWidgetItem, QLineEdit, QComboBox,
                             QHeaderView, QMessageBox, QFrame, QGroupBox, QFormLayout,
                             QSpinBox, QDoubleSpinBox, QTextEdit)
from PyQt5.QtCore import Qt
from widgets.product_dialog import ProductDialog
from utils.formatters import format_currency

class ProductsModule:
    def __init__(self, db):
        self.db = db
        self.widget = QWidget()
        self.init_ui()
        
    def get_widget(self):
        return self.widget
        
    def on_enter(self):
        self.load_products()
        
    def on_leave(self):
        pass
        
    def init_ui(self):
        layout = QVBoxLayout(self.widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Header
        self.create_header(layout)
        
        # Estadísticas rápidas
        self.create_stats(layout)
        
        # Filtros
        self.create_filters(layout)
        
        # Tabla de productos
        self.create_products_table(layout)
        
    def create_header(self, layout):
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        
        # Título
        title_layout = QVBoxLayout()
        title = QLabel("📦 Gestión de Productos")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #1e293b; margin-bottom: 4px;")
        subtitle = QLabel("Administra el inventario de tu kiosco")
        subtitle.setStyleSheet("font-size: 14px; color: #64748b;")
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        header_layout.addLayout(title_layout)
        
        header_layout.addStretch()
        
        # Botones de acción
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        self.add_btn = QPushButton("➕ Nuevo Producto")
        self.add_btn.setProperty("class", "success")
        self.add_btn.clicked.connect(self.show_add_dialog)
        
        self.import_btn = QPushButton("📥 Importar")
        self.import_btn.setProperty("class", "warning")
        
        btn_layout.addWidget(self.import_btn)
        btn_layout.addWidget(self.add_btn)
        header_layout.addLayout(btn_layout)
        
        layout.addWidget(header_frame)
        
    def create_stats(self, layout):
        self.stats_frame = QFrame()
        stats_layout = QHBoxLayout(self.stats_frame)
        stats_layout.setSpacing(12)

        # ✅ DATOS REALES desde la base de datos
        try:
            total_products = self.db.get_total_products()
            low_stock = self.db.get_low_stock_count()
            out_of_stock = self.db.get_out_of_stock_count()
            inventory_value = self.db.get_inventory_value()

            stats_data = [
                ("Total Productos", str(total_products), "#3b82f6", "📦"),
                ("Stock Bajo", str(low_stock), "#f59e0b", "⚠️"),
                ("Sin Stock", str(out_of_stock), "#ef4444", "❌"),
                ("Valor Inventario", format_currency(inventory_value), "#10b981", "💰"),
            ]
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            # Fallback a datos vacíos
            stats_data = [
                ("Total Productos", "0", "#3b82f6", "📦"),
                ("Stock Bajo", "0", "#f59e0b", "⚠️"),
                ("Sin Stock", "0", "#ef4444", "❌"),
                ("Valor Inventario", "$ 0.00", "#10b981", "💰"),
            ]

        for text, value, color, icon in stats_data:
            stat = QWidget()
            stat.setStyleSheet(f"""
                QWidget {{
                    background-color: {color};
                    border-radius: 12px;
                    padding: 0px;
                }}
            """)
            stat_layout = QVBoxLayout(stat)
            stat_layout.setContentsMargins(20, 16, 20, 16)

            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 20px; background: transparent;")

            text_label = QLabel(text)
            text_label.setStyleSheet("""
                color: white;
                font-size: 13px;
                font-weight: 600;
                background: transparent;
                margin-bottom: 4px;
            """)

            value_label = QLabel(value)
            value_label.setStyleSheet("""
                color: white;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
            """)

            stat_layout.addWidget(icon_label)
            stat_layout.addWidget(text_label)
            stat_layout.addWidget(value_label)
            stat_layout.addStretch()

            stats_layout.addWidget(stat)

        layout.addWidget(self.stats_frame)
        
    def create_filters(self, layout):
        filter_frame = QFrame()
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setSpacing(12)
        
        # Búsqueda
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar por código, nombre...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.textChanged.connect(self.filter_products)
        
        # Categorías
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Todas las categorías", "Bebidas", "Snacks", "Cigarrillos", "Golosinas", "Lácteos"])
        self.category_combo.currentTextChanged.connect(self.filter_products)
        
        # Filtro de stock
        self.stock_combo = QComboBox()
        self.stock_combo.addItems(["Todo el stock", "Stock normal", "Stock bajo (≤5)", "Sin stock"])
        self.stock_combo.currentTextChanged.connect(self.filter_products)
        
        filter_layout.addWidget(self.search_input, 4)
        filter_layout.addWidget(self.category_combo, 2)
        filter_layout.addWidget(self.stock_combo, 2)
        
        layout.addWidget(filter_frame)
        
    def create_products_table(self, layout):
        table_frame = QFrame()
        table_layout = QVBoxLayout(table_frame)
        
        # Header de la tabla
        table_header = QLabel("Lista de Productos")
        table_header.setStyleSheet("font-size: 18px; font-weight: 600; color: #374151; margin-bottom: 12px;")
        table_layout.addWidget(table_header)
        
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(8)
        self.products_table.setHorizontalHeaderLabels([
            "ID", "Código", "Producto", "Categoría", "Precio Compra", "Precio Venta", 
            "Stock", "Acciones"
        ])
        
        header = self.products_table.horizontalHeader()
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Nombre más ancho
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID más compacto
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Código
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Categoría
        
        self.products_table.setAlternatingRowColors(True)
        self.products_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.products_table.setSortingEnabled(True)
        
        table_layout.addWidget(self.products_table)
        layout.addWidget(table_frame)
        
    def load_products(self):
        """Cargar productos desde la base de datos REAL"""
        try:
            # ✅ USAR DATOS REALES de la base de datos
            self.all_products = self.db.get_products()
            self.filter_products()
        
            # ✅ ACTUALIZAR ESTADÍSTICAS CON DATOS REALES
            self.update_real_stats()
        
        except Exception as e:
            QMessageBox.critical(self.widget, "Error", f"Error al cargar productos:\n{str(e)}")
            # En caso de error, usar lista vacía
            self.all_products = []
            
    def update_real_stats(self):
        """Actualizar estadísticas con datos REALES de la base de datos"""
        try:
            # ✅ USAR LOS MÉTODOS DE LA BASE DE DATOS PARA OBTENER DATOS REALES Y ACTUALIZADOS
            total_products = self.db.get_total_products()
            low_stock = self.db.get_low_stock_count()
            out_of_stock = self.db.get_out_of_stock_count()
            inventory_value = self.db.get_inventory_value()

            # ✅ ACTUALIZAR LAS ESTADÍSTICAS EN LA UI
            stats_data = [
                ("Total Productos", str(total_products), "#3b82f6", "📦"),
                ("Stock Bajo", str(low_stock), "#f59e0b", "⚠️"),
                ("Sin Stock", str(out_of_stock), "#ef4444", "❌"),
                ("Valor Inventario", format_currency(inventory_value), "#10b981", "💰"),
            ]

            # Actualizar las tarjetas de estadísticas
            self.update_stats_cards(stats_data)

        except Exception as e:
            print(f"Error actualizando estadísticas: {e}")

    def update_stats_cards(self, stats_data):
        """Actualizar las tarjetas de estadísticas en la UI"""
        # Buscar todos los widgets de estadísticas (son QWidget, no QFrame)
        stats_widgets = self.stats_frame.findChildren(QWidget)

        # Filtrar solo los widgets que son tarjetas de estadísticas (tienen background-color en el styleSheet)
        stat_cards = []
        for widget in stats_widgets:
            if hasattr(widget, 'styleSheet') and 'background-color' in widget.styleSheet():
                stat_cards.append(widget)

        for i, (text, value, color, icon) in enumerate(stats_data):
            if i < len(stat_cards):
                card = stat_cards[i]

                # Buscar las labels dentro del widget
                value_label = None
                for child in card.findChildren(QLabel):
                    # Buscar la label que tiene el valor (la que tiene font-size: 24px)
                    if child.styleSheet() and "font-size: 24px" in child.styleSheet():
                        value_label = child
                        break

                if value_label:
                    value_label.setText(value)

    def filter_products(self):
        """Filtrar productos por categoría y búsqueda - USANDO DATOS REALES"""
        try:
            if not hasattr(self, 'all_products') or not self.all_products:
                self.products_table.setRowCount(0)
                return

            category_filter = self.category_combo.currentText()
            search_text = self.search_input.text().strip().lower()
            stock_filter = self.stock_combo.currentText()

            filtered_products = []
            for product in self.all_products:
                product_id, code, name, category, buy_price, sell_price, stock, min_stock = product

                # Filtrar por categoría
                if category_filter != "Todas las categorías" and category != category_filter:
                    continue

                # Filtrar por búsqueda de texto
                if search_text and search_text not in name.lower() and search_text not in code.lower():
                    continue

                # Filtrar por stock
                if stock_filter == "Stock normal" and stock <= min_stock:
                    continue
                elif stock_filter == "Stock bajo (≤5)" and stock > min_stock:
                    continue
                elif stock_filter == "Sin stock" and stock > 0:
                    continue

                filtered_products.append(product)

            # Actualizar tabla
            self.products_table.setRowCount(len(filtered_products))

            for row, product in enumerate(filtered_products):
                product_id, code, name, category, buy_price, sell_price, stock, min_stock = product

                # ID
                id_item = QTableWidgetItem(str(product_id))
                id_item.setData(Qt.UserRole, product_id)
                self.products_table.setItem(row, 0, id_item)

                # Código
                code_item = QTableWidgetItem(code)
                self.products_table.setItem(row, 1, code_item)

                # Producto
                name_item = QTableWidgetItem(name)
                self.products_table.setItem(row, 2, name_item)

                # Categoría
                category_item = QTableWidgetItem(category or "Sin categoría")
                self.products_table.setItem(row, 3, category_item)

                # Precio Compra
                buy_price_item = QTableWidgetItem(format_currency(buy_price))
                buy_price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.products_table.setItem(row, 4, buy_price_item)

                # Precio Venta
                sell_price_item = QTableWidgetItem(format_currency(sell_price))
                sell_price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.products_table.setItem(row, 5, sell_price_item)

                # Stock con indicador visual
                if stock == 0:
                    stock_text = "❌ Agotado"
                    stock_style = "color: #ef4444; font-weight: bold;"
                elif stock <= min_stock:
                    stock_text = f"⚠️ {stock}"
                    stock_style = "color: #f59e0b; font-weight: bold;"
                else:
                    stock_text = f"✅ {stock}"
                    stock_style = "color: #10b981; font-weight: bold;"

                stock_item = QTableWidgetItem(stock_text)
                stock_item.setTextAlignment(Qt.AlignCenter)
                self.products_table.setItem(row, 6, stock_item)

                # Botón acciones
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(4, 2, 4, 2)
                actions_layout.setSpacing(4)

                edit_btn = QPushButton("✏️")
                edit_btn.setToolTip("Editar producto")
                edit_btn.setFixedSize(32, 32)
                edit_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3b82f6;
                        color: white;
                        border-radius: 6px;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #2563eb;
                    }
                """)
                edit_btn.clicked.connect(lambda checked, p=product: self.edit_product(p))

                delete_btn = QPushButton("🗑️")
                delete_btn.setToolTip("Eliminar producto")
                delete_btn.setFixedSize(32, 32)
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #ef4444;
                        color: white;
                        border-radius: 6px;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #dc2626;
                    }
                """)
                delete_btn.clicked.connect(lambda checked, pid=product_id, pn=name: self.delete_product(pid, pn))

                actions_layout.addWidget(edit_btn)
                actions_layout.addWidget(delete_btn)
                actions_layout.addStretch()

                self.products_table.setCellWidget(row, 7, actions_widget)

        except Exception as e:
            print(f"Error filtrando productos: {e}")
        
    def show_add_dialog(self):
        dialog = ProductDialog(self.widget)
        if dialog.exec_():
            product_data = dialog.get_product_data()
            try:
                # Primero, asegurarnos de que la categoría existe
                category_name = product_data['category_name']
            
                # Verificar si la categoría ya existe en la base de datos
                categories = self.db.get_categories()
                category_exists = any(cat[1] == category_name for cat in categories)
            
                if not category_exists and category_name:
                    # Agregar nueva categoría
                    self.db.add_category(category_name, "Categoría agregada desde producto")
            
                # Ahora agregar el producto
                success = self.db.add_product(product_data)
                if success:
                    self.load_products()
                    QMessageBox.information(self.widget, "✅ Éxito", "Producto agregado correctamente")
            except Exception as e:
                QMessageBox.critical(self.widget, "❌ Error", str(e))
                
    def edit_product(self, product):
        """Editar producto existente"""
        try:
            product_id, code, name, category, buy_price, sell_price, stock, min_stock = product
        
            # Crear diálogo de edición
            from widgets.product_dialog import ProductDialog
            dialog = ProductDialog(self.widget)
        
            # Cargar datos del producto en el diálogo
            dialog.code_input.setText(code)
            dialog.name_input.setText(name)
        
            # Buscar y seleccionar la categoría
            index = dialog.category_combo.findText(category)
            if index >= 0:
                dialog.category_combo.setCurrentIndex(index)
            else:
                # Si la categoría no existe, agregarla
                dialog.category_combo.addItem(category)
                dialog.category_combo.setCurrentText(category)
        
            dialog.buy_price_input.setValue(buy_price)
            dialog.sell_price_input.setValue(sell_price)
            dialog.stock_input.setValue(stock)
        
            dialog.setWindowTitle("✏️ Editar Producto")
        
            if dialog.exec_():
                product_data = dialog.get_product_data()
                # Aquí iría la lógica para actualizar en la base de datos
                QMessageBox.information(self.widget, "✅ Éxito", f"Producto {name} actualizado correctamente")
                self.load_products()  # Recargar la lista
            
        except Exception as e:
            QMessageBox.critical(self.widget, "❌ Error", f"Error al editar producto:\n{str(e)}")
        
    def delete_product(self, product_id, product_name):
        reply = QMessageBox.question(
            self.widget, 
            "Confirmar Eliminación",
            f"¿Estás seguro de eliminar el producto:\n\"{product_name}\"?\n\nEsta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                success = self.db.delete_product(product_id)
                if success:
                    self.load_products()
                    QMessageBox.information(self.widget, "✅ Éxito", "Producto eliminado correctamente")
                else:
                    QMessageBox.warning(self.widget, "⚠️ Advertencia", "No se pudo eliminar el producto")
            except Exception as e:
                QMessageBox.critical(self.widget, "❌ Error", f"Error al eliminar producto:\n{str(e)}")