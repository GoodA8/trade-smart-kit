import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="贸智转·基础工具箱", layout="wide", page_icon="🚀")
st.title("🚀 贸智转·基础工具箱 V3 - 木工机械专版")
st.caption("已按你最新截图优化布局 + 滑动目录 + 分类上传保存")

# ==================== 全局数据（临时保存）===================
if 'material_library' not in st.session_state:
    st.session_state.material_library = {
        "产品素材": [],
        "企业素材": [],
        "物流交付": [],
        "木工机械公司信息": [],
        "木工机械产品信息": [],
        "客户背书": [],
        "物流信息": [],
        "CNC数控系列": [],
        "锯切系列": [],
        "雕刻系列": [],
        "封边系列": []
    }

# ==================== 布局：左侧窄栏 + 中间滑动 + 右侧内容 ====================
left_col, main_col = st.columns([1.2, 4.8])   # 左侧窄，右侧宽且紧凑

with left_col:
    st.subheader("📁 目录")
    # 模拟树状目录（可展开）
    with st.expander("全部素材", expanded=True):
        for folder in list(st.session_state.material_library.keys()):
            if st.button(folder, key=f"btn_{folder}", use_container_width=True):
                st.session_state.current_folder = folder

# 中间滑动区域（卡片式，可左右滑动）
with main_col:
    st.subheader("📌 快速选择目录（滑动查看）")
    categories = list(st.session_state.material_library.keys())
    tabs = st.tabs(categories)   # 滑动Tabs，点击切换
    
    current_folder = None
    for i, tab in enumerate(tabs):
        with tab:
            if st.button(f"进入 {categories[i]}", key=f"tab_{i}"):
                st.session_state.current_folder = categories[i]
                current_folder = categories[i]

    # 右侧内容（自动加载选中目录）
    if 'current_folder' in st.session_state:
        current_folder = st.session_state.current_folder
        st.subheader(f"📋 当前目录：{current_folder}")
        
        # 上传
        uploaded_files = st.file_uploader("上传素材到当前目录", accept_multiple_files=True)
        if uploaded_files:
            for file in uploaded_files:
                file_info = {
                    "名称": file.name,
                    "类型": file.type.split("/")[-1],
                    "大小": f"{file.size/1024:.1f}KB",
                    "上传时间": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state.material_library[current_folder].append(file_info)
            st.success(f"✅ 已上传 {len(uploaded_files)} 个文件到【{current_folder}】")
        
        # 显示文件列表
        if st.session_state.material_library[current_folder]:
            df = pd.DataFrame(st.session_state.material_library[current_folder])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("该目录暂无文件，点击上方上传")

# 右侧提示（整体往上左移）
st.sidebar.success("✅ V3 已优化：\n- 左侧窄版树状\n- 中间滑动目录\n- 上传临时保存\n- 布局更紧凑")
st.sidebar.info("刷新后数据仍在（同一浏览器会话）。下一步连Supabase永久保存 + Grok AI翻译")

st.caption("素材库已完全按木工机械类目设计，接下来可直接加报价单AI功能")
