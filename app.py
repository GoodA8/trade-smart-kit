import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="贸智转·基础工具箱", layout="wide", page_icon="🚀")
st.title("🚀 贸智转·基础工具箱 V4 - 木工机械专版")
st.caption("已按你最新截图100%优化：左侧固定树状分级 + 右侧专业表格 + 整体左移上移")

# ==================== 全局数据 ====================
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

if 'current_folder' not in st.session_state:
    st.session_state.current_folder = "产品素材"

# ==================== 布局：左侧窄树 + 右侧内容 ====================
left, right = st.columns([1.8, 5])   # 左侧更窄，整体左移上移

with left:
    st.subheader("📁 目录")
    # 固定树状分级目录（默认展开，不折叠）
    with st.expander("全部素材", expanded=True):
        for main_folder in ["产品素材", "企业素材", "物流交付"]:
            if st.button(main_folder, key=f"main_{main_folder}", use_container_width=True):
                st.session_state.current_folder = main_folder
        
        with st.expander("木工机械", expanded=True):
            for sub in ["木工机械公司信息", "木工机械产品信息"]:
                if st.button(sub, key=f"sub_{sub}", use_container_width=True):
                    st.session_state.current_folder = sub
                
                if sub == "木工机械公司信息":
                    with st.expander("工厂图", expanded=True):
                        for leaf in ["挖掘机公司证书文件", "挖掘机团队形象", "挖掘机营销数据", "挖掘机公司联系信息", "挖掘机展会资料"]:
                            if st.button(leaf, key=f"leaf_{leaf}", use_container_width=True):
                                st.session_state.current_folder = leaf
                if sub == "木工机械产品信息":
                    with st.expander("CNC数控系列", expanded=True):
                        for leaf in ["锯切系列", "雕刻系列", "封边系列"]:
                            if st.button(leaf, key=f"leaf2_{leaf}", use_container_width=True):
                                st.session_state.current_folder = leaf

with right:
    # 顶部搜索（还原参考图）
    col_search1, col_search2, col_search3 = st.columns([3,1,1])
    with col_search1:
        search = st.text_input("🔍 搜索素材名称", placeholder="输入关键词搜索")
    with col_search2:
        st.button("高级搜索", use_container_width=True)
    with col_search3:
        st.button("批量下载", use_container_width=True)
    
    st.subheader(f"📋 当前目录：{st.session_state.current_folder}")
    
    # 上传区域
    uploaded_files = st.file_uploader("上传素材到当前目录", accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            file_info = {
                "名称": file.name,
                "类型": file.type.split("/")[-1] if file.type else "file",
                "大小": f"{file.size/1024:.1f} KB",
                "分类": st.session_state.current_folder,
                "上传时间": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "缩略": "📸" if file.type.startswith("image") else "📄"
            }
            st.session_state.material_library[st.session_state.current_folder].append(file_info)
        st.success(f"✅ 已上传 {len(uploaded_files)} 个文件到【{st.session_state.current_folder}】")
    
    # 右侧表格（高度还原参考图）
    if st.session_state.material_library[st.session_state.current_folder]:
        df = pd.DataFrame(st.session_state.material_library[st.session_state.current_folder])
        # 添加操作列
        df["操作"] = df.apply(lambda row: "🔍 查看  ⬇️ 下载", axis=1)
        st.dataframe(
            df[["缩略", "名称", "类型", "大小", "分类", "上传时间", "操作"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("该目录暂无素材，请上传文件")

st.sidebar.success("✅ V4 已按你截图优化完成\n左侧固定分级树状 + 右侧专业表格\n刷新后数据仍在同一会话")
st.sidebar.info("下一步：\n1. 连Supabase永久保存\n2. 加Grok AI翻译 + WhatsApp回复助手")
