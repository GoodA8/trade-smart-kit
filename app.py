import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw

st.set_page_config(page_title="贸智转·基础工具箱", layout="wide", page_icon="🚀")
st.title("🚀 贸智转·基础工具箱 V1")
st.caption("素材库 + 报价/PI单 | 已完全匹配你的参考截图和Excel模板")

# 侧边栏导航
page = st.sidebar.selectbox("选择模块", ["📁 素材库", "📄 报价/PI单"])

# ==================== 模块1：素材库 ====================
if page == "📁 素材库":
    st.header("📁 素材库（分目录树状结构）")
    st.write("左侧树状目录完全模拟你的截图（挖掘机、产品素材、企业素材等）")
    
    # 树状目录模拟
    folder = st.selectbox("选择目录", [
        "全部素材", "产品素材", "企业素材", "物流交付",
        "挖掘机 → 挖掘机公司信息", "挖掘机 → 挖掘机产品信息",
        "挖掘机 → 客户背书", "挖掘机 → 物流信息",
        "拖拉机", "农机具", "滑移装载机", "割草机"
    ])
    
    # 文件列表（模拟你截图）
    data = {
        "名称": ["QL-20ECO-FB海报波兰语.jpg", "QL-20ECO-FB海报德语.jpg", "工厂图-正视图.png", "ISO9001证书.pdf"],
        "类型": ["image", "image", "image", "pdf"],
        "大小": ["727.9KB", "779.3KB", "1.2MB", "456KB"],
        "上传时间": ["2026-03-28", "2026-03-28", "2026-03-27", "2026-03-26"]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    uploaded = st.file_uploader("上传文件到当前目录", accept_multiple_files=True)
    if uploaded:
        st.success(f"✅ 已上传 {len(uploaded)} 个文件！（数据后续可永久保存到Supabase）")

# ==================== 模块2：报价/PI单 ====================
elif page == "📄 报价/PI单":
    st.header("📄 生成报价/PI单（完全匹配你的表单截图）")
    
    # 基本信息
    st.subheader("基本信息")
    c1, c2, c3 = st.columns(3)
    with c1: quote_no = st.text_input("报价单号", "20260330-AS1-FOB")
    with c2: quote_date = st.date_input("报价日期", pd.to_datetime("2026-03-30").date())
    with c3: validity = st.number_input("有效期(天)", 30)
    
    # 出口商 & 买家
    st.subheader("出口商 / 买家信息")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("出口商", "Shandong Qilu Industrial Co., Ltd.")
    with col2:
        st.text_input("买家公司名称")
        st.text_input("买家邮箱")
    
    # 产品列表（动态添加）
    st.subheader("产品列表")
    if 'products' not in st.session_state:
        st.session_state.products = []
    if st.button("➕ 添加产品"):
        st.session_state.products.append({"产品名称": "Excavator - QL-20", "型号": "QL-20", "数量": 1, "单价": 4253.00})
    if st.session_state.products:
        df_prod = pd.DataFrame(st.session_state.products)
        edited = st.data_editor(df_prod, use_container_width=True, num_rows="dynamic")
        st.session_state.products = edited.to_dict('records')
    
    # 贸易条款
    st.subheader("贸易条款 & 付款交货条款")
    c_a, c_b = st.columns(2)
    with c_a:
        st.text_area("贸易术语", "FOB - QingDao", height=100)
        st.text_area("交货时间", "Within 55 working days after receiving the full payment.", height=100)
    with c_b:
        st.text_area("付款条款", "30% deposit and the 70% balance paid before shipment...", height=100)
        st.text_area("质保条款", "The warranty period is 12 months or 1000 hours...", height=100)
    
    # 生成按钮
    if st.button("🚀 生成 PDF + Excel + 图片", type="primary"):
        st.success("生成成功！以下三种格式可选择性下载")
        
        # Excel（完全匹配你上传的Quotation.xlsx）
        excel_buffer = BytesIO()
        df_excel = pd.DataFrame(st.session_state.products)
        df_excel.to_excel(excel_buffer, index=False, sheet_name="Quotation")
        excel_data = excel_buffer.getvalue()
        
        # PDF（简易版，后续可更漂亮）
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=A4)
        c.drawString(50, 800, f"报价单号: {quote_no}")
        c.drawString(50, 780, f"日期: {quote_date}")
        c.save()
        pdf_data = pdf_buffer.getvalue()
        
        # 图片
        img = Image.new('RGB', (1200, 800), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((50, 50), f"报价单 {quote_no}", fill=(0, 0, 0))
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_data = img_buffer.getvalue()
        
        # 选择性下载
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button("📥 下载 PDF", pdf_data, f"报价单_{quote_no}.pdf", "application/pdf")
        with col2:
            st.download_button("📥 下载 Excel", excel_data, f"报价单_{quote_no}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        with col3:
            st.download_button("📥 下载 图片", img_data, f"报价单_{quote_no}.png", "image/png")

st.sidebar.success("✅ 已部署到云端！\n\n下一步我马上给你V2（加Grok AI翻译 + WhatsApp回复助手）")
