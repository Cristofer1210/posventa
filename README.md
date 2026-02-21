# 🏪 Sistema POS - Mi Emprendimiento

<<<<<<< HEAD
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
=======
Sistema de Punto de Venta (POS) para kiosco, desarrollado en Python con PyQt5.

## 📋 Descripción

**Mi Emprendimiento** es un sistema completo de gestión de ventas e inventario para pequeños comercios tipo kiosco. Permite gestionar productos, realizar ventas, controlar la caja, generar reportes y exportar datos.

### Características Principales

- ✅ **Gestión de Productos**: Catálogo completo con código de barras, categorías, precios de compra/venta y control de stock
- ✅ **Punto de Venta**: Carrito de compras interactivo, búsqueda por código de barras, múltiples métodos de pago
- ✅ **Control de Caja**: Apertura y cierre de caja con reportes detallados
- 📊 **Reportes**: Estadísticas de ventas, productos más vendidos, distribución de métodos de pago
- 📤 **Exportación**: Exportar reportes a Excel
- 🖨️ **Tickets**: Impresión de tickets de venta
- 🔐 **Seguridad**: Sistema de autenticación de usuarios
- 🌐 **Interfaz en Español**: Totalmente localizeado para Argentina

## 📁 Estructura del Proyecto

```
Sistema para kiosco/
├── main.py                 # Punto de entrada de la aplicación
├── database.py             # Clase de gestión de base de datos SQLite
├── login_dialog.py         # Diálogo de inicio de sesión
├── chat_dialog.py          # Diálogo de chat de soporte
├── movements.py            # Módulo de registro de movimientos
├── requirements.txt        # Dependencias del proyecto
├── estructura.txt          # Estructura original del proyecto
├── TODO.md                # Lista de tareas
│
├── modules/                # Módulos de la aplicación
│   ├── __init__.py
│   ├── dashboard.py       # Panel de control principal
│   ├── products.py        # Gestión de productos e inventario
│   ├── sales.py          # Módulo de ventas/POS
│   ├── reports.py        # Reportes y estadísticas
│   ├── cash.py           # Control de caja
│   ├── customers.py      # Gestión de clientes
│   ├── report_components.py  # Componentes reutilizables para reportes
│   └── ticket_printer.py # Impresión de tickets
│
├── widgets/               # Widgets personalizados
│   ├── product_dialog.py # Diálogo para agregar/editar productos
│   └── ...
│
└── utils/                # Utilidades
    └── formatters.py     # Formateadores (moneda, fechas)
```

## 🚀 Instalación

### Prerequisites

- Python 3.8 o superior
- Windows (para impresión de tickets)

### Pasos de Instalación

1. **Clonar o descargar el código**

2. **Crear un entorno virtual (recomendado)**
   
```
bash
   python -m venv venv
   
```

3. **Activar el entorno virtual**
   
```
bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   
```

4. **Instalar las dependencias**
   
```
bash
   pip install -r requirements.txt
   
```

## ⚙️ Configuración

### Credenciales de Acceso

Las credenciales por defecto son:
- **Usuario**: `usuario`
- **Contraseña**: `usuario123`

> ⚠️ **Nota**: Estas credenciales están hardcodeadas en `login_dialog.py`. Para un sistema de producción, se recomienda implementar un sistema de usuarios más seguro.

### Base de Datos

El sistema utiliza SQLite y crea automáticamente la base de datos `kiosco_pos.db` al iniciar. No se requiere configuración adicional.

### Categorías por Defecto

El sistema incluye las siguientes categorías iniciales:
- Bebidas
- Snacks
- Cigarrillos
- Golosinas
- Lácteos
- Panadería
- Limpieza
- Otros

## 📖 Uso del Sistema

### Inicio de Sesión

Al ejecutar `main.py`, aparece el diálogo de inicio de sesión. Ingrese las credenciales configuradas.

### Dashboard (Panel de Control)

