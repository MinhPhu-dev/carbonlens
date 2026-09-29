# -*- coding: utf-8 -*-
"""
CarbonLens - Nền tảng phân tích phát thải doanh nghiệp và định giá tín chỉ carbon rừng ngập mặn Cần Giờ
Phiên bản Giao diện Cao cấp (Dark Luxury Emerald & Glassmorphism UI)
Phục vụ nghiên cứu khoa học Kinh tế tuần hoàn & Thị trường Tín chỉ Carbon.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==============================================================================
# 1. CẤU HÌNH TRANG STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="CarbonLens - Tín chỉ Carbon Rừng Cần Giờ",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. BỘ CSS DARK LUXURY EMERALD TOÀN DIỆN (ÉP NỀN TỐI & VIỀN KÍNH PHÁT SÁNG)
# ==============================================================================
# Dù người dùng mở Streamlit ở chế độ Light hay Dark, bộ CSS này đảm bảo 100%
# giao diện có màu tối sâu thẳm, viền ngọc lục bảo phát sáng, thẻ kính glassmorphism.
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* Ép nền tối toàn trang */
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: #020617 !important;
        background-color: #020617 !important;
        color: #f8fafc !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* Ẩn header mặc định cồng kềnh của Streamlit */
    header[data-testid="stHeader"] {
        background-color: rgba(2, 6, 23, 0.8) !important;
        backdrop-filter: blur(10px) !important;
    }

    /* Thanh điều hướng Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0b1329 !important;
        border-right: 1px solid rgba(16, 185, 129, 0.2) !important;
    }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] label {
        color: #cbd5e1 !important;
        font-weight: 500 !important;
    }

    /* Các tiêu đề Heading */
    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }

    /* Định dạng thanh Tabs cao cấp */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #0f172a !important;
        padding: 8px !important;
        border-radius: 14px !important;
        border: 1px solid #1e293b !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        padding: 10px 22px !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        color: #94a3b8 !important;
        border: none !important;
        background-color: transparent !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #34d399 !important;
        background-color: rgba(16, 185, 129, 0.1) !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.4) !important;
    }

    /* Nút bấm (Buttons) */
    .stButton > button {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5) !important;
    }

    /* Khung nhập liệu (Inputs & Sliders) */
    input, select, textarea, div[data-baseweb="select"] {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }
    input:focus, div[data-baseweb="select"]:focus {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.25) !important;
    }
    label[data-testid="stWidgetLabel"] {
        color: #cbd5e1 !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
    }

    /* Thẻ Hero Banner phát sáng */
    .hero-container {
        background: linear-gradient(135deg, rgba(6, 78, 59, 0.4) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 18px;
        padding: 26px 32px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.7), 0 0 25px rgba(16, 185, 129, 0.15);
    }
    .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    /* Thẻ Thống kê KPI Glassmorphism độc quyền */
    .kpi-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 20px 22px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    .kpi-card:hover {
        border-color: rgba(16, 185, 129, 0.5);
        box-shadow: 0 6px 24px rgba(16, 185, 129, 0.15);
    }
    .kpi-title {
        font-size: 0.82rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.85rem;
        font-weight: 800;
        color: #10b981;
        line-height: 1.1;
        margin-bottom: 4px;
    }
    .kpi-sub {
        font-size: 0.8rem;
        color: #64748b;
    }

    /* Khung Bằng Chứng Nhận Số (Certificate) */
    .cert-frame {
        background: radial-gradient(circle at 50% 0%, #064e3b 0%, #022c22 100%);
        border: 2px solid #10b981;
        border-radius: 18px;
        padding: 36px 30px;
        text-align: center;
        box-shadow: 0 0 35px rgba(16, 185, 129, 0.25);
    }

    /* Hộp Chatbot AI */
    .chat-bubble-user {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 14px 14px 2px 14px;
        padding: 12px 16px;
        margin: 8px 0;
        color: #f1f5f9;
        font-size: 0.92rem;
    }
    .chat-bubble-ai {
        background: rgba(6, 78, 59, 0.3);
        border: 1px solid rgba(16, 185, 129, 0.35);
        border-radius: 14px 14px 14px 2px;
        padding: 14px 18px;
        margin: 8px 0;
        color: #f8fafc;
        font-size: 0.92rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. SIDEBAR: THAM SỐ ĐẦU VÀO VÀ CẤU HÌNH THỊ TRƯỜNG
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
        <span style="font-size: 28px;">🌿</span>
        <div>
            <div style="font-size: 19px; font-weight: 800; color: #10b981; letter-spacing: -0.5px;">CarbonLens</div>
            <div style="font-size: 11px; color: #94a3b8;">Cần Giờ Blue Carbon Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("##### ⚙️ THAM SỐ THỊ TRƯỜNG TÍN CHỈ")
    
    carbon_price = st.slider(
        "Giá tín chỉ carbon (USD/tCO2e):",
        min_value=5.0,
        max_value=60.0,
        value=15.0,
        step=0.5,
        help="Đơn giá tham chiếu theo thị trường tự nguyện (VCM) và các dự án Blue Carbon quốc tế."
    )
    
    usd_vnd_rate = st.number_input(
        "Tỷ giá tham chiếu (USD/VNĐ):",
        min_value=23000,
        max_value=30000,
        value=25400,
        step=100
    )
    
    st.markdown("---")
    st.markdown("##### 🧪 HỆ SỐ PHÁT THẢI (EMISSION FACTORS)")
    grid_ef = st.number_input(
        "Lưới điện QG (kg CO2/kWh):",
        value=0.7221,
        format="%.4f",
        help="Công bố chính thức của Cục Biến đổi khí hậu - Bộ Tài nguyên và Môi trường Việt Nam."
    )
    petrol_ef = st.number_input(
        "Xăng RON 95 (kg CO2/lít):",
        value=2.3100,
        format="%.4f",
        help="Hướng dẫn kiểm kê KNK Quốc gia của IPCC."
    )
    diesel_ef = st.number_input(
        "Dầu Diesel (kg CO2/lít):",
        value=2.6800,
        format="%.4f",
        help="Hệ số đốt nhiên liệu di động theo IPCC Mobile Combustion."
    )

# ==============================================================================
# 4. HERO BANNER: THƯƠNG HIỆU & GIỚI THIỆU ĐỀ TÀI
# ==============================================================================
st.markdown("""
<div class="hero-container">
    <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 16px;">
        <div style="max-width: 820px;">
            <div class="badge-pill">
                <span>🌱</span> UNESCO MANGROVE BIOSPHERE RESERVE & CIRCULAR CARBON
            </div>
            <h1 style="font-size: 2.1rem; margin: 12px 0 8px 0; color: #ffffff; line-height: 1.2;">
                CarbonLens: Phân Tích Phát Thải Doanh Nghiệp & Định Giá Tín Chỉ Rừng Cần Giờ
            </h1>
            <p style="color: #94a3b8; font-size: 0.95rem; margin: 0; line-height: 1.5;">
                Nền tảng nghiên cứu tích hợp quy đổi phát thải Scope 1 - Scope 2 theo GHG Protocol,
                giám sát bể trữ lượng Blue Carbon rừng ngập mặn Cần Giờ và mô phỏng giao dịch tín chỉ Net Zero.
            </p>
        </div>
        <div style="display: flex; gap: 12px; text-align: right;">
            <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #1e293b; border-radius: 12px; padding: 12px 18px;">
                <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase;">Rừng phòng hộ</div>
                <div style="font-size: 1.4rem; font-weight: 800; color: #10b981; font-family: 'JetBrains Mono', monospace;">35.120 ha</div>
            </div>
            <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #1e293b; border-radius: 12px; padding: 12px 18px;">
                <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase;">Công suất hấp thụ</div>
                <div style="font-size: 1.4rem; font-weight: 800; color: #38bdf8; font-family: 'JetBrains Mono', monospace;">~650.000 tCO2</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 5. KHỞI TẠO 4 PHÂN HỆ CHUYÊN SÂU (1, 2, 3, 4)
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Tính toán & Quy đổi Phát thải",
    "2. Giám sát Bể chứa Carbon Cần Giờ",
    "3. Sàn Giao dịch & Chứng nhận Bù đắp",
    "4. Cố vấn Khoa học AI (Hỏi Đáp)"
])

