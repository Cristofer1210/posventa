# 🏪 Sistema POS - Mi Emprendimiento

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)
![Windows](https://img.shields.io/badge/Platform-Windows-blue.svg)

> Sistema de Punto de Venta (POS) desarrollado para pequeños comercios. Una solución completa para gestión de ventas, inventario y reportes.

## 📋 Descripción

**Mi Emprendimiento** es un sistema completo de gestión de ventas e inventario para pequeños comercios tipo kiosco, desarrollado en Python con PyQt5. Permite gestionar productos, realizar ventas, controlar la caja, generar reportes y exportar datos.

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

### Seguridad y Control
- Sistema de autenticación de usuarios
- Apertura y cierre de caja con reportes detallados
- Impresión de tickets
- Interfaz en español adaptada para Argentina

## 🖥️ Tecnologías Utilizadas

| Tecnología | Propósito |
|------------|-----------|
| Python | Lenguaje base |
| PyQt5 | Interfaz gráfica profesional |
| SQLite | Base de datos liviana y portable |
| OpenPyXL | Exportación a Excel |
| Win32Print | Impresión de tickets |

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- Windows (para impresión de tickets)

### Pasos Rápidos

```bash
# 1. Clonar el repositorio
git clone https://github.com/Cristofer1210/sistema-pos-kiosco.git
cd sistema-pos-kiosco

# 2. Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar
python main.py

📌 Nota: La primera ejecución creará automáticamente la base de datos kiosco_pos.db

📁 Estructura del Proyecto

Sistema para kiosco/
├── main.py                 # Punto de entrada
├── database.py             # Gestión de base de datos SQLite
├── login_dialog.py         # Diálogo de inicio de sesión
├── chat_dialog.py          # Diálogo de chat de soporte
├── movements.py            # Registro de movimientos
├── requirements.txt        # Dependencias
├── estructura.txt          # Estructura original
├── TODO.md                 # Lista de tareas
│
├── modules/                # Módulos de la aplicación
│   ├── __init__.py
│   ├── dashboard.py        # Panel de control
│   ├── products.py         # Gestión de productos
│   ├── sales.py            # Módulo de ventas/POS
│   ├── reports.py          # Reportes y estadísticas
│   ├── cash.py             # Control de caja
│   ├── customers.py        # Gestión de clientes
│   ├── report_components.py # Componentes para reportes
│   └── ticket_printer.py   # Impresión de tickets
│
├── widgets/                 # Widgets personalizados
│   └── product_dialog.py    # Diálogo de productos
│
└── utils/                   # Utilidades
    └── formatters.py        # Formateadores (moneda, fechas)

⚙️ Configuración
Credenciales de Acceso
Las credenciales por defecto son:

Usuario: usuario

Contraseña: usuario123

⚠️ Nota: Estas credenciales están hardcodeadas. Para producción, implementar sistema de usuarios más seguro.

Base de Datos
El sistema utiliza SQLite y crea automáticamente kiosco_pos.db al iniciar.

Categorías por Defecto
Bebidas | Snacks | Cigarrillos | Golosinas

Lácteos | Panadería | Limpieza | Otros

📫 Contacto
Cristofer - Programador Python Jr.

https://img.shields.io/badge/LinkedIn-Perfil-blue.svg
https://img.shields.io/badge/GitHub-Cristofer1210-black.svg

📧 Email: cristofergallay62@gmail.com

⭐ ¿Te gustó el proyecto? ¡No olvides dejar una estrella en GitHub! ⭐
