import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="贸智转·素材库", layout="wide", page_icon="📁")

st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .sidebar .sidebar-content { background-color: #ffffff; }
    .dataframe { font-size: 14px; }
</style>
""", unsafe_allow_html=True)

st.title("📁 素材库")

# 左侧树状目录（尽量还原参考图）
col_left, col_right = st.columns([2, 5])

with col_left:
    st.subheader("目录")
    
    # 顶级目录
    if st.button("📁 全部素材", use_container_width=True):
        st.session_state.current_folder = "全部素材"
    
    for item in ["产品素材", "企业素材", "物流交付"]:
        if st.button(item, use_container_width=True):
            st.session_state.current_folder = item
    
    with st.expander("▼ 木工机械", expanded=True):
        if st.button("木工机械公司信息", use_container_width=True):
            st.session_state.current_folder = "木工机械公司信息"
        
        with st.expander("▼ 木工机械产品信息", expanded=True):
            for series in ["CNC数控系列", "锯切系列", "雕刻系列", "封边系列"]:
                if st.button(series, use_container_width=True):
                    st.session_state.current_folder = series

# 右侧内容
with col_right:
    st.subheader("素材库 > 全部素材")
    
    # 顶部操作栏（高度还原）
    c1, c2, c3, c4 = st.columns([3, 1.2, 1.2, 1])
    with c1:
        st.text_input("搜索素材名称", placeholder="输入关键词", label_visibility="collapsed")
    with c2:
        st.button("高级搜索", use_container_width=True)
    with c3:
        st.button("批量下载", use_container_width=True)
    with c4:
        st.button("视图切换", use_container_width=True)  # 可以后续改成卡片/列表切换
    
    # 模拟真实文件数据（带缩略图风格）
    data = [
        {"名称": "QL-20ECO-FB海报波兰语.jpg", "类型": "image", "大小": "727.9KB", "分类": "产品素材", "上传时间": "2026-03-28 14:17", "操作": "查看 下载"},
        {"名称": "QL-20ECO-FB海报德语.jpg", "类型": "image", "大小": "779.3KB", "分类": "产品素材", "上传时间": "2026-03-28 14:16", "操作": "查看 下载"},
        {"名称": "公司资质证书.pdf", "类型": "pdf", "大小": "456KB", "分类": "企业素材", "上传时间": "2026-03-27 10:05", "操作": "查看 下载"},
    ]
    
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # 上传区域
    st.file_uploader("上传新素材", accept_multiple_files=True, label_visibility="collapsed")

st.caption("当前为 Streamlit 最高还原版本。如果需要更像原图的现代UI，推荐切换到 Bubble.io 或 Retool 等低代码平台。")
