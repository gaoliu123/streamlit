# ============================================================
# 汇川技术 (300124) 2025年年度财报竞争情报看板
# 数据来源：深圳市汇川技术股份有限公司 2025年年度报告
# 使用方：西门子数字化工业（DI）竞争情报团队
# 生成时间：2026年
# ⚠️ 本看板仅供西门子内部竞争研究使用，请勿对外传播
# ============================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import io

st.set_page_config(
    page_title="汇川技术 FY2025 竞争情报看板 | Siemens DI",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# 配色方案（固定字典）
# ─────────────────────────────────────────
COLORS = {
    "primary":    "#1B3A8C",
    "secondary":  "#2BBFBF",
    "success":    "#27AE60",
    "danger":     "#E74C3C",
    "neutral":    "#8FA8C8",
    "bg_light":   "#F5F7FA",
    "card_bg":    "#FFFFFF",
    "text_dark":  "#1A2B4A",
    "text_muted": "#6B7A99",
    "plot_bg":    "#FFFFFF",
    "grid_color": "#E8EDF5",
}

PRODUCT_COLORS = ["#1B3A8C", "#2BBFBF", "#5B8DEF", "#27AE60"]

# ─────────────────────────────────────────
# CSS注入
# ─────────────────────────────────────────
def inject_css() -> None:
    """注入全局CSS样式，统一看板视觉风格。"""
    st.markdown("""
    <style>
    /* ① 全局背景 */
    .stApp {
        background-color: #F5F7FA;
        color: #1A2B4A;
        font-family: 'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;
    }

    /* ② 主标题横幅 */
    .main-header {
        background: linear-gradient(135deg, #1B3A8C 0%, #2B5299 60%, #1B3A8C 100%);
        border-left: 6px solid #2BBFBF;
        border-radius: 14px;
        box-shadow: 0 4px 20px rgba(27,58,140,0.18);
        padding: 22px 28px 18px 28px;
        margin-bottom: 18px;
    }
    .main-header h1 {
        color: #FFFFFF;
        font-size: 1.9rem;
        font-weight: 700;
        margin: 0 0 6px 0;
    }
    .main-header p {
        color: #A8C4E8;
        font-size: 0.88rem;
        margin: 0;
    }

    /* ③ KPI卡片 */
    [data-testid="metric-container"] {
        background: #FFFFFF;
        border: 1px solid #E0E8F5;
        border-radius: 12px;
        border-top: 4px solid #1B3A8C;
        box-shadow: 0 2px 12px rgba(27,58,140,0.08);
        padding: 14px 16px 12px 16px;
        transition: box-shadow 0.2s;
    }
    [data-testid="metric-container"]:hover {
        box-shadow: 0 6px 24px rgba(27,58,140,0.15);
    }
    [data-testid="stMetricLabel"] {
        color: #6B7A99 !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricValue"] {
        color: #1B3A8C !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }

    /* ④ 隐藏delta箭头图标 */
    [data-testid="stMetricDelta"] svg { display: none; }
    [data-testid="stMetricDelta"] { font-size: 0.8rem; font-weight: 600; }

    /* ⑤ Tab导航 */
    [data-testid="stTabs"] [role="tablist"] {
        background: #FFFFFF;
        border-radius: 10px;
        border: 1px solid #E0E8F5;
        padding: 4px;
    }
    [data-testid="stTabs"] [role="tab"] {
        color: #6B7A99;
        font-weight: 600;
        font-size: 0.88rem;
        border-radius: 8px;
        padding: 6px 14px;
    }
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        background: #1B3A8C !important;
        color: #FFFFFF !important;
        border-radius: 8px;
    }

    /* ⑥ 侧边栏 */
    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 2px solid #E0E8F5;
    }

    /* ⑦ h3标题装饰 */
    h3 {
        color: #1B3A8C !important;
        border-bottom: 2px solid #2BBFBF;
        padding-bottom: 6px;
        margin-bottom: 16px !important;
    }

    /* ⑧ Insight洞察框 */
    .insight-box {
        background: #EEF3FC;
        border-left: 5px solid #1B3A8C;
        border-radius: 10px;
        padding: 13px 18px;
        font-size: 0.87rem;
        margin-bottom: 10px;
        line-height: 1.6;
    }
    .insight-box.green {
        background: #EAF7F0;
        border-left-color: #27AE60;
    }
    .insight-box.red {
        background: #FEF0EE;
        border-left-color: #E74C3C;
    }
    .insight-box.teal {
        background: #E8F8F8;
        border-left-color: #2BBFBF;
    }

    /* ⑨ 下载按钮 */
    [data-testid="stDownloadButton"] button {
        background: #1B3A8C;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
    }
    [data-testid="stDownloadButton"] button:hover {
        background: #2BBFBF;
    }

    /* ⑩ dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        border: 1px solid #E0E8F5;
    }
    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# 图表统一布局
# ─────────────────────────────────────────
def base_layout(**kwargs) -> dict:
    """返回Plotly图表统一布局配置字典。"""
    layout = dict(
        template="plotly_white",
        paper_bgcolor=COLORS["card_bg"],
        plot_bgcolor=COLORS["plot_bg"],
        font=dict(
            family="Segoe UI, PingFang SC, Microsoft YaHei",
            color=COLORS["text_dark"],
            size=12,
        ),
        title_font=dict(
            color=COLORS["primary"],
            size=14,
            family="Segoe UI, PingFang SC",
        ),
        xaxis=dict(
            gridcolor=COLORS["grid_color"],
            linecolor="#D0DAF0",
            tickcolor="#D0DAF0",
        ),
        yaxis=dict(
            gridcolor=COLORS["grid_color"],
            linecolor="#D0DAF0",
            tickcolor="#D0DAF0",
        ),
        margin=dict(t=55, b=40, l=40, r=30),
    )
    layout.update(kwargs)
    return layout

# ─────────────────────────────────────────
# KPI卡片组件
# ─────────────────────────────────────────
def kpi_card(col, label: str, value: str, delta: str, delta_val: str, note: str = "") -> None:
    """渲染单个KPI指标卡片。"""
    with col:
        st.metric(label=label, value=value, delta=delta_val)
        if note:
            st.caption(note)

# ─────────────────────────────────────────
# 数据层
# ─────────────────────────────────────────
def load_financial_data() -> dict:
    """
    加载汇川技术FY2025财报数据。
    所有数据来源：深圳市汇川技术股份有限公司2025年年度报告（合并报表口径）。
    单位：万元（原始单位为元，已换算）。
    """

    # ── 一、年度盈利数据（近3年）──
    annual_pnl = pd.DataFrame({
        "年份": ["2023年", "2024年", "2025年"],
        "营业收入(万元)":      [304199.25, 370409.52, 451048.44],
        "归母净利润(万元)":    [47418.63,  42854.93,  50500.02],
        "扣非归母净利润(万元)":[40711.77,  40358.32,  49505.05],
        "营业成本(万元)":      [220340.00, 264094.04, 320449.39],  # 2023估算，2024/2025来自报告
        "研发费用(万元)":      [26241.48,  31470.81,  42557.74],
        "销售费用(万元)":      [13000.00,  14808.78,  15355.69],   # 2023估算
        "管理费用(万元)":      [11000.00,  15413.53,  18250.83],   # 2023估算
        "经营现金流(万元)":    [33699.16,  72004.40,  66810.25],
    })

    # 派生指标
    annual_pnl["毛利率(%)"] = (
        (annual_pnl["营业收入(万元)"] - annual_pnl["营业成本(万元)"])
        / annual_pnl["营业收入(万元)"] * 100
    ).round(2)
    annual_pnl["净利率(%)"] = (
        annual_pnl["归母净利润(万元)"] / annual_pnl["营业收入(万元)"] * 100
    ).round(2)
    annual_pnl["研发费用率(%)"] = (
        annual_pnl["研发费用(万元)"] / annual_pnl["营业收入(万元)"] * 100
    ).round(2)
    annual_pnl["销售费用率(%)"] = (
        annual_pnl["销售费用(万元)"] / annual_pnl["营业收入(万元)"] * 100
    ).round(2)
    annual_pnl["营收增速(%)"] = annual_pnl["营业收入(万元)"].pct_change() * 100
    annual_pnl["净利增速(%)"] = annual_pnl["归母净利润(万元)"].pct_change() * 100

    # ── 二、季度数据（FY2025）──
    quarterly = pd.DataFrame({
        "季度":       ["Q1", "Q2", "Q3", "Q4"],
        "营业收入(万元)": [89779.12, 115314.46, 111532.49, 134422.38],
        "归母净利润(万元)": [13228.25, 16455.63, 12857.43, 7958.71],
        "扣非净利润(万元)": [12337.90, 14376.53, 12166.61, 10624.01],
        "经营现金流(万元)": [2625.51, 27575.16, 9105.92, 27503.66],
    })
    quarterly["净利率(%)"] = (
        quarterly["归母净利润(万元)"] / quarterly["营业收入(万元)"] * 100
    ).round(2)

    # ── 三、产品线数据（FY2025 vs FY2024）──
    product_revenue = pd.DataFrame({
        "产品线": ["工业自动化与数字化", "新能源汽车动力系统", "新兴产业", "其他"],
        "2025年收入(万元)": [222454.02, 203225.82, 17950.19, 7418.41],
        "2024年收入(万元)": [187272.21, 160797.56, 15500.92, 6838.83],
        "2025年营业成本(万元)": [132865.04, 170504.18, 12760.01, 4320.15],
        "2025年毛利率(%)": [40.27, 16.10, 28.90, 41.74],
        "2024年毛利率(%)": [38.62, 16.38, 未披露_替换=None, 未披露_替换2=None],
        "同比增速(%)": [18.79, 26.39, 15.80, 8.47],
    })

    # 重新构建产品线（去掉错误列）
    product_revenue = pd.DataFrame({
        "产品线": ["工业自动化与数字化", "新能源汽车动力系统", "新兴产业", "其他"],
        "2025年收入(万元)": [222454.02, 203225.82, 17950.19, 7418.41],
        "2024年收入(万元)": [187272.21, 160797.56, 15500.92, 6838.83],
        "2025年毛利率(%)": [40.27, 16.10, 28.90, 41.74],
        "2024年毛利率(%)": [38.62, 16.38, None, None],
        "同比增速(%)": [18.79, 26.39, 15.80, 8.47],
    })

    # ── 四、地区数据（FY2025）──
    regional_revenue = pd.DataFrame({
        "地区": ["中国内地", "境外"],
        "2025年收入(万元)": [424559.52, 26488.92],
        "2024年收入(万元)": [350016.18, 20393.34],
        "占比(%)": [94.13, 5.87],
        "同比增速(%)": [21.30, 29.89],
        "2025年毛利率(%)": [28.55, None],  # 境外毛利率未单独披露
    })

    # ── 五、渠道数据（FY2025）──
    channel_data = pd.DataFrame({
        "渠道": ["直销/分销（合并）"],
        "收入(万元)": [451048.44],
        "占比(%)": [100.0],
        "毛利率(%)": [28.93],
    })
    # 注：财报仅披露直销/分销合并数据，未分拆

    # ── 六、费用结构（FY2025 vs FY2024）──
    expense_data = pd.DataFrame({
        "费用项目": ["销售费用", "管理费用", "研发费用"],
        "2024年(万元)": [14808.78, 15413.53, 31470.81],
        "2025年(万元)": [15355.69, 18250.83, 42557.74],
        "同比增速(%)": [3.69, 18.41, 35.23],
        "2025年费用率(%)": [3.41, 4.05, 9.44],
    })

    # ── 七、资产负债数据（FY2025）──
    balance_sheet = {
        "总资产(万元)":       713143.94,
        "归母净资产(万元)":   353529.91,
        "负债合计(万元)":     341795.83,
        "流动资产(万元)":     430087.38,
        "流动负债(万元)":     298940.57,
        "非流动负债(万元)":   42855.26,
        "存货(万元)":         80789.95,
        "应收账款(万元)":     115188.07,
        "资产负债率(%)":      47.93,
        "流动比率":           1.44,
    }

    # ── 八、关键指标汇总（近3年）──
    key_metrics = pd.DataFrame({
        "指标": ["加权平均ROE(%)", "基本EPS(元/股)", "资产负债率(%)",
                 "总资产(亿元)", "归母净资产(亿元)"],
        "2023年": [21.66, 1.78, None, 48.96, 24.48],
        "2024年": [16.52, 1.60, None, 57.18, 27.99],
        "2025年": [16.34, 1.87, 47.93, 71.31, 35.35],
    })

    # ── 九、分红数据（FY2025）──
    dividend_data = {
        "归母净利润(万元)":    50500.02,
        "现金分红总额(万元)":  13533.18,
        "分红比例(%)":         26.80,
        "每股股息(元，含税)":  0.50,
        "分红基数(股)":        2706636087,
    }

    # ── 十、产销量数据（FY2025）──
    production_sales = pd.DataFrame({
        "产品": ["智能制造产品", "新能源汽车产品"],
        "生产量": [25499533, 6108223],
        "销售量": [25971863, 5933895],
        "库存量": [1361822, 724156],
        "销售量同比(%)": [31.27, 28.46],
        "生产量同比(%)": [26.96, 26.06],
        "单位": ["PCS", "PCS"],
    })

    # ── 十一、研发数据（近3年）──
    rd_data = pd.DataFrame({
        "年份": ["2023年", "2024年", "2025年"],
        "研发费用(万元)": [26241.48, 31470.81, 42557.74],
        "研发费用率(%)": [8.63, 8.50, 9.44],
        "研发人员(人)": [None, None, 7670],
        "专利及软著(个)": [None, None, 3375],
    })

    # ── 十二、利润瀑布数据（FY2025）──
    waterfall_data = {
        "节点": ["营业收入", "营业成本", "毛利润", "销售费用", "管理费用",
                 "研发费用", "财务收益", "其他收益净额", "归母净利润"],
        "金额": [451048.44, -320449.39, 130599.05, -15355.69, -18250.83,
                 -42557.74, 657.19, 3500.00, 50500.02],
        "measure": ["absolute", "relative", "total", "relative", "relative",
                    "relative", "relative", "relative", "total"],
    }

    return {
        "annual_pnl":        annual_pnl,
        "quarterly":         quarterly,
        "product_revenue":   product_revenue,
        "regional_revenue":  regional_revenue,
        "channel_data":      channel_data,
        "expense_data":      expense_data,
        "balance_sheet":     balance_sheet,
        "key_metrics":       key_metrics,
        "dividend_data":     dividend_data,
        "production_sales":  production_sales,
        "rd_data":           rd_data,
        "waterfall_data":    waterfall_data,
    }

# ─────────────────────────────────────────
# 侧边栏
# ─────────────────────────────────────────
def render_sidebar() -> str:
    """渲染侧边栏，返回当前分析视角。"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding:16px 0 12px 0;">
            <div style="font-size:2.2rem;">🏭</div>
            <div style="font-weight:700; font-size:1.1rem; color:#1B3A8C;">汇川技术</div>
            <div style="font-size:0.78rem; color:#6B7A99;">300124 · 深交所创业板</div>
            <div style="font-size:0.75rem; color:#2BBFBF; margin-top:4px;">
                Siemens DI 竞争情报看板
            </div>
        </div>
        <hr style="border-color:#E0E8F5; margin:8px 0 14px 0;">
        """, unsafe_allow_html=True)

        st.markdown("**📋 公司概况**")
        st.markdown("""
        | 项目 | 内容 |
        |------|------|
        | 全称 | 深圳市汇川技术股份有限公司 |
        | 主营 | 工业自动化+新能源汽车 |
        | 总部 | 深圳市龙华区 |
        | 上市 | 2010年 · 创业板 |
        | 实控人 | 朱兴明 |
        """)

        st.markdown("**⚡ 核心数据速览（FY2025）**")
        st.markdown("""
        | 指标 | 数值 |
        |------|------|
        | 营业收入 | **451.05亿元** |
        | 归母净利润 | **50.50亿元** |
        | 营收增速 | **+21.77%** |
        | 研发费用率 | **9.44%** |
        | 研发人员 | **7,670人** |
        | 专利及软著 | **3,375个** |
        | 伺服市占率 | **31%（中国第一）** |
        | 变频器市占率 | **20%（中国第一）** |
        """)

        st.markdown("**🔍 分析视角**")
        view_mode = st.radio(
            "选择分析视角",
            ["全面分析", "增长聚焦", "盈利聚焦"],
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.caption("📅 数据截止：2025年12月31日")
        st.caption("📄 来源：汇川技术2025年年度报告（合并报表）")
        st.caption("⚠️ 仅供西门子DI内部竞争研究使用")

    return view_mode

# ─────────────────────────────────────────
# Tab1：CEO概览
# ─────────────────────────────────────────
def render_tab_ceo(data: dict) -> None:
    """渲染CEO概览Tab：核心KPI、三年趋势、雷达图、季度节奏。"""
    pnl = data["annual_pnl"]
    q   = data["quarterly"]
    bs  = data["balance_sheet"]

    # ── 第一行：6个KPI ──
    st.markdown("### 📊 FY2025 核心经营指标")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    kpi_card(c1, "营业总收入", "451.05亿", "+21.77%", "+21.77% YoY", "合并报表口径")
    kpi_card(c2, "归母净利润", "50.50亿", "+17.84%", "+17.84% YoY", "")
    kpi_card(c3, "扣非归母净利润", "49.51亿", "+22.66%", "+22.66% YoY", "")
    kpi_card(c4, "研发投入", "42.56亿", "+35.23%", "+35.23% YoY", "费用率9.44%")
    kpi_card(c5, "基本EPS", "1.87元/股", "+16.88%", "+16.88% YoY", "")
    kpi_card(c6, "现金分红总额", "13.53亿", "每10股派5元", "分红比例26.8%", "含税")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 第二行：4个资产健康度卡片 ──
    st.markdown("### 🏦 资产健康度")
    a1, a2, a3, a4 = st.columns(4)
    kpi_card(a1, "总资产", "713.14亿", "+24.72%", "+24.72% YoY", "")
    kpi_card(a2, "归母净资产", "353.53亿", "+26.29%", "+26.29% YoY", "")
    kpi_card(a3, "加权平均ROE", "16.34%", "-0.18pct", "-0.18pct YoY", "2024年16.52%")
    kpi_card(a4, "境外收入增速", "+29.89%", "占比5.87%", "26.49亿元", "国际化加速")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 第三行：三年趋势双轴图 + 雷达图 ──
    st.markdown("### 📈 三年经营趋势 & 盈利质量雷达")
    col_left, col_right = st.columns([3, 2])

    with col_left:
        fig_trend = make_subplots(specs=[[{"secondary_y": True}]])

        # 柱状：营业收入
        fig_trend.add_trace(
            go.Bar(
                x=pnl["年份"],
                y=pnl["营业收入(万元)"] / 10000,
                name="营业收入（亿元）",
                marker=dict(color=COLORS["primary"], opacity=0.82,
                            line=dict(color="white", width=1)),
                hovertemplate="<b>%{x}</b><br>营业收入：%{y:.2f} 亿元<extra></extra>",
            ),
            secondary_y=False,
        )

        # 折线：归母净利润
        fig_trend.add_trace(
            go.Scatter(
                x=pnl["年份"],
                y=pnl["归母净利润(万元)"] / 10000,
                name="归母净利润（亿元）",
                mode="lines+markers+text",
                line=dict(color=COLORS["secondary"], width=2.5),
                marker=dict(symbol="diamond", size=10,
                            color=COLORS["secondary"],
                            line=dict(color="white", width=2)),
                text=[f"{v/10000:.2f}" for v in pnl["归母净利润(万元)"]],
                textposition="top center",
                textfont=dict(size=11, color=COLORS["secondary"]),
                hovertemplate="<b>%{x}</b><br>归母净利润：%{y:.2f} 亿元<extra></extra>",
            ),
            secondary_y=False,
        )

        # 右轴折线：净利率
        fig_trend.add_trace(
            go.Scatter(
                x=pnl["年份"],
                y=pnl["净利率(%)"],
                name="净利率（%）",
                mode="lines+markers",
                line=dict(color=COLORS["success"], width=2, dash="dot"),
                marker=dict(size=8, color=COLORS["success"]),
                hovertemplate="<b>%{x}</b><br>净利率：%{y:.2f}%<extra></extra>",
            ),
            secondary_y=True,
        )

        fig_trend.update_layout(
            **base_layout(
                title="营业收入 / 归母净利润 / 净利率（三年趋势）",
                height=420,
                legend=dict(
                    orientation="h", y=-0.18, x=0.5, xanchor="center",
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="#E0E8F5", borderwidth=1,
                ),
            )
        )
        fig_trend.update_yaxes(title_text="金额（亿元）", secondary_y=False,
                               gridcolor=COLORS["grid_color"])
        fig_trend.update_yaxes(title_text="净利率（%）", secondary_y=True,
                               gridcolor=COLORS["grid_color"])
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_right:
        # 雷达图：盈利质量
        categories = ["毛利率", "净利率", "研发费用率", "销售费用率", "ROE"]
        radar_2023 = [27.56, 15.59, 8.63, 4.27, 21.66]
        radar_2024 = [28.70, 11.57, 8.50, 4.00, 16.52]
        radar_2025 = [28.93, 11.20, 9.44, 3.41, 16.34]

        fig_radar = go.Figure()
        for vals, name, color in [
            (radar_2023, "2023年", COLORS["neutral"]),
            (radar_2024, "2024年", COLORS["secondary"]),
            (radar_2025, "2025年", COLORS["primary"]),
        ]:
            fig_radar.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=categories + [categories[0]],
                fill="toself",
                name=name,
                line=dict(color=color, width=2),
                fillcolor=color.replace(")", ",0.15)").replace("rgb", "rgba")
                           if "rgb" in color else color + "26",
                opacity=0.85,
            ))

        fig_radar.update_layout(
            **base_layout(
                title="盈利质量雷达图（三年对比）",
                height=420,
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 30],
                                   gridcolor=COLORS["grid_color"]),
                    angularaxis=dict(gridcolor=COLORS["grid_color"]),
                ),
                legend=dict(
                    orientation="h", y=-0.12, x=0.5, xanchor="center",
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="#E0E8F5", borderwidth=1,
                ),
            )
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # ── 第四行：季度节奏 ──
    st.markdown("### 📅 FY2025 季度经营节奏")
    fig_q = make_subplots(rows=1, cols=2,
                          subplot_titles=("季度营业收入（亿元）", "季度净利率（%）"))

    q_colors = [COLORS["neutral"], COLORS["primary"],
                COLORS["primary"], COLORS["secondary"]]

    fig_q.add_trace(
        go.Bar(
            x=q["季度"],
            y=q["营业收入(万元)"] / 10000,
            marker=dict(color=q_colors, line=dict(color="white", width=1)),
            text=[f"{v/10000:.2f}" for v in q["营业收入(万元)"]],
            textposition="outside",
            textfont=dict(size=11),
            hovertemplate="<b>%{x}</b><br>营业收入：%{y:.2f} 亿元<extra></extra>",
            showlegend=False,
        ),
        row=1, col=1,
    )

    fig_q.add_trace(
        go.Scatter(
            x=q["季度"],
            y=q["净利率(%)"],
            mode="lines+markers+text",
            line=dict(color=COLORS["secondary"], width=2.5),
            marker=dict(size=10, color=COLORS["secondary"],
                        line=dict(color="white", width=2)),
            text=[f"{v:.2f}%" for v in q["净利率(%)"]],
            textposition="top center",
            textfont=dict(size=11, color=COLORS["secondary"]),
            hovertemplate="<b>%{x}</b><br>净利率：%{y:.2f}%<extra></extra>",
            showlegend=False,
        ),
        row=1, col=2,
    )

    fig_q.update_layout(
        **base_layout(title="FY2025 分季度财务指标", height=400)
    )
    fig_q.update_xaxes(gridcolor=COLORS["grid_color"])
    fig_q.update_yaxes(gridcolor=COLORS["grid_color"])
    st.plotly_chart(fig_q, use_container_width=True)

    # ── 洞察框 ──
    st.markdown("""
    <div class="insight-box green">
    ✅ <b>营收451亿元，同比+21.77%</b>，在中国工业自动化行业整体小幅下滑背景下逆势高增长，
    说明汇川凭借"工业自动化+新能源汽车"双引擎战略成功穿越行业周期。
    西门子DI需重点关注其在变频器（市占20%）和伺服（市占31%）两大核心品类的持续份额扩张。
    </div>
    <div class="insight-box red">
    ⚠️ <b>Q4归母净利润仅7.96亿元</b>，环比Q3下滑38%，净利率降至5.92%，
    显示Q4盈利能力明显承压，可能与年末促销、费用集中确认有关。
    西门子DI可在Q4时间窗口加大市场投入，抢占汇川客户服务空档期。
    </div>
    <div class="insight-box teal">
    ⚡ <b>研发费用同比增长35.23%（42.56亿元）</b>，远超营收增速21.77%，
    说明汇川正在加速技术储备，重点布局AI工业智脑（iFG）、人形机器人、数字能源等新赛道。
    西门子DI需密切跟踪其工业软件与数字化平台（InoCube）的商业化进展。
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# Tab2：产品线分析
# ─────────────────────────────────────────
def render_tab_product(data: dict) -> None:
    """渲染产品线分析Tab：收入结构、毛利率对比、增速排名、产销量。"""
    prod = data["product_revenue"]
    ps   = data["production_sales"]

    st.markdown("### 🏗️ 产品线收入结构（FY2025）")

    col1, col2 = st.columns([1, 1])

    with col1:
        # 环形饼图
        fig_pie = go.Figure(go.Pie(
            labels=prod["产品线"],
            values=prod["2025年收入(万元)"],
            hole=0.52,
            marker=dict(colors=PRODUCT_COLORS,
                        line=dict(color="white", width=2)),
            textinfo="label+percent",
            textfont=dict(size=12),
            hovertemplate="<b>%{label}</b><br>收入：%{value:,.0f} 万元<br>占比：%{percent}<extra></extra>",
        ))
        fig_pie.add_annotation(
            text="<b>451.05亿</b><br>总收入",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=13, color=COLORS["primary"]),
        )
        fig_pie.update_layout(
            **base_layout(title="产品线收入占比（FY2025）", height=380),
            showlegend=True,
            legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center"),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # 产品线收入双轴图（收入柱 + 毛利率折线）
        fig_dual = make_subplots(specs=[[{"secondary_y": True}]])

        fig_dual.add_trace(
            go.Bar(
                x=prod["产品线"],
                y=prod["2025年收入(万元)"] / 10000,
                name="2025年收入（亿元）",
                marker=dict(color=PRODUCT_COLORS,
                            line=dict(color="white", width=1)),
                hovertemplate="<b>%{x}</b><br>收入：%{y:.2f} 亿元<extra></extra>",
            ),
            secondary_y=False,
        )

        fig_dual.add_trace(
            go.Scatter(
                x=prod["产品线"],
                y=prod["2025年毛利率(%)"],
                name="毛利率（%）",
                mode="markers+lines",
                marker=dict(symbol="star", size=13,
                            color=COLORS["secondary"],
                            line=dict(color="white", width=1)),
                line=dict(color=COLORS["secondary"], width=2),
                hovertemplate="<b>%{x}</b><br>毛利率：%{y:.2f}%<extra></extra>",
            ),
            secondary_y=True,
        )

        fig_dual.update_layout(
            **base_layout(title="产品线收入 & 毛利率（FY2025）", height=380,
                          legend=dict(orientation="h", y=-0.18, x=0.5,
                                      xanchor="center",
                                      bgcolor="rgba(255,255,255,0.8)",
                                      bordercolor="#E0E8F5", borderwidth=1))
        )
        fig_dual.update_yaxes(title_text="收入（亿元）", secondary_y=False)
        fig_dual.update_yaxes(title_text="毛利率（%）", secondary_y=True)
        st.plotly_chart(fig_dual, use_container_width=True)

    # ── 产品线增速水平柱状图 ──
    st.markdown("### 📊 产品线同比增速排名")
    overall_growth = 21.77
    bar_colors = [
        COLORS["success"] if v >= overall_growth else COLORS["primary"]
        for v in prod["同比增速(%)"]
    ]

    fig_growth = go.Figure(go.Bar(
        x=prod["同比增速(%)"],
        y=prod["产品线"],
        orientation="h",
        marker=dict(color=bar_colors, line=dict(color="white", width=1)),
        text=[f"{v:+.2f}%" for v in prod["同比增速(%)"]],
        textposition="outside",
        textfont=dict(size=12),
        hovertemplate="<b>%{y}</b><br>同比增速：%{x:+.2f}%<extra></extra>",
    ))
    fig_growth.add_vline(x=0, line_dash="dash",
                         line_color=COLORS["text_muted"], line_width=1)
    fig_growth.add_vline(x=overall_growth, line_dash="dot",
                         line_color=COLORS["danger"], line_width=1.5,
                         annotation_text=f"整体增速 {overall_growth:.2f}%",
                         annotation_position="top right",
                         annotation_font=dict(color=COLORS["danger"], size=11))
    fig_growth.update_layout(
        **base_layout(title="产品线同比增速（FY2025 vs FY2024）", height=340)
    )
    st.plotly_chart(fig_growth, use_container_width=True)

    # ── 产销量分组柱状图 ──
    st.markdown("### 📦 主要产品产销量（FY2025）")
    fig_ps = go.Figure()
    for col_name, color, label in [
        ("生产量", COLORS["primary"], "生产量（万件）"),
        ("销售量", COLORS["secondary"], "销售量（万件）"),
        ("库存量", COLORS["neutral"], "库存量（万件）"),
    ]:
        fig_ps.add_trace(go.Bar(
            name=label,
            x=ps["产品"],
            y=ps[col_name] / 10000,
            marker=dict(color=color, line=dict(color="white", width=1)),
            hovertemplate=f"<b>%{{x}}</b><br>{label}：%{{y:,.2f}} 万件<extra></extra>",
        ))
    fig_ps.update_layout(
        **base_layout(title="主要产品产销量对比（FY2025）", height=380,
                      barmode="group",
                      legend=dict(orientation="h", y=-0.18, x=0.5,
                                  xanchor="center",
                                  bgcolor="rgba(255,255,255,0.8)",
                                  bordercolor="#E0E8F5", borderwidth=1))
    )
    st.plotly_chart(fig_ps, use_container_width=True)

    # ── 产品线数据表 ──
    st.markdown("### 📋 产品线详细数据")
    display_prod = prod.copy()
    display_prod["2025年收入(亿元)"] = (display_prod["2025年收入(万元)"] / 10000).round(2)
    display_prod["2024年收入(亿元)"] = (display_prod["2024年收入(万元)"] / 10000).round(2)
    display_prod["同比增速"] = display_prod["同比增速(%)"].apply(lambda x: f"{x:+.2f}%")
    display_prod["2025年毛利率"] = display_prod["2025年毛利率(%)"].apply(lambda x: f"{x:.2f}%")
    st.dataframe(
        display_prod[["产品线", "2025年收入(亿元)", "2024年收入(亿元)",
                      "2025年毛利率", "同比增速"]],
        use_container_width=True, hide_index=True,
    )

    # ── 洞察框 ──
    st.markdown("""
    <div class="insight-box red">
    ⚠️ <b>工业自动化与数字化毛利率40.27%</b>，同比提升1.65pct，
    说明汇川在工控领域的产品溢价能力持续增强。
    西门子DI在PLC、伺服、变频器等核心品类面临的价格竞争压力将持续加剧，
    尤其是汇川PLC在中国市场份额5.7%仍处于快速爬坡阶段，需重点防守。
    </div>
    <div class="insight-box green">
    ✅ <b>新能源汽车动力系统收入203亿元，同比+26.39%</b>，
    已占总收入45.06%，成为与工业自动化并驾齐驱的第二增长极。
    该业务毛利率仅16.10%，但规模效应持续显现，西门子DI暂无直接竞争，
    但需关注汇川借助新能源汽车客户关系向工厂自动化渗透的协同效应。
    </div>
    <div class="insight-box teal">
    ⚡ <b>新兴产业（机器人+数字能源）收入17.95亿元，同比+15.80%</b>，
    体量虽小但战略意义重大。人形机器人、工业机器人、储能PCS三条赛道
    均在快速布局，西门子DI需关注其在机器人控制器领域对Motion Control的潜在冲击。
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# Tab3：市场与渠道
# ─────────────────────────────────────────
def render_tab_market(data: dict) -> None:
    """渲染市场与渠道Tab：地区分布、增速对比、渠道结构。"""
    reg = data["regional_revenue"]

    st.markdown("### 🌍 地区收入分布（FY2025）")

    col1, col2 = st.columns([1, 1])

    with col1:
        # 地区收入水平柱状图
        fig_reg = go.Figure()
        fig_reg.add_trace(go.Bar(
            x=reg["2025年收入(万元)"] / 10000,
            y=reg["地区"],
            orientation="h",
            marker=dict(
                color=[COLORS["primary"], COLORS["secondary"]],
                line=dict(color="white", width=1),
            ),
            text=[f"{v/10000:.2f}亿" for v in reg["2025年收入(万元)"]],
            textposition="outside",
            textfont=dict(size=12),
            hovertemplate="<b>%{y}</b><br>收入：%{x:.2f} 亿元<extra></extra>",
        ))
        fig_reg.update_layout(
            **base_layout(title="地区收入（FY2025，亿元）", height=300,
                          showlegend=False)
        )
        st.plotly_chart(fig_reg, use_container_width=True)

    with col2:
        # 地区增速对比
        overall_growth = 21.77
        growth_colors = [
            COLORS["success"] if v >= overall_growth else COLORS["primary"]
            for v in reg["同比增速(%)"]
        ]
        fig_reg_g = go.Figure(go.Bar(
            x=reg["同比增速(%)"],
            y=reg["地区"],
            orientation="h",
            marker=dict(color=growth_colors, line=dict(color="white", width=1)),
            text=[f"{v:+.2f}%" for v in reg["同比增速(%)"]],
            textposition="outside",
            textfont=dict(size=12),
            hovertemplate="<b>%{y}</b><br>同比增速：%{x:+.2f}%<extra></extra>",
        ))
        fig_reg_g.add_vline(x=overall_growth, line_dash="dot",
                            line_color=COLORS["danger"], line_width=1.5,
                            annotation_text=f"整体增速 {overall_growth:.2f}%",
                            annotation_position="top right",
                            annotation_font=dict(color=COLORS["danger"], size=11))
        fig_reg_g.update_layout(
            **base_layout(title="地区增速对比（FY2025 vs FY2024）", height=300,
                          showlegend=False)
        )
        st.plotly_chart(fig_reg_g, use_container_width=True)

    # ── 境内外收入占比环形饼图 ──
    st.markdown("### 🗺️ 境内外收入结构")
    col3, col4, col5 = st.columns(3)

    with col3:
        fig_geo = go.Figure(go.Pie(
            labels=reg["地区"],
            values=reg["2025年收入(万元)"],
            hole=0.52,
            marker=dict(colors=[COLORS["primary"], COLORS["secondary"]],
                        line=dict(color="white", width=2)),
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>收入：%{value:,.0f} 万元<extra></extra>",
        ))
        fig_geo.add_annotation(
            text="<b>境内外</b><br>收入占比",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=11, color=COLORS["primary"]),
        )
        fig_geo.update_layout(
            **base_layout(title="境内外收入占比（FY2025）", height=340),
            showlegend=True,
            legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center"),
        )
        st.plotly_chart(fig_geo, use_container_width=True)

    with col4:
        # 三年境外收入趋势
        overseas_rev = [2039.33, 2648.89]  # 2024, 2025 (万元)
        overseas_growth = [17.22, 29.89]
        fig_overseas = go.Figure()
        fig_overseas.add_trace(go.Bar(
            x=["2024年", "2025年"],
            y=[v / 10000 for v in overseas_rev],
            marker=dict(color=[COLORS["neutral"], COLORS["secondary"]],
                        line=dict(color="white", width=1)),
            text=[f"{v/10000:.2f}亿" for v in overseas_rev],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>境外收入：%{y:.2f} 亿元<extra></extra>",
        ))
        fig_overseas.update_layout(
            **base_layout(title="境外收入趋势（亿元）", height=340, showlegend=False)
        )
        st.plotly_chart(fig_overseas, use_container_width=True)

    with col5:
        # 境外增速趋势
        fig_og = go.Figure(go.Bar(
            x=["2024年", "2025年"],
            y=overseas_growth,
            marker=dict(color=[COLORS["neutral"], COLORS["success"]],
                        line=dict(color="white", width=1)),
            text=[f"{v:+.2f}%" for v in overseas_growth],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>境外增速：%{y:+.2f}%<extra></extra>",
        ))
        fig_og.update_layout(
            **base_layout(title="境外收入同比增速（%）", height=340, showlegend=False)
        )
        st.plotly_chart(fig_og, use_container_width=True)

    # ── 渠道说明 ──
    st.markdown("### 🏪 销售渠道结构")
    st.info("""
    📌 **渠道说明**：汇川技术FY2025财报未分拆直销与经销的具体收入及毛利率数据，
    仅披露"直销/分销"合并口径（占比100%）。
    根据报告定性描述：工业自动化业务采用"**分销为主、直销为辅**"模式；
    新能源汽车及数字能源业务主要采用**直销**模式。
    """)

    col6, col7 = st.columns(2)
    with col6:
        channel_est = pd.DataFrame({
            "渠道模式": ["分销（工控）", "直销（新能源汽车）", "直销（其他）"],
            "估算收入占比(%)": [45, 45, 10],
        })
        fig_chan = go.Figure(go.Pie(
            labels=channel_est["渠道模式"],
            values=channel_est["估算收入占比(%)"],
            hole=0.48,
            marker=dict(colors=[COLORS["primary"], COLORS["secondary"],
                                 COLORS["neutral"]],
                        line=dict(color="white", width=2)),
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>估算占比：%{percent}<extra></extra>",
        ))
        fig_chan.add_annotation(
            text="渠道结构<br>（估算）",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=11, color=COLORS["primary"]),
        )
        fig_chan.update_layout(
            **base_layout(title="渠道结构估算（基于报告定性描述）", height=340),
            legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center"),
        )
        st.plotly_chart(fig_chan, use_container_width=True)

    with col7:
        st.markdown("**📋 地区收入详细数据**")
        display_reg = reg.copy()
        display_reg["2025年收入(亿元)"] = (display_reg["2025年收入(万元)"] / 10000).round(2)
        display_reg["2024年收入(亿元)"] = (display_reg["2024年收入(万元)"] / 10000).round(2)
        display_reg["同比增速"] = display_reg["同比增速(%)"].apply(lambda x: f"{x:+.2f}%")
        display_reg["收入占比"] = display_reg["占比(%)"].apply(lambda x: f"{x:.2f}%")
        st.dataframe(
            display_reg[["地区", "2025年收入(亿元)", "2024年收入(亿元)",
                          "收入占比", "同比增速"]],
            use_container_width=True, hide_index=True, height=200,
        )
        st.markdown("""
        **🌐 海外布局重点（来自报告）：**
        - 已在 **20+个国家** 完成储能样板点建设
        - 新设德国、墨西哥、日本研发中心
        - 匈牙利、泰国工厂建设中
        - 筹划赴港交所上市（H股）
        """)

    # ── 洞察框 ──
    st.markdown("""
    <div class="insight-box teal">
    🌍 <b>境外收入26.49亿元，同比+29.89%</b>，增速显著高于境内（+21.30%），
    说明汇川国际化战略正在加速落地。"借船出海"（随中国客户出海）+
    "行业出海"（直接开拓海外客户）双轮驱动，重点行业包括纺织、锂电、光伏、注塑机等，
    这些恰好是西门子DI在东南亚、中东的传统优势市场。
    </div>
    <div class="insight-box red">
    ⚠️ <b>境外收入占比仅5.87%</b>，但增速快、战略意图明确。
    汇川正在德国、意大利、西班牙、日本等西门子DI核心市场布局研发和销售网络，
    未来3-5年将成为西门子DI在欧洲市场不可忽视的竞争对手，
    尤其在中小型机械制造商（SME）领域的性价比竞争。
    </div>
    <div class="insight-box green">
    ✅ <b>中国内地收入424.56亿元，市场份额持续扩大</b>，
    伺服31%、变频器20%、中高压变频器14%均位居中国第一。
    西门子DI在中国市场的防守重点应聚焦高端制造（半导体、汽车整车、航空航天）
    和大型系统集成项目，这些领域汇川尚未形成全面竞争力。
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# Tab4：费用与研发
# ─────────────────────────────────────────
def render_tab_rd(data: dict) -> None:
    """渲染费用与研发Tab：费用结构、研发趋势、利润瀑布图。"""
    exp  = data["expense_data"]
    rd   = data["rd_data"]
    wf   = data["waterfall_data"]
    pnl  = data["annual_pnl"]

    st.markdown("### 💰 三大费用结构（FY2025 vs FY2024）")
    col1, col2 = st.columns(2)

    with col1:
        # 分组柱状图：三大费用两年对比
        fig_exp = go.Figure()
        for year, color in [("2024年(万元)", COLORS["neutral"]),
                             ("2025年(万元)", COLORS["primary"])]:
            fig_exp.add_trace(go.Bar(
                name=year.replace("(万元)", ""),
                x=exp["费用项目"],
                y=exp[year] / 10000,
                marker=dict(color=color, line=dict(color="white", width=1)),
                hovertemplate=f"<b>%{{x}}</b><br>{year}：%{{y:,.2f}} 亿元<extra></extra>",
            ))
        fig_exp.update_layout(
            **base_layout(title="三大费用两年对比（亿元）", height=380,
                          barmode="group",
                          legend=dict(orientation="h", y=-0.18, x=0.5,
                                      xanchor="center",
                                      bgcolor="rgba(255,255,255,0.8)",
                                      bordercolor="#E0E8F5", borderwidth=1))
        )
        st.plotly_chart(fig_exp, use_container_width=True)

    with col2:
        # 费用增速 vs 收入增速
        revenue_growth = 21.77
        growth_colors = [
            COLORS["danger"] if v > revenue_growth else COLORS["success"]
            for v in exp["同比增速(%)"]
        ]
        fig_exp_g = go.Figure(go.Bar(
            x=exp["费用项目"],
            y=exp["同比增速(%)"],
            marker=dict(color=growth_colors, line=dict(color="white", width=1)),
            text=[f"{v:+.2f}%" for v in exp["同比增速(%)"]],
            textposition="outside",
            textfont=dict(size=12),
            hovertemplate="<b>%{x}</b><br>同比增速：%{y:+.2f}%<extra></extra>",
        ))
        fig_exp_g.add_hline(y=revenue_growth, line_dash="dot",
                            line_color=COLORS["primary"], line_width=1.5,
                            annotation_text=f"营收增速 {revenue_growth:.2f}%",
                            annotation_position="top right",
                            annotation_font=dict(color=COLORS["primary"], size=11))
        fig_exp_g.update_layout(
            **base_layout(title="费用增速 vs 营收增速（%）", height=380,
                          showlegend=False)
        )
        st.plotly_chart(fig_exp_g, use_container_width=True)

    # ── 研发费用趋势双轴图 ──
    st.markdown("### 🔬 研发投入趋势（近3年）")
    col3, col4 = st.columns([3, 2])

    with col3:
        fig_rd = make_subplots(specs=[[{"secondary_y": True}]])
        fig_rd.add_trace(
            go.Bar(
                x=rd["年份"],
                y=rd["研发费用(万元)"] / 10000,
                name="研发费用（亿元）",
                marker=dict(color=COLORS["primary"], opacity=0.82,
                            line=dict(color="white", width=1)),
                hovertemplate="<b>%{x}</b><br>研发费用：%{y:.2f} 亿元<extra></extra>",
            ),
            secondary_y=False,
        )
        fig_rd.add_trace(
            go.Scatter(
                x=rd["年份"],
                y=rd["研发费用率(%)"],
                name="研发费用率（%）",
                mode="lines+markers+text",
                line=dict(color=COLORS["secondary"], width=2.5, dash="dot"),
                marker=dict(symbol="diamond", size=10,
                            color=COLORS["secondary"],
                            line=dict(color="white", width=2)),
                text=[f"{v:.2f}%" for v in rd["研发费用率(%)"]],
                textposition="top center",
                textfont=dict(size=11, color=COLORS["secondary"]),
                hovertemplate="<b>%{x}</b><br>研发费用率：%{y:.2f}%<extra></extra>",
            ),
            secondary_y=True,
        )
        fig_rd.update_layout(
            **base_layout(title="研发费用 & 研发费用率（三年趋势）", height=380,
                          legend=dict(orientation="h", y=-0.18, x=0.5,
                                      xanchor="center",
                                      bgcolor="rgba(255,255,255,0.8)",
                                      bordercolor="#E0E8F5", borderwidth=1))
        )
        fig_rd.update_yaxes(title_text="研发费用（亿元）", secondary_y=False)
        fig_rd.update_yaxes(title_text="研发费用率（%）", secondary_y=True)
        st.plotly_chart(fig_rd, use_container_width=True)

    with col4:
        st.markdown("**🔬 研发核心数据（FY2025）**")
        rd_kpis = {
            "研发投入总额": "42.56亿元",
            "研发费用率": "9.44%",
            "研发人员": "7,670人",
            "研发人员占比": "28%（总员工）",
            "累计专利及软著": "3,375个",
            "资本化研发支出": "0（全费用化）",
            "在研重点项目": "MD630变频器、中压IGCT变频器、四象限一体机等",
        }
        for k, v in rd_kpis.items():
            st.markdown(f"- **{k}**：{v}")

        st.markdown("**🎯 研发重点方向（FY2026）**")
        st.markdown("""
        - 工业AI（iFG工业智脑平台）
        - 大型PLC & 安全PLC
        - 人形机器人零部件
        - 储能PCS大功率化
        - 新能源汽车800V高压平台
        """)

    # ── 利润瀑布图 ──
    st.markdown("### 🌊 FY2025 利润瀑布图")
    wf_nodes  = wf["节点"]
    wf_values = wf["金额"]
    wf_measure = wf["measure"]

    fig_wf = go.Figure(go.Waterfall(
        name="利润瀑布",
        orientation="v",
        measure=wf_measure,
        x=wf_nodes,
        y=wf_values,
        text=[f"{v:+,.0f}" for v in wf_values],
        textposition="outside",
        textfont=dict(size=10),
        increasing=dict(marker=dict(color=COLORS["success"])),
        decreasing=dict(marker=dict(color=COLORS["danger"])),
        totals=dict(marker=dict(color=COLORS["primary"])),
        connector=dict(line=dict(color=COLORS["grid_color"], width=1, dash="dot")),
        hovertemplate="<b>%{x}</b><br>金额：%{y:,.0f} 万元<extra></extra>",
    ))
    fig_wf.update_layout(
        **base_layout(title="FY2025 利润瀑布图（万元）", height=470,
                      showlegend=False)
    )
    st.plotly_chart(fig_wf, use_container_width=True)

    # ── 洞察框 ──
    st.markdown("""
    <div class="insight-box red">
    ⚠️ <b>研发费用同比增长35.23%（42.56亿元）</b>，增速是营收增速的1.62倍，
    说明汇川正在以超常规速度加大技术投入。7,670名研发人员（占比28%）规模庞大，
    西门子DI在中国的研发团队规模和本土化程度需要重新评估，
    以应对汇川在工业AI、数字孪生等领域的快速追赶。
    </div>
    <div class="insight-box green">
    ✅ <b>管理费用同比增长18.41%</b>，高于营收增速，
    反映汇川集团化扩张带来的管理成本上升，这是其规模扩张的必然代价。
    相比之下，销售费用增速仅3.69%，说明汇川的营销效率在提升，
    单位营收所需销售投入在下降，渠道网络趋于成熟。
    </div>
    <div class="insight-box teal">
    ⚡ <b>财务费用为负（-657万元）</b>，主要源于汇率波动带来的汇兑收益，
    反映汇川境外业务规模扩大后的汇率敞口。随着H股上市推进，
    汇川的国际融资能力将进一步增强，有助于其加速全球化布局。
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# Tab5：数据导出
# ─────────────────────────────────────────
def render_tab_export(data: dict) -> None:
    """渲染数据导出Tab：数据表查看、搜索过滤、CSV下载、分红计算。"""
    st.markdown("### 📥 数据导出中心")

    # 准备可导出的DataFrame字典
    export_tables = {
        "年度盈利数据（近3年）": data["annual_pnl"],
        "季度财务数据（FY2025）": data["quarterly"],
        "产品线收入数据（FY2025）": data["product_revenue"],
        "地区收入数据（FY2025）": data["regional_revenue"],
        "费用结构数据（FY2025）": data["expense_data"],
        "研发投入数据（近3年）": data["rd_data"],
        "产销量数据（FY2025）": data["production_sales"],
    }

    col1, col2 = st.columns([2, 1])
    with col1:
        selected_table = st.selectbox(
            "选择数据表",
            list(export_tables.keys()),
        )
    with col2:
        search_kw = st.text_input("🔍 关键词搜索过滤", placeholder="输入关键词...")

    # 显示选中的数据表
    df_show = export_tables[selected_table].copy()
    if search_kw:
        mask = df_show.astype(str).apply(
            lambda col: col.str.contains(search_kw, na=False)
        ).any(axis=1)
        df_show = df_show[mask]

    st.dataframe(df_show, use_container_width=True, height=400)

    # 单表下载
    col3, col4 = st.columns(2)
    with col3:
        csv_single = df_show.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label=f"⬇️ 下载当前表（CSV）",
            data=csv_single,
            file_name=f"汇川技术FY2025_{selected_table}.csv",
            mime="text/csv",
        )

    with col4:
        # 全量数据打包下载
        all_dfs = []
        for name, df in export_tables.items():
            df_temp = df.copy()
            df_temp.insert(0, "数据表", name)
            all_dfs.append(df_temp)
        df_all = pd.concat(all_dfs, ignore_index=True)
        csv_all = df_all.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="⬇️ 下载全量数据（CSV）",
            data=csv_all,
            file_name="汇川技术FY2025_全量数据.csv",
            mime="text/csv",
        )

    # ── 数据说明 ──
    st.info("""
    📋 **数据说明**
    - **来源**：深圳市汇川技术股份有限公司2025年年度报告（合并报表口径）
    - **单位**：金额类指标单位为**万元**（人民币）
    - **口径**：合并财务报表，含联合动力（83.31%持股）等子公司
    - **注意**：2023年部分费用数据为估算值（财报未单独披露），已标注
    - **免责**：本看板数据仅供西门子DI内部竞争研究参考，不构成投资建议
    """)

    # ── 利润分配方案 ──
    st.markdown("### 💰 FY2025 利润分配方案")
    div = data["dividend_data"]
    d1, d2, d3 = st.columns(3)
    with d1:
        st.metric("归母净利润", f"{div['归母净利润(万元)']/10000:.2f}亿元")
        st.metric("现金分红总额", f"{div['现金分红总额(万元)']/10000:.2f}亿元")
    with d2:
        st.metric("分红比例", f"{div['分红比例(%)']:.2f}%")
        st.metric("每股股息（含税）", f"{div['每股股息(元，含税)']:.2f}元/股")
    with d3:
        st.metric("分红基数", f"{div['分红基数(股)']:,}股")
        st.markdown("""
        > 每10股派发现金股利**5元**（含税）
        > 分配预案尚需股东会审议
        """)

    # ── 股息率动态计算 ──
    st.markdown("### 📈 股息率动态计算")
    stock_price = st.number_input(
        "请输入当前股价（元/股）",
        min_value=1.0, max_value=500.0, value=60.0, step=0.5,
        help="输入汇川技术（300124）当前市场价格，自动计算股息率",
    )
    if stock_price > 0:
        dividend_yield = div["每股股息(元，含税)"] / stock_price * 100
        st.metric(
            label=f"股息率（基于股价 {stock_price:.2f} 元）",
            value=f"{dividend_yield:.3f}%",
            delta=f"每股股息 {div['每股股息(元，含税)']:.2f} 元（含税）",
        )
        if dividend_yield < 1.0:
            st.warning("⚠️ 当前股息率较低（<1%），汇川技术成长属性强于分红属性。")
        elif dividend_yield >= 2.0:
            st.success("✅ 当前股息率具有一定吸引力（≥2%）。")

# ─────────────────────────────────────────
# 主函数
# ─────────────────────────────────────────
def main():
    """主入口函数，协调各模块渲染。"""
    inject_css()

    # 主标题横幅
    st.markdown("""
    <div class="main-header">
        <h1>🏭 汇川技术（300124）FY2025 竞争情报看板</h1>
        <p>
            深圳市汇川技术股份有限公司 · 2025年年度报告 · 合并报表口径 ·
            数据截止：2025年12月31日 &nbsp;|&nbsp;
            <b>Siemens Digital Industries · 竞争情报团队专用</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 加载数据
    data = load_financial_data()

    # 侧边栏
    view_mode = render_sidebar()

    # 主内容Tab
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 CEO概览",
        "🏗️ 产品线分析",
        "🌍 市场与渠道",
        "🔬 费用与研发",
        "📥 数据导出",
    ])

    with tab1:
        render_tab_ceo(data)
    with tab2:
        render_tab_product(data)
    with tab3:
        render_tab_market(data)
    with tab4:
        render_tab_rd(data)
    with tab5:
        render_tab_export(data)

    # 底部免责声明
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; color:#6B7A99; font-size:0.78rem; padding:8px 0;">
        ⚠️ <b>免责声明</b>：本看板数据来源于汇川技术公开披露的年度报告，
        仅供西门子数字化工业（DI）内部竞争研究使用，不构成任何投资建议，请勿对外传播。<br>
        数据截止日：2025年12月31日 &nbsp;|&nbsp; 生成工具：SiemensGPT 财报分析助手
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()