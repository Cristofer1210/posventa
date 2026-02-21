import sys
import locale
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor
from database import Database
from login_dialog import LoginDialog

from modules.dashboard import DashboardModule
from modules.products import ProductsModule
from modules.sales import SalesModule
from modules.reports import ReportsModule
from modules.cash import CashModule

class ModernPOS(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.current_module = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("🏪 Mi Emprendimiento - Sistema para Kiosco")
        self.setGeometry(100, 100, 1400, 800)
        self.setMinimumSize(1200, 700)
        
        self.apply_modern_style()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.create_sidebar(main_layout)
        
        self.content_area = QStackedWidget()
        main_layout.addWidget(self.content_area)
        
        self.init_modules()
        self.show_dashboard()
        
    def apply_modern_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8fafc;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
            
            QWidget#sidebar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e293b, stop:1 #334155);
                border: none;
            }
            
            QPushButton#nav_button {
                background: transparent;
                color: #cbd5e1;
                text-align: left;
                padding: 16px 24px;
                border: none;
                border-radius: 0px;
                font-size: 14px;
                font-weight: 500;
                margin: 2px 8px;
            }
            
            QPushButton#nav_button:hover {
                background: rgba(255, 255, 255, 0.1);
                color: #ffffff;
            }
            
            QPushButton#nav_button:checked {
                background: rgba(255, 255, 255, 0.15);
                color: #60a5fa;
                border-left: 4px solid #60a5fa;
            }
        """)
        
    def create_sidebar(self, main_layout):
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(300)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Logo y marca
        logo_frame = QWidget()
        logo_frame.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e40af, stop:1 #3b82f6);")
        logo_layout = QVBoxLayout(logo_frame)
        logo_label = QLabel("🏪 MI EMPRENDIMIENTO")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 30px 20px;
                background: transparent;
            }
        """)
        logo_layout.addWidget(logo_label)
        sidebar_layout.addWidget(logo_frame)
        
        # Navegación principal
        nav_frame = QWidget()
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(8, 20, 8, 20)
        nav_layout.setSpacing(4)
        
        nav_buttons = [
            ("📊 Dashboard", "dashboard"),
            ("📦 Productos", "products"),
            ("💰 Ventas", "sales"),
            ("💰 Caja", "cash"),
            ("📈 Reportes", "reports"),
        ]
        
        self.nav_buttons_group = []
        for text, module_name in nav_buttons:
            btn = QPushButton(text)
            btn.setObjectName("nav_button")
            btn.setCheckable(True)
            btn.setProperty("module", module_name)
            btn.clicked.connect(lambda checked, m=module_name: self.show_module(m))
            nav_layout.addWidget(btn)
            self.nav_buttons_group.append(btn)
        
        sidebar_layout.addWidget(nav_frame)
        sidebar_layout.addStretch()
        
        # Footer de sesión con reloj en tiempo real
        footer_frame = QWidget()
        footer_frame.setStyleSheet("background: #1e293b;")
        footer_layout = QVBoxLayout(footer_frame)
        
        self.session_time_label = QLabel()
        self.session_time_label.setStyleSheet("""
            QLabel {
                color: #cbd5e1;
                font-size: 12px;
                padding: 20px;
                background: transparent;
                line-height: 1.4;
            }
        """)
        self.session_time_label.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(self.session_time_label)
        sidebar_layout.addWidget(footer_frame)
        
        # Actualizar reloj cada segundo
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.update_clock()  # Actualizar inmediatamente
        
        main_layout.addWidget(sidebar)
        
    def update_clock(self):
        """Actualizar el reloj en tiempo real"""
        from datetime import datetime
        current_time = datetime.now()
        time_text = f"🟢 En línea\n👤 Usuario: Admin\n📅 {current_time.strftime('%d de %B de %Y %H:%M:%S')}"
        self.session_time_label.setText(time_text)
        
    def init_modules(self):
        """Inicializar todos los módulos"""
        self.modules = {
            'dashboard': DashboardModule(self.db),
            'products': ProductsModule(self.db),
            'sales': SalesModule(self.db),
            'cash': CashModule(self.db),
            'reports': ReportsModule(self.db)
        }
        
        for name, module in self.modules.items():
            module_widget = module.get_widget()
            module_widget.setObjectName("content")
            self.content_area.addWidget(module_widget)
            
    def show_module(self, module_name):
        """Mostrar módulo específico"""
        if module_name in self.modules:
            module = self.modules[module_name]
            if self.current_module:
                self.current_module.on_leave()
            
            self.current_module = module
            module.on_enter()
            
            index = list(self.modules.keys()).index(module_name)
            self.content_area.setCurrentIndex(index)
            self.update_nav_buttons(module_name)
            
    def show_dashboard(self):
        self.show_module('dashboard')
        
    def show_products(self):
        self.show_module('products')
        
    def show_sales(self):
        self.show_module('sales')
        
    def show_reports(self):
        self.show_module('reports')

    def show_cash(self):
        self.show_module('cash')
        
    def update_nav_buttons(self, module_name):
        for btn in self.nav_buttons_group:
            btn.setChecked(btn.property("module") == module_name)
            
    def check_cash_opening(self):
        """Verificar si la caja está abierta y no cerrada para hoy"""
        from datetime import datetime
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        try:
            # Verificar aperturas y cierres para hoy
            cash_opens = self.db.get_cash_open_records(today, today)
            cash_closes = self.db.get_cash_close_records(today, today)
            
            if cash_opens and not cash_closes:
                # ✅ CASO: Hay apertura Y NO hay cierre (caja ABIERTA)
                opening_amount = cash_opens[0][2]
                QMessageBox.information(self, "Caja Abierta",
                    f"✅ La caja está ABIERTA para hoy ({today}).\n\n"
                    f"💰 Monto inicial: ${opening_amount:.2f}\n"
                    f"🟢 Puede comenzar a operar.")
                return
                
            elif cash_opens and cash_closes:
                # ⚠️ CASO: Hay apertura Y cierre (caja CERRADA)
                opening_amount = cash_opens[0][2]
                closing_amount = cash_closes[0][2]
                
                # Mostrar mensaje informativo
                QMessageBox.warning(self, "Caja Cerrada",
                    f"🔒 La caja del día {today} ya fue CERRADA.\n\n"
                    f"💰 Monto inicial: ${opening_amount:.2f}\n"
                    f"💵 Ingresos registrados: ${closing_amount:.2f}\n\n"
                    f"📊 Puede ver el detalle en el módulo 'Caja'.\n"
                    f"🔄 Si necesita operar hoy, debe realizar una NUEVA APERTURA.")
                
            elif not cash_opens:
                # 🆕 CASO: No hay apertura para hoy
                reply = QMessageBox.question(self, "Apertura de Caja Requerida",
                    f"❌ No hay apertura de caja para hoy ({today}).\n\n"
                    f"¿Desea realizar la apertura ahora?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes)
                
                if reply == QMessageBox.Yes:
                    self.open_cash_open_dialog()
                else:
                    QMessageBox.information(self, "Recordatorio",
                        "Puede abrir la caja en cualquier momento desde el módulo 'Caja'.\n"
                        "⚠️ Recuerde que NO podrá registrar ventas sin tener la caja abierta.")
        
        except Exception as e:
            print(f"Error en check_cash_opening: {e}")
            QMessageBox.warning(self, "Error",
                f"Error al verificar estado de caja:\n{str(e)}")

    def open_cash_open_dialog(self):
        """Mostrar diálogo para apertura de caja - VERSIÓN CORREGIDA"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
        from PyQt5.QtCore import Qt
        from datetime import datetime

        today = datetime.now().strftime("%Y-%m-%d")
        
        # ⚠️ NUEVO: Verificar estado actual de caja
        try:
            cash_opens = self.db.get_cash_open_records(today, today)
            cash_closes = self.db.get_cash_close_records(today, today)
            
            if cash_opens and not cash_closes:
                # Caso: Ya está abierta
                QMessageBox.warning(self, "Caja ya abierta",
                    f"⚠️ La caja ya está ABIERTA para hoy.\n"
                    f"No es necesario abrirla nuevamente.")
                return
                
            elif cash_opens and cash_closes:
                # Caso: Estaba abierta y cerrada (puede reabrir)
                reply = QMessageBox.question(self, "Reapertura de Caja",
                    f"⚠️ La caja del día {today} fue abierta y cerrada anteriormente.\n\n"
                    f"¿Desea realizar una NUEVA APERTURA?",
                    QMessageBox.Yes | QMessageBox.No)
                
                if reply == QMessageBox.No:
                    return
        except Exception as e:
            print(f"Error verificando estado de caja: {e}")

        # Continuar con el diálogo normal
        dialog = QDialog(self)
        dialog.setWindowTitle("🔓 Apertura de Caja")
        dialog.setModal(True)
        dialog.setFixedSize(400, 300)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Título
        title = QLabel("💰 Apertura de Caja del Día")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e293b;")
        layout.addWidget(title)

        # Fecha actual
        today_str = datetime.now().strftime("%d de %B de %Y")
        date_label = QLabel(f"📅 Fecha: {today_str}")
        date_label.setAlignment(Qt.AlignCenter)
        date_label.setStyleSheet("font-size: 14px; color: #6b7280;")
        layout.addWidget(date_label)

        # Monto inicial
        amount_label = QLabel("💵 Monto inicial en caja:")
        amount_label.setStyleSheet("font-weight: bold; color: #374151;")
        layout.addWidget(amount_label)

        self.opening_amount_input = QLineEdit()
        self.opening_amount_input.setPlaceholderText("0.00")
        self.opening_amount_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
            }
        """)
        layout.addWidget(self.opening_amount_input)

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

        open_btn = QPushButton("🔓 Abrir Caja")
        open_btn.setStyleSheet("""
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
        open_btn.clicked.connect(lambda: self.confirm_cash_open(dialog))

        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(open_btn)
        layout.addLayout(buttons_layout)

        dialog.exec_()

    def confirm_cash_open(self, dialog):
        """Confirmar apertura de caja - VERSIÓN CORREGIDA"""
        try:
            amount_text = self.opening_amount_input.text().strip()
            if not amount_text:
                QMessageBox.warning(dialog, "Monto Requerido",
                                "Por favor ingrese el monto inicial de la caja.")
                return

            amount = float(amount_text)
            if amount < 0:
                QMessageBox.warning(dialog, "Monto Inválido",
                                "El monto inicial no puede ser negativo.")
                return

            # Registrar apertura de caja
            from datetime import datetime
            today = datetime.now().strftime("%Y-%m-%d")
            
            # ⚠️ NUEVO: Verificar estado actual antes de insertar
            try:
                # Verificar aperturas existentes
                cash_opens = self.db.get_cash_open_records(today, today)
                cash_closes = self.db.get_cash_close_records(today, today)
                
                if cash_opens and not cash_closes:
                    # Caso: Ya hay apertura y NO hay cierre (caja abierta)
                    QMessageBox.warning(dialog, "Caja ya abierta",
                        f"⚠️ La caja para hoy ({today}) ya está ABIERTA.\n"
                        f"No se puede realizar otra apertura.")
                    dialog.reject()
                    return
                    
                elif cash_opens and cash_closes:
                    # Caso: Hubo apertura y cierre (reapertura)
                    # Esto es válido, continuar con la nueva apertura
                    reply = QMessageBox.question(dialog, "Confirmar Reapertura",
                        f"⚠️ La caja del día {today} fue abierta y cerrada anteriormente.\n\n"
                        f"¿Confirma que desea realizar una NUEVA APERTURA con monto ${amount:.2f}?",
                        QMessageBox.Yes | QMessageBox.No)
                    
                    if reply == QMessageBox.No:
                        dialog.reject()
                        return
                        
                # Si llegamos aquí, proceder con la apertura
                self.db.insert_cash_open_record(today, amount, "Apertura desde interfaz")
                
                QMessageBox.information(dialog, "✅ Caja Abierta",
                    f"¡Caja abierta exitosamente!\n\n"
                    f"📅 Fecha: {today}\n"
                    f"💰 Monto inicial: ${amount:.2f}\n\n"
                    f"🟢 Puede comenzar a operar.")
                
                dialog.accept()
                
                # Opcional: Actualizar algún indicador en la interfaz si es necesario
                
            except Exception as db_error:
                QMessageBox.critical(dialog, "Error de Base de Datos",
                    f"Error al verificar/guardar en base de datos:\n{str(db_error)}")
                dialog.reject()

        except ValueError:
            QMessageBox.warning(dialog, "Monto Inválido",
                            "Por favor ingrese un monto válido (número).")
        except Exception as e:
            QMessageBox.critical(dialog, "Error Inesperado",
                f"Error inesperado:\n{str(e)}")
            dialog.reject()

    def closeEvent(self, event):
        self.db.close_connection()
        self.timer.stop()
        event.accept()

def main():
    # Configurar locale para fechas en español
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    except locale.Error:
        try:
            # Fallback para Windows
            locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
        except locale.Error:
            # Si no se puede configurar, continuar sin cambios
            pass

    app = QApplication(sys.argv)

    # Configurar fuente global
    app.setFont(QFont("Segoe UI", 10))
    app.setStyle('Fusion')

    # Establecer paleta de colores
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(248, 250, 252))
    palette.setColor(QPalette.WindowText, QColor(30, 41, 59))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(248, 250, 252))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(30, 41, 59))
    palette.setColor(QPalette.Text, QColor(30, 41, 59))
    palette.setColor(QPalette.Button, QColor(59, 130, 246))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.Highlight, QColor(59, 130, 246))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)

    # Solo para desarrollo: descomentar para resetear la base de datos
    # Reset database to start completely clean (no products, no sales, no cash records)
    #try:
    #    import os
    #    db_name = "kiosco_pos.db"
    #    if os.path.exists(db_name):
    #        os.remove(db_name)
    #        print("Base de datos reseteada - comenzando completamente limpia")
    #except Exception as e:
    #    print(f"Error al resetear base de datos: {e}")

    # Mostrar diálogo de login
    login_dialog = LoginDialog()
    if login_dialog.exec_() != LoginDialog.Accepted:
        return  # Salir si login falló

    # Crear ventana principal después del login exitoso
    window = ModernPOS()

    # Verificar y manejar apertura de caja
    window.check_cash_opening()

    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()