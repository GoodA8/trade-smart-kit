import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="贸智转·基础工具箱", layout="wide", page_icon="🚀")

# ==================== 全局素材数据 ====================
if 'material_library' not in st.session_state:
    st.session_state.material_library = {
        "企业信息": {"公司资质": [], "企业宣传": [], "证书文件": [], "团队形象": []},
        "木工机械": {
            "系列1": {"型号1": {"图片": [], "视频": []}, "型号2": {"图片": [], "视频": []}},
            "系列2": {"图片": [], "视频": []}
        },
        "物流交付": []
    }

if 'current_path' not in st.session_state:
    st.session_state.current_path = ["企业信息"]

# ==================== 左侧导航栏 ====================
with st.sidebar:
    st.image("https://via.placeholder.com/150x60?text=公司Logo", use_column_width=True)  # 替换成你的真实Logo
    st.button("📁 素材库", use_container_width=True, on_click=lambda: st.session_state.update(page="素材库"))
    st.button("📄 报价单", use_container_width=True, on_click=lambda: st.session_state.update(page="报价单"))
    st.button("🤖 AI谈单助手", use_container_width=True, on_click=lambda: st.session_state.update(page="AI谈单助手"))
    st.button("🚀 AI获客", use_container_width=True, on_click=lambda: st.session_state.update(page="AI获客"))
    st.button("⋯ 更多", use_container_width=True)

# ==================== 主页面 ====================
page = st.session_state.get("page", "素材库")

if page == "素材库":
    st.title("素材库信息")

    col_left, col_right = st.columns([2, 5])

    # 左侧树状目录（严格按你的草图）
    with col_left:
        st.subheader("目录")
        
        # 企业信息
        if st.button("▼ 企业信息", key="ei", use_container_width=True):
            st.session_state.current_path = ["企业信息"]
        with st.expander("企业信息", expanded=True):
            for item in ["公司资质", "企业宣传", "证书文件", "团队形象"]:
                if st.button(item, key=f"ei_{item}", use_container_width=True):
                    st.session_state.current_path = ["企业信息", item]

        # 木工机械（多级）
        with st.expander("木工机械", expanded=True):
            for series in ["系列1", "系列2"]:
                if st.button(f"▼ {series}", key=f"s_{series}", use_container_width=True):
                    st.session_state.current_path = ["木工机械", series]
                if series == "系列1":
                    with st.expander("系列1", expanded=True):
                        for model in ["型号1", "型号2"]:
                            if st.button(model, key=f"m_{model}", use_container_width=True):
                                st.session_state.current_path = ["木工机械", "系列1", model]
                            with st.expander(model, expanded=False):
                                for file_type in ["图片", "视频"]:
                                    if st.button(file_type, key=f"ft_{model}_{file_type}", use_container_width=True):
                                        st.session_state.current_path = ["木工机械", "系列1", model, file_type]

    # 右侧表格（严格按原图1风格）
    with col_right:
        current_str = " > ".join(st.session_state.current_path)
        st.subheader(f"当前目录：{current_str}")

        # 顶部操作栏
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1:
            st.text_input("搜索", placeholder="搜索素材名称", label_visibility="collapsed")
        with c2:
            st.button("高级搜索", use_container_width=True)
        with c3:
            st.button("批量下载", use_container_width=True)

        # 表格
        # 这里用模拟数据演示结构，你上传后会显示真实文件
        demo_data = [
            {"缩略": "📸", "名称": "产品效果图-正面.jpg", "类型": "image", "大小": "1.2 MB", "分类": "产品素材", "上传时间": "2026-03-30 14:20", "操作": "查看 下载"},
            {"缩略": "📄", "名称": "公司资质证书.pdf", "类型": "pdf", "大小": "856 KB", "分类": "企业信息", "上传时间": "2026-03-29 09:15", "操作": "查看 下载"}
        ]
        
        df = pd.DataFrame(demo_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # 上传区域
        uploaded_files = st.file_uploader("上传文件到当前目录", accept_multiple_files=True)
        if uploaded_files:
            st.success(f"✅ 已成功上传 {len(uploaded_files)} 个文件到当前目录！（当前为演示，后面会永久保存）")

else:
    st.title(f"{page}")
    st.info(f"【{page}】模块正在开发中...\n你画草图告诉我具体要什么功能，我立刻加上。")

st.caption("贸智转·基础工具箱 | 按你的草图V7实现")
