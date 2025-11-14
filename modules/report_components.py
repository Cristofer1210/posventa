from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel,
                             QTableWidget, QTableWidgetItem, QWidget, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from utils.formatters import format_currency
from datetime import datetime, timedelta

class StatsCard:
    """Componente reutilizable para tarjetas de estadísticas"""
    
    @staticmethod
    def create(text, value, trend, color, icon, subtitle):
        stat_frame = QFrame()
        stat_frame.setMinimumHeight(120)
        stat_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color}, stop:1 {StatsCard.lighten_color(color)});
                border-radius: 12px;
                padding: 0px;
            }}
        """)
        stat_layout = QVBoxLayout(stat_frame)
        stat_layout.setContentsMargins(20, 16, 20, 16)
        
        # Fila superior: Icono y título
        top_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px; background: transparent;")
        text_label = QLabel(text)
        text_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent;")
        top_layout.addWidget(icon_label)
        top_layout.addWidget(text_label)
        top_layout.addStretch()
        
        # Valor principal
        value_label = QLabel(value)
        value_label.setStyleSheet("color: white; font-size: 28px; font-weight: bold; background: transparent;")
        value_label.setObjectName("value")
        
        # Fila inferior: Tendencia y subtítulo
        bottom_layout = QHBoxLayout()
        trend_label = QLabel(trend)
        trend_label.setStyleSheet("color: white; font-size: 12px; font-weight: 600; background: transparent;")
        trend_label.setObjectName("trend")
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 11px; background: transparent;")
        subtitle_label.setObjectName("subtitle")
        bottom_layout.addWidget(trend_label)
        bottom_layout.addStretch()
        bottom_layout.addWidget(subtitle_label)
        
        stat_layout.addLayout(top_layout)
        stat_layout.addWidget(value_label)
        stat_layout.addLayout(bottom_layout)
        stat_layout.addStretch()
        
        return stat_frame
    
    @staticmethod
    def lighten_color(hex_color, factor=0.3):
        """Aclarar color hexadecimal para gradientes"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        lighter = tuple(min(255, int(c + (255 - c) * factor)) for c in rgb)
        return f"#{lighter[0]:02x}{lighter[1]:02x}{lighter[2]:02x}"

class DataHelper:
    """Helper para cálculos y transformaciones de datos"""
    
    @staticmethod
    def adjust_timezone(datetime_str):
        """Ajustar hora a zona local (Argentina UTC-3)"""
        if not datetime_str:
            return "--:--"
        try:
            formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M:%S.%f", 
                "%Y-%m-%d %H:%M",
                "%H:%M:%S"
            ]
            
            dt = None
            for fmt in formats:
                try:
                    dt = datetime.strptime(datetime_str, fmt)
                    break
                except ValueError:
                    continue
            
            if dt:
                dt_local = dt - timedelta(hours=3)
                return dt_local.strftime("%H:%M")
            else:
                if ' ' in datetime_str and ':' in datetime_str:
                    return datetime_str.split(' ')[1][:5]
                return "--:--"
        except Exception:
            return "--:--"
    
    @staticmethod
    def calculate_growth(current, previous):
        """Calcular porcentaje de crecimiento"""
        if previous == 0:
            return "+0%" if current == 0 else "+100%"
        growth = ((current - previous) / previous) * 100
        return f"+{growth:.1f}%" if growth >= 0 else f"{growth:.1f}%"
    
    @staticmethod
    def get_growth_color(growth_str):
        """Determinar color basado en el crecimiento"""
        if growth_str.startswith('+'):
            return "#10b981"  # Verde para positivo
        elif growth_str.startswith('-'):
            return "#ef4444"  # Rojo para negativo
        return "#6b7280"  # Gris para cero

class TableManager:
    """Manager para manejo de tablas"""
    
    @staticmethod
    def setup_products_table(table):
        """Configurar tabla de productos más vendidos"""
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["#", "Producto", "Cantidad", "Total"])
        
        header = table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
    
    @staticmethod
    def setup_sales_table(table):
        """Configurar tabla de ventas recientes"""
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Hora", "Productos", "Total", "Pago", "Cliente"])
        
        header = table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)