import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render_metrics_row(analyzer):
    """Render the top metrics row with four key metrics."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📞 Total Calls Processed",
            value=f"{analyzer.total_calls:,}",
            help="All calls processed through Hiya's protection system"
        )

    with col2:
        st.metric(
            label="🛡️ Threats Blocked",
            value=f"{analyzer.total_blocked}",
            delta=f"{analyzer.protection_rate:.1f}% protection rate",
            help="Total spam and fraud calls prevented"
        )

    with col3:
        st.metric(
            label="⚠️ Spam Calls",
            value=f"{analyzer.spam_calls}",
            delta=f"{(analyzer.spam_calls / analyzer.total_calls) * 100:.1f}% of total",
            delta_color="inverse",
            help="Unwanted marketing and robocalls blocked"
        )

    with col4:
        st.metric(
            label="🚨 Fraud Attempts",
            value=f"{analyzer.fraud_calls}",
            delta=f"{(analyzer.fraud_calls / analyzer.total_calls) * 100:.1f}% of total",
            delta_color="inverse",
            help="High-risk fraud and scam attempts prevented"
        )

def render_daily_chart(daily_stats):
    """Render the daily call volume and protection analysis chart."""
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            name='Total Calls', 
            x=daily_stats['date_str'], 
            y=daily_stats['total_calls'],
            marker_color='lightblue', 
            opacity=0.7
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Bar(
            name='Blocked Calls', 
            x=daily_stats['date_str'], 
            y=daily_stats['blocked_calls'],
            marker_color='red', 
            opacity=0.8
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            name='Protection Rate (%)', 
            x=daily_stats['date_str'], 
            y=daily_stats['protection_rate'],
            line=dict(color='green', width=3), 
            mode='lines+markers'
        ),
        secondary_y=True,
    )

    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Number of Calls", secondary_y=False)
    fig.update_yaxes(title_text="Protection Rate (%)", secondary_y=True)
    fig.update_layout(
        title="Daily Call Processing and Protection Effectiveness",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

def render_insights(analyzer):
    """Render the three key insights boxes."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
            <h3>🎯 Value Delivered</h3>
            <p>Protected users from {total_blocked:,} unwanted calls this month, 
            maintaining a {protection_rate:.1f}% protection rate.</p>
        </div>
        """.format(
            total_blocked=analyzer.total_blocked,
            protection_rate=analyzer.protection_rate
        ), unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="insight-box">
            <h3>⚡ Efficiency</h3>
            <p>Processed {total_calls:,} calls with automated classification, 
            ensuring real-time protection.</p>
        </div>
        """.format(
            total_calls=analyzer.total_calls
        ), unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="insight-box">
            <h3>🧠 Intelligence</h3>
            <p>Identified {fraud_calls:,} fraud attempts and {spam_calls:,} spam calls 
            through advanced pattern recognition.</p>
        </div>
        """.format(
            fraud_calls=analyzer.fraud_calls,
            spam_calls=analyzer.spam_calls
        ), unsafe_allow_html=True)

def render_filters(analyzer):
    """Render the sidebar filters."""
    st.sidebar.header("📊 Data Filters")
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(analyzer.master_df['date'].min(), analyzer.master_df['date'].max())
    )
    
    call_types = st.sidebar.multiselect(
        "Select Call Types",
        options=['neutral', 'spam', 'fraud'],
        default=['neutral', 'spam', 'fraud']
    )
    
    return date_range, call_types

