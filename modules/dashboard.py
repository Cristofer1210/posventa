from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QGridLayout, QFrame, QGroupBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from utils.formatters import format_currency
from datetime import datetime


class DashboardModule:
    def __init__(self, db):
        self.db = db
        self.widget = QWidget()
        self.init_ui()

    def get_widget(self):
        return self.widget

    def on_enter(self):
        self.load_dashboard_data()

    def on_leave(self):
        pass

    def init_ui(self):
        layout = QVBoxLayout(self.widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        # 1. HEADER ELEGANTE
        self.create_header(layout)

        # 2. ACCESOS RÁPIDOS (Lo más importante)
        self.create_quick_access(layout)

        # 3. RESUMEN DEL DÍA (Solo lo esencial)
        self.create_daily_summary(layout)

        # 4. ALERTAS ÚTILES (Solo si hay problemas)
        self.create_smart_alerts(layout)

    def create_header(self, layout):
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)

        # Título principal
        title = QLabel("🏪 Centro de Control")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #1e293b; margin-bottom: 5px;")

        # Subtítulo dinámico
        self.subtitle = QLabel("Sistema listo para usar")
        self.subtitle.setStyleSheet("font-size: 16px; color: #64748b;")

        # Hora actual
        self.time_label = QLabel()
        self.time_label.setStyleSheet("font-size: 14px; color: #94a3b8;")
        self.update_time()

        # Timer para la hora
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_time)
        self.clock_timer.start(1000)

        header_layout.addWidget(title)
        header_layout.addWidget(self.subtitle)
        header_layout.addWidget(self.time_label)
        layout.addWidget(header_frame)

    def update_time(self):
        current_time = datetime.now().strftime("%A, %d %B %Y - %H:%M:%S")
        self.time_label.setText(f"🕒 {current_time}")

    def create_quick_access(self, layout):
        """Botones grandes para las funciones más usadas"""
        group = QGroupBox("🚀 Acceso Rápido")
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

        grid_layout = QGridLayout(group)
        grid_layout.setSpacing(15)

        # Botones principales - Solo las 4 funciones más importantes
        quick_actions = [
            ("💰 Nueva Venta", "Iniciar una venta rápida", "#10b981", "sales"),
            ("📦 Gestionar Productos", "Agregar o editar productos", "#3b82f6", "products"),
            ("📊 Ver Reportes", "Estadísticas y reportes", "#f59e0b", "reports"),
            ("💰 Gestión de Caja", "Administrar apertura y cierre de caja", "#8b5cf6", "cash")
        ]

        for i, (text, tooltip, color, action) in enumerate(quick_actions):
            btn = self.create_action_button(text, tooltip, color)
            btn.clicked.connect(lambda checked, a=action: self.handle_quick_action(a))
            grid_layout.addWidget(btn, i//2, i%2)

        layout.addWidget(group)

    def create_action_button(self, text, tooltip, color):
        btn = QPushButton(text)
        btn.setToolTip(tooltip)
        btn.setMinimumHeight(80)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {color}, stop:1 {self.lighten_color(color)});
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: bold;
                font-size: 16px;
                padding: 15px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {self.darken_color(color)}, stop:1 {color});
            }}
        """)
        return btn

    def create_daily_summary(self, layout):
        """Solo 3 métricas clave del día"""
        group = QGroupBox("📈 Resumen del Día")
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

        stats_layout = QHBoxLayout(group)
        stats_layout.setSpacing(15)

        # Solo 3 estadísticas importantes
        self.stats_cards = {}
        stats_config = [
            ("ventas_hoy", "💰 Ventas Hoy", "#10b981"),
            ("productos_vendidos", "📦 Productos Vendidos", "#3b82f6"),
            ("clientes_atendidos", "👥 Clientes Atendidos", "#f59e0b")
        ]

        for key, title, color in stats_config:
            card = self.create_stat_card(title, "0", color)
            stats_layout.addWidget(card)
            self.stats_cards[key] = card.findChild(QLabel, "value")

        layout.addWidget(group)

    def create_stat_card(self, title, value, color):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: white;
                border: 2px solid {color};
                border-radius: 10px;
                padding: 0px;
            }}
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)

        # Título
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: 600;")

        # Valor
        value_label = QLabel(value)
        value_label.setObjectName("value")
        value_label.setStyleSheet("color: #1e293b; font-size: 24px; font-weight: bold;")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()

        return frame

    def create_smart_alerts(self, layout):
        """Solo muestra alertas si hay problemas reales"""
        self.alerts_group = QGroupBox("🔔 Alertas del Sistema")
        self.alerts_group.setStyleSheet("""
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

        self.alerts_layout = QVBoxLayout(self.alerts_group)
        layout.addWidget(self.alerts_group)

    def load_dashboard_data(self):
        """Cargar datos simples y rápidos"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")

            # Obtener datos básicos del día
            sales_data = self.db.get_sales_summary(today, today)

            if sales_data:
                ventas, monto, ticket_promedio, clientes = sales_data

                # Actualizar estadísticas
                if 'ventas_hoy' in self.stats_cards:
                    self.stats_cards['ventas_hoy'].setText(format_currency(monto))
                if 'productos_vendidos' in self.stats_cards:
                    self.stats_cards['productos_vendidos'].setText(str(ventas))
                if 'clientes_atendidos' in self.stats_cards:
                    self.stats_cards['clientes_atendidos'].setText(str(clientes))

            # Verificar alertas importantes
            self.check_alerts()

            # Actualizar subtítulo según la hora
            self.update_welcome_message()

        except Exception as e:
            print(f"Error cargando dashboard: {e}")

    def check_alerts(self):
        """Verificar solo alertas críticas"""
        # Limpiar alertas anteriores
        while self.alerts_layout.count():
            child = self.alerts_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        alerts = []

        try:
            # 1. Verificar stock bajo
            low_stock = self.db.get_low_stock_count()
            if low_stock > 0:
                alerts.append(f"⚠️ {low_stock} productos con stock bajo")

            # 2. Verificar si no hay productos
            total_products = self.db.get_total_products()
            if total_products == 0:
                alerts.append("📦 No hay productos cargados en el sistema")

            # 3. Mostrar alertas o mensaje positivo
            if alerts:
                for alert in alerts:
                    alert_label = QLabel(alert)
                    alert_label.setStyleSheet("""
                        QLabel {
                            color: #dc2626;
                            font-weight: 600;
                            padding: 8px;
                            background-color: #fef2f2;
                            border-radius: 6px;
                            border: 1px solid #fecaca;
                        }
                    """)
                    self.alerts_layout.addWidget(alert_label)
            else:
                # Todo está bien
                success_label = QLabel("✅ Todo en orden - Sistema funcionando correctamente")
                success_label.setStyleSheet("""
                    QLabel {
                        color: #059669;
                        font-weight: 600;
                        padding: 8px;
                        background-color: #f0fdf4;
                        border-radius: 6px;
                        border: 1px solid #bbf7d0;
                    }
                """)
                self.alerts_layout.addWidget(success_label)

        except Exception as e:
            print(f"Error verificando alertas: {e}")

    def update_welcome_message(self):
        """Mensaje de bienvenida según la hora"""
        hour = datetime.now().hour

        if hour < 12:
            message = "¡Buenos días! Que tengas un gran día de ventas 🌞"
        elif hour < 18:
            message = "¡Buenas tardes! El sistema está funcionando perfectamente ☀️"
        else:
            message = "¡Buenas noches! Revisa el cierre del día 🌙"

        self.subtitle.setText(message)

    def handle_quick_action(self, action):
        """Manejar clicks en botones de acceso rápido"""
        # Cambiar de módulo en la aplicación principal
        # Necesitamos acceder al parent (ModernPOS) para cambiar módulos
        parent = self.widget.parent()
        while parent and not hasattr(parent, 'show_module'):
            parent = parent.parent()
        if parent and hasattr(parent, 'show_module'):
            parent.show_module(action)
        else:
            print(f"Acción rápida: {action} (no se pudo cambiar módulo)")

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
