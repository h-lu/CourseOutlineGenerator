import streamlit as st
from docxtpl import DocxTemplate
import os
from openai import OpenAI
import json
import pandas as pd  # 添加pandas导入

# DeepSeek客户端配置
client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],  # 需要在Streamlit secrets中配置
    base_url="https://api.deepseek.com"
)

# 1. 首先是所有的显示函数定义
def display_graduation_requirements(requirements):
    """显示毕业要求指标点"""
    st.subheader("毕业要求指标点")
    
    if not requirements:
        st.info("暂无毕业要求指标点数据")
        return
        
    try:
        # 创建三列布局
        col_k, col_a, col_q = st.columns(3)
        
        with col_k:
            st.markdown("**知识类指标点**")
            if 'knowledge' in requirements:
                for item in requirements['knowledge']:
                    st.write(f"- {item}")
            else:
                st.info("暂无知识类指标点")
        
        with col_a:
            st.markdown("**能力类指标点**")
            if 'ability' in requirements:
                for item in requirements['ability']:
                    st.write(f"- {item}")
            else:
                st.info("暂无能力类指标点")
        
        with col_a:
            st.markdown("**素养类指标点**")
            if 'quality' in requirements:
                for item in requirements['quality']:
                    st.write(f"- {item}")
            else:
                st.info("暂无素养类指标点")
                
    except Exception as e:
        st.error(f"显示毕业要求指标点时出错：{str(e)}")

def display_course_schedule(schedule_data):
    """显示课程内容与学时分配"""
    st.subheader("课程内容与学时分配")
    
    if not schedule_data:
        st.info("暂无课程内容与学时分配数据")
        return
        
    try:
        # 准备表格数据
        table_data = []
        for item in schedule_data:
            table_data.append({
                "章节/教学单元": item.get('chapter', ''),
                "主要内容": "\n".join(item.get('content', [])),
                "学习要求": "\n".join(item.get('requirements', [])),
                "学时/实验学时": item.get('hours', ''),
                "教学方式": item.get('type', '')
            })
        
        # 使用pandas创建表格
        if table_data:
            df = pd.DataFrame(table_data)
            
            # 设置表格样式，启用自动换行
            st.table(df.style.set_properties(**{
                'white-space': 'pre-wrap',
                'text-align': 'left',
                'vertical-align': 'top'
            }))
        else:
            st.warning("没有课程内容与学时分配数据可显示")
            
    except Exception as e:
        st.error(f"显示课程内容与学时分配表时出错：{str(e)}")

def display_lab_schedule(labs_data):
    """显示实验教学内容"""
    st.subheader("实验教学内容与安排")
    
    if not labs_data:
        st.info("暂无实验教学内容数据")
        return
        
    try:
        # 准备表格数据
        table_data = []
        for lab in labs_data:
            table_data.append({
                "序号": lab.get('number', ''),
                "实验名称": lab.get('name', ''),
                "主要内容": "\n".join(lab.get('content', [])),
                "学习要求": "\n".join(lab.get('requirements', [])),
                "实验学时": lab.get('hours', ''),
                "每组人数": lab.get('group_size', ''),
                "必修/选修": "必修" if lab.get('required', True) else "选修",
                "实验项目类型": lab.get('type', '')
            })
        
        # 使用pandas创建表格
        if table_data:
            df = pd.DataFrame(table_data)
            
            # 设置表格样式，启用自动换行
            st.table(df.style.set_properties(**{
                'white-space': 'pre-wrap',
                'text-align': 'left',
                'vertical-align': 'top',
                'min-height': '100px'  # 设置最小高度以确保有足够空间显示
            }))
        else:
            st.warning("没有实验教学内容数据可显示")
            
    except Exception as e:
        st.error(f"显示实验教学内容表时出错：{str(e)}")

def display_assessment_table(assessment_table):
    """显示考核方式和评价标准"""
    st.subheader("考核方式和评价标准")
    
    if not assessment_table:
        st.info("暂无考核方式和评价标准数据")
        return
        
    try:
        # 准备表格数据
        table_data = []
        for item in assessment_table:
            table_data.append({
                "考核方式": item.get('type', ''),
                "成绩占比": f"{item.get('percentage', '')}%",
                "评价标准": "\n".join(item.get('criteria', [])),
                "对应课程目标": ", ".join(item.get('objectives', []))
            })
        
        # 使用pandas创建表格
        if table_data:
            df = pd.DataFrame(table_data)
            
            # 设置表格样式，启用自动换行
            st.table(df.style.set_properties(**{
                'white-space': 'pre-wrap',
                'text-align': 'left',
                'vertical-align': 'top',
                'min-height': '100px'  # 设置最小高度以确保有足够空间显示
            }))
        else:
            st.warning("没有考核方式和评价标准数据可显示")
            
    except Exception as e:
        st.error(f"显示考核方式和评价标准表时出错：{str(e)}")

def display_objectives_mapping(mapping_data):
    """显示课程目标与毕业要求指标点对应关系"""
    st.subheader("课程目标与毕业要求指标点对应关系")
    
    if not mapping_data:
        st.info("暂无课程目标与毕业要求指标点对应关系数据")
        return
        
    try:
        # 使用pandas创建表格
        df = pd.DataFrame(mapping_data)
        # 设置列名
        df.columns = ["序号", "课程目标", "支撑毕业要求指标点"]
        # 显示表格
        st.table(df)
            
    except Exception as e:
        st.error(f"显示课程目标与毕业要求指标点对应关系表时出错：{str(e)}")

def display_aacsb_assessment(assessment_data):
    """显示AACSB评估体系"""
    st.subheader("AACSB评估体系")
    
    if not assessment_data:
        st.info("暂无AACSB评估体系数据")
        return
        
    try:
        # 准备表格数据
        table_data = []
        for assessment in assessment_data:
            # 获取CG信息
            cg = assessment.get('cg', '')
            
            # 获取OG列表
            og_list = assessment.get('og', [])
            if isinstance(og_list, str):
                og_list = [{'og': og_list}]  # 如果是字符串，转换为列表
            
            if isinstance(og_list, list):
                for og_item in og_list:
                    if isinstance(og_item, dict):
                        row = {
                            "毕业目标(CG)": cg,
                            "具体目标(OG)": og_item.get('og', ''),
                            "目标特征(Traits)": "\n".join(og_item.get('traits', [])),
                            "评量方式(Assessment)": "\n".join(og_item.get('methods', [])),
                            "评量标准(Criteria)": "\n".join(og_item.get('criteria', [])),
                            "映射关系": (
                                f"课程目标：{', '.join(og_item.get('mapping', {}).get('course_objectives', []))}\n"
                                f"指标点：{', '.join(og_item.get('mapping', {}).get('graduation_requirements', []))}"
                            )
                        }
                        table_data.append(row)
                    else:
                        st.error(f"OG数据格式不正确: {og_item}")
            else:
                st.error(f"OG列表格式不正确: {og_list}")
        
        # 使用pandas创建表格
        if table_data:
            df = pd.DataFrame(table_data)
            
            # 设置表格样式
            pd.set_option('display.max_colwidth', None)
            
            # 显示表格
            st.table(df.style.set_properties(**{
                'white-space': 'pre-wrap',
                'text-align': 'left',
                'vertical-align': 'top'
            }))
        else:
            st.warning("没有AACSB评估体系数据示")
            
    except Exception as e:
        st.error(f"显示AACSB评估体系表时出错：{str(e)}")
        # 显示原始数据以便调试
        st.error("原始数据：")
        st.json(assessment_data)

