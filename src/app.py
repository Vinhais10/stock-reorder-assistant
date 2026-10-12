import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from reorder import load_sales_data, calculate_avg_daily_sales, calculate_reorder_points
from agent import run_agent

st.set_page_config(
    page_title="Stock Reorder Assistant",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLORS = {
    "primary": "#6366F1",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger":  "#EF4444",
    "text":    "#F1F5F9",
    "muted":   "#94A3B8",
}

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1, h2, h3 { letter-spacing: -0.02em; }
    .kpi-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        height: 100%;
    }
    .kpi-label {
        color: #94A3B8;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    .kpi-value {
        color: #F1F5F9;
        font-size: 2rem;
        font-weight: 700;
        line-height: 1;
    }
    .kpi-sub {
        color: #94A3B8;
        font-size: 0.8rem;
        margin-top: 6px;
    }
    .status-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    .badge-danger  { background: rgba(239,68,68,0.15);  color: #EF4444; }
    .badge-success { background: rgba(16,185,129,0.15); color: #10B981; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def get_results():
    sales = load_sales_data()
    products = pd.read_csv("products.csv")
    avg_daily_sales = calculate_avg_daily_sales(sales)
    return calculate_reorder_points(products, avg_daily_sales)


result = get_results()

result["current_stock"] = pd.to_numeric(result["current_stock"], errors="coerce").fillna(0)
result["reorder_point"] = pd.to_numeric(result["reorder_point"], errors="coerce").fillna(0)
result["avg_daily_sales"] = pd.to_numeric(result["avg_daily_sales"], errors="coerce").fillna(0)
result["lead_time_days"] = pd.to_numeric(result["lead_time_days"], errors="coerce").fillna(0)

reorder_count = int(result["needs_reorder"].sum())
total_products = len(result)
stock_in_risk = int(result.loc[result["needs_reorder"], "current_stock"].sum())

result["days_to_stockout"] = (result["current_stock"] / result["avg_daily_sales"].replace(0, 1)).round(0)
avg_days = int(result.loc[result["needs_reorder"], "days_to_stockout"].mean())


st.title("📦 Stock Reorder Assistant")
st.caption("Inventory reorder recommendations based on real retail transaction history.")

tab_dashboard, tab_agent = st.tabs(["📊 Dashboard", "🤖 Ask the Agent"])


with tab_dashboard:

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Products tracked</div>
                <div class="kpi-value">{total_products}</div>
                <div class="kpi-sub">in current dataset</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Needs reorder</div>
                <div class="kpi-value" style="color:#EF4444;">{reorder_count}</div>
                <div class="kpi-sub">below reorder point</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Units in stock</div>
                <div class="kpi-value">{stock_in_risk}</div>
                <div class="kpi-sub">across flagged items</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Days to stockout</div>
                <div class="kpi-value" style="color:#F59E0B;">{avg_days}</div>
                <div class="kpi-sub">avg. for flagged items</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.subheader("📈 Stock vs Reorder Point")

    chart_df = result.sort_values("reorder_point", ascending=True).copy()
    chart_df["label"] = chart_df["product_id"].astype(str).str.strip()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=chart_df["label"].tolist(),
        y=chart_df["current_stock"].astype(float).tolist(),
        name="Current stock",
        marker_color=COLORS["primary"],
        text=[int(v) for v in chart_df["current_stock"]],
        textposition="outside",
        textfont=dict(size=14, color=COLORS["text"]),
        hovertemplate="<b>%{x}</b><br>Stock: %{y}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=chart_df["label"].tolist(),
        y=chart_df["reorder_point"].astype(float).tolist(),
        name="Reorder point",
        marker_color=COLORS["danger"],
        opacity=0.6,
        text=[int(v) for v in chart_df["reorder_point"]],
        textposition="outside",
        textfont=dict(size=14, color=COLORS["text"]),
        hovertemplate="<b>%{x}</b><br>ROP: %{y:.0f}<extra></extra>",
    ))
    fig.update_layout(
        barmode="group",
        height=450,
        margin=dict(l=10, r=10, t=60, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text"], size=14),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=14),
        ),
        xaxis=dict(
            type="category",
            gridcolor="rgba(0,0,0,0)",
            title=dict(text="Product", font=dict(size=15)),
            tickfont=dict(size=15),
        ),
        yaxis=dict(
            gridcolor="#334155",
            title=dict(text="Units", font=dict(size=15)),
            tickfont=dict(size=14),
            range=[0, float(chart_df["reorder_point"].max()) * 1.3],
        ),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("📦 Products")
    only_flagged = st.toggle("Show only products that need reorder", value=False)
    display = result[result["needs_reorder"]] if only_flagged else result

    for _, row in display.iterrows():
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])

            with c1:
                st.markdown(f"### {row['product_name']}")
                st.caption(f"ID: `{row['product_id']}`")

                ratio = min(row["current_stock"] / row["reorder_point"], 1.0) if row["reorder_point"] > 0 else 0
                bar_color = COLORS["danger"] if row["needs_reorder"] else COLORS["success"]

                st.markdown(
                    f"""
                    <div style="margin: 10px 0;">
                        <div style="display:flex; justify-content:space-between; font-size:0.85rem; color:#94A3B8; margin-bottom:6px;">
                            <span>Stock: <b style="color:#F1F5F9;">{int(row['current_stock'])}</b></span>
                            <span>Reorder point: <b style="color:#F1F5F9;">{row['reorder_point']:.0f}</b></span>
                        </div>
                        <div style="background:#0F172A; border-radius:999px; height:8px; overflow:hidden;">
                            <div style="width:{ratio*100:.1f}%; background:{bar_color}; height:100%;"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.caption(
                    f"Avg daily sales: **{row['avg_daily_sales']:.1f}** "
                    f"/ Lead time: **{int(row['lead_time_days'])}d** "
                    f"/ Days to stockout: **{int(row['days_to_stockout'])}**"
                )

            with c2:
                if row["needs_reorder"]:
                    st.markdown(
                        '<div class="status-badge badge-danger">⚠️ REORDER NEEDED</div>',
                        unsafe_allow_html=True,
                    )
                    shortage = int(row["reorder_point"] - row["current_stock"])
                    st.caption(f"Shortage: **{shortage}** units")
                else:
                    st.markdown(
                        '<div class="status-badge badge-success">✅ OK</div>',
                        unsafe_allow_html=True,
                    )


with tab_agent:

    with st.sidebar:
        st.markdown("### 💡 Example questions")

        examples = [
            ("Which products need reordering?", "🔴"),
            ("Tell me about product 85123A", "📦"),
            ("Why is 85123A flagged?", "❓"),
            ("How has 85123A been selling in the last 30 days?", "📈"),
            ("What if the lead time for 85123A became 20 days?", "🔮"),
        ]
        for q, icon in examples:
            if st.button(f"{icon} {q}", use_container_width=True):
                st.session_state.pending_question = q

        st.divider()
        if st.button("🗑️ Clear conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.divider()
        st.caption("**Powered by** Groq - Llama 3.3 70B")

    st.subheader("🤖 Ask about your inventory")
    st.caption("Answers use real data from reorder.py - the agent never invents numbers.")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hi! Ask me anything about your inventory. Use the suggestions on the left, or type below. You can ask in English or Portuguese.",
            }
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask a question about your inventory...")
    if "pending_question" in st.session_state and st.session_state.pending_question:
        user_input = st.session_state.pending_question
        st.session_state.pending_question = None

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer = run_agent(user_input, verbose=False)
                except Exception as e:
                    answer = f"Error: {e}"
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})