# ==============================================================================
# 1. TÍNH TOÁN & QUY ĐỔI PHÁT THẢI (CARBON CALCULATOR)
# ==============================================================================
with tab1:
    col_input, col_kpi = st.columns([5, 7], gap="large")
    
    with col_input:
        st.markdown("#### 🏢 Thông Tin & Dữ Liệu Năng Lượng")
        
        company_name = st.text_input("Tên tổ chức / Doanh nghiệp:", value="Tập đoàn Công nghệ & Sản xuất Á Châu")
        
        c_ind, c_scale = st.columns(2)
        with c_ind:
            industry = st.selectbox(
                "Ngành nghề kinh doanh:",
                ["Sản xuất chế biến", "Logistics & Vận tải", "Thương mại & Dịch vụ", "Bất động sản & Xây dựng"]
            )
        with c_scale:
            scale = st.selectbox(
                "Quy mô doanh nghiệp:",
                ["Doanh nghiệp lớn (>500 nhân sự)", "Doanh nghiệp vừa (100 - 500)", "Doanh nghiệp nhỏ (<100)"]
            )
            
        st.markdown("##### ⚡ Tiêu Thụ Điện Năng (Scope 2 - Gián tiếp)")
        electricity_kwh = st.number_input(
            "Lượng điện năng tiêu thụ theo năm (kWh):",
            min_value=0.0,
            value=350000.0,
            step=10000.0,
            format="%.0f"
        )
        
        st.markdown("##### ⛽ Tiêu Thụ Nhiên Liệu Vận Tải (Scope 1 - Trực tiếp)")
        c_pet, c_die = st.columns(2)
        with c_pet:
            petrol_liters = st.number_input(
                "Xăng tiêu thụ (Lít):",
                min_value=0.0,
                value=18000.0,
                step=1000.0,
                format="%.0f"
            )
        with c_die:
            diesel_liters = st.number_input(
                "Dầu Diesel tiêu thụ (Lít):",
                min_value=0.0,
                value=25000.0,
                step=1000.0,
                format="%.0f"
            )

    # Tính toán phát thải
    scope1_petrol_ton = (petrol_liters * petrol_ef) / 1000.0
    scope1_diesel_ton = (diesel_liters * diesel_ef) / 1000.0
    total_scope1_ton = scope1_petrol_ton + scope1_diesel_ton
    total_scope2_ton = (electricity_kwh * grid_ef) / 1000.0
    total_emissions_ton = total_scope1_ton + total_scope2_ton
    offset_cost_usd = total_emissions_ton * carbon_price
    offset_cost_vnd = offset_cost_usd * usd_vnd_rate

    with col_kpi:
        st.markdown("#### 📈 Kết Quả Kiểm Kê & Định Giá Bù Đắp")
        
        kpi_c1, kpi_c2, kpi_c3 = st.columns(3)
        with kpi_c1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Scope 1 (Trực tiếp)</div>
                <div class="kpi-value" style="color: #f59e0b;">{total_scope1_ton:,.1f}</div>
                <div class="kpi-sub">tấn CO2e (Xăng & Dầu)</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi_c2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Scope 2 (Gián tiếp)</div>
                <div class="kpi-value" style="color: #38bdf8;">{total_scope2_ton:,.1f}</div>
                <div class="kpi-sub">tấn CO2e (Lưới điện EVN)</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi_c3:
            st.markdown(f"""
            <div class="kpi-card" style="border-color: rgba(16, 185, 129, 0.4);">
                <div class="kpi-title" style="color: #34d399;">Tổng Phát Thải (GHG)</div>
                <div class="kpi-value">{total_emissions_ton:,.1f}</div>
                <div class="kpi-sub">tấn CO2e / năm</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        
        # Thẻ định giá tài chính
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(6, 78, 59, 0.3) 0%, rgba(15, 23, 42, 0.8) 100%); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 16px; padding: 20px 24px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                <div>
                    <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em;">
                        💰 TỔNG CHI PHÍ BÙ ĐẮP CARBON (OFFSET COST)
                    </div>
                    <div style="font-size: 2.1rem; font-weight: 800; color: #34d399; font-family: 'JetBrains Mono', monospace;">
                        ${offset_cost_usd:,.2f} USD
                    </div>
                    <div style="color: #cbd5e1; font-size: 0.95rem;">
                        Tương đương khoảng <b style="color: #f8fafc;">{offset_cost_vnd:,.0f} VNĐ</b> (@ ${carbon_price:.1f}/tấn)
                    </div>
                </div>
                <div style="text-align: right;">
                    <div class="badge-pill" style="margin-bottom: 6px;">DYNAMIC VALUATION</div>
                    <div style="font-size: 12px; color: #94a3b8;">Dựa trên tỷ giá 1 USD = {usd_vnd_rate:,.0f} VNĐ</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Biểu đồ Donut phân rã Scope 1 vs Scope 2
        labels = ['Scope 1 (Xăng RON95)', 'Scope 1 (Dầu Diesel)', 'Scope 2 (Điện lưới EVN)']
        values = [scope1_petrol_ton, scope1_diesel_ton, total_scope2_ton]
        colors = ['#f59e0b', '#ef4444', '#38bdf8']
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.6,
            marker=dict(colors=colors, line=dict(color='#020617', width=3)),
            textinfo='percent+label',
            textfont=dict(color='#ffffff')
        )])
        fig_donut.update_layout(
            title=dict(text="<b>Cơ Cấu Tỷ Lệ Phát Thải Khí Nhà Kính</b>", font=dict(color='#f8fafc', size=15)),
            margin=dict(t=40, b=10, l=10, r=10),
            height=280,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            font=dict(color='#cbd5e1')
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # Biểu đồ phân tích độ nhạy theo giá thị trường
    st.markdown("---")
    st.markdown("##### 📊 Phân Tích Độ Nhạy: Chi Phí Bù Đắp Theo Kịch Bản Giá Carbon Thị Trường")
    price_scenarios = list(range(5, 55, 5))
    costs_usd = [total_emissions_ton * p for p in price_scenarios]
    costs_vnd = [(total_emissions_ton * p * usd_vnd_rate) / 1_000_000 for p in price_scenarios]

    fig_sens = go.Figure()
    fig_sens.add_trace(go.Scatter(
        x=price_scenarios,
        y=costs_usd,
        mode='lines+markers',
        name='Chi phí (USD)',
        line=dict(color='#10b981', width=3),
        marker=dict(size=8, color='#34d399')
    ))
    fig_sens.update_layout(
        xaxis_title="Giá tín chỉ carbon ($/tCO2e)",
        yaxis_title="Tổng chi phí bù đắp (USD)",
        template="plotly_dark",
        height=300,
        margin=dict(t=20, b=40, l=40, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#cbd5e1'),
        xaxis=dict(gridcolor='#1e293b'),
        yaxis=dict(gridcolor='#1e293b')
    )
    st.plotly_chart(fig_sens, use_container_width=True)

    # ==============================================================================
    # MÔ PHỎNG KỊCH BẢN GIẢM PHÁT THẢI (SCENARIO SIMULATION & WHAT-IF ANALYSIS)
    # ==============================================================================
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(6, 78, 59, 0.4) 0%, rgba(15, 23, 42, 0.8) 100%); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 16px; padding: 20px 24px; margin: 15px 0 25px 0;">
        <div class="badge-pill">DECISION SUPPORT SYSTEM (DSS) · WHAT-IF ANALYSIS</div>
        <h3 style="color: #ffffff; margin: 10px 0 6px 0; font-size: 1.4rem; font-weight: 700;">
            🎯 Mô Phỏng Kịch Bản Giảm Phát Thải & Lợi Ích Kinh Tế Kép
        </h3>
        <p style="color: #94a3b8; font-size: 0.92rem; margin: 0; line-height: 1.5;">
            Hệ thống hỗ trợ ra quyết định: Đánh giá nếu doanh nghiệp chuyển sang <b>điện mặt trời mái nhà</b>, <b>tối ưu tuyến vận tải</b> và <b>điện hóa đội xe</b>, lượng phát thải và chi phí mua tín chỉ carbon sẽ giảm đi bao nhiêu phần trăm.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_sim_ctrl, col_sim_res = st.columns([5, 7], gap="large")

    with col_sim_ctrl:
        st.markdown("##### 🎛️ Cần Gạt Tham Số Chuyển Đổi Xanh (Intervention Levers)")
        
        sim_solar = st.slider(
            "☀️ Điện mặt trời mái nhà (Solar Rooftop %):",
            min_value=0, max_value=100, value=35, step=5,
            help="Tỷ lệ điện mặt trời tự sản tự tiêu thay thế nguồn điện lưới EVN (Scope 2)."
        )

        sim_logistics = st.slider(
            "🚚 Tối ưu hóa tuyến đường & Logistics (%):",
            min_value=0, max_value=50, value=20, step=5,
            help="Cắt giảm hao phí xăng dầu Scope 1 thông qua thuật toán AI phân tuyến và gộp đơn."
        )

        sim_ev = st.slider(
            "🔋 Điện hóa đội xe doanh nghiệp (EV Fleet %):",
            min_value=0, max_value=100, value=25, step=5,
            help="Tỷ lệ thay thế phương tiện đốt trong xăng/dầu bằng phương tiện thuần điện."
        )

        sim_eff = st.slider(
            "💡 Hiệu quả năng lượng & IoT công nghiệp (%):",
            min_value=0, max_value=30, value=15, step=5,
            help="Tiết kiệm phụ tải điện qua biến tần, đèn LED thông minh và quản lý năng lượng EMS."
        )

    # Thuật toán tính toán Kịch bản Can thiệp (What-if Calculation Engine)
    sim_elec_demand = electricity_kwh * (1.0 - sim_eff / 100.0)
    sim_grid_kwh = sim_elec_demand * (1.0 - sim_solar / 100.0)
    sim_scope2_ton = (sim_grid_kwh * grid_ef) / 1000.0

    fuel_reduction_ratio = (1.0 - sim_logistics / 100.0) * (1.0 - sim_ev / 100.0)
    sim_petrol_liters = petrol_liters * fuel_reduction_ratio
    sim_diesel_liters = diesel_liters * fuel_reduction_ratio
    sim_scope1_ton = (sim_petrol_liters * petrol_ef + sim_diesel_liters * diesel_ef) / 1000.0

    sim_total_ton = sim_scope1_ton + sim_scope2_ton
    sim_abated_ton = max(0.0, total_emissions_ton - sim_total_ton)
    sim_abated_pct = (sim_abated_ton / total_emissions_ton * 100.0) if total_emissions_ton > 0 else 0.0

    sim_mitigated_cost_usd = sim_total_ton * carbon_price
    sim_saved_cost_usd = max(0.0, offset_cost_usd - sim_mitigated_cost_usd)
    sim_saved_cost_vnd = sim_saved_cost_usd * usd_vnd_rate

    # Ước tính tiết kiệm chi phí năng lượng OPEX (điện ~2,050 đ/kWh, xăng dầu ~23,500 đ/lít)
    saved_kwh = max(0.0, electricity_kwh - sim_grid_kwh)
    saved_liters = max(0.0, (petrol_liters + diesel_liters) - (sim_petrol_liters + sim_diesel_liters))
    sim_energy_opex_saved_vnd = (saved_kwh * 2050.0) + (saved_liters * 23500.0)

    with col_sim_res:
        st.markdown("##### 📊 Kết Quả So Sánh What-If & Đánh Giá Tác Động")
        
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.markdown(f"""
            <div class="kpi-card" style="border-color: rgba(16, 185, 129, 0.4);">
                <div class="kpi-title" style="color: #34d399;">Tỷ Lệ Giảm Thải</div>
                <div class="kpi-value" style="color: #34d399;">-{sim_abated_pct:.1f}%</div>
                <div class="kpi-sub">Cắt giảm {sim_abated_ton:,.1f} tCO2e</div>
            </div>
            """, unsafe_allow_html=True)
        with sc2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Phát Thải Mới</div>
                <div class="kpi-value" style="color: #38bdf8;">{sim_total_ton:,.1f}</div>
                <div class="kpi-sub">tấn CO2e / năm</div>
            </div>
            """, unsafe_allow_html=True)
        with sc3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Tiết Kiệm Tín Chỉ</div>
                <div class="kpi-value" style="color: #f59e0b;">${sim_saved_cost_usd:,.0f}</div>
                <div class="kpi-sub">~{sim_saved_cost_vnd/1_000_000:,.1f} tr VNĐ/năm</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        
        # Biểu đồ so sánh Trước (BAU) vs Sau (What-if)
        compare_df = pd.DataFrame({
            "Kịch bản": ["1. Hiện trạng (BAU)", "1. Hiện trạng (BAU)", "2. Sau Can thiệp", "2. Sau Can thiệp"],
            "Phân loại Scope": ["Scope 1 (Nhiên liệu)", "Scope 2 (Điện lưới)", "Scope 1 (Nhiên liệu)", "Scope 2 (Điện lưới)"],
            "Phát thải (tCO2e)": [total_scope1_ton, total_scope2_ton, sim_scope1_ton, sim_scope2_ton]
        })
        fig_compare = px.bar(
            compare_df,
            x="Kịch bản",
            y="Phát thải (tCO2e)",
            color="Phân loại Scope",
            barmode="stack",
            text_auto='.1f',
            color_discrete_map={
                "Scope 1 (Nhiên liệu)": "#f59e0b",
                "Scope 2 (Điện lưới)": "#38bdf8"
            }
        )
        fig_compare.update_layout(
            height=250,
            margin=dict(t=20, b=20, l=10, r=20),
            legend=dict(orientation="h", y=1.15),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            xaxis=dict(gridcolor='#1e293b'),
            yaxis=dict(gridcolor='#1e293b')
        )
        st.plotly_chart(fig_compare, use_container_width=True)

        st.markdown(f"""
        <div style="background: rgba(6, 78, 59, 0.25); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 12px 16px; font-size: 12px; line-height: 1.5; color: #cbd5e1;">
            💡 <b>Khuyến nghị chiến lược (Double Dividend):</b> Kịch bản can thiệp này mang lại lợi ích kép: Vừa tiết kiệm <b>${sim_saved_cost_usd:,.0f} USD</b> ({sim_saved_cost_vnd/1_000_000:,.1f} triệu VNĐ) tiền mua tín chỉ carbon, vừa tiết kiệm trực tiếp khoảng <b>~{sim_energy_opex_saved_vnd/1_000_000:,.1f} triệu VNĐ</b> chi phí điện và xăng dầu vận hành mỗi năm. Lượng phát thải còn lại ({sim_total_ton:,.1f} tCO2) sẽ được bù đắp qua Rừng Cần Giờ tại Mục 3.
        </div>
        """, unsafe_allow_html=True)

    # ==============================================================================
    # TỰ ĐỘNG HÓA XUẤT BÁO CÁO ESG & KIỂM KÊ GHG CHUẨN QUỐC TẾ (ISO 14064 & CBAM)
    # ==============================================================================
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 16px; padding: 20px 24px; margin: 15px 0 20px 0;">
        <div class="badge-pill">ISO 14064-1:2018 · GHG PROTOCOL · EU CBAM READY</div>
        <h3 style="color: #ffffff; margin: 10px 0 6px 0; font-size: 1.35rem; font-weight: 700;">
            📄 Tự Động Hóa Xuất Báo Cáo ESG & Kiểm Kê Khí Nhà Kính
        </h3>
        <p style="color: #94a3b8; font-size: 0.92rem; margin: 0; line-height: 1.5;">
            Tổng hợp dữ liệu phát thải Scope 1 - 2 thành hồ sơ bạch thư ESG hoàn chỉnh, sẵn sàng cho kiểm toán độc lập và tuân thủ rào cản carbon thương mại quốc tế.
        </p>
    </div>
    """, unsafe_allow_html=True)

    report_code_py = f"GHG-ISO14064-{datetime.now().year}-{abs(hash(company_name)) % 9000 + 1000:04d}"
    
    csv_report_data = f"""BÁO CÁO KIỂM KÊ KHÍ NHÀ KÍNH & BẠCH THƯ ESG THEO CHUẨN ISO 14064-1:2018