def display_aacsb_goals(goals):
    """显示AACSB学习目标"""
    st.subheader("AACSB学习目标")
    
    if not goals:
        st.info("暂无AACSB学习目标数据")
        return
        
    try:
        if isinstance(goals, str):
            goals = goals.split("\n")
        
        if isinstance(goals, list):
            for goal in goals:
                st.markdown(f"- {goal}")
        else:
            st.error("AACSB学习目标数据格式不正确")
            
    except Exception as e:
        st.error(f"显示AACSB学习目标时出错：{str(e)}")

def display_course_objectives(objectives):
    """显示课程目标"""
    st.subheader("课程目标")
    
    if not objectives:
        st.info("暂无课程目标数据")
        return
        
    try:
        if isinstance(objectives, str):
            objectives = objectives.split("\n")
        
        if isinstance(objectives, list):
            for objective in objectives:
                st.markdown(f"- {objective}")
        else:
            st.error("课程目标数据格式不正确")
            
    except Exception as e:
        st.error(f"显示课程目标时出错：{str(e)}")

def display_assessment_explanation(assessment_data):
    """显示课程考核及成绩评定说明"""
    st.subheader("课程考核及成绩评定说明")
    
    if not assessment_data:
        st.info("暂无考核方式和评价标准数据")
        return
        
    try:
        # 准备说明数据
        explanation = {
            "总体说明": "本课程的考核方式及成绩评定标准如下：",
            "详细说明": [],
            "补充说明": []
        }
        
        for item in assessment_data:
            assessment_type = item.get('type', '')
            percentage = item.get('percentage', '')
            criteria = item.get('criteria', [])
            objectives = item.get('objectives', [])
            
            explanation["详细说明"].append(f"{assessment_type}：{percentage}%")
            for criterion in criteria:
                explanation["详细说明"].append(f"- {criterion}")
            explanation["详细说明"].append(f"对应课程目标：{', '.join(objectives)}")
            
        explanation["补充说明"].append("1. 课程考核方式及成绩评定标准可能会根据教学实际情况进行调整。")
        explanation["补充说明"].append("2. 考核方式和评价标准的具体实施细节将在课程教学过程中进一步明确。")
        
        # 显示说明
        st.write(explanation["总体说明"])
        for detail in explanation["详细说明"]:
            st.write(detail)
        for supplement in explanation["补充说明"]:
            st.write(supplement)
            
    except Exception as e:
        st.error(f"显示课程考核及成绩评定说明时出错：{str(e)}")

def generate_aacsb_goals(course_name, course_type, department, major, graduation_requirements, extra_info):
    system_prompt = """
    你是一个AACSB认证专家，请为给定的课程生成合适的学习目标。
    
    请以JSON格式输出学习目标，格式如下：
    {
        "goals": [
            "CG1 专业知识-L2 系统掌握核心理论与方法",
            "CG2 实践能力-L2 能够应用专业工具解决问题",
            "CG3 创新素养-L1 具备基本的创新意识和团队协作能力"
        ]
    }
    """
    
    user_prompt = f"""
    课程名称：{course_name}
    课程性质：{course_type}
    开课部门：{department}
    适用专业：{major}
    
    毕业要求指标点：
    知识类：
    {chr(10).join([f"- {x}" for x in graduation_requirements['knowledge']])}
    能力类：
    {chr(10).join([f"- {x}" for x in graduation_requirements['ability']])}
    素养类：
    {chr(10).join([f"- {x}" for x in graduation_requirements['quality']])}
    
    额外信息：{extra_info}
    
    请基于以上信息生成AACSB学习目标，要求：
    1. 目标数量和分布：
       - 总数必须为3个目标（不多不少）
       - 必须包含：知识类指标点、能力类指标点、素养类指标点各1个
       - CG1、CG2、CG3序编号
       - CG1必须是知识型，CG2必须是能力型，CG3必须是素养型
       - 必须与毕业要求指标点相对应
    
    2. 能力水平标注规则：
       L0（了解/知道）：
       - 适用于基础概念的认知
       - 用于通识类课程
       - 动词：识别、列举、描述
       
       L1（理解/掌握）：
       - 适用于专业基础知识
       - 用于专业基础课程
       - 动词：解释、总结、举例
       
       L2（应用/熟练）：
       - 适用于专业核心能力
       - 用于专业必修课程
       - 动词：应用、实施、操作
       
       L3（分析/精通）：
       - 适用于综合分析能力
       - 用于高级专业课程
       - 动词：分析、评估、设计
       
       L4（创新/引领）：
       - 适用于创新创造能力
       - 用于研究型课程
       - 动词：创造、优化、革新
    
    3. 课程性质对应规则：
       专业必修课：
       - 知识目标：L2-L3
       - 能力目标：L2-L3
       - 素养目标：L1-L2
       
       专业选修课：
       - 知识目标：L1-L2
       - 能力目标：L1-L2
       - 素养目标：L1-L2
       
       通识课程：
       - 知识目标：L0-L1
       - 能力目标：L0-L1
       - 素养目标：L0-L1
    
    4. 专业特色要求：
       - 体现开课部门的学科特点
       - 反映专业的核心竞争力
       - 对接行业发展需求
       - 符合毕业要求指标点
    
    请以json格式输出学习目标。
    """
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={'type': 'json_object'}
        )
        
        # 解析返回的JSON
        result = json.loads(response.choices[0].message.content)
        
        # 确保返回的数据格式正确
        if isinstance(result, dict) and "goals" in result:
            if isinstance(result["goals"], list):
                # 确保所有目标都是字符串
                goals = [str(goal) for goal in result["goals"]]
                return "\n".join(goals)
            else:
                st.error("API返回的goals不是列表格式")
                return None
        else:
            st.error("API返回的数据格式不正确")
            return None
            
    except Exception as e:
        st.error(f"生成学习目标时出错：{str(e)}")
        return None

def get_graduation_requirements(department, major, extra_info):
    system_prompt = """
    你是一个专业培养方案专家，请根据开课部门和适用专业生成合适的毕业要求指标点。
    
    请以JSON格式输出，格式如下：
    {
        "requirements": {
            "knowledge": [
                "K1 掌握数学与统计学基础知识",
                "K2 掌握数据科学核心理论与方法",
                "K3 了解人工智能前沿发展动态"
            ],
            "ability": [
                "A1 具备数据采集与预处理能力",
                "A2 具备数据分析与建模能力",
                "A3 熟练使用主流分析工具",
                "A4 能够解决实际数据问题"
            ],
            "quality": [
                "Q1 具备良好的职业道德",
                "Q2 具备团队协作能力"
            ]
        }
    }
    """
    
    user_prompt = f"""
    开课部门：{department}
    适用专业：{major}
    额外重要信息：{extra_info}
    
    请生成该专业的毕业要求指标点，要求：
    1. 指标点数量要求：
       - 知识类指标点：3-4个
       - 能力类指标点：4-5个
       - 素养类指标点：2-3个
    
    2. 编号规则：
       - 知识类(K)：K1-K4
       - 能力类(A)：A1-A5
       - 素养类(Q)：Q1-Q3
    
    3. 描述规则：
       - 每个指标点20字以内
       - 使用规范的表述动词
       - 确保可测量可评价
       - 体现专业特色
    
    请以json格式输出指标点。
    """
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={'type': 'json_object'}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get('requirements', None)
        
    except Exception as e:
        st.error(f"生成毕业要求指标点时出错：{str(e)}")
        return None

