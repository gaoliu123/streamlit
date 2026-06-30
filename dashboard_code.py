dashboard_code = '''# =============================================================================
# 深圳市汇川技术股份有限公司 2025年度财报竞争情报看板
# 公司名称：深圳市汇川技术股份有限公司
# 股票代码：300124.SZ（深交所创业板）
# 报告期：2025年度（2025年1月1日 - 2025年12月31日）
# 数据来源：汇川技术2025年年度报告（合并报表口径）
# 生成时间：2025年
# 使用方：西门子数字化工业（Siemens DI）竞争情报团队
# 免责声明：本看板仅供西门子内部竞争研究使用，数据来源于公开年度报告，
#           不构成任何投资建议，请勿对外传播。
# =============================================================================
# 运行说明：
#   pip install streamlit plotly pandas numpy
#   streamlit run dashboard.py
# =============================================================================

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import io

# ─────────────────────────────────────────
# 全局配色方案（禁止在代码其他位置硬编码色值）
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
    # 产品线专属色
    "auto":       "#1B3A8C",
    "nev":        "#2BBFBF",
    "emerging":   "#5B8DEF",
    "other":      "#8FA8C8",
}

PLOTLY_TEMPLATE = "plotly_white"

st.set_page_config(
    page_title="汇川技术 FY2025 竞争情报看板 | Siemens DI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# CSS 注入
# ─────────────────────────────────────────
def inject_css() -&gt; None:
    """注入全局CSS样式，统一看板视觉风格。"""
    st.markdown("""
    &lt;style&gt;
    /* ① 全局背景 */
    .stApp {
        background-color: #F5F7FA;
        color: #1A2B4A;
        font-family: \'Segoe UI\', \'PingFang SC\', \'Microsoft YaHei\', sans-serif;
    }

    /* ② 主标题横幅 */
    .main-header {
        background: linear-gradient(135deg, #1B3A8C 0%, #2B5299 60%, #1B3A8C 100%);
        border-left: 6px solid #2BBFBF;
        border-radius: 14px;
        box-shadow: 0 4px 20px rgba(27,58,140,0.18);
        padding: 22px 30px 18px 30px;
        margin-bottom: 20px;
    }
    .main-header h1 {
        color: #FFFFFF !important;
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
        padding: 14px 16px;
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
    [data-baseweb="tab-list"] {
        background: #FFFFFF;
        border-radius: 10px;
        border: 1px solid #E0E8F5;
        padding: 4px;
        gap: 4px;
    }
    [data-baseweb="tab"] {
        color: #6B7A99;
        font-weight: 600;
        font-size: 0.88rem;
        border-radius: 8px;
        padding: 8px 16px;
    }
    [aria-selected="true"] {
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

    /* ⑧ Insight洞察框 4个变体 */
    .insight-box {
        background: #EEF3FC;
        border-left: 5px solid #1B3A8C;
        border-radius: 10px;
        padding: 13px 18px;
        font-size: 0.87rem;
        margin: 10px 0;
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
    .stDownloadButton &gt; button {
        background: #1B3A8C;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }
    .stDownloadButton &gt; button:hover {
        background: #2BBFBF;
        color: white;
    }

    /* ⑩ dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        border: 1px solid #E0E8F5;
    }

    /* 侧边栏logo区 */
    .sidebar-logo {
        background: linear-gradient(135deg, #1B3A8C, #2B5299);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        margin-bottom: 16px;
        color: white;
    }
    .sidebar-logo .company-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #FFFFFF;
    }
    .sidebar-logo .ticker {
        font-size: 0.8rem;
        color: #A8C4E8;
    }
    .sidebar-logo .dashboard-title {
        font-size: 0.75rem;
        color: #2BBFBF;
        margin-top: 4px;
    }
    &lt;/style&gt;
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# 图表统一布局配置
# ─────────────────────────────────────────
def base_layout(**kwargs) -&gt; dict:
    """返回Plotly图表统一布局配置字典，确保视觉风格一致。"""
    layout = dict(
        template=PLOTLY_TEMPLATE,
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
def kpi_card(col, label: str, value: str, delta: str, delta_val: str, note: str = "") -&gt; None:
    """渲染单个KPI指标卡片。
    
    Args:
        col: Streamlit列对象
        label: 指标名称
        value: 主要数值（字符串）
        delta: delta标签文字
        delta_val: delta数值（正数为正向，负数为负向）
        note: 底部补充说明
    """
    with col:
        st.metric(label=label, value=value, delta=f"{delta}: {delta_val}")
        if note:
            st.caption(note)

# ─────────────────────────────────────────
# 数据层：集中定义所有DataFrame
# ─────────────────────────────────────────
def load_financial_data() -&gt; dict:
    """加载并计算所有财务数据，返回统一data字典供各Tab调用。
    
    数据来源：汇川技术2025年年度报告（合并报表口径）
    单位：万元（人民币）
    """

    # ── 1. 年度盈利指标（近3年）──
    annual = pd.DataFrame({
        "年份":         [2023, 2024, 2025],
        "营业收入":     [304199.25, 370409.52, 451048.44],
        "归母净利润":   [47418.63,  42854.93,  50500.02],
        "扣非净利润":   [40711.77,  40358.32,  49505.05],
        "研发费用":     [26241.48,  31470.81,  42557.74],
        "销售费用":     [None,      14808.78,  15355.69],
        "管理费用":     [None,      15413.53,  18250.83],
        "经营现金流":   [33699.16,  72004.40,  66810.25],
    })
    # 派生指标
    annual["毛利率"]       = [None, 28.70, 28.95]   # 2023未披露
    annual["净利率"]       = annual["归母净利润"] / annual["营业收入"] * 100
    annual["研发费用率"]   = annual["研发费用"] / annual["营业收入"] * 100
    annual["销售费用率"]   = annual["销售费用"] / annual["营业收入"] * 100
    annual["管理费用率"]   = annual["管理费用"] / annual["营业收入"] * 100
    annual["现金保障倍数"] = annual["经营现金流"] / annual["归母净利润"] * 100
    annual["营收增速"]     = annual["营业收入"].pct_change() * 100
    annual["净利增速"]     = annual["归母净利润"].pct_change() * 100

    # ── 2. 分季度数据（2025年）──
    quarterly = pd.DataFrame({
        "季度":       ["Q1", "Q2", "Q3", "Q4"],
        "季度序号":   [1, 2, 3, 4],
        "营业收入":   [89779.12, 115314.46, 111532.49, 134422.38],
        "归母净利润": [13228.25,  16455.63,  12857.43,   7958.71],
        "扣非净利润": [12337.90,  14376.53,  12166.61,  10624.01],
        "经营现金流": [2625.51,   27575.16,   9105.92,  27503.66],
    })
    quarterly["净利率"]     = quarterly["归母净利润"] / quarterly["营业收入"] * 100
    quarterly["环比增长率"] = quarterly["营业收入"].pct_change() * 100

    # ── 3. 分产品线数据（2025年）──
    product = pd.DataFrame({
        "产品线":   ["工业自动化与数字化", "新能源汽车动力系统", "新兴产业", "其他"],
        "营业收入": [222454.02, 203225.82, 17950.19, 7418.41],
        "营业成本": [132865.04, 170504.18, 12760.01, 4320.15],
        "同比增速": [18.79, 26.39, 15.80, 8.47],
        "收入占比": [49.32, 45.06, 3.98, 1.64],
        "颜色":     [COLORS["auto"], COLORS["nev"], COLORS["emerging"], COLORS["other"]],
    })
    product["毛利润"] = product["营业收入"] - product["营业成本"]
    product["毛利率"] = product["毛利润"] / product["营业收入"] * 100

    # 2024年对比数据（调整后口径）
    product_2024 = pd.DataFrame({
        "产品线":   ["工业自动化与数字化", "新能源汽车动力系统", "新兴产业", "其他"],
        "营业收入": [187272.21, 160797.56, 15500.92, 6838.83],
        "营业成本": [114947.83, 134465.14, None, None],
        "毛利率":   [38.62, 16.38, None, None],
    })

    # ── 4. 分地区数据（2025年）──
    regional = pd.DataFrame({
        "地区":     ["中国内地", "境外"],
        "营业收入": [424559.52, 26488.92],
        "占比":     [94.13, 5.87],
        "同比增速": [21.30, 29.89],
        "毛利率":   [None, None],  # 未披露分地区毛利率
    })

    # ── 5. 费用数据（2025 vs 2024）──
    expense = pd.DataFrame({
        "费用类型": ["销售费用", "管理费用", "研发费用"],
        "2024年":   [14808.78, 15413.53, 31470.81],
        "2025年":   [15355.69, 18250.83, 42557.74],
        "同比增速": [3.69, 18.41, 35.23],
    })
    revenue_growth_2025 = 21.77  # 营收增速基准

    # ── 6. 研发人员学历结构（2025年末）──
    rd_edu = pd.DataFrame({
        "学历":   ["博士", "硕士", "本科", "大专及以下"],
        "人数":   [94, 3461, 3290, 777],
        "颜色":   [COLORS["primary"], COLORS["secondary"], COLORS["emerging"], COLORS["neutral"]],
    })
    rd_edu["占比"] = rd_edu["人数"] / rd_edu["人数"].sum() * 100

    # ── 7. 专利数据（截至2025年末累计）──
    patent = pd.DataFrame({
        "类别":     ["发明专利", "实用新型", "外观设计", "软件著作权"],
        "报告期获得": [142, 210, 94, 194],
        "累计获得":   [579, 1583, 553, 660],
    })

    # ── 8. 股东回报数据──
    shareholder = pd.DataFrame({
        "年份":       [2023, 2024, 2025],
        "基本EPS":    [1.78, 1.60, 1.87],
        "每股股息":   [None, 0.41, 0.50],
        "分红总额":   [None, 11043.97, 13533.18],
        "分红比例":   [None, 25.77, 26.80],
    })

    # ── 9. 产销量数据（2025年）──
    production = pd.DataFrame({
        "行业":   ["智能制造", "新能源汽车"],
        "销售量": [25971863, 5933895],
        "生产量": [25499533, 6108223],
        "库存量": [1361822, 724156],
        "销售量同比": [31.27, 28.46],
        "生产量同比": [26.96, 26.06],
    })

    # ── 10. 雷达图数据（近3年盈利质量）──
    radar = pd.DataFrame({
        "维度":   ["毛利率", "净利率", "研发费用率", "销售费用率", "现金保障倍数/10"],
        "2023年": [None, 15.59, 8.63, None, 71.07/10],
        "2024年": [28.70, 11.57, 8.50, 4.00, 168.05/10],
        "2025年": [28.95, 11.20, 9.44, 3.41, 132.30/10],
    })

    return {
        "annual":            annual,
        "quarterly":         quarterly,
        "product":           product,
        "product_2024":      product_2024,
        "regional":          regional,
        "expense":           expense,
        "rd_edu":            rd_edu,
        "patent":            patent,
        "shareholder":       shareholder,
        "production":        production,
        "radar":             radar,
        "revenue_growth":    revenue_growth_2025,
    }

# ─────────────────────────────────────────
# Tab1：CEO概览圈
# ─────────────────────────────────────────
def render_tab_ceo(data: dict) -&gt; None:
    """渲染CEO概览Tab：KPI卡片、三年趋势、雷达图、季度节奏。"""
    annual = data["annual"]
    quarterly = data["quarterly"]
    radar = data["radar"]

    row2025 = annual[annual["年份"] == 2025].iloc[0]
    row2024 = annual[annual["年份"] == 2024].iloc[0]

    # ── 第一行：6个KPI卡片 ──
    st.markdown("### 📌 核心经营指标（2025年度）")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    kpi_card(c1, "营业总收入", "451.05亿元", "同比", "+21.77%", "合并报表口径")
    kpi_card(c2, "归母净利润", "50.50亿元", "同比", "+17.84%", "扣非49.51亿")
    kpi_card(c3, "扣非净利润", "49.51亿元", "同比", "+22.66%", "高质量利润")
    kpi_card(c4, "研发投入", "42.56亿元", "费用率", "9.44%", "同比+35.23%")
    kpi_card(c5, "基本EPS", "1.87元/股", "同比", "+16.88%", "稀释EPS 1.85")
    kpi_card(c6, "现金分红比例", "26.80%", "每股", "0.50元(含税)", "总额13.53亿")

    st.markdown("---")

    # ── 第二行：4个资产健康度卡片 ──
    st.markdown("### 🏦 财务健康度速览")
    a1, a2, a3, a4 = st.columns(4)
    kpi_card(a1, "经营现金净流量", "66.81亿元", "现金保障倍数", "132.30%✅", "优秀(&gt;100%)")
    kpi_card(a2, "利润弹性系数", "0.82", "净利增速/营收增速", "正常区间", "17.84%÷21.77%")
    kpi_card(a3, "境外收入占比", "5.87%", "境外增速", "+29.89%", "国际化加速中")
    kpi_card(a4, "研发人员", "7,670人", "占总员工", "28.10%", "同比+38.50%")

    st.markdown("---")

    # ── 第三行：三年趋势双轴图 + 雷达图 ──
    st.markdown("### 📈 三年财务趋势与盈利质量")
    col_trend, col_radar = st.columns([3, 2])

    with col_trend:
        fig_trend = make_subplots(specs=[[{"secondary_y": True}]])

        # 柱状：营业收入
        fig_trend.add_trace(
            go.Bar(
                x=annual["年份"].astype(str),
                y=annual["营业收入"],
                name="营业收入",
                marker_color=COLORS["primary"],
                opacity=0.82,
                text=[f"{v/10000:.1f}亿" for v in annual["营业收入"]],
                textposition="outside",
                textfont=dict(color=COLORS["primary"], size=11),
                hovertemplate="&lt;b&gt;%{x}年&lt;/b&gt;&lt;br&gt;营业收入：%{y:,.0f} 万元&lt;extra&gt;&lt;/extra&gt;",
            ),
            secondary_y=False,
        )

        # 折线：归母净利润
        fig_trend.add_trace(
            go.Scatter(
                x=annual["年份"].astype(str),
                y=annual["归母净利润"],
                name="归母净利润",
                mode="lines+markers+text",
                line=dict(color=COLORS["secondary"], width=3),
                marker=dict(symbol="diamond", size=10, color=COLORS["secondary"],
                            line=dict(color="white", width=2)),
                text=[f"{v/10000:.1f}亿" for v in annual["归母净利润"]],
                textposition="top center",
                textfont=dict(color=COLORS["secondary"], size=10),
                hovertemplate="&lt;b&gt;%{x}年&lt;/b&gt;&lt;br&gt;归母净利润：%{y:,.0f} 万元&lt;extra&gt;&lt;/extra&gt;",
            ),
            secondary_y=False,
        )

        # 右轴折线：净利率
        fig_trend.add_trace(
            go.Scatter(
                x=annual["年份"].astype(str),
                y=annual["净利率"],
                name="净利率",
                mode="lines+markers",
                line=dict(color=COLORS["success"], width=2, dash="dot"),
                marker=dict(size=8, color=COLORS["success"]),
                hovertemplate="&lt;b&gt;%{x}年&lt;/b&gt;&lt;br&gt;净利率：%{y:.2f}%&lt;extra&gt;&lt;/extra&gt;",
            ),
            secondary_y=True,
        )

        fig_trend.update_layout(
            **base_layout(
                height=420,
                title_text="营业收入 / 归母净利润 / 净利率（三年趋势）",
                legend=dict(
                    orientation="h", y=-0.18, x=0.5, xanchor="center",
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="#E0E8F5", borderwidth=1,
                ),
            )
        )
        fig_trend.update_yaxes(
            title_text="金额（万元）",
            gridcolor=COLORS["grid_color"], linecolor="#D0DAF0",
            secondary_y=False,
        )
        fig_trend.update_yaxes(
            title_text="净利率（%）",
            gridcolor=COLORS["grid_color"], linecolor="#D0DAF0",
            secondary_y=True,
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_radar:
        # 雷达图：盈利质量（三年叠加）
        categories = ["毛利率", "净利率", "研发费用率", "销售费用率", "现金保障/10"]

        fig_radar = go.Figure()
        radar_data = {
            "2023年": [None, 15.59, 8.63, None, 71.07/10],
            "2024年": [28.70, 11.57, 8.50, 4.00, 168.05/10],
            "2025年": [28.95, 11.20, 9.44, 3.41, 132.30/10],
        }
        colors_radar = {
            "2023年": COLORS["neutral"],
            "2024年": COLORS["secondary"],
            "2025年": COLORS["primary"],
        }

        for yr, vals in radar_data.items():
            # 替换None为0用于显示
            vals_clean = [v if v is not None else 0 for v in vals]
            fig_radar.add_trace(go.Scatterpolar(
                r=vals_clean + [vals_clean[0]],
                theta=categories + [categories[0]],
                fill="toself",
                name=yr,
                line=dict(color=colors_radar[yr], width=2),
                fillcolor=colors_radar[yr],
                opacity=0.25 if yr != "2025年" else 0.35,
                hovertemplate="&lt;b&gt;" + yr + "&lt;/b&gt;&lt;br&gt;%{theta}：%{r:.2f}&lt;extra&gt;&lt;/extra&gt;",
            ))

        fig_radar.update_layout(
            **base_layout(
                height=420,
                title_text="盈利质量雷达图（三年对比）",
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 30],
                                    gridcolor=COLORS["grid_color"]),
                    angularaxis=dict(gridcolor=COLORS["grid_color"]),
                    bgcolor=COLORS["plot_bg"],
                ),
                legend=dict(
                    orientation="h", y=-0.12, x=0.5, xanchor="center",
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="#E0E8F5", borderwidth=1,
                ),
            )
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # ── 第四行：季度营收节奏 ──
    st.markdown("### 📅 2025年分季度经营节奏")
    fig_qtr = make_subplots(
        rows=1, cols=2,
        subplot_titles=("季度营业收入（万元）", "季度净利率（%）"),
    )

    bar_colors = [COLORS["neutral"], COLORS["primary"], COLORS["primary"], COLORS["secondary"]]
    fig_qtr.add_trace(
        go.Bar(
            x=quarterly["季度"], y=quarterly["营业收入"],
            marker_color=bar_colors,
            text=[f"{v/10000:.1f}亿" for v in quarterly["营业收入"]],
            textposition="outside",
            textfont=dict(color=COLORS["text_dark"], size=10),
            hovertemplate="&lt;b&gt;%{x}&lt;/b&gt;&lt;br&gt;营业收入：%{y:,.0f} 万元&lt;extra&gt;&lt;/extra&gt;",
            name="营业收入",
        ),
        row=1, col=1,
    )

    fig_qtr.add_trace(
        go.Scatter(
            x=quarterly["季度"], y=quarterly["净利率"],
            mode="lines+markers+text",
            line=dict(color=COLORS["secondary"], width=3),
            marker=dict(size=11, color=COLORS["secondary"],
                        line=dict(color="white", width=2)),
            text=[f"{v:.1f}%" for v in quarterly["净利率"]],
            textposition="top center",
            textfont=dict(color=COLORS["primary"], size=11),
            hovertemplate="&lt;b&gt;%{x}&lt;/b&gt;&lt;br&gt;净利率：%{y:.2f}%&lt;extra&gt;&lt;/extra&gt;",
            name="净利率",
        ),
        row=1, col=2,
    )

    fig_qtr.update_layout(
        **base_layout(height=400, showlegend=False, margin=dict(t=55, b=30))
    )
    fig_qtr.update_xaxes(gridcolor=COLORS["grid_color"], linecolor="#D0DAF0")
    fig_qtr.update_yaxes(gridcolor=COLORS["grid_color"], linecolor="#D0DAF0")
    st.plotly_chart(fig_qtr, use_container_width=True)

    # ── 洞察框 ──
    st.markdown("""
    &lt;div class="insight-box green"&gt;
    🚀 &lt;b&gt;增长引擎确认：&lt;/b&gt;2025年营收451亿元同比+21.77%，归母净利润50.5亿元同比+17.84%（数据事实）。
    双轮驱动格局清晰：工业自动化+19%、新能源汽车+26%，说明汇川已成功构建跨周期增长飞轮（业务含义）。
    西门子DI需警惕：汇川在中国工控市场的规模效应正在形成，其伺服31%市占率已远超西门子在华份额，
    价格竞争将持续向高端市场延伸（DI视角）。
    &lt;/div&gt;
    &lt;div class="insight-box red"&gt;
    ⚠️ &lt;b&gt;Q4净利率骤降警示：&lt;/b&gt;Q4净利率仅5.92%，较Q2峰值14.27%下降超8个百分点（数据事实），
    反映年末新能源汽车业务价格压力和费用集中确认的双重冲击（业务含义）。
    西门子DI可关注：汇川新能源汽车业务盈利能力承压，可能倒逼其在工业自动化领域加大价格竞争以补偿利润（DI视角）。
    &lt;/div&gt;
    &lt;div class="insight-box teal"&gt;
    💡 &lt;b&gt;研发投入加速：&lt;/b&gt;研发费用42.56亿元同比+35.23%，研发费用率升至9.44%（数据事实），
    研发人员7,670人同比+38.50%，说明汇川正在全面加速技术储备（业务含义）。
    西门子DI需重点追踪其工业AI平台（iFG）、自主工业网络协议等项目的商业化进展（DI视角）。
    &lt;/div&gt;
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# Tab2：产品线分析
# ─────────────────────────────────────────
def render_tab_product(data: dict) -&gt; None:
    """渲染产品线分析Tab：收入结构、毛利率、增速、产销量。"""
    product = data["product"]
    production = data["production"]

    st.markdown("### 🏭 产品线收入结构（2025年）")
    col_pie, col_bar = st.columns([1, 2])

    with col_pie:
        # 环形饼图
        fig_pie = go.Figure(go.Pie(
            labels=product["产品线"],
            values=product["营业收入"],
            hole=0.52,
            marker=dict(colors=product["颜色"].tolist()),
            textinfo="label+percent",
            textfont=dict(size=11),
            hovertemplate="&lt;b&gt;%{label}&lt;/b&gt;&lt;br&gt;收入：%{value:,.0f} 万元&lt;br&gt;占比：%{percent}&lt;extra&gt;&lt;/extra&gt;",
        ))
        total_rev = product["营业收入"].sum()
        fig_pie.add_annotation(
            text=f"&lt;b&gt;{total_rev/10000:.1f}亿&lt;/b&gt;&lt;br&gt;&lt;span style=\'font-size:11px\'&gt;总收入&lt;/span&gt;",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color=COLORS["primary"]),
            align="center",
        )
        fig_pie.update_layout(
            **base_layout(
                height=340,
                title_text="产品线收入占比",
                showlegend=False,
            )
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_bar:
        # 双轴图：收入柱状 + 毛利率折线
        fig_dual = make_subplots(specs=[[{"secondary_y": True}]])

        fig_dual.add_trace(
            go.Bar(
                x=product["产品线"],
                y=product["营业收入"],
                name="营业收入",
                marker_color=product["颜色"].tolist(),
                opacity=0.85,
                text=[f"{v/10000:.1f}亿" for v in product["营业收入"]],
                textposition="outside",
                hovertemplate="&lt;b&gt;%{x}&lt;/b&gt;&lt;br&gt;营业收入：%{y:,.0f} 万元&lt;extra&gt;&lt;/extra&gt;",
            ),
            secondary_y=False,
        )

        fig_dual.add_trace(
            go.Scatter(
                x=product["产品线"],
                y=product["毛利率"],
                name="毛利率",
                mode="lines+markers",
                line=dict(color=COLORS["danger"], width=2),
                marker=dict(symbol="star", size=13, color=COLORS["danger"],
                            line=dict(color="white", width=1)),
                text=[f"{v:.1f}%" for v in product["毛利率"]],
                textposition="top center",
                hovertemplate="&lt;b&gt;%{x}&lt;/b&gt;&lt;br&gt;毛利率：%{y:.2f}%&lt;extra&gt;&lt;/extra&gt;",
            ),
            secondary_y=True,
        )

        fig_dual.update_layout(
            **base_layout(
                height=340,
                title_text="产品线收入与毛利率",
                legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                            bgcolor="rgba(255,255,255,0.8)",
                            bordercolor="#E0E8F5", borderwidth=1),
            )
        )
        fig_dual.update_yaxes(title_text="收入（万元）", secondary_y=False,
                               gridcolor=COLORS["grid_color"])
        fig_dual.update_yaxes(title_text="毛利率（%）", secondary_y=True,
                               gridcolor=COLORS["grid_color"])
        st.plotly_chart(fig_dual, use_container_width=True)

    # ── 产品线同比增长率 ──
    st.markdown("### 📊 产品线同比增速排名")
    product_sorted = product.sort_values("同比增速", ascending=True)
    bar_colors_growth = [
        COLORS["success"] if v &gt;= 0 else COLORS["danger"]
        for v in product_sorted["同比增速"]
    ]
    overall_growth = 21.77

    fig_growth = go.Figure()
    fig_growth.add_trace(go.Bar(
        x=product_sorted["同比增速"],
        y=product_sorted["产品线"],
        orientation="h",
        marker_color=bar_colors_growth,
        text=[f"{v:+.2f}%" for v in product_sorted["同比增速"]],
        textposition="outside",
        hovertemplate="&lt;b&gt;%{y}&lt;/b&gt;&lt;br&gt;同比增速：%{x:+.2f}%&lt;extra&gt;&lt;/extra&gt;",
    ))
    fig_growth.add_vline(x=0, line_dash="dash", line_color=COLORS["text_muted"], line_width=1)
    fig_growth.add_vline(
        x=overall_growth, line_dash="dot",
        line_color=COLORS["primary"], line_width=2,
        annotation_text=f"整体增速 {overall_growth:+.2f}%",
        annotation_position="top right",
        annotation_font=dict(color=COLORS["primary"], size=11),
    )
    fig_growth.update_layout(
        **base_layout(
            height=370,
            title_text="产品线同比增速（%）",
            showlegend=False,
        )
    )
    st.plotly_chart(fig_growth, use_container_width=True)

    # ── 产销量对比 ──
    st.markdown("### 📦 主要业务产销量（2025年）")
    fig_prod = go.Figure()
    x_labels = production["行业"]
    for col_name, color, label in [
        ("生产量", COLORS["primary"], "生产量"),
        ("销售量", COLORS["secondary"], "销售量"),
        ("库存量", COLORS["neutral"], "库存量"),
    ]:
        fig_prod.add_trace(go.Bar(
            name=label,
            x=x_labels,
            y=production[col_name],
            marker_color=color,
            text=[f"{v:,.0f}" for v in production[col_name]],
            textposition="outside",
            hovertemplate=f"&lt;b&gt;%{{x}}&lt;/b&gt;&lt;br&gt;{label}：%{{y:,.0f}} PCS&lt;extra&gt;&lt;/extra&gt;",
        ))

    fig_prod.update_layout(
        **base_layout(
            height=400,
            title_text="产销量对比（PCS）",
            barmode="group",
            legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                        bgcolor="rgba(255,255,255,0.8)",
                        bordercolor="#E0E8F5", borderwidth=1),
        )
    )
    st.plotly_chart(fig_prod, use_container_width=True)

    # ── 洞察框 ──
    st.markdown("""
    &lt;div class="insight-box red"&gt;
    ⚡ &lt;b&gt;新能源汽车毛利率严重承压：&lt;/b&gt;新能源汽车动力系统毛利率仅16.10%，远低于工业自动化40.27%（数据事实），
    说明汇川在新能源赛道面临主机厂强势压价和同业激烈竞争（业务含义）。
    西门子DI需关注：汇川可能将新能源业务的规模优势反哺工控产品定价，形成交叉补贴式价格竞争（DI视角）。
    &lt;/div&gt;
    &lt;div class="insight-box green"&gt;
    🏆 &lt;b&gt;工业自动化高毛利护城河：&lt;/b&gt;工业自动化与数字化毛利率40.27%，同比增速+18.79%（数据事实），
    说明汇川在工控核心产品上已建立强定价权，高端化转型初见成效（业务含义）。
    西门子DI需重点防守：机床、半导体、汽车装备等高端离散制造场景，这是汇川2026年重点攻坚方向（DI视角）。
    &lt;/div&gt;
    &lt;div class="insight-box teal"&gt;
    🤖 &lt;b&gt;新兴产业快速起量：&lt;/b&gt;新兴产业（智能机器人+数字能源）收入17.95亿元，同比+15.80%（数据事实），
    SCARA机器人中国市占率约28%排名第一，说明汇川在机器人赛道已形成规模壁垒（业务含义）。
    西门子DI需警惕：汇川"控制+驱动+机器人"一体化解决方案正在侵蚀西门子在智能装备领域的系统集成优势（DI视角）。
    &lt;/div&gt;
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# Tab3：市场与渠道
# ─────────────────────────────────────────
def render_tab_market(data: dict) -&gt; None:
    """渲染市场与渠道Tab：地区分布、渠道结构、国际化分析。"""
    regional = data["regional"]

    st.markdown("### 🌍 地区市场分布（2025年）")

    # 地区收入水平柱状图
    fig_region = go.Figure()
    fig_region.add_trace(go.Bar(
        x=regional["营业收入"],
        y=regional["地区"],
        orientation="h",
        marker_color=[COLORS["primary"], COLORS["secondary"]],
        text=[f"{v/10000:.1f}亿" for v in regional["营业收入"]],
        textposition="outside",
        hovertemplate="&lt;b&gt;%{y}&lt;/b&gt;&lt;br&gt;营业收入：%{x:,.0f} 万元&lt;extra&gt;&lt;/extra&gt;",
        name="营业收入",
    ))
    fig_region.update_layout(
        **base_layout(
            height=340,
            title_text="分地区营业收入（万元）",
            showlegend=False,
        )
    )
    st.plotly_chart(fig_region, use_container_width=True)

    # 地区增速
    st.markdown("### 📈 地区增速对比")
    overall_growth = data["revenue_growth"]
    growth_colors = [
        COLORS["success"] if v &gt;= overall_growth else COLORS["primary"]
        for v in regional["同比增速"]
    ]
    fig_reg_growth = go.Figure(go.Bar(
        x=regional["同比增速"],
        y=regional["地区"],
        orientation="h",
        marker_color=growth_colors,
        text=[f"{v:+.2f}%" for v in regional["同比增速"]],
        textposition="outside",
        hovertemplate="&lt;b&gt;%{y}&lt;/b&gt;&lt;br&gt;同比增速：%{x:+.2f}%&lt;extra&gt;&lt;/extra&gt;",
    ))
    fig_reg_growth.add_vline(
        x=overall_growth, line_dash="dot",
        line_color=COLORS["primary"], line_width=2,
        annotation_text=f"整体增速 {overall_growth:.2f}%",
        annotation_position="top right",
        annotation_font=dict(color=COLORS["primary"], size=11),
    )
    fig_reg_growth.update_layout(
        **base_layout(height=340, title_text="分地区同比增速（%）", showlegend=False)
    )
    st.plotly_chart(fig_reg_growth, use_container_width=True)

    # ── 三个环形饼图 ──
    st.markdown("### 🔄 市场结构分析")
    c1, c2, c3 = st.columns(3)

    with c1:
        # 境内 vs 境外
        fig_geo = go.Figure(go.Pie(
            labels=["中国内地", "境外"],
            values=[424559.52, 26488.92],
            hole=0.52,
            marker=dict(colors=[COLORS["primary"], COLORS["secondary"]]),
            textinfo="label+percent",
            hovertemplate="&lt;b&gt;%{label}&lt;/b&gt;&lt;br&gt;收入：%{value:,.0f} 万元&lt;extra&gt;&lt;/extra&gt;",
        ))
        fig_geo.add_annotation(
            text="&lt;b&gt;地理&lt;/b&gt;&lt;br&gt;分布",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=12, color=COLORS["primary"]),
        )
        fig_geo.update_layout(
            **base_layout(height=340, title_text="境内 vs 境外", showlegend=False)
        )
        st.plotly_chart(fig_geo, use_container_width=True)

    with c2:
        # 产品线结构
        product = data["product"]
        fig_prod_pie = go.Figure(go.Pie(
            labels=product["产品线"],
            values=product["营业收入"],
            hole=0.52,
            marker=dict(colors=product["颜色"].tolist()),
            textinfo="label+percent",
            hovertemplate="&lt;b&gt;%{label}&lt;/b&gt;&lt;br&gt;收入：%{value:,.0f} 万元&lt;extra&gt;&lt;/extra&gt;",
        ))
        fig_prod_pie.add_annotation(
            text="&lt;b&gt;业务&lt;/b&gt;&lt;br&gt;结构",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=12, color=COLORS["primary"]),
        )
        fig_prod_pie.update_layout(
            **base_layout(height=340, title_text="业务结构分布", showlegend=False)
        )
        st.plotly_chart(fig_prod_pie, use_container_width=True)

    with c3:
        # 境外增速 vs 境内增速对比柱状
        fig_growth_compare = go.Figure(go.Bar(
            x=["中国内地", "境外"],
            y=[21.30, 29.89],
            marker_color=[COLORS["primary"], COLORS["success"]],
            text=[f"{v:.2f}%" for v in [21.30, 29.89]],
            textposition="outside",
            hovertemplate="&lt;b&gt;%{x}&lt;/b&gt;&lt;br&gt;同比增速：%{y:.2f}%&lt;extra&gt;&lt;/extra&gt;",
        ))
        fig_growth_compare.update_layout(
            **base_layout(height=340, title_text="境内外增速对比（%）", showlegend=False)
        )
        st.plotly_chart(fig_growth_compare, use_container_width=True)

    st.markdown("""
    &lt;div class="insight-box teal"&gt;
    🌐 &lt;b&gt;国际化加速但基数仍低：&lt;/b&gt;境外收入26.49亿元，同比增速+29.89%超越境内+21.30%（数据事实），
    说明汇川"借船出海"策略在纺织、锂电、光伏等行业取得实质进展（业务含义）。
    西门子DI需关注：汇川正在东南亚、中东等新兴市场快速建立渠道网络，
    其境外占比5.87%虽低，但增速领先将在3-5年内形成规模竞争（DI视角）。
    &lt;/div&gt;
    &lt;div class="insight-box"&gt;
    🎯 &lt;b&gt;中国市场仍是核心战场：&lt;/b&gt;境内收入424.6亿元占比94.13%，绝对规模庞大（数据事实），
    说明汇川的核心竞争力仍高度集中于中国市场，国际化处于早期阶段（业务含义）。
    西门子DI机会：在欧洲、美洲等成熟市场，汇川短期内难以形成实质威胁，
    但需提前布局东南亚市场的防御策略（DI视角）。
    &lt;/div&gt;
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# Tab4：费用与研发
# ─────────────────────────────────────────
def render_tab_rd(data: dict) -&gt; None:
    """渲染费用与研发Tab：三大费用、研发趋势、学历结构、利润瀑布图。"""
    expense = data["expense"]
    annual = data["annual"]
    rd_edu = data["rd_edu"]
    patent = data["patent"]
    revenue_growth = data["revenue_growth"]

    # ── 三大费用对比 ──
    st.markdown("### 💰 三大费用对比（2024 vs 2025）")
    col_exp, col_growth = st.columns(2)

    with col_exp:
        fig_exp = go.Figure()
        for yr, color in [("2024年", COLORS["neutral"]), ("2025年", COLORS["primary"])]:
            fig_exp.add_trace(go.Bar(
                name=yr,
                x=expense["费用类型"],
                y=expense[yr],
                marker_color=color,
                text=[f"{v/10000:.2f}亿" for v in expense[yr]],
                textposition="outside",
                hovertemplate=f"&lt;b&gt;%{{x}}&lt;/b&gt;&lt;br&gt;{yr}：%{{y:,.0f}} 万元&lt;extra&gt;&lt;/extra&gt;",
            ))
        fig_exp.update_layout(
            **base_layout(
                height=400,
                title_text="三大费用两年对比（万元）",
                barmode="group",
                legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                            bgcolor="rgba(255,255,255,0.8)",
                            bordercolor="#E0E8F5", borderwidth=1),
            )
        )
        st.plotly_chart(fig_exp, use_container_width=True)

    with col_growth:
        growth_colors = [
            COLORS["danger"] if v &gt; revenue_growth else COLORS["success"]
            for v in expense["同比增速"]
        ]
        fig_exp_growth = go.Figure(go.Bar(
            x=expense["费用类型"],
            y=expense["同比增速"],
            marker_color=growth_colors,
            text=[f"{v:+.2f}%" for v in expense["同比增速"]],
            textposition="outside",
            hovertemplate="&lt;b&gt;%{x}&lt;/b&gt;&lt;br&gt;同比增速：%{y:+.2f}%&lt;extra&gt;&lt;/extra&gt;",
        ))
        fig_exp_growth.add_hline(
            y=revenue_growth, line_dash="dot",
            line_color=COLORS["primary"], line_width=2,
            annotation_text=f"营收增速 {revenue_growth:.2f}%",
            annotation_position="top right",
            annotation_font=dict(color=COLORS["primary"], size=11),
        )
        fig_exp_growth.update_layout(
            **base_layout(
                height=400,
                title_text="费用同比增速 vs 营收增速（%）",
                showlegend=False,
            )
        )
        st.plotly_chart(fig_exp_growth, use_container_width=True)

    # ── 研发费用趋势 ──
    st.markdown("### 🔬 研发投入趋势（近3年）")
    col_rd, col_edu = st.columns([3, 2])

    with col_rd:
        fig_rd = make_subplots(specs=[[{"secondary_y": True}]])
        fig_rd.add_trace(
            go.Bar(
                x=annual["年份"].astype(str),
                y=annual["研发费用"],
                name="研发费用",
                marker_color=COLORS["primary"],
                opacity=0.82,
                text=[f"{v/10000:.2f}亿" for v in annual["研发费用"]],
                textposition="outside",
                hovertemplate="&lt;b&gt;%{x}年&lt;/b&gt;&lt;br&gt;研发费用：%{y:,.0f} 万元&lt;extra&gt;&lt;/extra&gt;",
            ),
            secondary_y=False,
        )
        fig_rd.add_trace(
            go.Scatter(
                x=annual["年份"].astype(str),
                y=annual["研发费用率"],
                name="研发费用率",
                mode="lines+markers+text",
                line=dict(color=COLORS["secondary"], width=3),
                marker=dict(symbol="diamond", size=10, color=COLORS["secondary"],
                            line=dict(color="white", width=2)),
                text=[f"{v:.2f}%" for v in annual["研发费用率"]],
                textposition="top center",
                hovertemplate="&lt;b&gt;%{x}年&lt;/b&gt;&lt;br&gt;研发费用率：%{y:.2f}%&lt;extra&gt;&lt;/extra&gt;",
            ),
            secondary_y=True,
        )
        fig_rd.update_layout(
            **base_layout(
                height=420,
                title_text="研发费用（万元）&amp; 研发费用率（%）",
                legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                            bgcolor="rgba(255,255,255,0.8)",
                            bordercolor="#E0E8F5", borderwidth=1),
            )
        )
        fig_rd.update_yaxes(title_text="研发费用（万元）", secondary_y=False,
                             gridcolor=COLORS["grid_color"])
        fig_rd.update_yaxes(title_text="研发费用率（%）", secondary_y=True,
                             gridcolor=COLORS["grid_color"])
        st.plotly_chart(fig_rd, use_container_width=True)

    with col_edu:
        # 研发人员学历结构环形饼图
        fig_edu = go.Figure(go.Pie(
            labels=rd_edu["学历"],
            values=rd_edu["人数"],
            hole=0.42,
            marker=dict(colors=rd_edu["颜色"].tolist()),
            textinfo="label+percent",
            textfont=dict(size=11),
            hovertemplate="&lt;b&gt;%{label}&lt;/b&gt;&lt;br&gt;人数：%{value:,}人&lt;br&gt;占比：%{percent}&lt;extra&gt;&lt;/extra&gt;",
        ))
        fig_edu.add_annotation(
            text="&lt;b&gt;7,670&lt;/b&gt;&lt;br&gt;研发人员",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=13, color=COLORS["primary"]),
        )
        fig_edu.update_layout(
            **base_layout(
                height=420,
                title_text="研发人员学历结构（2025年末）",
                showlegend=False,
            )
        )
        st.plotly_chart(fig_edu, use_container_width=True)

    # ── 利润瀑布图 ──
    st.markdown("### 🌊 2025年利润瀑布图（万元）")

    # 从财报数据构建瀑布
    revenue_2025    = 451048.44
    cogs_2025       = 320449.39
    gross_profit    = revenue_2025 - cogs_2025   # 130599.05
    selling_exp     = -15355.69
    admin_exp       = -18250.83
    rd_exp          = -42557.74
    fin_income      = 657.19      # 财务收益（财务费用为负，即收益）
    other_income    = 2314.50     # 营业外收入等估算
    net_profit      = 50500.02

    waterfall_x = [
        "营业收入", "营业成本", "毛利润",
        "销售费用", "管理费用", "研发费用",
        "财务收益", "其他收益", "归母净利润"
    ]
    waterfall_y = [
        revenue_2025, -cogs_2025, gross_profit,
        selling_exp, admin_exp, rd_exp,
        fin_income, other_income, net_profit
    ]
    waterfall_measure = [
        "absolute", "relative", "total",
        "relative", "relative", "relative",
        "relative", "relative", "total"
    ]

    fig_wf = go.Figure(go.Waterfall(
        x=waterfall_x,
        y=waterfall_y,
        measure=waterfall_measure,
        text=[f"{v:,.0f}" for v in waterfall_y],
        textposition="outside",
        textfont=dict(size=10, color=COLORS["text_dark"]),
        increasing=dict(marker=dict(color=COLORS["success"])),
        decreasing=dict(marker=dict(color=COLORS["danger"])),
        totals=dict(marker=dict(color=COLORS["primary"])),
        connector=dict(line=dict(color=COLORS["grid_color"], width=1, dash="dot")),
        hovertemplate="&lt;b&gt;%{x}&lt;/b&gt;&lt;br&gt;金额：%{y:,.0f} 万元&lt;extra&gt;&lt;/extra&gt;",
    ))
    fig_wf.update_layout(
        **base_layout(
            height=470,
            title_text="利润瀑布图：从营业收入到归母净利润（万元）",
            showlegend=False,
        )
    )
    st.plotly_chart(fig_wf, use_container_width=True)

    # ── 专利情况 ──
    st.markdown("### 📋 专利与知识产权（截至2025年末）")
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    for col, row in zip([col_p1, col_p2, col_p3, col_p4], patent.itertuples()):
        with col:
            st.metric(
                label=row.类别,
                value=f"{row.累计获得:,}件",
                delta=f"本期新增 {row.报告期获得}件",
            )

    st.markdown("""
    &lt;div class="insight-box red"&gt;
    ⚠️ &lt;b&gt;研发费用增速远超营收：&lt;/b&gt;研发费用同比+35.23%，远超营收增速21.77%（数据事实），
    说明汇川正处于技术投入加速期，短期将压缩利润空间（业务含义）。
    西门子DI机会窗口：汇川研发产出转化需要2-3年周期，当前是西门子在高端客户中
    强化技术壁垒、锁定关键账户的关键时间窗口（DI视角）。
    &lt;/div&gt;
    &lt;div class="insight-box green"&gt;
    🔬 &lt;b&gt;研发人才大规模扩张：&lt;/b&gt;研发人员7,670人同比+38.50%，硕博占比约46.3%（数据事实），
    说明汇川正在构建高端研发能力，AI、工业软件等领域人才储备快速增长（业务含义）。
    西门子DI需关注：汇川工业AI平台iFG、自主工业网络协议等项目若商业化成功，
    将直接挑战西门子TIA Portal和PROFINET的生态壁垒（DI视角）。
    &lt;/div&gt;
    &lt;div class="insight-box teal"&gt;
    📜 &lt;b&gt;知识产权加速积累：&lt;/b&gt;累计3,375项专利及软著，2025年新增640项（数据事实），
    发明专利累计579项，说明汇川的技术原创性持续提升（业务含义）。
    西门子DI需追踪：汇川在运动控制算法、工业通信协议领域的专利布局，
    评估其对西门子核心技术的替代风险（DI视角）。
    &lt;/div&gt;
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# Tab5：数据导出
# ─────────────────────────────────────────
def render_tab_export(data: dict) -&gt; None:
    """渲染数据导出Tab：数据浏览、搜索过滤、CSV下载。"""
    st.markdown("### 📥 数据导出中心")

    # 构建可导出的数据表字典
    export_tables = {
        "年度盈利指标（近3年）":   data["annual"][["年份","营业收入","归母净利润","扣非净利润","研发费用","经营现金流","毛利率","净利率","研发费用率","营收增速","净利增速"]],
        "分季度数据（2025年）":    data["quarterly"],
        "分产品线数据（2025年）":  data["product"][["产品线","营业收入","营业成本","毛利润","毛利率","同比增速","收入占比"]],
        "分地区数据（2025年）":    data["regional"],
        "费用明细（2024 vs 2025）": data["expense"],
        "研发人员学历结构":        data["rd_edu"][["学历","人数","占比"]],
        "专利情况":               data["patent"],
        "股东回报指标":            data["shareholder"],
        "产销量数据（2025年）":    data["production"],
    }

    selected_table = st.selectbox("📋 选择数据表", list(export_tables.keys()))
    search_kw = st.text_input("🔍 关键词搜索过滤（可选）", placeholder="输入关键词过滤行...")

    df_show = export_tables[selected_table].copy()

    if search_kw:
        mask = df_show.astype(str).apply(
            lambda col: col.str.contains(search_kw, case=False, na=False)
        ).any(axis=1)
        df_show = df_show[mask]

    st.dataframe(df_show, use_container_width=True, height=400)

    # 单表下载
    csv_single = df_show.to_csv(index=False, encoding="utf-8-sig")
    st.download_button(
        label=f"⬇️ 下载当前表格（{selected_table}）",
        data=csv_single,
        file_name=f"汇川FY25_{selected_table}.csv",
        mime="text/csv",
    )

    st.markdown("---")

    # 全量打包下载
    all_dfs = []
    for name, df in export_tables.items():
        df_temp = df.copy()
        df_temp.insert(0, "数据表", name)
        all_dfs.append(df_temp)
    df_all = pd.concat(all_dfs, ignore_index=True)
    csv_all = df_all.to_csv(index=False, encoding="utf-8-sig")
    st.download_button(
        label="📦 下载全量数据包（所有表格合并）",
        data=csv_all,
        file_name="汇川FY25_全量数据包.csv",
        mime="text/csv",
    )

    # ── 利润分配方案 ──
    st.markdown("### 💵 2025年度利润分配方案")
    d1, d2, d3 = st.columns(3)
    with d1:
        st.metric("每10股现金股利（含税）", "5.00元", delta="2024年为4.10元")
    with d2:
        st.metric("现金分红总额（含税）", "13.53亿元", delta="+22.56% vs 2024")
    with d3:
        st.metric("分红比例", "26.80%", delta="2024年为25.77%")

    # ── 股息率动态计算 ──
    st.markdown("### 📈 股息率动态计算")
    current_price = st.number_input(
        "请输入当前股价（元/股）",
        min_value=1.0, max_value=500.0, value=50.0, step=0.5,
        help="输入汇川技术（300124.SZ）当前市场价格，自动计算股息率"
    )
    dividend_per_share = 0.50  # 元/股（含税）
    dividend_yield = dividend_per_share / current_price * 100
    st.metric(
        label=f"预估股息率（股价 {current_price:.2f} 元）",
        value=f"{dividend_yield:.2f}%",
        delta=f"每股股息 {dividend_per_share:.2f} 元（含税）",
    )

    # ── 数据说明 ──
    st.info("""
    📌 **数据说明**
    - **数据来源**：深圳市汇川技术股份有限公司2025年年度报告（公开披露）
    - **报表口径**：合并报表（人民币）
    - **数据单位**：万元（人民币），EPS/股息单位为元/股
    - **免责声明**：本看板仅供西门子数字化工业（Siemens DI）内部竞争研究使用，
      数据来源于公开年度报告，不构成任何投资建议，请勿对外传播。
    - **数据截止日期**：2025年12月31日
    - **生成工具**：Siemens DI 竞争情报分析系统
    """)

# ─────────────────────────────────────────
# 侧边栏
# ─────────────────────────────────────────
def render_sidebar() -&gt; str:
    """渲染侧边栏，返回用户选择的分析视角。"""
    with st.sidebar:
        # Logo区
        st.markdown("""
        &lt;div class="sidebar-logo"&gt;
            &lt;div class="company-name"&gt;🏭 汇川技术&lt;/div&gt;
            &lt;div class="ticker"&gt;300124.SZ · 深交所创业板&lt;/div&gt;
            &lt;div class="dashboard-title"&gt;Siemens DI 竞争情报看板&lt;/div&gt;
        &lt;/div&gt;
        """, unsafe_allow_html=True)

        # 公司概况
        st.markdown("#### 📋 公司概况")
        st.markdown("""
        | 项目 | 内容 |
        |------|------|
        | **全称** | 深圳市汇川技术股份有限公司 |
        | **主营** | 工业自动化、新能源汽车动力系统 |
        | **核心产品** | 变频器、伺服、PLC/HMI、电驱 |
        | **总部** | 深圳市 |
        | **上市时间** | 2010年9月 |
        """)

        # 核心数据速览
        st.markdown("#### 📊 核心数据速览（FY2025）")
        st.markdown("""
        | 指标 | 数值 |
        |------|------|
        | 营业收入 | **451.05亿元** |
        | 归母净利润 | **50.50亿元** |
        | 毛利率 | **28.95%** |
        | 研发费用率 | **9.44%** |
        | 营收增速 | **+21.77%** |
        | 净利增速 | **+17.84%** |
        | 研发人员 | **7,670人** |
        """)

        # 分析视角
        st.markdown("#### 🎯 分析视角")
        view_mode = st.radio(
            "选择分析模式",
            ["全面分析", "增长聚焦", "盈利聚焦"],
            index=0,
        )

        st.markdown("---")
        st.caption("📅 数据截止：2025年12月31日")
        st.caption("📄 数据来源：汇川技术2025年年度报告")
        st.caption("🔒 仅供Siemens DI内部使用")

    return view_mode

# ─────────────────────────────────────────
# 主函数
# ─────────────────────────────────────────
def main():
    """主函数：初始化看板，协调各模块渲染。"""
    inject_css()

    # 侧边栏
    view_mode = render_sidebar()

    # 主标题横幅
    st.markdown("""
    &lt;div class="main-header"&gt;
        &lt;h1&gt;📊 汇川技术 FY2025 竞争情报分析看板&lt;/h1&gt;
        &lt;p&gt;深圳市汇川技术股份有限公司 · 300124.SZ · 2025年度报告 · Siemens Digital Industries 竞争情报团队&lt;/p&gt;
    &lt;/div&gt;
    """, unsafe_allow_html=True)

    # 加载数据
    data = load_financial_data()

    # Tab导航
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 CEO概览圈",
        "🏭 产品线分析",
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
    st.markdown(
        "&lt;p style=\'text-align:center;color:#6B7A99;font-size:0.78rem;\'&gt;"
        "⚠️ 本看板仅供西门子数字化工业（Siemens DI）内部竞争研究使用 · "
        "数据来源于公开年度报告 · 不构成任何投资建议 · 请勿对外传播"
        "&lt;/p&gt;",
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
'''

# 写出文件
output_path = '/tmp/汇川FY25_竞争情报看板.py'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(dashboard_code)

print(f"✅ 文件已生成：{output_path}")
print(f"📦 文件大小：{len(dashboard_code):,} 字符")
print(f"📝 代码行数：{dashboard_code.count(chr(10)):,} 行")