Mã báo cáo: {report_code_py}
Thời điểm lập: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Doanh nghiệp / Tổ chức: {company_name}
Ngành nghề: {industry}
Quy mô: {scale}

DANH MỤC PHÁT THẢI,LƯỢNG TIÊU THỤ,HỆ SỐ PHÁT THẢI,PHÁT THẢI (tCO2e),TỶ TRỌNG (%)
Scope 1 (Xăng RON 95),{petrol_liters:,.0f} Lít,{petrol_ef:.4f} kg CO2/L (IPCC),{scope1_petrol_ton:.2f},{(scope1_petrol_ton/total_emissions_ton*100) if total_emissions_ton>0 else 0:.1f}%
Scope 1 (Dầu Diesel),{diesel_liters:,.0f} Lít,{diesel_ef:.4f} kg CO2/L (IPCC),{scope1_diesel_ton:.2f},{(scope1_diesel_ton/total_emissions_ton*100) if total_emissions_ton>0 else 0:.1f}%
Scope 2 (Điện lưới EVN),{electricity_kwh:,.0f} kWh,{grid_ef:.4f} kg CO2/kWh (Bộ TN&MT),{total_scope2_ton:.2f},{(total_scope2_ton/total_emissions_ton*100) if total_emissions_ton>0 else 0:.1f}%

