import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="贸智转·基础工具箱", layout="wide", page_icon="🚀")
st.title("🚀 贸智转·基础工具箱 V5 - 木工机械专版")
st.caption("左侧固定树状分级 + 右侧专业表格 + 整体左移上移")

# 全局数据
if 'material_library' not in st.session_state:
    st.session_state.material_library = {
        "产品素材": [], "企业素材": [], "物流交付": [],
        "木工机械公司信息": [], "木工机械产品信息": [],
        "客户背书": [], "物流信息": [],
        "CNC数控系列": [], "锯切系列": [], "雕刻系列": [], "封边系列": []
    }
if 'current_folder' not in st.session_state:
    st.session_state.current_folder = "产品素材"

# 布局：左侧窄树 + 右侧内容（整体左移上移）
left, right = st.columns([1.5, 5.5])   # 左侧更窄

with left:
    st.subheader("📁 目录")
    # 固定竖向树状（默认展开，不折叠）
    for main in ["产品素材", "企业素材", "物流交付"]:
        if st.button(main, key=f"main_{main}", use_container_width=True):
            st.session_state.current_folder = main
    
    with st.expander("木工机械", expanded=True):
        for sub in ["木工机械公司信息", "木工机械产品信息"]:
            if st.button(sub, key=f"sub_{sub}", use_container_width=True):
                st.session_state.current_folder = sub
            
            if sub == "木工机械公司信息":
                with st.expander("工厂图", expanded=True):
                    for leaf in ["证书文件", "团队形象", "营销数据", "联系信息", "展会资料"]:
                        if st.button(leaf, key=f"leaf_{leaf}", use_container_width=True):
                            st.session_state.current_folder = leaf
            if sub == "木工机械产品信息":
                with st.expander("CNC数控系列", expanded=True):
                    for leaf in ["锯切系列", "雕刻系列", "封边系列"]:
                        if st.button(leaf, key=f"leaf2_{leaf}", use_container_width=True):
                            st.session_state.current_folder = leaf

with right:
    # 顶部搜索 + 批量下载
    c1, c2, c3 = st.columns([3, 1, 1])
    with c1: st.text_input("🔍 搜索素材名称", placeholder="输入关键词")
    with c2: st.button("高级搜索", use_container_width=True)
    with c3: st.button("批量下载", use_container_width=True)
    
    st.subheader(f"📋 当前目录：{st.session_state.current_folder}")
    
    # 上传
    uploaded = st.file_uploader("上传素材到当前目录", accept_multiple_files=True)
    if uploaded:
        for f in uploaded:
            info = {
                "名称": f.name, "类型": f.type.split("/")[-1], "大小": f"{f.size/1024:.1f} KB",
                "分类": st.session_state.current_folder, "上传时间": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.material_library[st.session_state.current_folder].append(info)
        st.success(f"✅ 已上传 {len(uploaded)} 个文件")
    
    # 右侧专业表格
    data = st.session_state.material_library[st.session_state.current_folder]
    if data:
        df = pd.DataFrame(data)
        df["操作"] = "🔍 查看  ⬇️ 下载"
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("该目录暂无素材，请上传")

st.sidebar.success("V5 已按你截图彻底优化左侧树状")
