import streamlit as st
import json
from ExamDB import ExamDatabase
import pandas as pd
from datetime import datetime

# 设置页面配置
st.set_page_config(page_title="考试系统数据库管理", page_icon="🗄️", layout="wide")

# 初始化数据库
db = ExamDatabase()

def load_course_outline(uploaded_file):
    """加载课程大纲JSON文件"""
    if uploaded_file is not None:
        return json.load(uploaded_file)
    return None

def display_course_info(course_data):
    """显示课程信息"""
    st.subheader("课程基本信息")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"课程名称（中文）：{course_data['course_name_cn']}")
        st.write(f"课程名称（英文）：{course_data['course_name_en']}")
        st.write(f"课程代码：{course_data['course_code']}")
        st.write(f"开设院系：{course_data['department']}")
    with col2:
        st.write(f"适用专业：{course_data['major']}")
        st.write(f"课程类型：{course_data['course_type']}")
        st.write(f"学分：{course_data['credits']}")
        st.write(f"考核方式：{course_data['exam_type']}")

def main():
    st.title("考试系统数据库管理 🗄️")
    
    # 侧边栏导航
    page = st.sidebar.selectbox(
        "选择功能",
        ["课程管理", "考试内容管理", "题库管理", "使用统计"]
    )
    
    if page == "课程管理":
        st.header("课程管理")
        
        tab1, tab2, tab3 = st.tabs(["添加课程", "查看课程", "编辑课程"])
        
        with tab1:
            st.subheader("添加新课程")
            uploaded_file = st.file_uploader("上传课程大纲JSON文件", type=['json'])
            
            if uploaded_file is not None:
                course_data = load_course_outline(uploaded_file)
                if course_data:
                    display_course_info(course_data['basic_info'])
                    
                    if st.button("确认添加课程"):
                        try:
                            course_id = db.add_course(course_data['basic_info'])
                            st.success(f"课程添加成功！课程ID：{course_id}")
                        except Exception as e:
                            st.error(f"添加课程失败：{str(e)}")
        
        with tab2:
            st.subheader("课程列表")
            # TODO: 实现课程列表显示功能
            
        with tab3:
            st.subheader("编辑课程")
            # TODO: 实现课程编辑功能
    
    elif page == "考试内容管理":
        st.header("考试内容管理")
        
        # 选择课程
        course_id = st.selectbox(
            "选择课程",
            ["Course 1", "Course 2", "Course 3"]  # TODO: 从数据库获取课程列表
        )
        
        if course_id:
            tab1, tab2 = st.tabs(["查看考试", "导入考试"])
            
            with tab1:
                st.subheader("考试列表")
                exams = db.get_course_exams(course_id)
                if exams:
                    for exam in exams:
                        with st.expander(f"{exam[1]} - {exam[3]}"):
                            st.json(exam[2])
            
            with tab2:
                st.subheader("导入考试内容")
                uploaded_file = st.file_uploader("上传考试内容JSON文件", type=['json'])
                if uploaded_file is not None:
                    exam_data = json.load(uploaded_file)
                    st.json(exam_data)
                    if st.button("确认导入"):
                        try:
                            exam_id = db.save_exam({
                                'course_id': course_id,
                                'exam_content': exam_data,
                                'exam_type': 'imported'
                            })
                            st.success(f"考试内容导入成功！考试ID：{exam_id}")
                        except Exception as e:
                            st.error(f"导入失败：{str(e)}")
    
    elif page == "题库管理":
        st.header("题库管理")
        
        # 选择课程
        course_id = st.selectbox(
            "选择课程",
            ["Course 1", "Course 2", "Course 3"]  # TODO: 从数据库获取课程列表
        )
        
        if course_id:
            tab1, tab2 = st.tabs(["查看题目", "题目分析"])
            
            with tab1:
                # 题型筛选
                question_type = st.selectbox(
                    "选择题型",
                    ["全部", "选择题", "判断题", "填空题", "简答题", "编程题"]
                )
                
                # 获取题目
                questions = db.get_question_bank(
                    course_id,
                    None if question_type == "全部" else question_type
                )
                
                # 显示题目
                if questions:
                    for q in questions:
                        with st.expander(f"{q[1]} - {q[3]}"):
                            st.write(q[2])
            
            with tab2:
                st.subheader("题目统计分析")
                # TODO: 实现题目统计分析功能
    
    elif page == "使用统计":
        st.header("使用统计")
        
        tab1, tab2 = st.tabs(["总体统计", "详细记录"])
        
        with tab1:
            # 获取使用统计数据
            stats = db.get_usage_statistics()
            if stats:
                # 转换为DataFrame
                df = pd.DataFrame(stats, columns=['考试类型', '使用次数', '月份'])
                
                # 显示统计图表
                st.subheader("每月使用情况")
                st.line_chart(df.pivot(index='月份', columns='考试类型', values='使用次数'))
                
                st.subheader("考试类型分布")
                st.bar_chart(df.groupby('考试类型')['使用次数'].sum())
        
        with tab2:
            st.subheader("使用记录")
            # TODO: 实现详细使用记录显示功能

if __name__ == "__main__":
    main()
