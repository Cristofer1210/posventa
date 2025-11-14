import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self, db_name="kiosco_pos.db"):
        self.db_name = db_name
        self.init_database()
        
    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Tabla de Clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                current_credit REAL DEFAULT 0.00,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabla de categorías
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
       # Tabla de Productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE,
                name TEXT NOT NULL,
                category_id INTEGER,
                description TEXT,
                buy_price REAL NOT NULL,
                sell_price REAL NOT NULL,
                stock INTEGER NOT NULL,
                min_stock INTEGER DEFAULT 5,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        ''')
        
        # Tabla de Ventas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                total REAL NOT NULL,
                payment_method TEXT NOT NULL, -- 'Efectivo', 'Transferencia', 'Cuenta Corriente', etc.
                payment_status TEXT NOT NULL, -- 'pagado' o 'cuenta_corriente'
                customer_type TEXT NOT NULL, -- 'Consumidor Final' o nombre del cliente
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')

        # Tabla de Abonos a Cuenta Corriente
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credit_payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                sale_id INTEGER,
                amount REAL NOT NULL,
                payment_method TEXT NOT NULL, -- <<-- CAMBIO CLAVE: Registrar método (Efectivo/Transf.)
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (sale_id) REFERENCES sales(id)
            )
        ''')
        
        # Tabla de Items de Venta
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL, -- Precio al momento de la venta
                subtotal REAL NOT NULL,
                FOREIGN KEY (sale_id) REFERENCES sales(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')

        # Tabla de Cierres de Caja
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cash_closes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL UNIQUE,
                total_income REAL NOT NULL,
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabla de Aperturas de Caja
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cash_opens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL UNIQUE,
                opening_amount REAL NOT NULL,
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # ✅ ELIMINADO: No insertar productos de ejemplo
        # Base de datos queda VACÍA para que el usuario cargue sus productos
        # Verificar y actualizar esquema si es necesario
        self.update_schema(cursor)

        # Insertar categorías por defecto solo si no existen
        cursor.execute('SELECT COUNT(*) FROM categories')
        if cursor.fetchone()[0] == 0:
            self.insert_default_categories(cursor)
            
        # NO insertar productos de ejemplo - base de datos vacía para que el usuario cargue sus productos
        
        conn.commit()
        conn.close()
        
    def update_schema(self, cursor):
        """Actualizar el esquema si hay cambios"""
        try:
            cursor.execute("PRAGMA table_info(categories)")
            categories_exist = len(cursor.fetchall()) > 0
            
            if not categories_exist:
                cursor.execute('''
                    CREATE TABLE categories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
            # Verificar si products tiene category_id
            cursor.execute("PRAGMA table_info(products)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'category_id' not in columns:
                cursor.execute('ALTER TABLE products ADD COLUMN category_id INTEGER')
                
        except Exception as e:
            print(f"Error actualizando esquema: {e}")
        
    def insert_default_categories(self, cursor):
        """Insertar categorías por defecto"""
        default_categories = [
            ("Bebidas", "Bebidas y refrescos"),
            ("Snacks", "Snacks y picadas"),
            ("Cigarrillos", "Cigarrillos y tabaco"),
            ("Golosinas", "Golosinas y chocolates"),
            ("Lácteos", "Productos lácteos"),
            ("Panadería", "Panadería y facturería"),
            ("Limpieza", "Artículos de limpieza"),
            ("Otros", "Otros productos")
        ]
        
        for name, description in default_categories:
            try:
                cursor.execute('INSERT INTO categories (name, description) VALUES (?, ?)', (name, description))
            except sqlite3.IntegrityError:
                continue
        
    def get_connection(self):
        return sqlite3.connect(self.db_name)
        
    # ===== MÉTODOS PARA CATEGORÍAS =====
    
    def get_categories(self):
        """Obtener todas las categorías"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT id, name, description FROM categories ORDER BY name')
            return cursor.fetchall()
        finally:
            conn.close()
            
    def add_category(self, name, description=""):
        """Agregar nueva categoría"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('INSERT INTO categories (name, description) VALUES (?, ?)', (name, description))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            conn.rollback()
            raise Exception(f"Ya existe una categoría con el nombre: {name}")
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al agregar categoría: {str(e)}")
        finally:
            conn.close()
            
    def delete_category(self, category_id):
        """Eliminar categoría (solo si no tiene productos)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar si la categoría tiene productos
            cursor.execute('SELECT COUNT(*) FROM products WHERE category_id = ?', (category_id,))
            product_count = cursor.fetchone()[0]
            
            if product_count > 0:
                raise Exception(f"No se puede eliminar la categoría porque tiene {product_count} productos asociados")
                
            cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar categoría: {str(e)}")
        finally:
            conn.close()
    
    # ===== MÉTODOS PARA PRODUCTOS =====
        
    def add_product(self, product_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO products (code, name, category_id, description, buy_price, sell_price, stock, min_stock)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                product_data.get('code', '').strip(),
                product_data.get('name', '').strip(),
                product_data.get('category_id'),
                product_data.get('description', ''),
                product_data.get('buy_price', 0),
                product_data.get('sell_price', 0),
                product_data.get('stock', 0),
                product_data.get('min_stock', 5)
            ))
            
            conn.commit()
            return True
            
        except sqlite3.IntegrityError as e:
            conn.rollback()
            raise Exception(f"❌ Ya existe un producto con el código: {product_data.get('code', '')}")
        except Exception as e:
            conn.rollback()
            raise Exception(f"❌ Error al guardar producto: {str(e)}")
        finally:
            conn.close()
        
    def get_products(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT p.id, p.code, p.name, c.name as category_name, p.buy_price, p.sell_price, p.stock, p.min_stock
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                ORDER BY p.name
            ''')
            products = cursor.fetchall()
            return products
        except Exception as e:
            print(f"Error getting products: {e}")
            return []
        finally:
            conn.close()
        
    def get_product_by_id(self, product_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
            return cursor.fetchone()
        finally:
            conn.close()
            
    def get_product_by_code(self, code):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM products WHERE code = ?', (code,))
            return cursor.fetchone()
        finally:
            conn.close()
        
    def update_product_stock(self, product_id, new_stock):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('UPDATE products SET stock = ? WHERE id = ?', (new_stock, product_id))
            conn.commit()
        finally:
            conn.close()
            
    def delete_product(self, product_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar producto: {str(e)}")
        finally:
            conn.close()
    
    # ===== MÉTODOS PARA VENTAS =====
        
    def save_sale(self, sale_data, items):
        conn = self.get_connection()
        cursor = conn.cursor()
    
        try:
            # Determinar payment_status basado en payment_method
            payment_method = sale_data.get('payment_method', 'Efectivo')
            payment_status = 'cuenta_corriente' if payment_method == 'Cuenta Corriente' else 'pagado'

            # Insertar venta
            cursor.execute('''
                INSERT INTO sales (customer_id, total, payment_method, payment_status, customer_type, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                sale_data.get('customer_id'),  # Puede ser None
                sale_data['total'],
                payment_method,
                payment_status,
                sale_data.get('customer_type', 'Consumidor Final'),
                self.get_current_local_time()  # Usar hora local de Argentina
            ))
        
            sale_id = cursor.lastrowid
        
            # Insertar items de la venta
            for item in items:
                # Buscar el ID del producto por nombre
                product_id = None
                if item.get('product_id'):
                    product_id = item['product_id']
                else:
                    # Si no tenemos product_id, buscar por nombre
                    cursor.execute('SELECT id FROM products WHERE name = ?', (item['name'],))
                    result = cursor.fetchone()
                    if result:
                        product_id = result[0]
            
                cursor.execute('''
                    INSERT INTO sale_items (sale_id, product_id, product_name, quantity, price, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    sale_id,
                    product_id,
                    item['name'],
                    item['quantity'],
                    item['price'],
                    item['subtotal']
                ))
            
                # Actualizar stock si tenemos product_id
                if product_id:
                    cursor.execute('UPDATE products SET stock = stock - ? WHERE id = ?', 
                                 (item['quantity'], product_id))
        
            conn.commit()
            return sale_id
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al guardar venta: {str(e)}")
        finally:
            conn.close()
            
    def get_sales_report(self, start_date=None, end_date=None):
        """Obtener reporte de ventas para el módulo de reportes - MEJORADO"""
        conn = self.get_connection()
        cursor = conn.cursor()
    
        try:
            query = '''
                SELECT 
                    s.id,
                    s.total,
                    s.payment_method,
                    s.customer_type,
                    s.created_at,
                    COUNT(si.id) as items_count,
                    GROUP_CONCAT(si.product_name || ' x' || si.quantity, ', ') as items_description
                FROM sales s
                LEFT JOIN sale_items si ON s.id = si.sale_id
            '''
        
            params = []
            if start_date and end_date:
                query += ' WHERE DATE(s.created_at) BETWEEN ? AND ?'
                params.extend([start_date, end_date])
            
            query += ' GROUP BY s.id ORDER BY s.created_at DESC LIMIT 100'
        
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en get_sales_report: {e}")
            return []
        finally:
            conn.close()
            
    def get_top_products(self, start_date=None, end_date=None, limit=10):
        """Obtener productos más vendidos - VERSIÓN CORREGIDA"""
        conn = self.get_connection()
        cursor = conn.cursor()
    
        try:
            query = '''
                SELECT 
                    p.name,
                    COALESCE(SUM(si.quantity), 0) as total_quantity,
                    COALESCE(SUM(si.subtotal), 0) as total_amount
                FROM sale_items si
                JOIN products p ON si.product_id = p.id
                JOIN sales s ON si.sale_id = s.id
            '''
        
            params = []
            if start_date and end_date:
                query += ' WHERE DATE(s.created_at) BETWEEN ? AND ?'
                params.extend([start_date, end_date])
            
            query += '''
                GROUP BY p.id, p.name
                ORDER BY total_quantity DESC
                LIMIT ?
            '''
            params.append(limit)
        
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en get_top_products: {e}")
            return []
        finally:
            conn.close()
            
    def get_sales_summary(self, start_date=None, end_date=None):
        """Obtener resumen de ventas - VERSIÓN CORREGIDA"""
        conn = self.get_connection()
        cursor = conn.cursor()
    
        try:
            query = '''
                SELECT 
                    COUNT(*) as total_sales,
                    COALESCE(SUM(total), 0) as total_amount,
                    COALESCE(AVG(total), 0) as average_ticket,
                    COUNT(DISTINCT customer_type) as unique_customers
                FROM sales
            '''
        
            params = []
            if start_date and end_date:
                query += ' WHERE DATE(created_at) BETWEEN ? AND ?'
                params.extend([start_date, end_date])
            
            cursor.execute(query, params)
            result = cursor.fetchone()
        
            # Asegurarnos de que no haya None
            if result:
                return (
                    result[0] or 0,  # total_sales
                    result[1] or 0.0,  # total_amount
                    result[2] or 0.0,  # average_ticket
                    result[3] or 0  # unique_customers
                )
            else:
                return (0, 0.0, 0.0, 0)
            
        except Exception as e:
            print(f"Error en get_sales_summary: {e}")
            return (0, 0.0, 0.0, 0)
        finally:
            conn.close()
        
    def close_connection(self):
        pass
        
    def reset_database(self):
        """Método para resetear completamente la base de datos"""
        if os.path.exists(self.db_name):
            os.remove(self.db_name)
        self.init_database()

    def debug_sales(self):
        """Método para debug - verificar ventas en la base de datos"""
        conn = self.get_connection()
        cursor = conn.cursor()
    
        try:
            # Verificar ventas
            cursor.execute('SELECT COUNT(*) as total_ventas FROM sales')
            total_ventas = cursor.fetchone()[0]
        
            # Verificar items de venta
            cursor.execute('SELECT COUNT(*) as total_items FROM sale_items')
            total_items = cursor.fetchone()[0]
        
            # Verificar últimas ventas
            cursor.execute('''
                SELECT s.id, s.total, s.created_at, COUNT(si.id) as items_count
                FROM sales s 
                LEFT JOIN sale_items si ON s.id = si.sale_id 
                GROUP BY s.id 
                ORDER BY s.created_at DESC 
                LIMIT 5
            ''')
            ultimas_ventas = cursor.fetchall()
        
            print(f"=== DEBUG BASE DE DATOS ===")
            print(f"Total ventas: {total_ventas}")
            print(f"Total items: {total_items}")
            print(f"Últimas 5 ventas: {ultimas_ventas}")
        
            return {
                'total_ventas': total_ventas,
                'total_items': total_items,
                'ultimas_ventas': ultimas_ventas
            }
        
        except Exception as e:
            print(f"Error en debug: {e}")
            return None
        finally:
            conn.close()

    def get_detailed_movements(self, date):
        """Obtiene una lista detallada de ventas (movimientos) para una fecha."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                s.id,
                TIME(s.created_at) as hora,
                COALESCE(c.name, 'Consumidor Final') as cliente,
                GROUP_CONCAT(p.name || ' (' || si.quantity || ')', ', ') as productos,
                s.total,
                s.payment_method,
                s.payment_status
            FROM sales s
            LEFT JOIN customers c ON s.customer_id = c.id
            JOIN sale_items si ON s.id = si.sale_id
            JOIN products p ON si.product_id = p.id
            WHERE DATE(s.created_at) = ?
            GROUP BY s.id
            ORDER BY s.created_at DESC
        '''
        cursor.execute(query, (date,))
        movements = cursor.fetchall()
        conn.close()
        return movements

    def get_credit_payments_by_date(self, date):
        """Obtiene abonos a cuentas corrientes para una fecha específica, incluyendo el método de pago."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                cp.id,
                TIME(cp.created_at) as hora,
                c.name as cliente,
                'Abono Cuenta Corriente' as productos,
                cp.amount as total,
                cp.payment_method as metodo_pago,  -- <<-- Método de pago real del abono
                'pagado' as estado
            FROM credit_payments cp
            JOIN customers c ON cp.customer_id = c.id
            WHERE DATE(cp.created_at) = ?
            ORDER BY cp.created_at DESC
        '''
        cursor.execute(query, (date,))
        payments = cursor.fetchall()
        conn.close()
        return payments
        
        """"
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al registrar abono: {str(e)}")
        finally:
            conn.close()
        """

    def get_current_local_time(self):
        """Obtener hora local de Argentina (UTC-3)"""
        from datetime import datetime, timedelta
        utc_now = datetime.utcnow()
        argentina_time = utc_now - timedelta(hours=3)
        return argentina_time.strftime("%Y-%m-%d %H:%M:%S")

    def get_previous_period_sales(self, start_date, end_date):
        """Obtener ventas del período anterior para comparación"""
        conn = self.get_connection()
        cursor = conn.cursor()
    
        try:
            # Calcular período anterior (misma duración)
            from datetime import datetime, timedelta
            current_start = datetime.strptime(start_date, "%Y-%m-%d")
            current_end = datetime.strptime(end_date, "%Y-%m-%d")
        
            period_days = (current_end - current_start).days + 1
            previous_end = current_start - timedelta(days=1)
            previous_start = previous_end - timedelta(days=period_days - 1)
        
            previous_start_str = previous_start.strftime("%Y-%m-%d")
            previous_end_str = previous_end.strftime("%Y-%m-%d")
        
            # Obtener datos del período anterior
            query = '''
                SELECT 
                    COUNT(*) as total_sales,
                    COALESCE(SUM(total), 0) as total_amount,
                    COALESCE(AVG(total), 0) as average_ticket,
                    COUNT(DISTINCT customer_type) as unique_customers
                FROM sales
                WHERE DATE(created_at) BETWEEN ? AND ?
            '''
        
            cursor.execute(query, (previous_start_str, previous_end_str))
            result = cursor.fetchone()
        
            if result:
                return (
                    result[0] or 0,  # total_sales
                    result[1] or 0.0,  # total_amount
                    result[2] or 0.0,  # average_ticket
                    result[3] or 0  # unique_customers
                )
            else:
                return (0, 0.0, 0.0, 0)
            
        except Exception as e:
            print(f"Error en get_previous_period_sales: {e}")
            return (0, 0.0, 0.0, 0)
        finally:
            conn.close()

    def get_total_products_sold(self, start_date=None, end_date=None):
        """Obtener total de productos vendidos"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            query = '''
                SELECT COALESCE(SUM(quantity), 0) as total_products
                FROM sale_items si
                JOIN sales s ON si.sale_id = s.id
            '''

            params = []
            if start_date and end_date:
                query += ' WHERE DATE(s.created_at) BETWEEN ? AND ?'
                params.extend([start_date, end_date])

            cursor.execute(query, params)
            result = cursor.fetchone()
            return result[0] if result else 0

        except Exception as e:
            print(f"Error en get_total_products_sold: {e}")
            return 0
        finally:
            conn.close()

    def get_hourly_sales(self, start_date=None, end_date=None):
        """Obtener ventas agrupadas por hora"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            query = '''
                SELECT
                    strftime('%H', s.created_at) as hour,
                    COUNT(*) as sales_count,
                    COALESCE(SUM(s.total), 0) as total_amount
                FROM sales s
            '''

            params = []
            if start_date and end_date:
                query += ' WHERE DATE(s.created_at) BETWEEN ? AND ?'
                params.extend([start_date, end_date])

            query += ' GROUP BY strftime(\'%H\', s.created_at) ORDER BY hour'

            cursor.execute(query, params)
            return cursor.fetchall()

        except Exception as e:
            print(f"Error en get_hourly_sales: {e}")
            return []
        finally:
            conn.close()

    def get_payment_methods_distribution(self, start_date=None, end_date=None):
        """Obtener distribución de métodos de pago"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            query = '''
                SELECT
                    payment_method,
                    COUNT(*) as count,
                    COALESCE(SUM(total), 0) as total_amount
                FROM sales
            '''

            params = []
            if start_date and end_date:
                query += ' WHERE DATE(created_at) BETWEEN ? AND ?'
                params.extend([start_date, end_date])

            query += ' GROUP BY payment_method ORDER BY total_amount DESC'

            cursor.execute(query, params)
            return cursor.fetchall()

        except Exception as e:
            print(f"Error en get_payment_methods_distribution: {e}")
            return []
        finally:
            conn.close()

    def get_detailed_sales_report(self, start_date=None, end_date=None):
        """Obtener reporte DETALLADO de ventas con todos los productos"""
        conn = self.get_connection()
        cursor = conn.cursor()
    
        try:
            query = '''
                SELECT 
                    s.id,
                    s.total,
                    s.payment_method,
                    s.customer_type,
                    s.created_at,
                    s.payment_status,
                    GROUP_CONCAT(
                        si.product_name || ' x' || si.quantity || ' = $' || si.subtotal, 
                        '\n'
                    ) as items_detail,
                    COUNT(si.id) as items_count
                FROM sales s
                LEFT JOIN sale_items si ON s.id = si.sale_id
            '''
        
            params = []
            if start_date and end_date:
                query += ' WHERE DATE(s.created_at) BETWEEN ? AND ?'
                params.extend([start_date, end_date])
        
            query += ' GROUP BY s.id ORDER BY s.created_at DESC'
        
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en get_detailed_sales_report: {e}")
            return []
        finally:
            conn.close()

    def add_credit_payment_detailed(self, customer_id, payments_data):
        """Agregar abono a cuenta corriente con detalle de métodos de pago"""
        conn = self.get_connection()
        cursor = conn.cursor()
    
        try:
            cursor.execute('BEGIN TRANSACTION')
        
            # Insertar pago principal
            total_amount = sum(payment['amount'] for payment in payments_data)
            cursor.execute('''
                INSERT INTO credit_payments (customer_id, amount, notes)
                VALUES (?, ?, ?)
            ''', (customer_id, total_amount, f"Abono con {len(payments_data)} métodos"))
        
            payment_id = cursor.lastrowid
        
            # Insertar detalles de métodos de pago
            for payment in payments_data:
                cursor.execute('''
                    INSERT INTO credit_payments_detail (credit_payment_id, payment_method, amount)
                    VALUES (?, ?, ?)
                ''', (payment_id, payment['method'], payment['amount']))
        
            # Actualizar saldo del cliente
            cursor.execute('''
                UPDATE customers 
                SET current_balance = current_balance - ? 
                WHERE id = ?
            ''', (total_amount, customer_id))
        
            conn.commit()
            return payment_id
        
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al registrar abono: {str(e)}")
        finally:
            conn.close()

    def create_automatic_backup(self):
        """Crea una copia de seguridad con la fecha actual."""
        # Evitamos la ruta absoluta aquí para que el backup quede en el mismo directorio
        backup_dir = 'backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = os.path.join(backup_dir, f'backup_{timestamp}_{self.db_name}')
        
        conn_src = self.get_connection()
        conn_bck = sqlite3.connect(backup_filename)
        
        conn_src.backup(conn_bck)
        
        conn_bck.close()
        conn_src.close()
        print(f"Backup creado exitosamente en: {backup_filename}")

    def clean_old_backups(self, backup_dir, max_backups=10):
        """Limpiar backups antiguos"""
        try:
            backups = []
            for f in os.listdir(backup_dir):
                if f.startswith("backup_") and f.endswith(".db"):
                    file_path = os.path.join(backup_dir, f)
                    backups.append((file_path, os.path.getctime(file_path)))
        
            # Ordenar por fecha de creación (más antiguos primero)
            backups.sort(key=lambda x: x[1])
        
            # Eliminar los más antiguos si excedemos el límite
            while len(backups) > max_backups:
                old_backup = backups.pop(0)
                os.remove(old_backup[0])
                print(f"🗑️ Backup antiguo eliminado: {old_backup[0]}")
            
        except Exception as e:
            print(f"Error limpiando backups: {e}")

    def get_total_products(self):
        """Obtener total de productos"""
        conn = self.get_connection()
        cursor = conn.cursor()
    
        try:
            cursor.execute('SELECT COUNT(*) FROM products')
            return cursor.fetchone()[0] or 0
        except Exception as e:
            print(f"Error en get_total_products: {e}")
            return 0
        finally:
            conn.close()

    def get_low_stock_count(self):
        """Obtener cantidad de productos con stock bajo"""
        conn = self.get_connection()
        cursor = conn.cursor()
    
        try:
            cursor.execute('SELECT COUNT(*) FROM products WHERE stock > 0 AND stock <= min_stock')
            return cursor.fetchone()[0] or 0
        except Exception as e:
            print(f"Error en get_low_stock_count: {e}")
            return 0
        finally:
            conn.close()

    def get_out_of_stock_count(self):
        """Obtener cantidad de productos sin stock"""
        conn = self.get_connection()
        cursor = conn.cursor()
    
        try:
            cursor.execute('SELECT COUNT(*) FROM products WHERE stock = 0')
            return cursor.fetchone()[0] or 0
        except Exception as e:
            print(f"Error en get_out_of_stock_count: {e}")
            return 0
        finally:
            conn.close()

    def get_inventory_value(self):
        """Calcular valor total del inventario"""
        conn = self.get_connection()
        cursor = conn.cursor()
    
        try:
            cursor.execute('SELECT COALESCE(SUM(stock * buy_price), 0) FROM products WHERE stock > 0')
            return cursor.fetchone()[0] or 0.0
        except Exception as e:
            print(f"Error en get_inventory_value: {e}")
            return 0.0
        finally:
            conn.close()

    def get_cash_register_income_summary(self, date):
        """
        Calcula el total de INGRESOS MONETARIOS para el cierre de caja.
        Suma ventas pagadas (excluye 'cuenta_corriente') y abonos.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        total_income = 0
        
        # 1. Sumar ventas cuyo estado de pago sea 'pagado'
        try:
            query_sales = """
                SELECT SUM(total) FROM sales
                WHERE DATE(created_at) = ? AND payment_status = 'pagado';
            """
            cursor.execute(query_sales, (date,))
            cash_sales = cursor.fetchone()[0] or 0
            total_income += cash_sales
        except Exception as e:
            print(f"Error al obtener ventas pagadas: {e}")

        # 2. Sumar abonos a cuenta corriente
        try:
            query_payments = """
                SELECT SUM(amount) FROM credit_payments
                WHERE DATE(created_at) = ?;
            """
            cursor.execute(query_payments, (date,))
            credit_payments = cursor.fetchone()[0] or 0
            total_income += credit_payments
        except Exception as e:
            print(f"Error al obtener abonos: {e}")
            
        conn.close()
        return total_income

    def insert_cash_close_record(self, date, total_income, notes=""):
        """Insertar registro de cierre de caja"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO cash_closes (date, total_income, notes)
                VALUES (?, ?, ?)
            ''', (date, total_income, notes))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            conn.rollback()
            raise Exception(f"Ya existe un cierre de caja para la fecha: {date}")
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al guardar cierre de caja: {str(e)}")
        finally:
            conn.close()

    def insert_cash_open_record(self, date, opening_amount, notes=""):
        """Insertar registro de apertura de caja"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO cash_opens (date, opening_amount, notes)
                VALUES (?, ?, ?)
            ''', (date, opening_amount, notes))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            conn.rollback()
            raise Exception(f"Ya existe una apertura de caja para la fecha: {date}")
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al guardar apertura de caja: {str(e)}")
        finally:
            conn.close()

    def get_cash_close_records(self, start_date=None, end_date=None):
        """Obtener registros de cierres de caja"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            query = 'SELECT id, date, total_income, notes, created_at FROM cash_closes'
            params = []

            if start_date and end_date:
                query += ' WHERE date BETWEEN ? AND ?'
                params.extend([start_date, end_date])

            query += ' ORDER BY date DESC'

            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en get_cash_close_records: {e}")
            return []
        finally:
            conn.close()

    def get_cash_open_records(self, start_date=None, end_date=None):
        """Obtener registros de aperturas de caja"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            query = 'SELECT id, date, opening_amount, notes, created_at FROM cash_opens'
            params = []

            if start_date and end_date:
                query += ' WHERE date BETWEEN ? AND ?'
                params.extend([start_date, end_date])

            query += ' ORDER BY date DESC'

            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en get_cash_open_records: {e}")
            return []
        finally:
            conn.close()
