import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
from src.check_supplier_emails import check_supplier_emails


DB_PATH = "data/procurement.db"


st.set_page_config(
    page_title="AI Procurement Dashboard",
    page_icon="📦",
    layout="wide"
)


@st.cache_data(ttl=5)
def load_requests():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        """
        SELECT *
        FROM procurement_requests
        ORDER BY datetime(created_at) DESC
        """,
        conn
    )

    conn.close()

    return df


df = load_requests()


st.title("📦 AI Procurement Dashboard")

st.markdown(
    "Human-in-the-loop procurement system powered by AI"
)

if st.button(
    "📥 Check Supplier Responses"
):

    check_supplier_emails()

    st.cache_data.clear()

    st.success(
        "Supplier responses processed successfully."
    )

    st.rerun()

if df.empty:

    st.info("No procurement requests found.")

    st.stop()


# ==================================================
# KPI CARDS
# ==================================================

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)


with col1:

    st.metric(
        "📦 Total Requests",
        len(df)
    )


with col2:

    st.metric(
        "🟡 Pending",
        len(
            df[
                df["status"] == "PENDING_APPROVAL"
            ]
        )
    )


with col3:

    st.metric(
        "🟢 Approved",
        len(
            df[
                df["status"].isin(
                    [
                        "APPROVED",
                        "EMAIL_SENT"
                    ]
                )
            ]
        )
    )


with col4:

    st.metric(
        "❌ Rejected",
        len(
            df[
                df["status"] == "REJECTED"
            ]
        )
    )


with col5:

    st.metric(
        "📧 Emails Sent",
        len(
            df[
                df["status"] == "EMAIL_SENT"
            ]
        )
    )


with col6:

    st.metric(
        "🔴 High Risk",
        len(
            df[
                df["risk_level"] == "HIGH"
            ]
        )
    )


st.divider()


# ==================================================
# SEARCH + FILTERS
# ==================================================

st.subheader("🔍 Search & Filters")


search_text = st.text_input(
    "Search by Part or Supplier"
)


filter_col1, filter_col2 = st.columns(2)


with filter_col1:

    status_filter = st.selectbox(
        "Filter by Status",
        [
            "ALL",
            "PENDING_APPROVAL",
            "REJECTED",
            "EMAIL_SENT",
            "MODIFICATION_REQUESTED"
        ]
    )


with filter_col2:

    risk_filter = st.selectbox(
        "Filter by Risk",
        [
            "ALL",
            "HIGH",
            "MEDIUM",
            "LOW"
        ]
    )


filtered_df = df.copy()


if search_text:

    filtered_df = filtered_df[
        filtered_df["part_name"]
        .str.contains(
            search_text,
            case=False,
            na=False
        )
        |
        filtered_df["supplier_name"]
        .str.contains(
            search_text,
            case=False,
            na=False
        )
    ]


if status_filter != "ALL":

    filtered_df = filtered_df[
        filtered_df["status"] == status_filter
    ]


if risk_filter != "ALL":

    filtered_df = filtered_df[
        filtered_df["risk_level"] == risk_filter
    ]


st.divider()


# ==================================================
# REQUEST TABLE
# ==================================================

st.subheader("📋 Procurement Requests")


display_columns = [

    "request_id",

    "part_name",

    "current_stock",

    "recommended_order",

    "ordered_quantity",

    "supplier_name",

    "risk_level",

    "status",

    "supplier_status",

    "expected_delivery_date"
]


st.dataframe(
    filtered_df[
        display_columns
    ],
    use_container_width=True
)


st.divider()


# ==================================================
# REQUEST DETAILS
# ==================================================

st.subheader("📄 Request Details")


if not filtered_df.empty:

    selected_request = st.selectbox(
        "Select Request",
        filtered_df["request_id"]
    )


    request = filtered_df[
        filtered_df["request_id"]
        == selected_request
    ].iloc[0]


    left, right = st.columns(2)


    with left:

        st.markdown(
            "### 📦 Part Information"
        )

        st.write(
            f"**Part Name:** {request['part_name']}"
        )

        st.write(
            f"**Current Stock:** {request['current_stock']}"
        )

        st.write(
            f"**Recommended Order:** {request['recommended_order']}"
        )

        st.write(
            f"**Risk Level:** {request['risk_level']}"
        )


    with right:

        st.markdown(
        "### 🏭 Supplier Information"
        )

        st.write(
            f"**Supplier:** {request['supplier_name']}"
        )

        st.write(
            f"**Supplier Email:** {request['supplier_email']}"
        )

        st.write(
            f"**Procurement Status:** {request['status']}"
        )

        st.write(
            f"**Supplier Status:** {request['supplier_status']}"
        )

        st.write(
            f"**Expected Delivery Date:** "
            f"{request['expected_delivery_date']}"
        )

        st.write(
            f"**Supplier Response:** "
            f"{request['supplier_response']}"
        )

        st.write(
            f"**Created At:** {request['created_at']}"
        )


