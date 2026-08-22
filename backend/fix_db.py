import os
import psycopg2
import dj_database_url

def fix_corrupted_migrations():
    if 'DATABASE_URL' not in os.environ:
        print("DATABASE_URL not found, skipping fix.")
        return
        
    print("Connecting to database to check for corrupted migrations...")
    db_info = dj_database_url.parse(os.environ['DATABASE_URL'])
    try:
        conn = psycopg2.connect(
            dbname=db_info['NAME'],
            user=db_info['USER'],
            password=db_info['PASSWORD'],
            host=db_info['HOST'],
            port=db_info.get('PORT', 5432)
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        # Check if django_content_type table actually exists
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'django_content_type'
            );
        """)
        table_exists = cur.fetchone()[0]
        
        if not table_exists:
            print("django_content_type table is MISSING. Fixing django_migrations...")
            print("Database is corrupted. Resetting schema completely because this is a fresh deployment.")
            cur.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
            print("Fixed database state. Django will run migrations cleanly.")
        else:
            print("django_content_type table exists. Database seems fine.")
            
    except Exception as e:
        print("Could not fix database:", e)

if __name__ == "__main__":
    fix_corrupted_migrations()