def generate_course_content(course_name, course_type, department, major, aacsb_goals, extra_info, total_hours, theory_hours, practice_hours, graduation_requirements):
    system_prompt = """
    你是一个课程设计专家，请基于完整的课程信息生成课程内容。
    
    请以JSON格式输出，格式如下：
    {
        "introduction": {
            "position": "课程定位说明（50字以内）",
            "purpose": "课程目的说明（50字以内）",
            "content": "课程内容说明（100字以内）",
            "method": "教学方法说明（50字以内）",
            "outcome": "预期成果说明（50字内）"
        },
        "objectives": [
            "1. 知识目标：掌握xxx",
            "2. 能力目标：能够xxx",
            "3. 素养目标：具备xxx",
            "4. 创新目标：能够xxx"
        ],
        "textbooks": {
            "main": [
                "1.《xxx》（英文）, 作者, 出版社, 2023年（第x版）- 主要用于xxx",
                "2.《xxx》（中文）, 作者, 出版社, 2022年（第x- 主要用于xxx"
            ],
            "references": [
                "1. 经典教材：《xxx》",
                "2. 实践指南：《xxx》",
                "3. 在线资源：xxx平台课程",
                "4. 技术文档：xxx官方文档",
                "5. 前沿资料：xxx会议/期刊论文"
            ]
        },
        "objectives_mapping": [
            {
                "objective": "1. 知识目标：掌握xxx",
                "requirements": ["K1 xxx", "K2 xxx"]
            }
        ]
    }
    """
    
    user_prompt = f"""
    课程名称：{course_name}
    课程性质：{course_type}
    开课部门：{department}
    适用专业：{major}
    总学时：{total_hours}学时
    理论学时：{theory_hours}学时
    实学时{practice_hours}学时
    
    AACSB学目标：
    {aacsb_goals}
    
    毕业要求指标点：
    知识类：
    {chr(10).join([f"- {x}" for x in graduation_requirements['knowledge']])}
    能力类：
    {chr(10).join([f"- {x}" for x in graduation_requirements['ability']])}
    素养类：
    {chr(10).join([f"- {x}" for x in graduation_requirements['quality']])}
    
    额外信息：
    {extra_info}
    
    请生成课程内容，要求：
    1. 课程简介要求（总字数300字左右）：
       - 课程定位：说明在专业培养中的地位和作用
       - 课程目的：明确培养目标和预期效果
       - 课程内容：概述主要知识体系和技能要求
       - 教学方法：说明理论课（{theory_hours}学时）和实践课（{practice_hours}学时）的实施方式
       - 预期成果：描述学生通过本课程获得的能力提升
    
    2. 课程目标要求（必须4个）：
       - 知识目标：对应AACSB的CG1，映射知识类指标点
       - 能力目标：对应AACSB的CG2，映射能力类指标点
       - 素养目标：对应AACSB的CG3，映射素养类指标点
       - 创新目标：综合性目标，可映射多类指标点
    
    3. 教材要求：
       - 主教材（2本）：
         * 1本英文教材（近3年版）
         * 1本中文教材（近3年版）
         * 要说明适用的教学内容
       
       - 参考资料（5项）：
         * 经典教材：系统性强的基础教材
         * 实践指南：案例丰富的实践教材
         * 在线资源：优质MOOC或在线课程
         * 技术文档：相关工具或平台文档
         * 前沿资料：学术会议/期刊论文
    
    4. 目标映要求：
       - 每个课程目标映射1-2个指标点
       - 知识目标必须映射知识类标
       - 力标必须射能力类指标点
       - 养目标必须映射养类指标点
       - 创新目标可以跨类映
    
    5. 整体要求：
       - 内容逻辑性强
       - 目标可测量
       - 资源可获得
       - 映射有依据
    
    请以json格式输出课程内容。
    """
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={'type': 'json_object'}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # 验证返回的数据格式
        if not all(key in result for key in ['introduction', 'objectives', 'textbooks', 'objectives_mapping']):
            st.error("API返回的数据格式不正确")
            return None
        
        # 验证课程目标的一致性
        objectives_set = set(result['objectives'])
        mapping_objectives = set(item['objective'] for item in result['objectives_mapping'])
        
        if objectives_set != mapping_objectives:
            st.error("课程目标与映射关系表的目标不一致")
            return None
            
        if not all(key in result['textbooks'] for key in ['main', 'references']):
            st.error("API返回的教材数据格式不正确")
            return None
            
        if not isinstance(result['objectives'], list):
            st.error("课程目标必须是列表格式")
            return None
            
        if not isinstance(result['textbooks']['main'], list):
            st.error("主教材必须是列表格式")
            return None
            
        if not isinstance(result['textbooks']['references'], list):
            st.error("参考资料必须是列表格式")
            return None
            
        return result
        
    except Exception as e:
        st.error(f"生成课程内容时出错：{str(e)}")
        return None

def generate_aacsb_assessment(aacsb_goals, course_objectives, graduation_requirements):
    """生成AACSB学习目标评估体系"""
    system_prompt = """
    你是一个AACSB认证专家，请为给定的学习目标生成评估体系。
    
    请以JSON格式输出评估体系，格式示例：
    {
        "assessments": [
            {
                "cg": "CG1 专业知识-L2 系统掌握核心理论与方法",
                "og": [
                    {
                        "og": "OG1.1 握基础概念原理",
                        "traits": [
                            "能够准确解释核心概念",
                            "能够描述基本原理和方法"
                        ],
                        "methods": [
                            "课堂测验（20%）",
                            "期末考试（30%）"
                        ],
                        "criteria": [
                            "优秀(90-100分)：完全掌握概念和原理",
                            "良好(80-89分)：较好掌握概念和原理",
                            "合格(70-79分)：基本掌握概念和原理"
                        ],
                        "mapping": {
                            "course_objectives": ["1", "2"],
                            "graduation_requirements": ["K1", "K2"]
                        }
                    }
                ]
            }
        ]
    }
    """
    
    user_prompt = f"""
    AACSB学习目标：
    {aacsb_goals}
    
    课程目标：
    {course_objectives}
    
    毕业要求指标点：
    {json.dumps(graduation_requirements, ensure_ascii=False)}
    
    请生成AACSB评估体系，要求：
    1. CG与OG的对应规则：
       - 每个CG必须对应2个OG（不多不少）
       - OGx.1：基础能力目标（对L0-L1级别）
       - OGx.2：进阶能力目标（对应L2-L4级别）
       - OG必须与课程目标和毕业要求指标点相对应
    
    2. 评估征(Traits)设计规则：
       基础力特征（L0-L1）：
       - "能够识别和描述xxx"
       - "能够理解和解释xxx"
       - "能够举例说明xxx"
       
       应用能力特征（L2）：
       - "能够用xxx解决xxx"
       - "能够实施xxx完成xxx"
       - "能够操作xxx实现xxx"
       
       分析能力特征（L3）：
       - "能够分析xxx提出xxx"
       - "能够评估xxx优化xxx"
       - "能够设计xxx改进xxx"
       
       创新能力特征（L4）：
       - "能够创造xxx"
       - "能够革新xxx"
       - "能够引领xxx"
    
    3. 评估方式(Methods)设计规则：
       过程性评估（30-40%）：
       - 课堂表现（10-15%）
       - 作业完成（10-15%）
       - 实验报告（10-15%）
       
       阶段性评估（30-40%）：
       - 单元测验（10-15%）
       - 项目报告（15-20%）
       - 期中考试（15-20%）
       
       终结性评估（30-40%）：
       - 期末考试（30-40%）
       - 课程设计（30-40%）
       - 综合项目（30-40%）
    
    请以json格式输出评估体系。
    """
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={'type': 'json_object'}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get('assessments', None)
        
    except Exception as e:
        st.error(f"生成AACSB评估体系时出错：{str(e)}")
        return None

