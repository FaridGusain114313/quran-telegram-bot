import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    """Database əməliyyatları üçün menecer sinif"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or os.getenv('DATABASE_PATH', 'quran_bot.db')
        self._init_db()
    
    def _init_db(self):
        """Database faylının mövcudluğunu yoxlayır"""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database faylı tapılmadı: {self.db_path}")
    
    def get_connection(self):
        """Yeni database bağlantısı qaytarır"""
        return sqlite3.connect(self.db_path)
    
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        """Sorğunu icra edir"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            result = None
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_surahs(self, page=0, per_page=10):
        """Səhifələnmiş surə siyahısı"""
        offset = page * per_page
        query = '''
            SELECT order_no, name_az, verses_count 
            FROM surahs 
            ORDER BY order_no 
            LIMIT ? OFFSET ?
        '''
        return self.execute_query(query, (per_page, offset), fetch_all=True)
    
    def get_total_surahs(self):
        """Ümumi surə sayı"""
        query = 'SELECT COUNT(*) FROM surahs'
        result = self.execute_query(query, fetch_one=True)
        return result[0] if result else 0
    
    def get_surah_by_name(self, name):
        """Adına görə surə məlumatı"""
        query = 'SELECT id, order_no, name_az, verses_count, revelation_place, summary FROM surahs WHERE name_az = ?'
        return self.execute_query(query, (name,), fetch_one=True)
    
    def get_verses(self, surah_id, page=0, per_page=20):
        """Bir surənin ayələri"""
        offset = page * per_page
        query = '''
            SELECT verse_no, text_az 
            FROM verses 
            WHERE surah_id = ? 
            ORDER BY verse_no 
            LIMIT ? OFFSET ?
        '''
        return self.execute_query(query, (surah_id, per_page, offset), fetch_all=True)
    
    def get_verse(self, surah_id, verse_no):
        """Tək ayə"""
        query = 'SELECT text_az FROM verses WHERE surah_id = ? AND verse_no = ?'
        return self.execute_query(query, (surah_id, verse_no), fetch_one=True)
    
    def search_verses(self, keyword, limit=10):
        """Açar sözlə axtarış"""
        query = '''
            SELECT s.name_az, v.verse_no, v.text_az 
            FROM verses v
            JOIN surahs s ON v.surah_id = s.id
            WHERE v.text_az LIKE ? 
            LIMIT ?
        '''
        return self.execute_query(query, (f'%{keyword}%', limit), fetch_all=True)
    
    def get_random_verse(self):
        """Təsadüfi ayə"""
        query = '''
            SELECT s.name_az, v.verse_no, v.text_az 
            FROM verses v
            JOIN surahs s ON v.surah_id = s.id
            ORDER BY RANDOM() 
            LIMIT 1
        '''
        return self.execute_query(query, fetch_one=True)