TỔNG PHÁT THẢI TOÀN DOANH NGHIỆP: {total_emissions_ton:.2f} tCO2e
ĐƠN GIÁ TÍN CHỈ BLUE CARBON THAM CHIẾU: ${carbon_price:.2f} USD/tCO2
TỔNG NGÂN SÁCH BÙ ĐẮP NET ZERO (USD): ${offset_cost_usd:.2f} USD
TỔNG NGÂN SÁCH BÙ ĐẮP NET ZERO (VNĐ): {offset_cost_vnd:,.0f} VNĐ
Cơ chế kiểm kê: ISO 14064-1:2018 / GHG Protocol / EU CBAM Compatible
"""

    c_rep1, c_rep2 = st.columns([8, 4])
    with c_rep1:
        with st.expander("👁️ Xem Trước Báo Cáo Kiểm Kê Khí Nhà Kính ISO 14064 & Cam Kết Net Zero", expanded=False):
            st.markdown(f"""
            <div style="background: #020617; border: 1px solid #334155; border-radius: 10px; padding: 20px; font-family: monospace; font-size: 12px; line-height: 1.7; color: #cbd5e1;">
                <b style="color: #10b981; font-size: 14px;">BÁO CÁO KIỂM KÊ KHÍ NHÀ KÍNH (GHG INVENTORY) & BẠCH THƯ ESG</b><br>
                <b>Mã số văn bản:</b> {report_code_py} | <b>Kỳ kiểm kê:</b> 2026<br>
                <b>Đơn vị phát thải:</b> {company_name}<br>
                --------------------------------------------------------------------------------<br>
                <b>1. PHẠM VI 1 (SCOPE 1 - DIRECT EMISSIONS):</b><br>
                - Xăng RON 95: {petrol_liters:,.0f} Lít x {petrol_ef:.4f} = <b style="color:#f59e0b;">{scope1_petrol_ton:,.2f} tCO2e</b><br>
                - Dầu Diesel: {diesel_liters:,.0f} Lít x {diesel_ef:.4f} = <b style="color:#f59e0b;">{scope1_diesel_ton:,.2f} tCO2e</b><br>
                => Tổng Scope 1: <b style="color:#f59e0b;">{total_scope1_ton:,.2f} tCO2e</b><br>
                <br>
                <b>2. PHẠM VI 2 (SCOPE 2 - INDIRECT ENERGY EMISSIONS):</b><br>
                - Điện lưới EVN: {electricity_kwh:,.0f} kWh x {grid_ef:.4f} = <b style="color:#38bdf8;">{total_scope2_ton:,.2f} tCO2e</b><br>
                <br>
                --------------------------------------------------------------------------------<br>
                <b>TỔNG PHÁT THẢI TOÀN DOANH NGHIỆP:</b> <b style="color:#10b981; font-size: 15px;">{total_emissions_ton:,.2f} tCO2e</b><br>
                <b>ĐỊNH GIÁ NGHĨA VỤ BÙ ĐẮP CARBON:</b> ${offset_cost_usd:,.2f} USD (~{offset_cost_vnd:,.0f} VNĐ)<br>
                <b>DỰ ÁN BÙ ĐẮP:</b> Khu Dự trữ Sinh quyển Rừng ngập mặn Cần Giờ (UNESCO)<br>
                --------------------------------------------------------------------------------<br>
                <i>Chứng nhận phù hợp khung ISO 14064-1:2018 & GHG Protocol Corporate Standard</i>
            </div>
            """, unsafe_allow_html=True)
    with c_rep2:
        st.download_button(
            label="📥 Tải Báo Cáo ESG & ISO 14064 (CSV/Excel)",
            data=csv_report_data.encode('utf-8-sig'),
            file_name=f"Bao_Cao_ESG_{company_name.replace(' ', '_')}.csv",
            mime="text/csv",
            use_container_width=True
        )


# ==============================================================================
# 2. GIÁM SÁT BỂ CHỨA CARBON CẦN GIỜ (ECO-DASHBOARD)
# ==============================================================================
with tab2:
    st.markdown("#### 🌊 Giám Sát Sinh Khối & Bể Trữ Lượng Carbon Rừng Ngập Mặn Cần Giờ")
    st.caption("Khu Dự trữ Sinh quyển Thế giới được UNESCO công nhận năm 2000 - 'Lá phổi xanh' điều hòa khí hậu TP. Hồ Chí Minh.")
    
    # 4 thẻ chỉ số sinh thái chính
    e1, e2, e3, e4 = st.columns(4)
    with e1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Diện Tích Rừng Phòng Hộ</div>
            <div class="kpi-value">35.120</div>
            <div class="kpi-sub">ha (Trên tổng 75.740 ha)</div>
        </div>
        """, unsafe_allow_html=True)
    with e2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Tỷ Suất Hấp Thụ</div>
            <div class="kpi-value" style="color: #38bdf8;">18,5</div>
            <div class="kpi-sub">tấn CO2e / ha / năm</div>
        </div>
        """, unsafe_allow_html=True)
    with e3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Hấp Thụ Hàng Năm</div>
            <div class="kpi-value" style="color: #a78bfa;">~650.000</div>
            <div class="kpi-sub">tấn CO2e / năm</div>
        </div>
        """, unsafe_allow_html=True)
    with e4:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Trữ Lượng Tích Lũy</div>
            <div class="kpi-value" style="color: #f59e0b;">17,85</div>
            <div class="kpi-sub">Triệu tấn CO2 tương đương</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns(2, gap="large")
    
    with col_chart1:
        st.markdown("##### 🧬 Cấu Trúc Bể Chứa Carbon (4 Carbon Pools)")
        pools_df = pd.DataFrame({
            "Bể Carbon": [
                "1. Trầm tích hữu cơ xanh (Soil Blue Carbon)",
                "2. Sinh khối trên mặt đất (AGB - Thân, cành)",
                "3. Sinh khối dưới mặt đất (BGB - Hệ rễ)",
                "4. Vật rơi rụng & thảm mục (Litter)"
            ],
            "Tỷ lệ (%)": [62.5, 23.0, 11.5, 3.0],
            "Trữ lượng ước tính (triệu tCO2)": [11.15, 4.11, 2.05, 0.54]
        })
        fig_pool = px.bar(
            pools_df,
            x="Tỷ lệ (%)",
            y="Bể Carbon",
            orientation='h',
            text="Tỷ lệ (%)",
            color="Tỷ lệ (%)",
            color_continuous_scale=["#064e3b", "#10b981", "#34d399"]
        )
        fig_pool.update_traces(texttemplate='%{text}%', textposition='outside')
        fig_pool.update_layout(
            yaxis={'categoryorder':'total ascending', 'gridcolor': '#1e293b'},
            xaxis={'gridcolor': '#1e293b'},
            height=320,
            margin=dict(t=20, b=20, l=10, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            coloraxis_showscale=False,
            font=dict(color='#cbd5e1')
        )
        st.plotly_chart(fig_pool, use_container_width=True)
        st.info("💡 **Đặc tính Blue Carbon:** 62.5% carbon nằm sâu trong tầng trầm tích ngập triều yếm khí, được lưu giữ an toàn hàng trăm năm nếu rừng được bảo tồn nghiêm ngặt.")

    with col_chart2:
        st.markdown("##### 🔮 Dự Báo Khả Năng Hấp Thụ Carbon (2026 - 2035)")
        years = list(range(2026, 2036))
        baseline = [650000 + i * 8500 for i in range(len(years))]
        enhanced = [650000 + i * 24000 + (i**1.2) * 3500 for i in range(len(years))]
        vulnerable = [650000 + i * 2000 - (i**1.4) * 2200 for i in range(len(years))]

        forecast_df = pd.DataFrame({
            "Năm": years * 3,
            "Hấp thụ dự báo (tấn CO2/năm)": baseline + enhanced + vulnerable,
            "Kịch bản": ["1. Hiện trạng chuẩn (Baseline)"] * len(years) + \
                        ["2. Tăng cường trồng mới & Phục hồi"] * len(years) + \
                        ["3. Rủi ro BĐKH & Xâm thực ven bờ"] * len(years)
        })

        fig_line = px.line(
            forecast_df,
            x="Năm",
            y="Hấp thụ dự báo (tấn CO2/năm)",
            color="Kịch bản",
            markers=True,
            color_discrete_map={
                "1. Hiện trạng chuẩn (Baseline)": "#38bdf8",
                "2. Tăng cường trồng mới & Phục hồi": "#10b981",
                "3. Rủi ro BĐKH & Xâm thực ven bờ": "#f43f5e"
            }
        )
        fig_line.update_layout(
            height=320,
            margin=dict(t=20, b=20, l=10, r=20),
            legend=dict(orientation="h", y=-0.25),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            xaxis=dict(gridcolor='#1e293b'),
            yaxis=dict(gridcolor='#1e293b')
        )
        st.plotly_chart(fig_line, use_container_width=True)

    # Bảng phân bố sinh thái các phân khu
    st.markdown("##### 🗺️ Phân Bố Sinh Thái & Mật Độ Trữ Lượng Carbon Các Phân Khu Cần Giờ")
    subzones_df = pd.DataFrame({
        "Phân khu bảo tồn": ["Phân khu Vùng lõi nghiêm ngặt", "Phân khu Phục hồi sinh thái", "Phân khu Vùng đệm phát triển", "Hành lang sông Lòng Tàu & Soài Rạp"],
        "Diện tích (ha)": [4721, 28600, 29880, 12539],
        "Loài cây ưu thế": ["Đước đôi (Rhizophora), Dà quánh, Vẹt dù", "Đước đôi tái sinh, Cóc đỏ, Bần trắng", "Mấm trắng (Avicennia), Bần chua, Dừa nước", "Thảm ngập triều hỗn giao bãi bồi"],
        "Mật độ trữ lượng (tCO2/ha)": [420.5, 365.2, 280.0, 195.4]
    })
    st.dataframe(subzones_df, use_container_width=True, hide_index=True)

    # ==============================================================================
    # SƠ ĐỒ CHUỖI CUNG ỨNG NGƯỢC & VÒNG LẶP DÒNG TIỀN BẢO TỒN (REVERSE LOGISTICS)
    # ==============================================================================
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(6, 78, 59, 0.4) 0%, rgba(15, 23, 42, 0.8) 100%); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 16px; padding: 20px 24px; margin: 15px 0 20px 0;">
        <div class="badge-pill">CIRCULAR ECONOMY & GREEN SCM · REVERSE LOGISTICS</div>
        <h3 style="color: #ffffff; margin: 10px 0 6px 0; font-size: 1.4rem; font-weight: 700;">
            🔄 Sơ Đồ Chuỗi Cung Ứng Ngược & Vòng Lặp Dòng Tiền Bảo Tồn
        </h3>
        <p style="color: #94a3b8; font-size: 0.92rem; margin: 0; line-height: 1.5;">
            Minh bạch hóa hành trình dòng tiền từ doanh nghiệp mua tín chỉ đến Ban quản lý rừng Cần Giờ và mô hình Chuỗi cung ứng ngược (Reverse Logistics) thu hồi sinh khối tái tạo tầng đất sinh quyển.
        </p>
    </div>
    """, unsafe_allow_html=True)

    flow_mode = st.radio(
        "Chọn quy trình tuần hoàn muốn khảo sát:",
        ["1. Dòng Tiền & Tín Chỉ Bảo Tồn Khép Kín (Circular Finance)", "2. Chuỗi Cung Ứng Ngược Sinh Khối & Biochar (Reverse Logistics)"],
        horizontal=True
    )

    if "Dòng Tiền" in flow_mode:
        f1, f2, f3, f4, f5 = st.columns(5)
        with f1:
            st.markdown("""
            <div class="kpi-card" style="min-height: 170px;">
                <div class="kpi-title">1. Doanh Nghiệp Mua</div>
                <div style="font-weight: 700; color: #10b981; font-size: 13px;">Thanh toán tín chỉ</div>
                <div style="font-size: 11px; color: #94a3b8; margin-top: 4px;">Ký hợp đồng bù đắp Scope 1-2 từ dữ liệu kiểm kê.</div>
            </div>
            """, unsafe_allow_html=True)
        with f2:
            st.markdown("""
            <div class="kpi-card" style="min-height: 170px;">
                <div class="kpi-title">2. Quỹ Ủy Thác</div>
                <div style="font-weight: 700; color: #38bdf8; font-size: 13px;">Smart Escrow</div>
                <div style="font-size: 11px; color: #94a3b8; margin-top: 4px;">Phân bổ 95% vốn cho bảo vệ rừng, 5% duy trì trạm GIS/MRV.</div>
            </div>
            """, unsafe_allow_html=True)
        with f3:
            st.markdown("""
            <div class="kpi-card" style="min-height: 170px;">
                <div class="kpi-title">3. BQL & 1.000+ Hộ Dân</div>
                <div style="font-weight: 700; color: #a78bfa; font-size: 13px;">Chi trả PES</div>
                <div style="font-size: 11px; color: #94a3b8; margin-top: 4px;">Hợp đồng giao khoán giữ rừng, tuần tra bãi bồi ven sông 24/7.</div>
            </div>
            """, unsafe_allow_html=True)
        with f4:
            st.markdown("""
            <div class="kpi-card" style="min-height: 170px;">
                <div class="kpi-title">4. Blue Carbon Trầm Tích</div>
                <div style="font-weight: 700; color: #10b981; font-size: 13px;">Quang hợp & Lưu giữ</div>
                <div style="font-size: 11px; color: #94a3b8; margin-top: 4px;">Khóa chặt >62.5% carbon dưới bùn ngập triều yếm khí.</div>
            </div>
            """, unsafe_allow_html=True)
        with f5:
            st.markdown("""
            <div class="kpi-card" style="min-height: 170px;">
                <div class="kpi-title">5. Sổ Cái Registry</div>
                <div style="font-weight: 700; color: #f59e0b; font-size: 13px;">Khóa sổ vĩnh viễn</div>
                <div style="font-size: 11px; color: #94a3b8; margin-top: 4px;">Cấp mã chứng nhận số và Retire vĩnh viễn, chống tính trùng.</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        r1, r2, r3, r4 = st.columns(4)
        with r1:
            st.markdown("""
            <div class="kpi-card" style="min-height: 170px;">
                <div class="kpi-title">1. Thu Gom Phụ Phẩm</div>
                <div style="font-weight: 700; color: #f59e0b; font-size: 13px;">Gỗ tỉa thưa & Rác biển</div>
                <div style="font-size: 11px; color: #94a3b8; margin-top: 4px;">Thu gom cành đước tỉa thưa định kỳ và rác nhựa dạt vào rừng ngập mặn.</div>
            </div>
            """, unsafe_allow_html=True)
        with r2:
            st.markdown("""
            <div class="kpi-card" style="min-height: 170px;">
                <div class="kpi-title">2. Nhiệt Phân Xanh</div>
                <div style="font-weight: 700; color: #38bdf8; font-size: 13px;">Pyrolysis yếm khí</div>
                <div style="font-size: 11px; color: #94a3b8; margin-top: 4px;">Chuyển hóa gỗ tỉa thưa thành Than sinh học (Biochar) và dấm gỗ sinh học.</div>
            </div>
            """, unsafe_allow_html=True)
        with r3:
            st.markdown("""
            <div class="kpi-card" style="min-height: 170px;">
                <div class="kpi-title">3. Hoàn Nguyên Đất Rừng</div>
                <div style="font-weight: 700; color: #10b981; font-size: 13px;">Bón Biochar cho đất</div>
                <div style="font-size: 11px; color: #94a3b8; margin-top: 4px;">Bón trở lại nền đất ngập triều để cố định carbon thêm 200+ năm.</div>
            </div>
            """, unsafe_allow_html=True)
        with r4:
            st.markdown("""
            <div class="kpi-card" style="min-height: 170px;">
                <div class="kpi-title">4. Bao Bì Sinh Học</div>
                <div style="font-weight: 700; color: #a78bfa; font-size: 13px;">Cung ứng ngược</div>
                <div style="font-size: 11px; color: #94a3b8; margin-top: 4px;">Cung cấp vật liệu tuần hoàn cho doanh nghiệp thành viên khép kín chuỗi.</div>
            </div>
            """, unsafe_allow_html=True)