El dashboard muestra:
- Resumen de ventas del día
- Productos vendidos
- Clientes atendidos
- Alertas de stock bajo
- Acceso rápido a las funciones principales

### Módulo de Productos

Permite:
- Agregar nuevos productos con código, nombre, categoría, precios y stock
- Editar productos existentes
- Eliminar productos
- Filtrar por categoría
- Buscar por código o nombre
- Ver estadísticas del inventario

### Módulo de Ventas

Funcionalidades:
- Buscar productos por código de barras o nombre
- Agregar productos al carrito con un clic
- Modificar cantidades directamente en el carrito
- Cambiar precios si es necesario
- Seleccionar tipo de cliente (Consumidor Final, Cliente Habitual, etc.)
- Elegir método de pago (Efectivo, Mercado Pago, Débito, Cuenta Corriente)
- Procesar venta y generar ticket
- Apertura y cierre de caja directo desde el módulo

### Módulo de Caja

Opciones disponibles:
- **Apertura de Caja**: Registrar el monto inicial del día
- **Cierre de Caja**: Generar reporte detallado con:
  - Total de ventas
  - Productos vendidos
  - Ingresos monetarios
  - Productos más vendidos
  - Estado del inventario
- **Reporte Diario**: Resumen del día actual
- **Historial**: Ver registros históricos de caja

### Módulo de Reportes

Incluye:
- Filtros por período (Hoy, Ayer, Últimos 7 días, Este mes, etc.)
- Vista Resumen y Vista Detallada
- Estadísticas principales:
  - Ventas totales
  - Productos vendidos
  - Ticket promedio
  - Clientes atendidos
- Productos más vendidos
- Ventas por horario
- Distribución de métodos de pago
- Exportación a Excel

## 💾 Base de Datos

### Tablas Principales

| Tabla | Descripción |
|-------|-------------|
| `customers` | Clientes registrados |
| `categories` | Categorías de productos |
| `products` | Catálogo de productos |
| `sales` | Registro de ventas |
| `sale_items` | Items de cada venta |
| `cash_opens` | Aperturas de caja |
| `cash_closes` | Cierres de caja |
| `credit_payments` | Abonos a cuenta corriente |

### Respaldo

El sistema incluye funcionalidades de respaldo automático en `database.py`.

## 🛠️ Personalización

### Agregar Productos de Ejemplo

El sistema inicia vacío para que el usuario cargue sus propios productos. Para agregar productos de ejemplo, puede ejecutar código adicional o usar la interfaz.

### Modificar Categorías

Las categorías pueden gestionarse desde el módulo de productos o directamente en la base de datos.

### Personalizar Tickets

El módulo `ticket_printer.py` permite personalizar el formato de impresión de tickets.

## 🔧 Solución de Problemas

### Error al iniciar

Verifique que:
- Las dependencias estén correctamente instaladas
- Python 3.8+ esté instalado
- Los archivos de la aplicación estén completos

### Problemas de impresión

- Verifique que la impresora esté configurada en Windows
- Instale `pywin32` para soporte de impresión en Windows

### Error de base de datos

Si la base de datos se corrompe, puede eliminarla (`kiosco_pos.db`) y el sistema creará una nueva automáticamente.

## 📝 Notas de Desarrollo

- **Framework GUI**: PyQt5
- **Base de Datos**: SQLite3
- **Exportación**: openpyxl (incluido en módulos de reportes)
- **Locale**: Configurado para español de Argentina
- **Moneda**: Pesos Argentinos (formato $ XXX.XX)

## 📄 Licencia

Este proyecto es de uso libre para fines educativos y comerciales.

---

**Versión**: 1.0  
**Desarrollado con**: ❤️ para pequeños comercios

¿Necesitas ayuda? Consulta el sistema de soporte integrado en la aplicación.
>>>>>>> 7bd0020 (Actualización del Sistema POS - Cristofer)
