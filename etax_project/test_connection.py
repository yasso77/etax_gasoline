import pyodbc

# Replace with your actual info
server = 'NB-YASSER\SQLEXPRESS'          # or 'localhost', or 'SERVERNAME\\SQLEXPRESS'
database = 'EmaratLive'     # your DB name
username = 'saAdmin'        # SQL username
password = 'Pa$$w0rd'    # SQL password
driver = 'ODBC Driver 17 for SQL Server'  # or use what `pyodbc.drivers()` shows

# Connection string
conn_str = (
    f'DRIVER={{{driver}}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
)

try:
    conn = pyodbc.connect(conn_str)
    print("✅ Connected successfully!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 * FROM sys.tables")
    
    for row in cursor.fetchall():
        print(row)
    
    conn.close()
except Exception as e:
    print("❌ Connection failed:")
    print(e)