st.divider()


# ==================================================
# RECENT ACTIVITY
# ==================================================

st.subheader("📝 Recent Activity")


recent = df.head(5)


for _, row in recent.iterrows():

    st.info(
        f"""
{row['status']}

📦 {row['part_name']}

🏭 {row['supplier_name']}
"""
    )


st.divider()


# ==================================================
# SUPPLIER LEADERBOARD
# ==================================================

st.subheader("🏆 Supplier Leaderboard")


supplier_stats = (

    df.groupby(
        "supplier_name"
    )

    .size()

    .reset_index(
        name="orders"
    )

    .sort_values(
        by="orders",
        ascending=False
    )
)


st.dataframe(
    supplier_stats,
    use_container_width=True
)


st.divider()

# ==================================================
# CHARTS
# ==================================================

chart_col1, chart_col2 = st.columns(2)


with chart_col1:

    st.subheader("📦 Orders by Supplier")

    supplier_orders = (

        df.groupby(
            "supplier_name"
        )

        .size()

        .reset_index(
            name="orders"
        )
    )

    fig = px.pie(
        supplier_orders,
        names="supplier_name",
        values="orders",
        hole=0.4
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with chart_col2:

    st.subheader("📊 Status Distribution")

    status_counts = (

        df["status"]

        .value_counts()

        .reset_index()
    )

    status_counts.columns = [
        "status",
        "count"
    ]

    fig = px.pie(
        status_counts,
        names="status",
        values="count",
        hole=0.5
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.divider()


# ==================================================
# RISK + TIMELINE
# ==================================================

risk_col, timeline_col = st.columns(2)


with risk_col:

    st.subheader("🔴 Risk Distribution")

    risk_counts = (

        df["risk_level"]

        .value_counts()

        .reset_index()
    )

    risk_counts.columns = [
        "risk",
        "count"
    ]

    fig = px.pie(
        risk_counts,
        names="risk",
        values="count",
        hole=0.4
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with timeline_col:

    st.subheader("📈 Orders Over Time")

    timeline_df = df.copy()

    timeline_df["created_at"] = pd.to_datetime(
        timeline_df["created_at"]
    )

    timeline_df["date"] = (
        timeline_df["created_at"]
        .dt.date
    )

    orders_by_day = (

        timeline_df

        .groupby("date")

        .size()

        .reset_index(
            name="orders"
        )
    )

    fig = px.line(
        orders_by_day,
        x="date",
        y="orders",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.divider()


# ==================================================
# TOP ORDERED PARTS
# ==================================================

st.subheader("🔥 Top Ordered Parts")


top_parts = (

    df.groupby(
        "part_name"
    )

    .size()

    .reset_index(
        name="orders"
    )

    .sort_values(
        by="orders",
        ascending=False
    )
)


fig = px.bar(
    top_parts,
    x="part_name",
    y="orders"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


st.divider()

# ==================================================
# EXPORT CSV
# ==================================================


csv = filtered_df.to_csv(
    index=False
)


st.download_button(
    label="📥 Download Report",
    data=csv,
    file_name="procurement_report.csv",
    mime="text/csv"
)


# ==================================================
# REFRESH
# ==================================================

if st.button("🔄 Refresh Dashboard"):

    st.cache_data.clear()

    st.rerun()

# ==================================================
# Print
# ==================================================

st.components.v1.html(
    """
    <body style="margin: 0; padding: 0; overflow: hidden;">
        <button
            onclick="window.parent.print();"
            style="
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background-color: #FFFFFF;
                color: #31333F;
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 8px;
                padding: 10px 16px;
                font-size: 16px;
                font-family: Source Sans Pro, sans-serif;
                cursor: pointer;
                font-weight: 400;
                line-height: 1.2;
                transition: border-color 0.2s, color 0.2s;
                box-sizing: border-box;
                width: auto;
                height: 42px;
            "
            onmouseover="this.style.borderColor='#FF4B4B'; this.style.color='#FF4B4B';"
            onmouseout="this.style.borderColor='rgba(49, 51, 63, 0.2)'; this.style.color='#31333F';"
        >
            <span style="margin-right: 10px; font-size: 16px; display: inline-block; transform: translateY(-1px);">🖨️</span> Print Dashboard
        </button>
    </body>
    """,
    height=45
)