import sqlite3

conn = sqlite3.connect('kiosco_pos.db')
cursor = conn.cursor()

# Ver tablas
cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = cursor.fetchall()
print('Tablas en la base de datos:')
for table in tables:
    print(f'- {table[0]}')

# Ver estructura de sales
print('\nEstructura de tabla sales:')
cursor.execute('PRAGMA table_info(sales)')
columns = cursor.fetchall()
for col in columns:
    print(f'  {col[1]}: {col[2]}')

# Ver últimas ventas
print('\nÚltimas 5 ventas:')
cursor.execute('SELECT id, total, payment_method, payment_status, created_at FROM sales ORDER BY created_at DESC LIMIT 5')
sales = cursor.fetchall()
for sale in sales:
    print(f'  ID: {sale[0]}, Total: {sale[1]}, Método: {sale[2]}, Estado: {sale[3]}, Fecha: {sale[4]}')

conn.close()
