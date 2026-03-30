import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="贸智转·基础工具箱", layout="wide", page_icon="🚀")

# 全局数据（素材库用）
if 'material_library' not in st.session_state:
    st.session_state.material_library = {
        "产品素材": [], "企业素材": [], "物流交付": [],
        "木工机械公司信息": [], "木工机械产品信息": [],
        "客户背书": [], "物流信息": [],
        "CNC数控系列": [], "锯切系列": [], "雕刻系列": [], "封边系列": []
    }
if 'current_folder' not in st.session_state:
    st.session_state.current_folder = "产品素材"

# ==================== 左侧垂直主导航栏 ====================
st.sidebar.title("贸智转")
st.sidebar.button("📁 素材库", use_container_width=True, on_click=lambda: st.session_state.update(page="素材库"))
st.sidebar.button("📄 报价单", use_container_width=True, on_click=lambda: st.session_state.update(page="报价单"))
st.sidebar.button("🤖 AI助手", use_container_width=True, on_click=lambda: st.session_state.update(page="AI助手"))
st.sidebar.button("🚀 获客", use_container_width=True, on_click=lambda: st.session_state.update(page="获客"))
st.sidebar.button("⋯ 更多模块", use_container_width=True, on_click=lambda: st.session_state.update(page="更多"))

st.sidebar.divider()   # 分隔线

# ==================== 主内容区 ====================
page = st.session_state.get("page", "素材库")

if page == "素材库":
    st.title("📁 素材库 - 木工机械专版")
    
    left, right = st.columns([1.5, 5.5])
    with left:
        st.subheader("目录")
        for main in ["产品素材", "企业素材", "物流交付"]:
            if st.button(main, key=f"m_{main}", use_container_width=True):
                st.session_state.current_folder = main
        with st.expander("木工机械", expanded=True):
            for sub in ["木工机械公司信息", "木工机械产品信息"]:
                if st.button(sub, key=f"s_{sub}", use_container_width=True):
                    st.session_state.current_folder = sub
                if sub == "木工机械公司信息":
                    with st.expander("工厂图", expanded=True):
                        for leaf in ["证书文件", "团队形象", "营销数据", "联系信息", "展会资料"]:
                            if st.button(leaf, key=f"l_{leaf}", use_container_width=True):
                                st.session_state.current_folder = leaf
                if sub == "木工机械产品信息":
                    with st.expander("CNC数控系列", expanded=True):
                        for leaf in ["锯切系列", "雕刻系列", "封边系列"]:
                            if st.button(leaf, key=f"l2_{leaf}", use_container_width=True):
                                st.session_state.current_folder = leaf

    with right:
        st.subheader(f"当前目录：{st.session_state.current_folder}")
        uploaded = st.file_uploader("上传素材到当前目录", accept_multiple_files=True)
        if uploaded:
            for f in uploaded:
                info = {"名称": f.name, "类型": f.type.split("/")[-1], "大小": f"{f.size/1024:.1f} KB", "上传时间": datetime.now().strftime("%Y-%m-%d %H:%M")}
                st.session_state.material_library[st.session_state.current_folder].append(info)
            st.success(f"✅ 已上传 {len(uploaded)} 个文件")
        
        data = st.session_state.material_library[st.session_state.current_folder]
        if data:
            df = pd.DataFrame(data)
            df["操作"] = "🔍 查看  ⬇️ 下载"
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("该目录暂无素材，请上传")

elif page == "报价单":
    st.title("📄 报价单")
    st.info("报价单模块占位页 —— 你画草图告诉我需要什么字段，我就立刻加上完整功能")
    
elif page == "AI助手":
    st.title("🤖 AI助手")
    st.info("AI助手模块占位页 —— 后续可放WhatsApp回复助手、Grok翻译等")

elif page == "获客":
    st.title("🚀 获客")
    st.info("获客模块占位页 —— 后续可放买家背调、开发信生成等")

else:
    st.title("更多模块")
    st.info("这里可以继续扩展你想要的任何新模块")

st.sidebar.success("V6 已按你最新截图完成\n左侧现在是垂直主导航栏 + 分隔线")