def generate_course_schedule(course_intro, course_objectives, total_hours, theory_hours):
    """生成课程内容与学时分配表"""
    # 计算实践学时
    practice_hours = total_hours - theory_hours
    
    system_prompt = """
    你是一个课程设计专家，请根据课程信息生成课程内容与学时分配表。
    
    请以JSON格式输出，格式如下：
    {
        "schedule": [
            {
                "chapter": "1. 绪论",
                "content": [
                    "1.1 基本概念与理论体系",
                    "1.2 发展历史与研究现状",
                    "1.3 应用领域与发展趋势"
                ],
                "requirements": [
                    "理解本课程的基本概念和理论体系",
                    "掌握主要研究内容和应用领域",
                    "了解学科发展趋势"
                ],
                "hours": "2/2",  # 理论/实践学时
                "type": "讲授、案例分析、讨论"
            }
        ]
    }
    """
    
    user_prompt = f"""
    课程简介：
    {json.dumps(course_intro, ensure_ascii=False)}
    
    课程目标：
    {course_objectives}
    
    总学时：{total_hours}
    理论学时：{theory_hours}
    实践学时：{practice_hours}
    
    请根据课程简介和课程目标生成课程内容与学时分配表，要求：
    1. 内容组织原则：
       - 知识体系完整，逻辑性强
       - 难度循序渐进，由浅入深
       - 理论联系实际，突出应用
       - 反映学科前沿，体现创新
       - 符合认知规律，便于学习
    
    2. 章节结构要求：
       - 每章标题简明扼要，突出重点
       - 每章必须包含3个主要小节
       - 小节内容具体详实，可操作
       - 章节之间有机衔接，避免重复
       - 理论与实际紧密结合
    
    3. 学时分配规则：
       理论课：
       - 按2学时或4学时为单位安排
       - 重要章节可安排4学时
       - 基础章节安排2学时
       - 总计必须为{theory_hours}学时
       
       实践课：
       - 统一按2学时为单位安排
       - 尽量安排在对应理论课后
       - 总计必须为{practice_hours}学时
       - 难度与理论课程同步
    
    4. 教学方式设计：
       理论教学：
       - 课堂讲授：系统讲解知识点
       - 案例分析：加深理解应用
       - 课堂研讨：促进思维碰撞
       - 专题讲座：拓展前沿视野
       
       实践教学：
       - 上机操作：培养实践技能
       - 案例实践：解决实际问题
       - 项目训练：提升综合能力
       - 研讨交流：分享学习体会
    
    5. 学习要求设计：
       知识要求：
       - 明确重点难点
       - 指明掌握程度
       - 突出核心概念
       - 强调应用价值
       
       能力要求：
       - 具体可操作
       - 可测量评价
       - 注重实践性
       - 体现创新性
    
    6. 考虑因素：
       - 课程性质和定位
       - 学生知识基础
       - 教学资源条件
       - 实践教学环境
       - 课程考核要求
       - 毕业要求指标点
    
    7. 时间分配建议：
       - 导论与基础（约15%）：课程概述、基本概念、理论基础
       - 核心内容（约50%）：重点理论、关键技术、主要方法
       - 前沿拓展（约20%）：新理论、新技术、新应用
       - 综合应用（约15%）：案例分析、实践创新、总结提升
    
    请以json格式输出课程内容与学时分配表。注意：
    1. 内容要具体明确，避免空泛
    2. 每章都要有清晰的教学目标
    3. 理论与实践要紧密结合
    4. 学时分配要准确合理
    5. 教学方式要多样灵活
    6. 学习要求量
    """
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={'type': 'json_object'}
        )
        
        result = json.loads(response.choices[0].message.content)
        schedule_data = result.get('schedule', [])
        
        # 验证学时总和
        theory_sum = sum(int(item['hours'].split('/')[0]) for item in schedule_data)
        practice_sum = sum(int(item['hours'].split('/')[1]) for item in schedule_data)
        
        if theory_sum != theory_hours:
            st.warning(f"⚠️ 理论学时总和不正确：当前{theory_sum}学时，应为{theory_hours}学时")
            
        if practice_sum != practice_hours:
            st.warning(f"⚠️ 实践学时总和不正确：当前{practice_sum}学时，应为{practice_hours}学时")
        
        # 验证每章内容
        for item in schedule_data:
            if len(item.get('content', [])) != 3:
                st.warning(f"⚠️ 章节{item['chapter']}的小节数量不正确")
                
            if not item.get('requirements', []):
                st.warning(f"⚠️ 章节{item['chapter']}缺少学习要求")
                
            if not item.get('type', ''):
                st.warning(f"⚠️ 章节{item['chapter']}缺少教学方式")
        
        return schedule_data if schedule_data else []
        
    except Exception as e:
        st.warning(f"⚠️ 生成课程内容与学时分配表时出错：{str(e)}")
        return []

