import json
from openai import OpenAI
import streamlit as st

def load_course_data(file):
    """从上传的文件加载课程数据"""
    try:
        if file is not None:
            content = file.getvalue().decode('utf-8')
            return json.loads(content)
        return None
    except Exception as e:
        st.error(f"加载课程数据失败: {str(e)}")
        return None

def generate_paper_requirements(course_data):
    if course_data is None:
        return None
        
    client = OpenAI(
        api_key=st.secrets["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com/v1"    # 更新为正确的API endpoint
    )

    # 构建系统提示
    system_prompt = """
    你是一位资深的教育专家。请解析课程信息并生成课程论文要求。
    
    你需要返回如下JSON格式的数据：
    {
        "course_name": "课程名称",
        "paper_title": "论文题目要求和示例",
        "topics": ["建议研究方向1", "建议研究方向2"],
        "structure": ["具体章节要求1", "具体章节要求2"],
        "format_requirements": ["格式要求1", "格式要求2"],
        "evaluation_criteria": ["评分标准1", "评分标准2"],
        "submission_requirements": ["提交要求1", "提交要求2"],
        "data_analysis_requirements": ["数据分析要求1", "数据分析要求2"]
    }
    """

    # 构建用户提示
    user_prompt = f"""
    请将以下课程信息解析为json格式的课程论文要求：

    课程名称：{course_data['basic_info']['course_name_cn']}
    课程目标：{course_data['course_objectives']}
    考核方式：{course_data['basic_info']['exam_form']}
    考核标准：{json.dumps(course_data['assessment_table'], ensure_ascii=False)}
    教材参考：{json.dumps(course_data['course_textbooks'], ensure_ascii=False)}
    
    生成要求：
    1. 论文选题必须结合课程特点和实践
    2. 评分标准需要与课程考核标准对应
    3. 论文结构要体现理论分析和实践操作两个方面
    4. 必须包含具体的实践操作要求
    5. 要求应具体且可操作

    请返回json格式的结果。
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},  # 确保返回JSON格式
            temperature=0.7,
            max_tokens=2000,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        # 添加调试信息
        st.sidebar.write("API Response Status:", response.model_dump_json())
        
        result = json.loads(response.choices[0].message.content)
        # 确保包含课程名称
        result['course_name'] = course_data['basic_info']['course_name_cn']
        return result
    except Exception as e:
        st.error(f"API调用错误: {str(e)}")
        # 添加详细错误信息
        import traceback
        st.sidebar.error(f"详细错误: {traceback.format_exc()}")
        return None

def display_paper_requirements(requirements):
    if not requirements:
        st.error("无法生成论文要求，请检查API配置或重试")
        return
        
    st.title(f"{requirements['course_name']} - 课程论文要求")
    
    st.header("📝 论文题目要求")
    st.write(requirements["paper_title"])
    
    st.header("🎯 建议研究方向")
    for topic in requirements["topics"]:
        st.write(f"- {topic}")
    
    st.header("📊 实践要求")
    for item in requirements.get("data_analysis_requirements", []):
        st.write(f"- {item}")
    
    st.header("📑 论文结构")
    for item in requirements["structure"]:
        st.write(f"- {item}")
    
    st.header("📋 格式要求")
    for item in requirements["format_requirements"]:
        st.write(f"- {item}")
    
    st.header("💯 评分标准")
    for item in requirements["evaluation_criteria"]:
        st.write(f"- {item}")
    
    st.header("📤 提交要求")
    for item in requirements["submission_requirements"]:
        st.write(f"- {item}")

def main():
    st.set_page_config(
        page_title="课程论文要求生成器",
        page_icon="📊",
        layout="wide"
    )
    
    # 显示API密钥状态
    if st.secrets.get("DEEPSEEK_API_KEY"):
        st.sidebar.success("API密钥已配置")
    else:
        st.sidebar.error("未找到API密钥配置")
    
    # 文件上传部分
    st.sidebar.header("课程大纲上传")
    uploaded_file = st.sidebar.file_uploader(
        "上传课程大纲JSON文件",
        type=['json'],
        help="请上传符合格式的课程大纲JSON文件"
    )
    
    # 加载课程数据
    if uploaded_file is not None:
        if 'course_data' not in st.session_state or uploaded_file != st.session_state.get('last_uploaded_file'):
            st.session_state.course_data = load_course_data(uploaded_file)
            st.session_state.last_uploaded_file = uploaded_file
            st.session_state.paper_requirements = None  # 清除之前的生成结果
    
        if st.session_state.course_data:
            st.sidebar.success(f"已加载课程：{st.session_state.course_data['basic_info']['course_name_cn']}")
            
            # 添加刷新按钮
            if st.sidebar.button("重新生成要求"):
                st.session_state.paper_requirements = None
            
            # 生成论文要求
            if 'paper_requirements' not in st.session_state:
                with st.spinner('正在生成课程论文要求...'):
                    st.session_state.paper_requirements = generate_paper_requirements(st.session_state.course_data)
            
            # 显示论文要求
            display_paper_requirements(st.session_state.paper_requirements)
    else:
        st.info("请上传课程大纲JSON文件")
        # 清除session state
        for key in ['course_data', 'paper_requirements', 'last_uploaded_file']:
            if key in st.session_state:
                del st.session_state[key]

if __name__ == "__main__":
    main()