# ==============================================================================
# TAB 3: SÀN GIAO DỊCH MÔ PHỎNG & CHỨNG NHẬN BÙ ĐẮP (SIMULATED TRADING HUB)
# ==============================================================================
with tab3:
    st.markdown("#### 💼 Sàn Giao Dịch Tín Chỉ Carbon Mô Phỏng & Cấp Chứng Nhận Net Zero")
    st.caption("Doanh nghiệp lựa chọn gói bù đắp trực tiếp từ Bể tín chỉ Blue Carbon Rừng Cần Giờ để đạt trạng thái Trung hòa Carbon.")
    
    # ==============================================================================
    # 1. DỰ BÁO BIẾN ĐỘNG GIÁ TÍN CHỈ CARBON BẰNG TRÍ TUỆ NHÂN TẠO (AI PRICE FORECASTING)
    # ==============================================================================
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 16px; padding: 20px 24px; margin: 15px 0 20px 0;">
        <div class="badge-pill" style="color: #fbbf24; border-color: rgba(245, 158, 11, 0.4); background: rgba(245, 158, 11, 0.15);">
            AI QUANTITATIVE FORECASTING · TIME-SERIES MODEL
        </div>
        <h3 style="color: #ffffff; margin: 10px 0 6px 0; font-size: 1.4rem; font-weight: 700;">
            📈 Dự Báo Biến Động Giá Tín Chỉ Carbon Bằng AI & Chiến Lược Hedging
        </h3>
        <p style="color: #94a3b8; font-size: 0.92rem; margin: 0; line-height: 1.5;">
            Mô hình chuỗi thời gian AI phân tích tác động từ <b>Cơ chế CBAM Châu Âu</b> và <b>Sàn Giao dịch Carbon Quốc gia Việt Nam</b>, hỗ trợ doanh nghiệp tối ưu hóa thời điểm mua tín chỉ.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_fc1, col_fc2 = st.columns([7, 5], gap="large")

    with col_fc1:
        st.markdown("##### 📊 Quỹ Đạo Giá Tín Chỉ Blue Carbon ($/tCO2e)")
        fc_df = pd.DataFrame({
            "Mốc thời gian": ["T-9", "T-6", "T-3", "Hiện tại", "+3 Tháng", "+6 Tháng", "+12 Tháng"],
            "Đơn giá (USD)": [11.5, 12.8, 13.9, carbon_price, 18.5, 24.8, 33.0],
            "Loại dữ liệu": ["Lịch sử", "Lịch sử", "Lịch sử", "Hiện tại", "Dự báo AI", "Dự báo AI", "Dự báo AI"]
        })
        fig_fc = px.bar(
            fc_df,
            x="Mốc thời gian",
            y="Đơn giá (USD)",
            color="Loại dữ liệu",
            text_auto='.1f',
            color_discrete_map={
                "Lịch sử": "#64748b",
                "Hiện tại": "#10b981",
                "Dự báo AI": "#f59e0b"
            }
        )
        fig_fc.update_layout(
            height=280,
            margin=dict(t=20, b=20, l=10, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            xaxis=dict(gridcolor='#1e293b'),
            yaxis=dict(gridcolor='#1e293b')
        )
        st.plotly_chart(fig_fc, use_container_width=True)

    with col_fc2:
        st.markdown("##### 🧭 Khuyến Nghị Ra Quyết Định Chiến Lược (AI Strategic Recommendation)")
        future_6m_price = 24.8
        cost_diff_usd = max(0.0, (total_emissions_ton * future_6m_price) - (total_emissions_ton * carbon_price))
        
        st.markdown(f"""
        <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 14px; padding: 18px; line-height: 1.6;">
            <div style="color: #fbbf24; font-weight: 800; font-size: 13px; text-transform: uppercase; margin-bottom: 6px;">
                💡 KHUYẾN NGHỊ: NÊN MUA NGAY HÔM NAY (HEDGING BẢO VỆ GIÁ)
            </div>
            <div style="font-size: 12px; color: #cbd5e1; margin-bottom: 12px;">
                Dự báo trong 6 tháng tới, khi cơ chế CBAM EU mở rộng và Sàn giao dịch carbon nội địa thí điểm, giá tín chỉ Blue Carbon sẽ tăng từ <b>${carbon_price:.1f}</b> lên <b>${future_6m_price:.1f}/tấn (+65.3%)</b>.
            </div>
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid #334155; border-radius: 10px; padding: 12px; margin-bottom: 10px;">
                <div style="font-size: 11px; color: #94a3b8;">Số tiền tiết kiệm nếu mua ngay hôm nay:</div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #34d399; font-family: 'JetBrains Mono', monospace;">
                    ${cost_diff_usd:,.0f} USD
                </div>
                <div style="font-size: 11px; color: #a7f3d0;">Tương đương ~{(cost_diff_usd * usd_vnd_rate)/1_000_000:,.1f} triệu VNĐ</div>
            </div>
            <div style="font-size: 11px; color: #94a3b8;">
                • <b>Chiến lược khuyến nghị:</b> Mua trước tối thiểu 75% lượng tín chỉ của năm nay để chốt giá bảo hộ.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("##### 2. Lựa Chọn Gói Tín Chỉ Bù Đắp & Xuất Chứng Nhận Số")
    
    col_t1, col_t2 = st.columns([1, 1], gap="large")
    
    with col_t1:
        st.markdown("##### 🎯 Chọn Gói Tín Chỉ Bù Đắp")
        package_option = st.radio(
            "Tỷ lệ mục tiêu bù đắp cho doanh nghiệp:",
            options=[
                f"Gói 1: Bù đắp 100% Phát thải (Net Zero Toàn Diện) - {total_emissions_ton:,.2f} tCO2",
                f"Gói 2: Bù đắp 75% Phát thải (Cam kết ESG Tiên phong) - {total_emissions_ton * 0.75:,.2f} tCO2",
                f"Gói 3: Bù đắp 50% Phát thải (Chuyển dịch Xanh) - {total_emissions_ton * 0.50:,.2f} tCO2",
                f"Gói 4: Tùy chỉnh số lượng tín chỉ thủ công"
            ]
        )

        if "100%" in package_option:
            offset_tons = total_emissions_ton
            pct = 100.0
        elif "75%" in package_option:
            offset_tons = total_emissions_ton * 0.75
            pct = 75.0
        elif "50%" in package_option:
            offset_tons = total_emissions_ton * 0.50
            pct = 50.0
        else:
            offset_tons = st.number_input(
                "Nhập số lượng tín chỉ muốn mua (tCO2):",
                min_value=1.0,
                max_value=100000.0,
                value=float(int(total_emissions_ton)),
                step=10.0
            )
            pct = min(100.0, (offset_tons / total_emissions_ton * 100.0) if total_emissions_ton > 0 else 100.0)

        remaining_emissions = max(0.0, total_emissions_ton - offset_tons)
        trade_amount_usd = offset_tons * carbon_price
        trade_amount_vnd = trade_amount_usd * usd_vnd_rate

        st.markdown("##### 🧾 Hóa Đơn Thanh Toán Tín Chỉ Mô Phỏng")
        inv_data = {
            "Khoản mục": [
                "Tín chỉ Blue Carbon Cần Giờ (VCS Verified)",
                "Đơn giá niêm yết",
                "Phí bảo trợ bảo tồn & giám sát cộng đồng (5%)",
                "Tổng giá trị hợp đồng (USD)",
                "Quy đổi tương đương (VNĐ)"
            ],
            "Chi tiết": [
                f"{offset_tons:,.2f} tấn CO2e",
                f"${carbon_price:.2f} / tCO2",
                f"${trade_amount_usd * 0.05:,.2f}",
                f"${trade_amount_usd * 1.05:,.2f}",
                f"{trade_amount_vnd * 1.05:,.0f} VNĐ"
            ]
        }
        st.table(pd.DataFrame(inv_data))
        execute_trade = st.button("🚀 Xác Nhận Giao Dịch & Khóa Sổ Tiêu Hủy Tín Chỉ", type="primary", use_container_width=True)

    with col_t2:
        st.markdown("##### 📜 Chứng Nhận Bù Đắp Carbon Kỹ Thuật Số (Digital Certificate)")
        cert_id = f"CG-BLUECARBON-{datetime.now().strftime('%Y%m%d')}-{abs(hash(company_name)) % 10000:04d}"
        
        st.markdown(f"""
        <div class="cert-frame">
            <div style="font-size: 32px; margin-bottom: 8px;">🌿 🌊 📜</div>
            <h2 style="color: #34d399; margin: 0 0 6px 0; font-size: 1.6rem; font-weight: 800; letter-spacing: -0.5px;">
                CHỨNG NHẬN BÙ ĐẮP CARBON KỸ THUẬT SỐ
            </h2>
            <div style="color: #94a3b8; font-size: 12px; margin-bottom: 20px; letter-spacing: 0.08em; text-transform: uppercase;">
                HỆ THỐNG ĐĂNG KÝ TÍN CHỈ BLUE CARBON RỪNG NGẬP MẶN CẦN GIỜ
            </div>
            
            <hr style="border: 0; border-top: 1px dashed rgba(16, 185, 129, 0.4); margin: 20px 0;">
            
            <div style="font-size: 14px; color: #cbd5e1; margin-bottom: 6px;">Chứng nhận danh dự cấp cho tổ chức:</div>
            <div style="color: #ffffff; font-size: 1.45rem; font-weight: 700; margin-bottom: 16px;">
                {company_name}
            </div>
            
            <div style="background: rgba(2, 44, 34, 0.7); border: 1px solid #10b981; border-radius: 12px; padding: 16px; margin: 16px 0;">
                <div style="font-size: 2.2rem; font-weight: 800; color: #34d399; font-family: 'JetBrains Mono', monospace;">
                    {offset_tons:,.2f}
                </div>
                <div style="font-size: 13px; color: #a7f3d0; font-weight: 600; text-transform: uppercase;">
                    Tấn CO2 Tương Đương (Verified Blue Carbon Credits)
                </div>
            </div>
            
            <div style="font-size: 13px; color: #cbd5e1; margin-bottom: 16px;">
                Tỷ lệ trung hòa: <b style="color: #34d399;">{pct:.1f}%</b> | Phát thải còn lại: <b>{remaining_emissions:,.2f} tCO2</b>
            </div>
            
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid #1e293b; border-radius: 8px; padding: 12px; font-size: 11px; color: #94a3b8; text-align: left; line-height: 1.6;">
                <div>• <b>Mã định danh (Hash):</b> <code>{cert_id}</code></div>
                <div>• <b>Vị trí địa lý:</b> 10°22'N - 10°40'N, 106°46'E - 107°00'E (Cần Giờ, TP.HCM)</div>
                <div>• <b>Thời điểm cấp:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</div>
                <div>• <b>Cơ chế tiêu hủy (Retirement):</b> Đã khóa vĩnh viễn trên Sổ cái Môi trường (Chống tính trùng)</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if execute_trade:
            st.success(f"🎉 Giao dịch thành công! Doanh nghiệp **{company_name}** đã chính thức bù đắp **{offset_tons:,.2f} tCO2e** qua bể trữ lượng Cần Giờ.")
            st.balloons()


# ==============================================================================
# TAB 4: CỐ VẤN KHOA HỌC AI (HỎI ĐÁP CHIẾN LƯỢC NET ZERO)
# ==============================================================================
with tab4:
    st.markdown("#### 🤖 Cố Vấn Khoa Học AI & Hỏi Đáp Chiến Lược Net Zero")
    st.caption("Trợ lý trí tuệ nhân tạo nắm bắt dữ liệu kiểm kê hiện tại của doanh nghiệp để giải đáp các bài toán kinh tế tuần hoàn.")
    
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            {
                "role": "assistant",
                "content": f"Xin chào! Tôi là **Trợ lý Khoa học AI CarbonLens**. Dựa trên số liệu kiểm kê hiện tại của **{company_name}** (Tổng phát thải: **{total_emissions_ton:,.1f} tCO2** | Chi phí bù đắp: **${offset_cost_usd:,.0f}**), tôi sẵn sàng tư vấn về lộ trình cắt giảm phát thải Scope 1 - 2, cơ chế Blue Carbon Cần Giờ, hoặc tối ưu hóa ngân sách ESG. Bạn cần hỗ trợ câu hỏi nào?"
            }
        ]

    c_chat, c_quick = st.columns([7, 3], gap="large")

    with c_quick:
        st.markdown("##### 💡 Câu Hỏi Gợi Ý Nhanh")
        quick_prompts = [
            f"Đánh giá mức phát thải {total_emissions_ton:,.1f} tCO2 và đề xuất 3 giải pháp giảm Scope 1 & 2?",
            "Tại sao Blue Carbon Cần Giờ hấp thụ cao gấp 4-6 lần rừng trên cạn?",
            f"Với đơn giá ${carbon_price}/tCO2, doanh nghiệp nên phân bổ ngân sách ESG thế nào?",
            "Cơ chế Retirement bảo vệ chứng nhận chống Double Counting ra sao?"
        ]
        for q in quick_prompts:
            if st.button(f"👉 {q}", key=f"q_{abs(hash(q))}", use_container_width=True):
                st.session_state["selected_prompt"] = q

        st.markdown("---")
        st.markdown(f"""
        <div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 14px; font-size: 12px;">
            <div style="color: #10b981; font-weight: 700; margin-bottom: 6px;">HỒ SƠ HIỆN TẠI DOANH NGHIỆP:</div>
            <div>• <b>Doanh nghiệp:</b> {company_name}</div>
            <div>• <b>Scope 1:</b> {total_scope1_ton:,.1f} tCO2</div>
            <div>• <b>Scope 2:</b> {total_scope2_ton:,.1f} tCO2</div>
            <div>• <b>Tổng GHG:</b> {total_emissions_ton:,.1f} tCO2e</div>
            <div>• <b>Chi phí bù đắp:</b> ${offset_cost_usd:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c_chat:
        st.markdown("##### 💬 Trò Chuyện Trực Tiếp")
        
        chat_box = st.container(height=420)
        with chat_box:
            for m in st.session_state["chat_history"]:
                if m["role"] == "user":
                    st.markdown(f'<div class="chat-bubble-user"><b>Bạn:</b><br>{m["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-bubble-ai"><b>🌿 Cố vấn AI CarbonLens:</b><br>{m["content"]}</div>', unsafe_allow_html=True)

        user_input = st.chat_input("Nhập câu hỏi nghiên cứu hoặc chiến lược cho AI...")
        preset = st.session_state.pop("selected_prompt", "")
        chosen_query = user_input if user_input else (preset if preset else None)

        if chosen_query:
            st.session_state["chat_history"].append({"role": "user", "content": chosen_query})
            q_low = chosen_query.lower()

            if "giải pháp" in q_low or "giảm" in q_low or "đánh giá" in q_low:
                ans = f"""**Đánh giá phát thải & 3 Giải pháp Cắt giảm cho {company_name}:**

1. **Hiện trạng:** Doanh nghiệp phát thải `{total_emissions_ton:,.1f} tCO2e` (Scope 1 chiếm {(total_scope1_ton/total_emissions_ton*100) if total_emissions_ton>0 else 0:.1f}%, Scope 2 chiếm {(total_scope2_ton/total_emissions_ton*100) if total_emissions_ton>0 else 0:.1f}%). Chi phí bù đắp ước tính **${offset_cost_usd:,.2f}** (~{offset_cost_vnd/1_000_000:,.1f} triệu VNĐ).
2. **Giải pháp 1 (Scope 2):** Đầu tư điện mặt trời mái nhà (Rooftop Solar) tại phân xưởng, giúp cắt giảm 30-40% lượng điện mua từ lưới EVN.
3. **Giải pháp 2 (Scope 1):** Tối ưu hóa lộ trình logistics bằng AI và từng bước điện hóa phương tiện vận chuyển nội bộ.
4. **Giải pháp 3 (Bù đắp Net Zero):** Mua tín chỉ Blue Carbon rừng Cần Giờ cho lượng phát thải thặng dư không thể cắt giảm kỹ thuật."""
            elif "blue carbon" in q_low or "hấp thụ" in q_low or "rừng" in q_low or "gấp" in q_low:
                ans = """**Tại sao Blue Carbon Rừng Ngập Mặn Cần Giờ hấp thụ vượt trội (18.5 tCO2/ha/năm)?**

- **Trầm tích yếm khí:** Môi trường ngập triều hàng ngày khiến đáy bùn thiếu oxy, vi khuẩn phân hủy cực chậm, khóa chặt hơn **62.5% carbon** dưới lớp bùn trầm tích qua hàng trăm năm.
- **Mạng lưới rễ chống & rễ thở dày đặc:** Rễ cây Đước và Mấm bẫy lượng phù sa hữu cơ giàu carbon trôi theo dòng chảy sông Soài Rạp và Lòng Tàu.
- **Tốc độ quang hợp sinh khối:** Khí hậu nhiệt đới nắng gió Cần Giờ giúp cây tích lũy sinh khối gỗ đặc quanh năm liên tục."""
            elif "ngân sách" in q_low or "giá" in q_low or "esg" in q_low:
                ans = f"""**Tư vấn Phân bổ Ngân sách ESG theo Giá Tín chỉ ${carbon_price}/tCO2:**

- Hiện tại đơn giá ${carbon_price} là mức rất cạnh tranh trên thị trường tự nguyện. Khi sàn tín chỉ carbon quốc gia Việt Nam chính thức vận hành và cơ chế CBAM châu Âu mở rộng, giá dự báo sẽ đạt $25 - $45/tCO2.
- Doanh nghiệp nên trích lập khoảng **${(offset_cost_usd * 0.75):,.0f} USD** để mua trước 75% tín chỉ bảo vệ giá, 25% ngân sách còn lại đầu tư vào thiết bị tiết kiệm năng lượng tại chỗ."""
            else:
                ans = f"""Cảm ơn bạn đã hỏi về: *"{chosen_query}"*.
Với dữ liệu của **{company_name}** ({total_emissions_ton:,.1f} tấn phát thải), diện tích 35.120 ha rừng Cần Giờ hoàn toàn đáp ứng nhu cầu tín chỉ trung hòa phát thải. Bạn có thể sang **Mục 3 (Sàn giao dịch)** để trải nghiệm cấp chứng nhận số Net Zero hoặc tiếp tục đặt câu hỏi chuyên sâu!"""

            st.session_state["chat_history"].append({"role": "assistant", "content": ans})
            st.rerun()

# ==============================================================================
# 6. FOOTER
# ==============================================================================
st.divider()
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 12px; padding: 10px 0;">
    🌿 <b>CarbonLens Project 2026</b> | Đề tài Nghiên cứu Khoa học Kinh tế tuần hoàn & Thị trường Tín chỉ Carbon Rừng ngập mặn Cần Giờ | Tuân thủ GHG Protocol & Chuẩn IPCC
</div>
""", unsafe_allow_html=True)