def generate_lab_schedule(course_schedule, practice_hours, course_objectives):
    """生成实验教学内容与安排表"""
    system_prompt = """
    你是一个课程设计专家，请根据课程内容生成实验教学安排表。
    
    请以JSON格式输出，格式如下：
    {
        "labs": [
            {
                "number": "1",
                "name": "基础环境搭建与工具使用",
                "content": [
                    "1. 开发环境配置",
                    "2. 基本工具使用",
                    "3. 示例程序运行"
                ],
                "requirements": [
                    "掌握环境配置方法",
                    "熟练使用基本工具",
                    "理解工作流程"
                ],
                "hours": 2,
                "group_size": 1,
                "type": "基础性",  # 基础性/综合性/设计性
                "required": true,   # true表示必修
                "objectives": ["2", "3"],  # 对应的课程目标编号
                "chapter": "第1章"  # 对应的教学章节
            }
        ]
    }
    """
    
    user_prompt = f"""
    课程实践总学时：{practice_hours}
    
    课程教学内容：
    {json.dumps(course_schedule, ensure_ascii=False)}
    
    课程目标：
    {course_objectives}
    
    请生成实验教学安排表，要求：
    1. 实验类型及分布：
       基础性实验（25-30%学时）：
       - 基本技能训练
       - 工具使用方法
       - 单人完成
       - 对应课程前期章节
       
       综合性实验（35-40%学时）：
       - 综合应用能力
       - 多知识点结合
       - 2人协作
       - 对应课程中期章节
       
       设计性实验（35-40%学时）：
       - 创新设计能力
       - 方案规划实施
       - 2-3人团队
       - 对应课程后期章
    
    2. 实验内容要求：
       - 必须与教学进度同步
       - 实验内容层次
       - 难度循序渐进
       - 体现能力培养
       - 注重实际应用能力
    
    3. 学时分配规则：
       - 总学时必须等于{practice_hours}
       - 基础性实验：2-4学时/个
       - 综合性实验：4学/个
       - 设计性实验4-6学时/个
       - 合理分配各类实验
    
    4. 分组要求：
       - 基础性：单人（1人/组）
       - 综合性：双人（2人/组）
       - 设计性：团队（2-3人/组）
       - 明确每个实验分组
    
    请以json格式输出实验教学安排表。
    """
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={'type': 'json_object'}
        )
        
        result = json.loads(response.choices[0].message.content)
        labs_data = result.get('labs', [])
        
        # 验证实验数量
        if len(labs_data) < 1:
            st.warning("⚠️ 实验数量不能少于1个")
            return None
        
        # 验证实验学时总和
        total_lab_hours = sum(item['hours'] for item in labs_data)
        if total_lab_hours != practice_hours:
            st.warning(f"⚠️ 实验学时总和不正确：当前{total_lab_hours}学时，应为{practice_hours}学时")
        
        # 验证每个实验的内容和要求
        for lab in labs_data:
            if len(lab.get('content', [])) < 1:
                st.warning(f"⚠️ 实验{lab['number']}缺少内容")
            
            if len(lab.get('requirements', [])) < 1:
                st.warning(f"⚠️ 实验{lab['number']}缺少学习要求")
        
        return labs_data
        
    except Exception as e:
        st.error(f"生成实验教学内容与安排表时出错：{str(e)}")
        return None
    

def generate_assessment_scheme(course_objectives, assessment_data, labs_data, theory_hours, practice_hours, exam_type, exam_form, course_type):
    """生成考核方案"""
    
    # 根据考核方式选择不同的提示词模板
    if exam_type == "考试":
        if exam_form == "闭卷笔试":
            assessment_template = """
            请生成考核方案，要求：
            1. 期末考试（闭卷笔试）（40-50%）：
               - 基础知识（40%）：概念理解、原理掌握
               - 应用能力（40%）：问题分析、算法设计
               - 综合创新（20%）：方案优化、拓展应用
            
            2. 平时成绩（30-40%）：
               课堂表现（10-15%）：
               - 出勤记录
               - 课堂互动
               - 学习态度
               
               课后作业（10-15%）：
               - 完成质量
               - 提交时效
               - 创新思维
               
               单元测验（10%）：
               - 知识掌握
               - 应用能力
               - 理解程度
            
            3. 实验成绩（20-30%）：
               实验操作（10-15%）：
               - 规范操作
               - 完成情况
               - 独立性
               
               实验报告（10-15%）：
               - 数据记录
               - 分析讨论
               - 报告规范
            """
        else:  # 开卷笔试
            assessment_template = """
            请生成考核方案，要求：
            1. 期末考试（开卷笔试）（40-50%）：
               - 应用能力（50%）：问题分析、方案设计
               - 综合创新（30%）：方案优化、创新思维
               - 文献运用（20%）：资料查找、知识整合
            
            2. 平时成绩（30-40%）：
               课堂参与（15-20%）：
               - 讨论发言
               - 案例分析
               - 问题解答
               
               研究报告（15-20%）：
               - 文献综述
               - 方法应用
               - 创新见解
            
            3. 实验成绩（20-30%）：
               项目实现（10-15%）：
               - 功能完整
               - 技术水平
               - 创新性
               
               技术报告（10-15%）：
               - 方案设计
               - 实现过程
               - 结果分析
            """
    else:  # 考查课程
        if exam_form == "课程论文":
            assessment_template = """
            请生成考核方案，要求：
            1. 课程论文（35-45%）：
               - 选题价值（10%）：选题新颖性、研究意义
               - 内容水平（15%）：文献综述、研究方法
               - 创新程度（15%）：观点创新、方法创新
               - 写作规范（5%）：结构完整、格式规范
            
            2. 平时表现（35-45%）：
               文献研读（15-20%）：
               - 阅读笔记
               - 文献综述
               - 研究动态
               
               研究过程（20-25%）：
               - 选题报告
               - 开题答辩
               - 进度汇报
            
            3. 实验实践（20-30%）：
               研究实践（10-15%）：
               - 数据收集
               - 模型构建
               - 实验验证
               
               成果展示（10-15%）：
               - 论文答辩
               - 研究成果
               - 创新贡献
            """
        elif exam_form == "项目报告":
            assessment_template = """
            请生成考核方案，要求：
            1. 项目成果（35-45%）：
               - 需求分析（10%）：需求理解、问题定义
               - 设计方案（15%）：技术路线、创新点
               - 实现效果（15%）：功能完整、性能指标
               - 文档质量（5%）：文档规范、内容完整
            
            2. 过程考核（35-45%）：
               团队协作（15-20%）：
               - 任务分工
               - 进度管理
               - 团队贡献
               
               阶段评审（20-25%）：
               - 方案评审
               - 中期检查
               - 测试报告
            
            3. 技术实现（20-30%）：
               代码质量（10-15%）：
               - 代码规范
               - 功能实现
               - 性能优化
               
               部署运维（10-15%）：
               - 环境部署
               - 系统测试
               - 问题修复
            """
        else:  # 课程设计
            assessment_template = """
            请生成考核方案，要求：
            1. 设计成果（40-50%）：
               - 设计方案（20%）：创新性、可行性
               - 实现质量（20%）：完整性、技术性
               - 答辩表现（10%）：表达、回答
            
            2. 设计过程（30-40%）：
               过程管理（15-20%）：
               - 进度计划
               - 文档管理
               - 版本控制
               
               阶段评审（15-20%）：
               - 方案评审
               - 中期检查
               - 验收测试
            
            3. 技术实现（20-30%）：
               实现质量（10-15%）：
               - 代码规范
               - 功能完整
               - 性能优化
               
               创新应用（10-15%）：
               - 技术创新
               - 应用价值
               - 实用效果
            """
    
    system_prompt = """
    你是一个课程设计专家，请根据课程信息生成考核方案。
    
    请严格按照以下JSON格式输出：
    {
        "assessment_items": [
            {
                "type": "期末考试（闭卷笔试）",
                "percentage": 50,
                "criteria": [
                    "1. 基础知识（20%）：概念理解、原理掌握",
                    "2. 应用能力（20%）：问题分析、方案设计",
                    "3. 创新思维（10%）：方案优化、拓展思考"
                ],
                "objectives": ["1", "2"]
            }
        ]
    }
    """
    
    user_prompt = f"""
    课程目标：
    {course_objectives}
    
    AACSB评估体系：
    {json.dumps(assessment_data, ensure_ascii=False)}
    
    实验安排：
    {json.dumps(labs_data, ensure_ascii=False) if labs_data else "无实验环节"}
    
    考核方式：{exam_type}（{exam_form}）
    课程性质：{course_type}
    理论学时：{theory_hours}
    实践学时：{practice_hours}
    
    {assessment_template}
    
    请注意：
    1. 各部分考核比例必须在规定范围内
    2. 所有考核项目必须对应课程目标
    3. 考核标准必须具体且可操作
    4. 总评成绩必须为100%
    5. 评分标准应体现区分度
    
    请以json格式输出考核方案。
    """
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={'type': 'json_object'}
        )
        
        result = json.loads(response.choices[0].message.content)
        assessment_items = result.get('assessment_items', [])
        
        # 验证考核比例总和
        total_percentage = sum(item.get('percentage', 0) for item in assessment_items)
        if total_percentage != 100:
            st.warning(f"⚠️ 考核比例总和({total_percentage}%)不等于100%")
        
        # 验证考试课程的期末考试要求
        if exam_type == "考试":
            final_exam = next((item for item in assessment_items if '期末考试' in item['type']), None)
            if not final_exam:
                st.warning("⚠️ 考试课程必须包含期末考试")
            elif final_exam['percentage'] < 40 or final_exam['percentage'] > 60:
                st.warning(f"⚠️ 考试课程的期末考试比例({final_exam['percentage']}%)应在40-60%之间")
        
        # 验证每项考核都有对应的课程目标
        for item in assessment_items:
            if not item.get('objectives'):
                st.warning(f"⚠️ {item['type']}缺少对应的课程目标")
        
        return assessment_items
        
    except Exception as e:
        st.warning(f"⚠️ 生成考核方案时出错：{str(e)}")
        return []

