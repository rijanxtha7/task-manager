import pymysql
import config

def get_connection():
    """Establish MySQL connection"""
    try:
        connection = pymysql.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DATABASE,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("✓ Database connected successfully")
        return connection
    except Exception as e:
        print("✗ Database connection failed:")
        print(e)
        return None

def create_tables():
    """Create database tables if they don't exist"""
    conn = get_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    try:
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                status VARCHAR(20) DEFAULT 'pending',
                priority VARCHAR(20) DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Add priority column if it doesn't exist (for existing databases)
        try:
            cursor.execute("ALTER TABLE tasks ADD COLUMN priority VARCHAR(20) DEFAULT 'medium'")
            conn.commit()
            print("✓ Priority column added successfully")
        except Exception:
            pass  # Column already exists
        
        # Create default admin user if doesn't exist
        cursor.execute("SELECT * FROM users WHERE email = %s", ("admin@taskmanager.com",))
        if not cursor.fetchone():
            from werkzeug.security import generate_password_hash
            cursor.execute(
                "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                ("Admin", "admin@taskmanager.com", generate_password_hash("admin123"), "admin")
            )
        
        conn.commit()
        print("✓ Database tables created successfully")
        
    except Exception as e:
        print("✗ Error creating tables:")
        print(e)
    finally:
        cursor.close()
        conn.close()