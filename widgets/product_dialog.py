from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit,
                             QComboBox, QDoubleSpinBox, QSpinBox, QTextEdit,
                             QDialogButtonBox, QGroupBox, QLabel, QWidget, QHBoxLayout)
from PyQt5.QtCore import Qt

class ProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("➕ Nuevo Producto")
        self.setModal(True)
        self.setFixedSize(500, 550)  # Un poco más grande para mejor visualización
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # Título
        title_label = QLabel("Agregar Nuevo Producto")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #1e293b;
                padding: 10px 0px;
                background-color: #f8fafc;
                border-radius: 8px;
                text-align: center;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Información básica - MEJORADO
        basic_group = QGroupBox("📋 Información Básica del Producto")
        basic_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        basic_layout = QFormLayout(basic_group)
        basic_layout.setLabelAlignment(Qt.AlignRight)
        basic_layout.setVerticalSpacing(15)
        basic_layout.setHorizontalSpacing(20)
        basic_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Ingresar código de barras...")
        self.code_input.setMinimumHeight(35)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre completo del producto...")
        self.name_input.setMinimumHeight(35)

        # Categoría con posibilidad de agregar nuevas
        category_widget = QWidget()
        category_layout = QHBoxLayout(category_widget)
        category_layout.setContentsMargins(0, 0, 0, 0)

        self.category_combo = QComboBox()
        self.category_combo.setEditable(True)  # Permite escribir nuevas categorías
        self.category_combo.setMinimumHeight(35)

        self.load_categories()  # Cargar categorías existentes

        category_layout.addWidget(self.category_combo)

        basic_layout.addRow("Código:", self.code_input)
        basic_layout.addRow("Nombre:", self.name_input)
        basic_layout.addRow("Categoría:", category_widget)

        # Descripción - MEJORADA (sin corte de palabras)
        desc_label = QLabel("Descripción:")
        desc_label.setStyleSheet("font-weight: bold;")
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Descripción opcional del producto...")
        self.description_input.setMinimumHeight(100)  # Más alto para mejor visualización
        self.description_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
            }
            QTextEdit:focus {
                border: 1px solid #3b82f6;
            }
        """)
        self.description_input.setLineWrapMode(QTextEdit.WidgetWidth)  # Ajuste de texto mejorado

        basic_layout.addRow(desc_label, self.description_input)

        layout.addWidget(basic_group)

        # Precios y stock - MEJORADO
        price_group = QGroupBox("💰 Precios y Stock")
        price_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        price_layout = QFormLayout(price_group)
        price_layout.setLabelAlignment(Qt.AlignRight)
        price_layout.setVerticalSpacing(15)
        price_layout.setHorizontalSpacing(20)

        self.buy_price_input = QDoubleSpinBox()
        self.buy_price_input.setPrefix("$ ")
        self.buy_price_input.setMaximum(99999.99)
        self.buy_price_input.setDecimals(2)
        self.buy_price_input.setMinimumHeight(35)
        self.buy_price_input.setStyleSheet("padding: 5px;")

        self.sell_price_input = QDoubleSpinBox()
        self.sell_price_input.setPrefix("$ ")
        self.sell_price_input.setMaximum(99999.99)
        self.sell_price_input.setDecimals(2)
        self.sell_price_input.setMinimumHeight(35)
        self.sell_price_input.setStyleSheet("padding: 5px;")

        self.stock_input = QSpinBox()
        self.stock_input.setMaximum(9999)
        self.stock_input.setMinimumHeight(35)
        self.stock_input.setStyleSheet("padding: 5px;")

        price_layout.addRow("Precio de Compra:", self.buy_price_input)
        price_layout.addRow("Precio de Venta:", self.sell_price_input)
        price_layout.addRow("Stock Inicial:", self.stock_input)

        layout.addWidget(price_group)

        # Botones
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.setStyleSheet("""
            QDialogButtonBox {
                background-color: #f8fafc;
                padding: 10px;
                border-radius: 8px;
            }
        """)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        # Establecer valores por defecto
        self.stock_input.setValue(10)
        self.buy_price_input.setValue(0)
        self.sell_price_input.setValue(0)

    def load_categories(self):
        """Cargar categorías existentes desde la base de datos"""
        # Esto se conectará con la base de datos
        # Por ahora usamos categorías por defecto + cualquier nueva que se haya agregado
        default_categories = [
            "Bebidas", "Snacks", "Cigarrillos", "Golosinas",
            "Lácteos", "Panadería", "Limpieza", "Otros"
        ]

        self.category_combo.clear()
        self.category_combo.addItems(default_categories)

    def get_product_data(self):
        # Obtener el ID de la categoría si existe, o crear una nueva
        category_name = self.category_combo.currentText().strip()

        return {
            'code': self.code_input.text().strip(),
            'name': self.name_input.text().strip(),
            'category_name': category_name,  # Enviar nombre de categoría
            'description': self.description_input.toPlainText().strip(),
            'buy_price': self.buy_price_input.value(),
            'sell_price': self.sell_price_input.value(),
            'stock': self.stock_input.value()
        }
