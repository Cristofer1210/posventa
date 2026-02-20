# 🏪 Sistema POS - Mi Emprendimiento

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)
![Windows](https://img.shields.io/badge/Platform-Windows-blue.svg)

> Sistema de Punto de Venta (POS) desarrollado para pequeños comercios. Una solución completa para gestión de ventas, inventario y reportes.


## 🎯 Características Destacadas

### Punto de Venta Intuitivo
- **Interfaz tipo carrito** similar a sistemas comerciales
- Búsqueda instantánea por código de barras
- Modificación de cantidades en tiempo real
- Múltiples métodos de pago (Efectivo, MP, Débito, Ctda. Cte.)

### Gestión de Inventario
- Control de stock automático
- Alertas de productos con stock bajo
- Categorías personalizables
- Precios de compra/venta diferenciados

### Reportes y Análisis
- Dashboard con métricas clave
- Productos más vendidos
- Ventas por horario
- Exportación a Excel

## 🖥️ Tecnologías Utilizadas

| Tecnología | Propósito |
|------------|-----------|
| Python | Lenguaje base |
| PyQt5 | Interfaz gráfica profesional |
| SQLite | Base de datos liviana y portable |
| OpenPyXL | Exportación a Excel |
| Win32Print | Impresión de tickets |

## 🚀 Instalación Rápida

```bash
# 1. Clonar
git clone https://github.com/Cristofer1210/sistema-pos-kiosco.git

# 2. Entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Instalar
pip install -r requirements.txt

# 4. Ejecutar
python main.py