def validate_data():
    """验证所有必要数据是否已生成"""
    required_data = {
        'graduation_requirements': '毕业要求指标点',
        'aacsb_goals': 'AACSB学习目标',
        'course_intro': '课程简介',
        'course_objectives': '课程目标',
        'course_textbooks': '教材信息',
        'aacsb_assessment': 'AACSB评估体系',
        'course_schedule': '课程内容与学时分配',
        'assessment_table': '考核方式和标准'
    }
    
    missing_data = []
    for key, name in required_data.items():
        if key not in st.session_state or not st.session_state[key]:
            missing_data.append(name)
    
    if practice_hours > 0 and 'labs_schedule' not in st.session_state:
        missing_data.append('实验教学内容')
    
    return missing_data

def validate_hours():
    """验证学时分配是否合理"""
    if total_hours != theory_hours + practice_hours:
        return False, "总学时必须等于理论学时与实践学时之和"
    if theory_hours < 0 or practice_hours < 0:
        return False, "学时不能为负数"
    return True, ""

def show_generation_progress():
    """显示生成进度"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # 1. 生成毕业要求指标点 (10%)
        status_text.text("正在生成毕业要求指标点...")
        progress_bar.progress(10)
        
        # 2. 生成AACSB学习目标
        status_text.text("正在生成AACSB学习目标...")
        progress_bar.progress(20)
        
    finally:
        progress_bar.empty()
        status_text.empty()

def prepare_document_context():
    """准备文档上下文数据"""
    context = {
        # 基本信息
        'course_name_cn': course_name_cn,
        'course_name_en': course_name_en,
        'course_code': course_code,
        'course_type': course_type,
        'credits': credits,
        'total_hours': total_hours,
        'theory_hours': theory_hours,
        'practice_hours': practice_hours,
        'exam_type': exam_type,
        'exam_form': exam_form,
        'department': department,
        'major': major,
        'prerequisites': prerequisites,
        
        # 业要求指标点
        'graduation_requirements': st.session_state.get('graduation_requirements', {
            'knowledge': [],
            'ability': [],
            'quality': []
        }),
        
        # AACSB学习目标
        'aacsb_goals': st.session_state.get('aacsb_goals', '').split('\n') if st.session_state.get('aacsb_goals') else [],
        
        # 课程简介
        'course_intro': st.session_state.get('course_intro', {
            'position': '',
            'purpose': '',
            'content': '',
            'method': '',
            'outcome': ''
        }),
        
        # 课程目标
        'course_objectives': st.session_state.get('course_objectives', '').split('\n') if st.session_state.get('course_objectives') else [],
        
        # 教材信息
        'course_textbooks': st.session_state.get('course_textbooks', {
            'main': [],
            'references': []
        }),
        
        # 课程目标与毕业要求指标点对应关系
        'objectives_mapping': [
            {
                'number': item['number'],
                'objective': item['objective'],
                'requirements': item['requirements']
            }
            for item in st.session_state.get('objectives_mapping', [])
        ],
        
        # AACSB评估体系
        'aacsb_assessment': st.session_state.get('aacsb_assessment', []),
        
        # 课程内容与学时分配
        'course_schedule': [
            {
                'chapter': item.get('chapter', ''),
                'content': item.get('content', []),
                'requirements': item.get('requirements', []),
                'hours': item.get('hours', ''),
                'type': item.get('type', '')
            }
            for item in st.session_state.get('course_schedule', [])
        ],
        
        # 实验教学内容（如果有）
        'labs_schedule': [
            {
                'number': lab.get('number', ''),
                'name': lab.get('name', ''),
                'content': lab.get('content', []),
                'requirements': lab.get('requirements', []),
                'hours': lab.get('hours', ''),
                'group_size': lab.get('group_size', ''),
                'required': lab.get('required', True),
                'type': lab.get('type', '')
            }
            for lab in st.session_state.get('labs_schedule', [])
        ] if practice_hours > 0 else [],
        
        # 考核方式和评价标准
        'assessment_table': [
            {
                'type': item.get('type', ''),
                'percentage': item.get('percentage', 0),
                'criteria': item.get('criteria', []),
                'objectives': item.get('objectives', [])
            }
            for item in st.session_state.get('assessment_table', [])
        ]
    }
    
    # 添加总评成绩计算方式
    context['total_assessment'] = sum(item.get('percentage', 0) for item in context['assessment_table'])
    
    # 添加实验课程标记
    context['has_labs'] = practice_hours > 0
    
    # 添加试/考查课程标记
    context['is_exam'] = exam_type == "考试"
    
    return context

def provide_document_download(doc):
    """提供文档下载"""
    # 渲染文档到内存
    from io import BytesIO
    doc_io = BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    
    # 使用课程名动态生成文件名
    file_name = f"{course_name_cn}-课程大纲.docx"
    st.download_button(
        label="下载生成的文档",
        data=doc_io,
        file_name=file_name,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    st.success("文档生成成功！")

# Streamlit页面配置和主要UI代码
st.set_page_config(page_title="课程大纲生成器", layout="wide")
st.title("教学大纲生成器")

# 创建两列布局
col1, col2 = st.columns(2)

with col1:
    # 基本信息
    st.subheader("课程基本信息")
    course_name_cn = st.text_input("课程名称(中文)", value="机器学(Python)")
    course_name_en = st.text_input("课程名称(英文)", value="Machine Learning (Python)")
    course_code = st.text_input("课程代码", value="B3104505")
    course_type = st.text_input("课程性质", value="专业必修课")
    
    # 学分和学时
    credits = st.number_input("总学分", value=3)
    total_hours = st.number_input("总学时", value=64)
    theory_hours = st.number_input("理论学时", value=32)
    practice_hours = st.number_input("实验学时", value=32)

with col2:
    # 其他息
    st.subheader("其他信息")
    exam_type = st.radio("期末考核方式", ["考试", "考查"])
    
    # 添加期末考核具体形式选择
    if exam_type == "考试":
        exam_form = st.radio(
            "考试形式",
            ["闭卷笔试", "开卷笔试"],
            help="考试课程必须选择考试形式"
        )
    else:
        exam_form = st.radio(
            "考查形式",
            ["课程论文", "项目报告", "课程设计"],
            help="考查课程可以选择多种考核形式"
        )
    
    department = st.text_input("开课部门", value="经济与管理学院")
    major = st.text_input("适用专业", value="大数据管理与应用")
    prerequisites = st.text_input("先修课程", value="统计学、Python程序设计、数据结构")
    
    # 添加额外信息输入框
    extra_info = st.text_area(
        "额外重要信息",
        placeholder="请输入任何需要特别考虑的信息，如：\n- 特殊的培养目标\n- 行业认证要求\n- 专业特色\n- 就业方向\n- 其他重要说明",
        height=100
    )

# 添加统一的生成按钮
if st.button("🤖 一键生成所有内容", type="primary"):
    with st.spinner("正在生成所有内容..."):
        # 1. 获取毕业要求指标点
        graduation_requirements = get_graduation_requirements(
            department, 
            major,
            extra_info
        )
        if not graduation_requirements:
            st.error("生成毕业要求指标点失败")
            st.stop()
        
        # 保存到session_state
        st.session_state.graduation_requirements = graduation_requirements
        
        # 2. 生成AACSB学习目标 - 修改这部分
        suggested_goals = generate_aacsb_goals(
            course_name_cn,
            course_type,
            department,
            major,
            graduation_requirements,  # 添加毕要求指标点作为参数
            extra_info
        )
        if suggested_goals:
            st.session_state.aacsb_goals = suggested_goals
            
            # 3. 生成课程内容（包含课程目标）
            content = generate_course_content(
                course_name_cn, 
                course_type, 
                department, 
                major, 
                suggested_goals, 
                extra_info,
                total_hours,
                theory_hours,
                practice_hours,
                graduation_requirements
            )
            
            if content:
                # 保存课程简介
                st.session_state.course_intro = content.get('introduction', {})
                
                # 保存课程目标
                st.session_state.course_objectives = "\n".join(content.get('objectives', []))
                
                # 保存教材信息
                st.session_state.course_textbooks = {
                    'main': content.get('textbooks', {}).get('main', []),
                    'references': content.get('textbooks', {}).get('references', [])
                }
                
                # 保存目标映射关系
                if 'objectives_mapping' in content:
                    mapping_data = []
                    for i, mapping in enumerate(content['objectives_mapping'], 1):
                        mapping_data.append({
                            "number": i,
                            "objective": mapping['objective'],
                            "requirements": "；".join(mapping['requirements'])
                        })
                    st.session_state.objectives_mapping = mapping_data
                
                # 4. 生成AACSB评估体系
                assessment_data = generate_aacsb_assessment(
                    suggested_goals,
                    content['objectives'],
                    graduation_requirements
                )
                if assessment_data:
                    st.session_state.aacsb_assessment = assessment_data
                    
                    # 5. 生成课程内容与学时分配
                    schedule_data = generate_course_schedule(
                        content['introduction'],
                        content['objectives'],
                        total_hours,
                        theory_hours
                    )
                    st.session_state.course_schedule = schedule_data
                    
                    # 6. 生成实验教学内容（如果有实验学时）
                    if practice_hours > 0:
                        labs_data = generate_lab_schedule(
                            schedule_data,
                            practice_hours,
                            content['objectives']
                        )
                        if labs_data:
                            st.session_state.labs_schedule = labs_data
                    
                    # 7. 生成考核方式和标准
                    assessment_scheme = generate_assessment_scheme(
                        content['objectives'],
                        assessment_data,
                        labs_data if practice_hours > 0 else None,
                        theory_hours,
                        practice_hours,
                        exam_type,
                        exam_form,
                        course_type
                    )
                    if assessment_scheme:
                        st.session_state.assessment_table = assessment_scheme
                        st.success("所有内容生成完成！")
                        st.rerun()
                else:
                    st.error("生成AACSB评估体系失败")
            else:
                st.error("生成课程内容失败")
        else:
            st.error("生成AACSB学习目标失败")

# 添加课程简介显示函数
def display_course_intro(intro_data):
    """显示课程简介"""
    st.subheader("课程简介")
    
    if not intro_data:
        st.info("暂无课程简介")
        return
        
    try:
        if isinstance(intro_data, dict):
            st.markdown("**课程定位**")
            st.write(intro_data.get('position', ''))
            
            st.markdown("**课程目的**")
            st.write(intro_data.get('purpose', ''))
            
            st.markdown("**课程内容**")
            st.write(intro_data.get('content', ''))
            
            st.markdown("**教学方法**")
            st.write(intro_data.get('method', ''))
            
            st.markdown("**预期成果**")
            st.write(intro_data.get('outcome', ''))
        else:
            st.write(intro_data)
            
    except Exception as e:
        st.error(f"显示课程简介时出错：{str(e)}")
    
# 添加教材信息显示函数
def display_textbooks(textbooks_data):
    """显示教材信息"""
    st.subheader("教材及参考资料")
    
    if not textbooks_data:
        st.info("暂无教材信息")
        return
        
    try:
        # 显示主教材
        st.markdown("**主教材**")
        if 'main' in textbooks_data:
            for book in textbooks_data['main']:
                st.write(f"- {book}")
        else:
            st.info("暂无主教材信息")
            
        # 显示参考资料
        st.markdown("**参考资料**")
        if 'references' in textbooks_data:
            for ref in textbooks_data['references']:
                st.write(f"- {ref}")
        else:
            st.info("暂无参考资料信息")
            
    except Exception as e:
        st.error(f"显示教材信息时出错：{str(e)}")
    
# 添加显示AACSB学习目标的函数
def display_aacsb_goals(goals_data):
    """显示AACSB学习目标"""
    st.subheader("AACSB学习目标")
    
    if not goals_data:
        st.info("暂无AACSB学习目标数据")
        return
        
    try:
        # 如果是字符串格式，按换行符分割
        if isinstance(goals_data, str):
            goals = goals_data.split('\n')
        # 如果是列表格式��直接使用
        elif isinstance(goals_data, list):
            goals = goals_data
        else:
            st.error("AACSB学习目标数据格式不正确")
            return
            
        # 显示每个学习目标
        for goal in goals:
            if goal.strip():  # 只显示非空目标
                st.write(f"- {goal.strip()}")
            
    except Exception as e:
        st.error(f"显示AACSB学习目标时出错：{str(e)}")

# 添加显示课程目标的函数
def display_course_objectives(objectives_data):
    """显示课程目标"""
    st.subheader("课程目标")
    
    if not objectives_data:
        st.info("暂无课程目标数据")
        return
        
    try:
        # 果是字符串格式，按换行符分割
        if isinstance(objectives_data, str):
            objectives = objectives_data.split('\n')
        # 如果是列表格式，直接使用
        elif isinstance(objectives_data, list):
            objectives = objectives_data
        else:
            st.error("课程目标数据格式不正确")
            return
            
        # 显示每个课程目标
        for objective in objectives:
            if objective.strip():  # 只显示非空目标
                st.write(f"- {objective.strip()}")
            
    except Exception as e:
        st.error(f"显示课程目标时出错：{str(e)}")

# 添加显示课程考核及成绩评定说明的函数
def display_assessment_description(assessment_table):
    """显示课程考核及成绩评定说明"""
    st.subheader("课程考核及成绩评定说明")
    
    if not assessment_table:
        st.info("暂无课程考核及成绩评定说明")
        return
        
    try:
        # 1. 总体说明
        st.markdown("**1. 考核方式及成绩构成**")
        total_score = 0
        for item in assessment_table:
            score_type = item.get('type', '')
            percentage = item.get('percentage', 0)
            total_score += percentage
            st.write(f"- {score_type}：占总成绩的{percentage}%")
        st.write(f"总计：{total_score}%")
        
        # 2. 详细说明
        st.markdown("**2. 各部分考核说明**")
        for item in assessment_table:
            st.markdown(f"**（{item.get('type', '')}）{item.get('percentage', '')}%**")
            criteria = item.get('criteria', [])
            for criterion in criteria:
                st.write(f"- {criterion}")
            
            # 显示对应的课程目标
            objectives = item.get('objectives', [])
            if objectives:
                st.write(f"*对应课程目标：{', '.join(objectives)}*")
            st.write("")  # 添加空行分隔
        
        # 3. 补充说明
        st.markdown("**3. 补充说明**")
        st.write("- 所有成绩均采用百分制记分")
        st.write("- 各部分成绩按照权重加权平均得到最终成绩")
        if any(item.get('type') == '期末考试' for item in assessment_table):
            st.write("- 期末考试成绩不及格者，总评成绩不及格")
        if any(item.get('type', '').startswith('实验') for item in assessment_table):
            st.write("- 实验成绩不及格者，总评成绩不及格")
            
    except Exception as e:
        st.error(f"显示课程考核及成绩评定说明时出错：{str(e)}")

# 在主程序中显示所有内容（按顺序）
# 1. 显示毕业要求指标点
display_graduation_requirements(st.session_state.get('graduation_requirements', {}))

# 2. 显示AACSB学习目标
display_aacsb_goals(st.session_state.get('aacsb_goals', ''))

# 3. 显示课程简介
display_course_intro(st.session_state.get('course_intro', {}))

# 4. 显示课程目标
display_course_objectives(st.session_state.get('course_objectives', ''))

# 5. 显示教材信息
display_textbooks(st.session_state.get('course_textbooks', {}))

# 6. 显示课程目标与毕业要求指标点对应关系
display_objectives_mapping(st.session_state.get('objectives_mapping', []))

# 7. 显示AACSB评估体系
display_aacsb_assessment(st.session_state.get('aacsb_assessment', []))

# 8. 显示课程内容与学时分配
display_course_schedule(st.session_state.get('course_schedule', []))

# 9. 显示实验教学内容（如果有）
if practice_hours > 0:
    labs_data = st.session_state.get('labs_schedule', [])
    display_lab_schedule(labs_data)

# 10. 显示课程考核及成绩评定说明
display_assessment_description(st.session_state.get('assessment_table', []))

# 11. 显示考核方式和评价标准
display_assessment_table(st.session_state.get('assessment_table', []))

# 在生成文档按钮旁边添加下载数据按钮
col_doc, col_data = st.columns(2)

with col_doc:
    if st.button("📄 生成文档", key="generate_doc"):
        # 验证数据完整性
        missing_data = validate_data()
        if missing_data:
            st.error(f"以下内容尚未生成：\n" + "\n".join([f"- {item}" for item in missing_data]))
            st.stop()
        
        try:
            # 加载模板
            doc = DocxTemplate("template.docx")
            
            # 准备上下文数据
            context = prepare_document_context()
            
            # 检查数据
            if context['objectives_mapping']:
                st.write("课程目标与毕业要求指标点对应关系数据已准备")
            
            # 渲染文档
            doc.render(context)
            
            # 提供下载
            provide_document_download(doc)
            
        except Exception as e:
            st.error(f"生成文档时出错：{str(e)}")

with col_data:
    if st.button("💾 下载课程数据", key="download_data"):
        try:
            # 准备所有数据
            all_data = {
                # 基本信息
                "basic_info": {
                    "course_name_cn": course_name_cn,
                    "course_name_en": course_name_en,
                    "course_code": course_code,
                    "course_type": course_type,
                    "credits": credits,
                    "total_hours": total_hours,
                    "theory_hours": theory_hours,
                    "practice_hours": practice_hours,
                    "exam_type": exam_type,
                    "exam_form": exam_form,  # 添加考核具体形式
                    "department": department,
                    "major": major,
                    "prerequisites": prerequisites,
                    "extra_info": extra_info
                },
                
                # 从session_state获取已生成的数据
                "graduation_requirements": st.session_state.get('graduation_requirements', {}),
                "aacsb_goals": st.session_state.get('aacsb_goals', ''),
                "course_intro": st.session_state.get('course_intro', {}),
                "course_objectives": st.session_state.get('course_objectives', ''),
                "course_textbooks": st.session_state.get('course_textbooks', {}),
                "objectives_mapping": st.session_state.get('objectives_mapping', []),
                "aacsb_assessment": st.session_state.get('aacsb_assessment', []),
                "course_schedule": st.session_state.get('course_schedule', []),
                "assessment_table": st.session_state.get('assessment_table', [])
            }
            
            # 只在有实验学时时添加实验相关数据
            if practice_hours > 0:
                all_data["labs_schedule"] = st.session_state.get('labs_schedule', [])
            
            # 转换为JSON字符串，确保中文正确显示
            json_str = json.dumps(all_data, ensure_ascii=False, indent=2)
            
            # 创建下载按钮
            st.download_button(
                label="点击下载JSON文件",
                data=json_str.encode('utf-8'),
                file_name=f"{course_name_cn}_课程大纲数据.json",
                mime="application/json",
            )
            
            # 显示数据完整性提示
            missing_data = validate_data()
            if missing_data:
                st.warning(f"⚠️ 以下内容尚未生成，但您仍可以下载已有数据：\n" + "\n".join([f"- {item}" for item in missing_data]))
            else:
                st.success("所有数据已生成完成！")
            
        except Exception as e:
            st.error(f"准备数据文件时出错：{str(e)}")

# 添加数据导入功能
st.subheader("导入课程数据")
uploaded_file = st.file_uploader("选择要导入的JSON文件", type=['json'], key="upload_json")

if uploaded_file is not None:
    try:
        # 读取并解析JSON文件
        content = uploaded_file.read()
        data = json.loads(content.decode('utf-8'))
        
        # 更新session_state中的数据
        for key in [
            'graduation_requirements', 'aacsb_goals', 'course_intro',
            'course_objectives', 'course_textbooks', 'objectives_mapping',
            'aacsb_assessment', 'course_schedule', 'assessment_table',
            'labs_schedule'
        ]:
            if key in data:
                st.session_state[key] = data[key]
        
        # 更新表单中的基本信息
        if 'basic_info' in data:
            basic_info = data['basic_info']
            # 这里不能直接更新表单值，但可以显示提示信息
            st.success("数据导入成功！请刷新页面以更新表单值。")
            st.json(basic_info)  # 显示导入的基本信息
            
    except Exception as e:
        st.error(f"导入数据时出错：{str(e)}")

