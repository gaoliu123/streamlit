# =============================================================================
# 深圳市汇川技术股份有限公司 2025年度财报竞争情报看板
# 股票代码：300124.SZ（深交所创业板）
# 使用方：西门子数字化工业（Siemens DI）竞争情报团队
# 运行：streamlit run app.py
# =============================================================================

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# ─────────────────────────────────────────
# 全局配色
# ─────────────────────────────────────────
C = {
    "primary":    "#1B3A8C",
    "secondary":  "#2BBFBF",
    "success":    "#27AE60",
    "danger":     "#E74C3C",
    "neutral":    "#8FA8C8",
    "emerging":   "#5B8DEF",
    "card_bg":    "#FFFFFF",
    "plot_bg":    "#FFFFFF",
    "text_dark":  "#1A2B4A",
    "text_muted": "#6B7A99",
    "grid":       "#E8EDF5",
}

st.set_page_config(
    page_title="汇川技术 FY2025 竞争情报看板 | Siemens DI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# CSS
# ─────────────────────────────────────────
def inject_css():
    st.markdown("""
<style>
.stApp {
    background-color: #F5F7FA;
    color: #1A2B4A;
    font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
}
.main-header {
    background: linear-gradient(135deg, #1B3A8C 0%, #2B5299 60%, #1B3A8C 100%);
    border-left: 6px solid #2BBFBF;
    border-radius: 14px;
    box-shadow: 0 4px 20px rgba(27,58,140,0.18);
    padding: 22px 30px 18px 30px;
    margin-bottom: 20px;
}
.main-header h1 { color: #FFFFFF !important; font-size: 1.9rem; font-weight: 700; margin: 0 0 6px 0; }
.main-header p  { color: #A8C4E8; font-size: 0.88rem; margin: 0; }
[data-testid="metric-container"] {
    background: #FFFFFF;
    border: 1px solid #E0E8F5;
    border-radius: 12px;
    border-top: 4px solid #1B3A8C;
    box-shadow: 0 2px 12px rgba(27,58,140,0.08);
    padding: 14px 16px;
}
[data-testid="stMetricLabel"] { color: #6B7A99 !important; font-size: 0.82rem !important; font-weight: 600 !important; }
[data-testid="stMetricValue"] { color: #1B3A8C !important; font-size: 1.5rem !important; font-weight: 700 !important; }
[data-baseweb="tab-list"] {
    background: #FFFFFF; border-radius: 10px;
    border: 1px solid #E0E8F5; padding: 4px; gap: 4px;
}
[data-baseweb="tab"] { color: #6B7A99; font-weight: 600; font-size: 0.88rem; border-radius: 8px; padding: 8px 16px; }
[aria-selected="true"] { background: #1B3A8C !important; color: #FFFFFF !important; border-radius: 8px; }
[data-testid="stSidebar"] { background: #FFFFFF; border-right: 2px solid #E0E8F5; }
h3 { color: #1B3A8C !important; border-bottom: 2px solid #2BBFBF; padding-bottom: 6px; margin-bottom: 16px !important; }
.insight-box {
    background: #EEF3FC; border-left: 5px solid #1B3A8C;
    border-radius: 10px; padding: 13px 18px;
    font-size: 0.87rem; margin: 10px 0; line-height: 1.6;
}
.insight-box.green { background: #EAF7F0; border-left-color: #27AE60; }
.insight-box.red   { background: #FEF0EE; border-left-color: #E74C3C; }
.insight-box.teal  { background: #E8F8F8; border-left-color: #2BBFBF; }
.stDownloadButton > button { background: #1B3A8C; color: white; border: none; border-radius: 8px; font-weight: 600; }
.stDownloadButton > button:hover { background: #2BBFBF; color: white; }
.sidebar-logo {
    background: linear-gradient(135deg, #1B3A8C, #2B5299);
    border-radius: 12px; padding: 16px; text-align: center; margin-bottom: 16px; color: white;
}
.sidebar-logo .company-name { font-size: 1.1rem; font-weight: 700; color: #FFFFFF; }
.sidebar-logo .ticker       { font-size: 0.8rem; color: #A8C4E8; }
.sidebar-logo .dash-title   { font-size: 0.75rem; color: #2BBFBF; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 图表基础布局
# ─────────────────────────────────────────
def base_layout(**kw):
    layout = dict(
        template="plotly_white",
        paper_bgcolor=C["card_bg"],
        plot_bgcolor=C["plot_bg"],
        font=dict(family="Segoe UI, PingFang SC, Microsoft YaHei", color=C["text_dark"], size=12),
        title_font=dict(color=C["primary"], size=14),
        xaxis=dict(gridcolor=C["grid"], linecolor="#D0DAF0", tickcolor="#D0DAF0"),
        yaxis=dict(gridcolor=C["grid"], linecolor="#D0DAF0", tickcolor="#D0DAF0"),
        margin=dict(t=55, b=40, l=40, r=30),
    )
    layout.update(kw)
    return layout

# ─────────────────────────────────────────
# KPI 卡片
# ─────────────────────────────────────────
def kpi(col, label, value, delta_label, delta_val, note=""):
    with col:
        st.metric(label=label, value=value, delta=f"{delta_label}: {delta_val}")
        if note:
            st.caption(note)

# ─────────────────────────────────────────
# 数据层
# ─────────────────────────────────────────
def load_data():
    annual = pd.DataFrame({
        "年份":       [2023, 2024, 2025],
        "营业收入":   [304199.25, 370409.52, 451048.44],
        "归母净利润": [47418.63,  42854.93,  50500.02],
        "扣非净利润": [40711.77,  40358.32,  49505.05],
        "研发费用":   [26241.48,  31470.81,  42557.74],
        "销售费用":   [None,      14808.78,  15355.69],
        "管理费用":   [None,      15413.53,  18250.83],
        "经营现金流": [33699.16,  72004.40,  66810.25],
    })
    annual["毛利率"]       = [None, 28.70, 28.95]
    annual["净利率"]       = annual["归母净利润"] / annual["营业收入"] * 100
    annual["研发费用率"]   = annual["研发费用"]   / annual["营业收入"] * 100
    annual["现金保障倍数"] = annual["经营现金流"] / annual["归母净利润"] * 100
    annual["营收增速"]     = annual["营业收入"].pct_change() * 100
    annual["净利增速"]     = annual["归母净利润"].pct_change() * 100

    quarterly = pd.DataFrame({
        "季度":       ["Q1", "Q2", "Q3", "Q4"],
        "营业收入":   [89779.12, 115314.46, 111532.49, 134422.38],
        "归母净利润": [13228.25,  16455.63,  12857.43,   7958.71],
        "扣非净利润": [12337.90,  14376.53,  12166.61,  10624.01],
        "经营现金流": [2625.51,   27575.16,   9105.92,  27503.66],
    })
    quarterly["净利率"] = quarterly["归母净利润"] / quarterly["营业收入"] * 100

    product = pd.DataFrame({
        "产品线":   ["工业自动化与数字化", "新能源汽车动力系统", "新兴产业", "其他"],
        "营业收入": [222454.02, 203225.82, 17950.19, 7418.41],
        "营业成本": [132865.04, 170504.18, 12760.01, 4320.15],
        "同比增速": [18.79, 26.39, 15.80, 8.47],
        "收入占比": [49.32, 45.06, 3.98, 1.64],
        "颜色":     [C["primary"], C["secondary"], C["emerging"], C["neutral"]],
    })
    product["毛利润"] = product["营业收入"] - product["营业成本"]
    product["毛利率"] = product["毛利润"] / product["营业收入"] * 100

    regional = pd.DataFrame({
        "地区":     ["中国内地", "境外"],
        "营业收入": [424559.52, 26488.92],
        "占比":     [94.13, 5.87],
        "同比增速": [21.30, 29.89],
    })

    expense = pd.DataFrame({
        "费用类型": ["销售费用", "管理费用", "研发费用"],
        "2024年":   [14808.78, 15413.53, 31470.81],
        "2025年":   [15355.69, 18250.83, 42557.74],
        "同比增速": [3.69, 18.41, 35.23],
    })

    rd_edu = pd.DataFrame({
        "学历": ["博士", "硕士", "本科", "大专及以下"],
        "人数": [94, 3461, 3290, 777],
        "颜色": [C["primary"], C["secondary"], C["emerging"], C["neutral"]],
    })
    rd_edu["占比"] = rd_edu["人数"] / rd_edu["人数"].sum() * 100

    patent = pd.DataFrame({
        "类别":       ["发明专利", "实用新型", "外观设计", "软件著作权"],
        "报告期获得": [142, 210, 94, 194],
        "累计获得":   [579, 1583, 553, 660],
    })

    shareholder = pd.DataFrame({
        "年份":     [2023, 2024, 2025],
        "基本EPS":  [1.78, 1.60, 1.87],
        "每股股息": [None, 0.41, 0.50],
        "分红总额": [None, 11043.97, 13533.18],
        "分红比例": [None, 25.77, 26.80],
    })

    production = pd.DataFrame({
        "行业":       ["智能制造", "新能源汽车"],
        "销售量":     [25971863, 5933895],
        "生产量":     [25499533, 6108223],
        "库存量":     [1361822,  724156],
        "销售量同比": [31.27, 28.46],
        "生产量同比": [26.96, 26.06],
    })

    return dict(
        annual=annual, quarterly=quarterly, product=product,
        regional=regional, expense=expense, rd_edu=rd_edu,
        patent=patent, shareholder=shareholder, production=production,
        revenue_growth=21.77,
    )

# ─────────────────────────────────────────
# Tab 1 — CEO 概览
# ─────────────────────────────────────────
def tab_ceo(d):
    annual    = d["annual"]
    quarterly = d["quarterly"]

    st.markdown("### 📌 核心经营指标（2025年度）")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    kpi(c1, "营业总收入",   "451.05亿元", "同比", "+21.77%", "合并报表口径")
    kpi(c2, "归母净利润",   "50.50亿元",  "同比", "+17.84%", "扣非49.51亿")
    kpi(c3, "扣非净利润",   "49.51亿元",  "同比", "+22.66%", "高质量利润")
    kpi(c4, "研发投入",     "42.56亿元",  "费用率", "9.44%",  "同比+35.23%")
    kpi(c5, "基本EPS",      "1.87元/股",  "同比", "+16.88%", "稀释EPS 1.85")
    kpi(c6, "现金分红比例", "26.80%",     "每股", "0.50元(含税)", "总额13.53亿")

    st.markdown("---")
    st.markdown("### 🏦 财务健康度速览")
    a1, a2, a3, a4 = st.columns(4)
    kpi(a1, "经营现金净流量", "66.81亿元", "现金保障倍数", "132.30%✅", "优秀(>100%)")
    kpi(a2, "利润弹性系数",   "0.82",      "净利增速/营收增速", "正常区间", "17.84%÷21.77%")
    kpi(a3, "境外收入占比",   "5.87%",     "境外增速", "+29.89%", "国际化加速中")
    kpi(a4, "研发人员",       "7,670人",   "占总员工", "28.10%",  "同比+38.50%")

    st.markdown("---")
    st.markdown("### 📈 三年财务趋势与盈利质量")
    col_trend, col_radar = st.columns([3, 2])

    with col_trend:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=annual["年份"].astype(str), y=annual["营业收入"],
            name="营业收入", marker_color=C["primary"], opacity=0.82,
            text=[f"{v/10000:.1f}亿" for v in annual["营业收入"]],
            textposition="outside",
            hovertemplate="<b>%{x}年</b><br>营业收入：%{y:,.0f} 万元<extra></extra>",
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=annual["年份"].astype(str), y=annual["归母净利润"],
            name="归母净利润", mode="lines+markers+text",
            line=dict(color=C["secondary"], width=3),
            marker=dict(symbol="diamond", size=10, color=C["secondary"], line=dict(color="white", width=2)),
            text=[f"{v/10000:.1f}亿" for v in annual["归母净利润"]],
            textposition="top center",
            hovertemplate="<b>%{x}年</b><br>归母净利润：%{y:,.0f} 万元<extra></extra>",
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=annual["年份"].astype(str), y=annual["净利率"],
            name="净利率", mode="lines+markers",
            line=dict(color=C["success"], width=2, dash="dot"),
            marker=dict(size=8, color=C["success"]),
            hovertemplate="<b>%{x}年</b><br>净利率：%{y:.2f}%<extra></extra>",
        ), secondary_y=True)
        fig.update_layout(**base_layout(
            height=420, title_text="营业收入 / 归母净利润 / 净利率（三年趋势）",
            legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center"),
        ))
        fig.update_yaxes(title_text="金额（万元）", gridcolor=C["grid"], secondary_y=False)
        fig.update_yaxes(title_text="净利率（%）",  gridcolor=C["grid"], secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

    with col_radar:
        categories = ["毛利率", "净利率", "研发费用率", "销售费用率", "现金保障/10"]
        radar_data = {
            "2023年": [0,     15.59, 8.63, 0,    71.07/10],
            "2024年": [28.70, 11.57, 8.50, 4.00, 168.05/10],
            "2025年": [28.95, 11.20, 9.44, 3.41, 132.30/10],
        }
        colors_r = {"2023年": C["neutral"], "2024年": C["secondary"], "2025年": C["primary"]}
        fig_r = go.Figure()
        for yr, vals in radar_data.items():
            fig_r.add_trace(go.Scatterpolar(
                r=vals + [vals[0]], theta=categories + [categories[0]],
                fill="toself", name=yr,
                line=dict(color=colors_r[yr], width=2),
                fillcolor=colors_r[yr],
                opacity=0.25 if yr != "2025年" else 0.35,
                hovertemplate="<b>" + yr + "</b><br>%{theta}：%{r:.2f}<extra></extra>",
            ))
        fig_r.update_layout(**base_layout(
            height=420, title_text="盈利质量雷达图（三年对比）",
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 30], gridcolor=C["grid"]),
                angularaxis=dict(gridcolor=C["grid"]),
                bgcolor=C["plot_bg"],
            ),
            legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center"),
        ))
        st.plotly_chart(fig_r, use_container_width=True)

    st.markdown("### 📅 2025年分季度经营节奏")
    fig_q = make_subplots(rows=1, cols=2, subplot_titles=("季度营业收入（万元）", "季度净利率（%）"))
    bar_colors = [C["neutral"], C["primary"], C["primary"], C["secondary"]]
    fig_q.add_trace(go.Bar(
        x=quarterly["季度"], y=quarterly["营业收入"],
        marker_color=bar_colors,
        text=[f"{v/10000:.1f}亿" for v in quarterly["营业收入"]],
        textposition="outside", name="营业收入",
        hovertemplate="<b>%{x}</b><br>营业收入：%{y:,.0f} 万元<extra></extra>",
    ), row=1, col=1)
    fig_q.add_trace(go.Scatter(
        x=quarterly["季度"], y=quarterly["净利率"],
        mode="lines+markers+text",
        line=dict(color=C["secondary"], width=3),
        marker=dict(size=11, color=C["secondary"], line=dict(color="white", width=2)),
        text=[f"{v:.1f}%" for v in quarterly["净利率"]],
        textposition="top center", name="净利率",
        hovertemplate="<b>%{x}</b><br>净利率：%{y:.2f}%<extra></extra>",
    ), row=1, col=2)
    fig_q.update_layout(**base_layout(height=400, showlegend=False, margin=dict(t=55, b=30)))
    fig_q.update_xaxes(gridcolor=C["grid"])
    fig_q.update_yaxes(gridcolor=C["grid"])
    st.plotly_chart(fig_q, use_container_width=True)

    st.markdown("""
<div class="insight-box green">
🚀 <b>增长引擎确认：</b>2025年营收451亿元同比+21.77%，归母净利润50.5亿元同比+17.84%。
双轮驱动格局清晰：工业自动化+19%、新能源汽车+26%，汇川已成功构建跨周期增长飞轮。
西门子DI需警惕：汇川在中国工控市场的规模效应正在形成，价格竞争将持续向高端市场延伸。
</div>
<div class="insight-box red">
⚠️ <b>Q4净利率骤降警示：</b>Q4净利率仅5.92%，较Q2峰值14.27%下降超8个百分点，
反映年末新能源汽车业务价格压力和费用集中确认的双重冲击。
西门子DI可关注：汇川新能源汽车业务盈利能力承压，可能倒逼其在工业自动化领域加大价格竞争。
</div>
<div class="insight-box teal">
💡 <b>研发投入加速：</b>研发费用42.56亿元同比+35.23%，研发费用率升至9.44%，
研发人员7,670人同比+38.50%，汇川正在全面加速技术储备。
西门子DI需重点追踪其工业AI平台（iFG）、自主工业网络协议等项目的商业化进展。
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# Tab 2 — 产品线分析
# ─────────────────────────────────────────
def tab_product(d):
    product    = d["product"]
    production = d["production"]

    st.markdown("### 🏭 产品线收入结构（2025年）")
    col_pie, col_bar = st.columns([1, 2])

    with col_pie:
        fig_pie = go.Figure(go.Pie(
            labels=product["产品线"], values=product["营业收入"],
            hole=0.52, marker=dict(colors=product["颜色"].tolist()),
            textinfo="label+percent", textfont=dict(size=11),
            hovertemplate="<b>%{label}</b><br>收入：%{value:,.0f} 万元<br>占比：%{percent}<extra></extra>",
        ))
        fig_pie.add_annotation(
            text=f"<b>{product['营业收入'].sum()/10000:.1f}亿</b><br><span style='font-size:11px'>总收入</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color=C["primary"]), align="center",
        )
        fig_pie.update_layout(**base_layout(height=340, title_text="产品线收入占比", showlegend=False))
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_bar:
        fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
        fig_dual.add_trace(go.Bar(
            x=product["产品线"], y=product["营业收入"],
            name="营业收入", marker_color=product["颜色"].tolist(), opacity=0.85,
            text=[f"{v/10000:.1f}亿" for v in product["营业收入"]],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>营业收入：%{y:,.0f} 万元<extra></extra>",
        ), secondary_y=False)
        fig_dual.add_trace(go.Scatter(
            x=product["产品线"], y=product["毛利率"],
            name="毛利率", mode="lines+markers",
            line=dict(color=C["danger"], width=2),
            marker=dict(symbol="star", size=13, color=C["danger"], line=dict(color="white", width=1)),
            text=[f"{v:.1f}%" for v in product["毛利率"]],
            textposition="top center",
            hovertemplate="<b>%{x}</b><br>毛利率：%{y:.2f}%<extra></extra>",
        ), secondary_y=True)
        fig_dual.update_layout(**base_layout(
            height=340, title_text="产品线收入与毛利率",
            legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center"),
        ))
        fig_dual.update_yaxes(title_text="收入（万元）", secondary_y=False, gridcolor=C["grid"])
        fig_dual.update_yaxes(title_text="毛利率（%）",  secondary_y=True,  gridcolor=C["grid"])
        st.plotly_chart(fig_dual, use_container_width=True)

    st.markdown("### 📊 产品线同比增速排名")
    ps = product.sort_values("同比增速", ascending=True)
    fig_g = go.Figure(go.Bar(
        x=ps["同比增速"], y=ps["产品线"], orientation="h",
        marker_color=[C["success"] if v >= 0 else C["danger"] for v in ps["同比增速"]],
        text=[f"{v:+.2f}%" for v in ps["同比增速"]], textposition="outside",
        hovertemplate="<b>%{y}</b><br>同比增速：%{x:+.2f}%<extra></extra>",
    ))
    fig_g.add_vline(x=0, line_dash="dash", line_color=C["text_muted"], line_width=1)
    fig_g.add_vline(x=21.77, line_dash="dot", line_color=C["primary"], line_width=2,
                    annotation_text="整体增速 +21.77%",
                    annotation_position="top right",
                    annotation_font=dict(color=C["primary"], size=11))
    fig_g.update_layout(**base_layout(height=370, title_text="产品线同比增速（%）", showlegend=False))
    st.plotly_chart(fig_g, use_container_width=True)

    st.markdown("### 📦 主要业务产销量（2025年）")
    fig_p = go.Figure()
    for col_name, color, label in [("生产量", C["primary"], "生产量"),
                                    ("销售量", C["secondary"], "销售量"),
                                    ("库存量", C["neutral"],   "库存量")]:
        fig_p.add_trace(go.Bar(
            name=label, x=production["行业"], y=production[col_name],
            marker_color=color,
            text=[f"{v:,.0f}" for v in production[col_name]], textposition="outside",
            hovertemplate=f"<b>%{{x}}</b><br>{label}：%{{y:,.0f}} PCS<extra></extra>",
        ))
    fig_p.update_layout(**base_layout(
        height=400, title_text="产销量对比（PCS）", barmode="group",
        legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center"),
    ))
    st.plotly_chart(fig_p, use_container_width=True)

    st.markdown("""
<div class="insight-box red">
⚡ <b>新能源汽车毛利率严重承压：</b>新能源汽车动力系统毛利率仅16.10%，远低于工业自动化40.27%，
说明汇川在新能源赛道面临主机厂强势压价和同业激烈竞争。
西门子DI需关注：汇川可能将新能源业务的规模优势反哺工控产品定价，形成交叉补贴式价格竞争。
</div>
<div class="insight-box green">
🏆 <b>工业自动化高毛利护城河：</b>工业自动化与数字化毛利率40.27%，同比增速+18.79%，
说明汇川在工控核心产品上已建立强定价权，高端化转型初见成效。
西门子DI需重点防守：机床、半导体、汽车装备等高端离散制造场景。
</div>
<div class="insight-box teal">
🤖 <b>新兴产业快速起量：</b>新兴产业收入17.95亿元，同比+15.80%，
SCARA机器人中国市占率约28%排名第一，汇川在机器人赛道已形成规模壁垒。
西门子DI需警惕：汇川"控制+驱动+机器人"一体化解决方案正在侵蚀西门子在智能装备领域的系统集成优势。
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# Tab 3 — 市场与渠道
# ─────────────────────────────────────────
def tab_market(d):
    regional = d["regional"]
    product  = d["product"]

    st.markdown("### 🌍 地区市场分布（2025年）")
    fig_r = go.Figure(go.Bar(
        x=regional["营业收入"], y=regional["地区"], orientation="h",
        marker_color=[C["primary"], C["secondary"]],
        text=[f"{v/10000:.1f}亿" for v in regional["营业收入"]], textposition="outside",
        hovertemplate="<b>%{y}</b><br>营业收入：%{x:,.0f} 万元<extra></extra>",
    ))
    fig_r.update_layout(**base_layout(height=300, title_text="分地区营业收入（万元）", showlegend=False))
    st.plotly_chart(fig_r, use_container_width=True)

    st.markdown("### 📈 地区增速对比")
    fig_rg = go.Figure(go.Bar(
        x=regional["同比增速"], y=regional["地区"], orientation="h",
        marker_color=[C["primary"], C["success"]],
        text=[f"{v:+.2f}%" for v in regional["同比增速"]], textposition="outside",
        hovertemplate="<b>%{y}</b><br>同比增速：%{x:+.2f}%<extra></extra>",
    ))
    fig_rg.add_vline(x=21.77, line_dash="dot", line_color=C["primary"], line_width=2,
                     annotation_text="整体增速 21.77%",
                     annotation_position="top right",
                     annotation_font=dict(color=C["primary"], size=11))
    fig_rg.update_layout(**base_layout(height=300, title_text="分地区同比增速（%）", showlegend=False))
    st.plotly_chart(fig_rg, use_container_width=True)

    st.markdown("### 🔄 市场结构分析")
    c1, c2, c3 = st.columns(3)

    with c1:
        fig_geo = go.Figure(go.Pie(
            labels=["中国内地", "境外"], values=[424559.52, 26488.92],
            hole=0.52, marker=dict(colors=[C["primary"], C["secondary"]]),
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>收入：%{value:,.0f} 万元<extra></extra>",
        ))
        fig_geo.add_annotation(text="<b>地理</b><br>分布", x=0.5, y=0.5, showarrow=False,
                                font=dict(size=12, color=C["primary"]))
        fig_geo.update_layout(**base_layout(height=340, title_text="境内 vs 境外", showlegend=False))
        st.plotly_chart(fig_geo, use_container_width=True)

    with c2:
        fig_pp = go.Figure(go.Pie(
            labels=product["产品线"], values=product["营业收入"],
            hole=0.52, marker=dict(colors=product["颜色"].tolist()),
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>收入：%{value:,.0f} 万元<extra></extra>",
        ))
        fig_pp.add_annotation(text="<b>业务</b><br>结构", x=0.5, y=0.5, showarrow=False,
                               font=dict(size=12, color=C["primary"]))
        fig_pp.update_layout(**base_layout(height=340, title_text="业务结构分布", showlegend=False))
        st.plotly_chart(fig_pp, use_container_width=True)

    with c3:
        fig_gc = go.Figure(go.Bar(
            x=["中国内地", "境外"], y=[21.30, 29.89],
            marker_color=[C["primary"], C["success"]],
            text=["21.30%", "29.89%"], textposition="outside",
            hovertemplate="<b>%{x}</b><br>同比增速：%{y:.2f}%<extra></extra>",
        ))
        fig_gc.update_layout(**base_layout(height=340, title_text="境内外增速对比（%）", showlegend=False))
        st.plotly_chart(fig_gc, use_container_width=True)

    st.markdown("""
<div class="insight-box teal">
🌐 <b>国际化加速但基数仍低：</b>境外收入26.49亿元，同比增速+29.89%超越境内+21.30%，
说明汇川"借船出海"策略在纺织、锂电、光伏等行业取得实质进展。
西门子DI需关注：汇川正在东南亚、中东等新兴市场快速建立渠道网络。
</div>
<div class="insight-box">
🎯 <b>中国市场仍是核心战场：</b>境内收入424.6亿元占比94.13%，绝对规模庞大，
汇川的核心竞争力仍高度集中于中国市场，国际化处于早期阶段。
西门子DI机会：在欧洲、美洲等成熟市场，汇川短期内难以形成实质威胁，
但需提前布局东南亚市场的防御策略。
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# Tab 4 — 费用与研发
# ─────────────────────────────────────────
def tab_rd(d):
    expense        = d["expense"]
    annual         = d["annual"]
    rd_edu         = d["rd_edu"]
    patent         = d["patent"]
    revenue_growth = d["revenue_growth"]

    st.markdown("### 💰 三大费用对比（2024 vs 2025）")
    col_exp, col_growth = st.columns(2)

    with col_exp:
        fig_e = go.Figure()
        for yr, color in [("2024年", C["neutral"]), ("2025年", C["primary"])]:
            fig_e.add_trace(go.Bar(
                name=yr, x=expense["费用类型"], y=expense[yr],
                marker_color=color,
                text=[f"{v/10000:.2f}亿" for v in expense[yr]], textposition="outside",
                hovertemplate=f"<b>%{{x}}</b><br>{yr}：%{{y:,.0f}} 万元<extra></extra>",
            ))
        fig_e.update_layout(**base_layout(
            height=400, title_text="三大费用两年对比（万元）", barmode="group",
            legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center"),
        ))
        st.plotly_chart(fig_e, use_container_width=True)

    with col_growth:
        fig_eg = go.Figure(go.Bar(
            x=expense["费用类型"], y=expense["同比增速"],
            marker_color=[C["danger"] if v > revenue_growth else C["success"] for v in expense["同比增速"]],
            text=[f"{v:+.2f}%" for v in expense["同比增速"]], textposition="outside",
            hovertemplate="<b>%{x}</b><br>同比增速：%{y:+.2f}%<extra></extra>",
        ))
        fig_eg.add_hline(y=revenue_growth, line_dash="dot", line_color=C["primary"], line_width=2,
                         annotation_text=f"营收增速 {revenue_growth:.2f}%",
                         annotation_position="top right",
                         annotation_font=dict(color=C["primary"], size=11))
        fig_eg.update_layout(**base_layout(height=400, title_text="费用同比增速 vs 营收增速（%）", showlegend=False))
        st.plotly_chart(fig_eg, use_container_width=True)

    st.markdown("### 🔬 研发投入趋势（近3年）")
    col_rd, col_edu = st.columns([3, 2])

    with col_rd:
        fig_rd = make_subplots(specs=[[{"secondary_y": True}]])
        fig_rd.add_trace(go.Bar(
            x=annual["年份"].astype(str), y=annual["研发费用"],
            name="研发费用", marker_color=C["primary"], opacity=0.82,
            text=[f"{v/10000:.2f}亿" for v in annual["研发费用"]], textposition="outside",
            hovertemplate="<b>%{x}年</b><br>研发费用：%{y:,.0f} 万元<extra></extra>",
        ), secondary_y=False)
        fig_rd.add_trace(go.Scatter(
            x=annual["年份"].astype(str), y=annual["研发费用率"],
            name="研发费用率", mode="lines+markers+text",
            line=dict(color=C["secondary"], width=3),
            marker=dict(symbol="diamond", size=10, color=C["secondary"], line=dict(color="white", width=2)),
            text=[f"{v:.2f}%" for v in annual["研发费用率"]], textposition="top center",
            hovertemplate="<b>%{x}年</b><br>研发费用率：%{y:.2f}%<extra></extra>",
        ), secondary_y=True)
        fig_rd.update_layout(**base_layout(
            height=420, title_text="研发费用（万元）& 研发费用率（%）",
            legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center"),
        ))
        fig_rd.update_yaxes(title_text="研发费用（万元）", secondary_y=False, gridcolor=C["grid"])
        fig_rd.update_yaxes(title_text="研发费用率（%）",  secondary_y=True,  gridcolor=C["grid"])
        st.plotly_chart(fig_rd, use_container_width=True)

    with col_edu:
        fig_edu = go.Figure(go.Pie(
            labels=rd_edu["学历"], values=rd_edu["人数"],
            hole=0.42, marker=dict(colors=rd_edu["颜色"].tolist()),
            textinfo="label+percent", textfont=dict(size=11),
            hovertemplate="<b>%{label}</b><br>人数：%{value:,}人<br>占比：%{percent}<extra></extra>",
        ))
        fig_edu.add_annotation(text="<b>7,670</b><br>研发人员", x=0.5, y=0.5, showarrow=False,
                                font=dict(size=13, color=C["primary"]))
        fig_edu.update_layout(**base_layout(height=420, title_text="研发人员学历结构（2025年末）", showlegend=False))
        st.plotly_chart(fig_edu, use_container_width=True)

    st.markdown("### 🌊 2025年利润瀑布图（万元）")
    wf_x = ["营业收入", "营业成本", "毛利润", "销售费用", "管理费用", "研发费用", "财务收益", "其他收益", "归母净利润"]
    wf_y = [451048.44, -320449.39, 130599.05, -15355.69, -18250.83, -42557.74, 657.19, 2314.50, 50500.02]
    wf_m = ["absolute", "relative", "total", "relative", "relative", "relative", "relative", "relative", "total"]
    fig_wf = go.Figure(go.Waterfall(
        x=wf_x, y=wf_y, measure=wf_m,
        text=[f"{v:,.0f}" for v in wf_y], textposition="outside",
        textfont=dict(size=10, color=C["text_dark"]),
        increasing=dict(marker=dict(color=C["success"])),
        decreasing=dict(marker=dict(color=C["danger"])),
        totals=dict(marker=dict(color=C["primary"])),
        connector=dict(line=dict(color=C["grid"], width=1, dash="dot")),
        hovertemplate="<b>%{x}</b><br>金额：%{y:,.0f} 万元<extra></extra>",
    ))
    fig_wf.update_layout(**base_layout(height=470, title_text="利润瀑布图：从营业收入到归母净利润（万元）", showlegend=False))
    st.plotly_chart(fig_wf, use_container_width=True)

    st.markdown("### 📋 专利与知识产权（截至2025年末）")
    cols = st.columns(4)
    for col, row in zip(cols, patent.itertuples()):
        with col:
            st.metric(label=row.类别, value=f"{row.累计获得:,}件", delta=f"本期新增 {row.报告期获得}件")

    st.markdown("""
<div class="insight-box red">
⚠️ <b>研发费用增速远超营收：</b>研发费用同比+35.23%，远超营收增速21.77%，
汇川正处于技术投入加速期，短期将压缩利润空间。
西门子DI机会窗口：汇川研发产出转化需要2-3年周期，当前是西门子强化技术壁垒、锁定关键账户的关键时间窗口。
</div>
<div class="insight-box green">
🔬 <b>研发人才大规模扩张：</b>研发人员7,670人同比+38.50%，硕博占比约46.3%，
汇川正在构建高端研发能力，AI、工业软件等领域人才储备快速增长。
西门子DI需关注：汇川工业AI平台iFG、自主工业网络协议等项目若商业化成功，
将直接挑战西门子TIA Portal和PROFINET的生态壁垒。
</div>
<div class="insight-box teal">
📜 <b>知识产权加速积累：</b>累计3,375项专利及软著，2025年新增640项，
发明专利累计579项，汇川的技术原创性持续提升。
西门子DI需追踪：汇川在运动控制算法、工业通信协议领域的专利布局，评估替代风险。
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# Tab 5 — 数据导出
# ─────────────────────────────────────────
def tab_export(d):
    st.markdown("### 📥 数据导出中心")

    export_tables = {
        "年度盈利指标（近3年）":    d["annual"][["年份","营业收入","归母净利润","扣非净利润","研发费用","经营现金流","净利率","研发费用率","营收增速","净利增速"]],
        "分季度数据（2025年）":     d["quarterly"],
        "分产品线数据（2025年）":   d["product"][["产品线","营业收入","营业成本","毛利润","毛利率","同比增速","收入占比"]],
        "分地区数据（2025年）":     d["regional"],
        "费用明细（2024 vs 2025）": d["expense"],
        "研发人员学历结构":         d["rd_edu"][["学历","人数","占比"]],
        "专利情况":                d["patent"],
        "股东回报指标":             d["shareholder"],
        "产销量数据（2025年）":     d["production"],
    }

    selected = st.selectbox("📋 选择数据表", list(export_tables.keys()))
    kw = st.text_input("🔍 关键词搜索过滤（可选）", placeholder="输入关键词过滤行...")

    df_show = export_tables[selected].copy()
    if kw:
        mask = df_show.astype(str).apply(lambda col: col.str.contains(kw, case=False, na=False)).any(axis=1)
        df_show = df_show[mask]

    st.dataframe(df_show, use_container_width=True, height=400)

    st.download_button(
        label=f"⬇️ 下载当前表格（{selected}）",
        data=df_show.to_csv(index=False, encoding="utf-8-sig"),
        file_name=f"汇川FY25_{selected}.csv",
        mime="text/csv",
    )

    st.markdown("---")
    all_dfs = []
    for name, df in export_tables.items():
        tmp = df.copy()
        tmp.insert(0, "数据表", name)
        all_dfs.append(tmp)
    df_all = pd.concat(all_dfs, ignore_index=True)
    st.download_button(
        label="📦 下载全量数据包（所有表格合并）",
        data=df_all.to_csv(index=False, encoding="utf-8-sig"),
        file_name="汇川FY25_全量数据包.csv",
        mime="text/csv",
    )

    st.markdown("### 💵 2025年度利润分配方案")
    d1, d2, d3 = st.columns(3)
    with d1: st.metric("每10股现金股利（含税）", "5.00元",    delta="2024年为4.10元")
    with d2: st.metric("现金分红总额（含税）",   "13.53亿元", delta="+22.56% vs 2024")
    with d3: st.metric("分红比例",               "26.80%",    delta="2024年为25.77%")

    st.markdown("### 📈 股息率动态计算")
    price = st.number_input("请输入当前股价（元/股）", min_value=1.0, max_value=500.0, value=50.0, step=0.5)
    yield_pct = 0.50 / price * 100
    st.metric(label=f"预估股息率（股价 {price:.2f} 元）",
              value=f"{yield_pct:.2f}%",
              delta="每股股息 0.50 元（含税）")

    st.info("""
📌 **数据说明**
- **数据来源**：深圳市汇川技术股份有限公司2025年年度报告（公开披露）
- **报表口径**：合并报表（人民币）
- **数据单位**：万元（人民币），EPS/股息单位为元/股
- **免责声明**：本看板仅供西门子数字化工业（Siemens DI）内部竞争研究使用，不构成任何投资建议，请勿对外传播。
- **数据截止日期**：2025年12月31日
""")

# ─────────────────────────────────────────
# 侧边栏
# ─────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
<div class="sidebar-logo">
    <div class="company-name">🏭 汇川技术</div>
    <div class="ticker">300124.SZ · 深交所创业板</div>
    <div class="dash-title">Siemens DI 竞争情报看板</div>
</div>
""", unsafe_allow_html=True)

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

        st.markdown("#### 🎯 分析视角")
        view_mode = st.radio("选择分析模式", ["全面分析", "增长聚焦", "盈利聚焦"], index=0)
        st.markdown("---")
        st.caption("📅 数据截止：2025年12月31日")
        st.caption("📄 数据来源：汇川技术2025年年度报告")
        st.caption("🔒 仅供Siemens DI内部使用")

    return view_mode

# ─────────────────────────────────────────
# 主函数
# ─────────────────────────────────────────
def main():
    inject_css()
    render_sidebar()

    st.markdown("""
<div class="main-header">
    <h1>📊 汇川技术 FY2025 竞争情报分析看板</h1>
    <p>深圳市汇川技术股份有限公司 · 300124.SZ · 2025年度报告 · Siemens Digital Industries 竞争情报团队</p>
</div>
""", unsafe_allow_html=True)

    data = load_data()

    t1, t2, t3, t4, t5 = st.tabs([
        "📈 CEO概览圈",
        "🏭 产品线分析",
        "🌍 市场与渠道",
        "🔬 费用与研发",
        "📥 数据导出",
    ])

    with t1: tab_ceo(data)
    with t2: tab_product(data)
    with t3: tab_market(data)
    with t4: tab_rd(data)
    with t5: tab_export(data)

    st.markdown("---")
    st.markdown(
        "<p style='text-align:center;color:#6B7A99;font-size:0.78rem;'>"
        "⚠️ 本看板仅供西门子数字化工业（Siemens DI）内部竞争研究使用 · "
        "数据来源于公开年度报告 · 不构成任何投资建议 · 请勿对外传播"
        "</p>",
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()