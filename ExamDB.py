import sqlite3
import json
import datetime
from pathlib import Path

class ExamDatabase:
    def __init__(self, db_path="exam_system.db"):
        """初始化数据库连接"""
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """初始化数据库表结构"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 创建课程信息表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_name_cn TEXT NOT NULL,
                    course_name_en TEXT,
                    course_code TEXT UNIQUE NOT NULL,
                    department TEXT NOT NULL,
                    major TEXT NOT NULL,
                    course_type TEXT NOT NULL,
                    credits INTEGER,
                    exam_type TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建考试内容表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS exams (
                    exam_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_id INTEGER NOT NULL,
                    exam_type TEXT NOT NULL,
                    exam_content JSON NOT NULL,
                    chapters TEXT,
                    difficulty TEXT,
                    creator TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'draft',
                    FOREIGN KEY (course_id) REFERENCES courses (course_id)
                )
            ''')
            
            # 创建题目库表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS questions (
                    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_id INTEGER NOT NULL,
                    exam_id INTEGER,
                    question_type TEXT NOT NULL,
                    question_content TEXT NOT NULL,
                    answer TEXT,
                    explanation TEXT,
                    difficulty TEXT,
                    course_objectives TEXT,
                    aacsb_goals TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (course_id) REFERENCES courses (course_id),
                    FOREIGN KEY (exam_id) REFERENCES exams (exam_id)
                )
            ''')
            
            # 创建使用记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usage_logs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_id INTEGER NOT NULL,
                    exam_type TEXT NOT NULL,
                    generation_params JSON,
                    result_status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ip_address TEXT,
                    FOREIGN KEY (course_id) REFERENCES courses (course_id)
                )
            ''')
            
            conn.commit()

    def add_course(self, course_data):
        """添加课程信息"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO courses (
                    course_name_cn, course_name_en, course_code, 
                    department, major, course_type, 
                    credits, exam_type
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                course_data['course_name_cn'],
                course_data['course_name_en'],
                course_data['course_code'],
                course_data['department'],
                course_data['major'],
                course_data['course_type'],
                course_data['credits'],
                course_data['exam_type']
            ))
            return cursor.lastrowid

    def save_exam(self, exam_data):
        """保存生成的考试内容"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO exams (
                    course_id, exam_type, exam_content,
                    chapters, difficulty, creator, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                exam_data['course_id'],
                exam_data['exam_type'],
                json.dumps(exam_data['exam_content'], ensure_ascii=False),
                json.dumps(exam_data['chapters']) if exam_data.get('chapters') else None,
                exam_data.get('difficulty'),
                exam_data.get('creator'),
                exam_data.get('status', 'draft')
            ))
            exam_id = cursor.lastrowid
            
            # 如果有题目，保存到题目库
            if 'questions' in exam_data['exam_content']:
                self._save_questions(cursor, exam_data['course_id'], exam_id, 
                                  exam_data['exam_content']['questions'])
            
            return exam_id

    def _save_questions(self, cursor, course_id, exam_id, questions):
        """保存题目到题目库"""
        for question in questions:
            cursor.execute('''
                INSERT INTO questions (
                    course_id, exam_id, question_type,
                    question_content, answer, explanation,
                    difficulty, course_objectives, aacsb_goals
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                course_id,
                exam_id,
                question['type'],
                question['question'],
                question.get('answer'),
                question.get('explanation'),
                question.get('difficulty'),
                json.dumps(question.get('course_objectives', []), ensure_ascii=False),
                json.dumps(question.get('aacsb_goals', []), ensure_ascii=False)
            ))

    def log_usage(self, usage_data):
        """记录系统使用情况"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usage_logs (
                    course_id, exam_type, generation_params,
                    result_status, ip_address
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                usage_data['course_id'],
                usage_data['exam_type'],
                json.dumps(usage_data.get('generation_params', {}), ensure_ascii=False),
                usage_data['result_status'],
                usage_data.get('ip_address')
            ))
            return cursor.lastrowid

    def get_course_exams(self, course_id):
        """获取课程的所有考试"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT exam_id, exam_type, exam_content, created_at, status
                FROM exams
                WHERE course_id = ?
                ORDER BY created_at DESC
            ''', (course_id,))
            return cursor.fetchall()

    def get_question_bank(self, course_id, question_type=None):
        """获取题目库中的题目"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = '''
                SELECT question_id, question_type, question_content,
                       difficulty, created_at
                FROM questions
                WHERE course_id = ?
            '''
            params = [course_id]
            
            if question_type:
                query += ' AND question_type = ?'
                params.append(question_type)
            
            cursor.execute(query, params)
            return cursor.fetchall()

    def get_usage_statistics(self, course_id=None):
        """获取使用统计信息"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = '''
                SELECT exam_type, COUNT(*) as count,
                       strftime('%Y-%m', created_at) as month
                FROM usage_logs
            '''
            params = []
            
            if course_id:
                query += ' WHERE course_id = ?'
                params.append(course_id)
            
            query += ' GROUP BY exam_type, month'
            cursor.execute(query, params)
            return cursor.fetchall()
