import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

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
    """Render the sidebar filters and export option."""
    st.sidebar.header("📊 Data Filters")
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(analyzer.master_df['date'].min().date(), 
               analyzer.master_df['date'].max().date())
    )
    
    call_types = st.sidebar.multiselect(
        "Select Call Types",
        options=['neutral', 'spam', 'fraud'],
        default=['neutral', 'spam', 'fraud']
    )
    
    # Add export functionality
    st.sidebar.markdown("---")
    st.sidebar.header("📥 Export Data")
    
    # Convert date_range to pandas datetime for comparison
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
    
    # Filter data based on selections
    mask = (analyzer.master_df['date'].dt.date >= date_range[0]) & \
           (analyzer.master_df['date'].dt.date <= date_range[1]) & \
           (analyzer.master_df['flagged'].isin(call_types))
           
    filtered_df = analyzer.master_df[mask]
    
    if st.sidebar.button("Export Filtered Data"):
        # Convert to CSV
        csv = filtered_df.to_csv(index=False)
        
        # Create download button
        st.sidebar.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"call_data_{date_range[0]}_{date_range[1]}.csv",
            mime="text/csv",
        )
        
    return date_range, call_types

def render_hourly_heatmap(analyzer):
    """Render heatmap showing call volume by hour and day of week"""
    df = analyzer.master_df.copy()
    df['hour'] = df['date'].dt.hour
    df['day'] = df['date'].dt.day_name()
    
    hourly_data = df.groupby(['day', 'hour']).size().reset_index(name='calls')
    
    fig = go.Figure(data=go.Heatmap(
        x=hourly_data['hour'],
        y=hourly_data['day'],
        z=hourly_data['calls'],
        colorscale='Viridis'
    ))
    
    fig.update_layout(
        title='Call Volume by Hour and Day',
        xaxis_title='Hour of Day',
        yaxis_title='Day of Week',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_threat_trend(analyzer):
    """Render line chart showing threat trends over time"""
    df = analyzer.master_df.copy()
    daily_threats = df.groupby(['date', 'flagged']).size().unstack(fill_value=0)
    
    fig = go.Figure()
    
    for flag in ['spam', 'fraud']:
        if flag in daily_threats.columns:
            fig.add_trace(go.Scatter(
                x=daily_threats.index,
                y=daily_threats[flag],
                name=flag.capitalize(),
                mode='lines+markers'
            ))
    
    fig.update_layout(
        title='Daily Threat Trends',
        xaxis_title='Date',
        yaxis_title='Number of Calls',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_country_map(analyzer):
    """Render European map showing call origins"""
    df = analyzer.master_df.copy()
    country_threats = df[df['flagged'].isin(['spam', 'fraud'])].groupby('country').size()
    
    fig = go.Figure(data=go.Choropleth(
        locations=country_threats.index,
        z=country_threats.values,
        locationmode='country names',
        colorscale='Reds',
        colorbar_title='Threat Calls'
    ))
    
    # Configure the map to focus on Europe
    fig.update_layout(
        title='Geographic Distribution of Threats in Europe',
        geo=dict(
            scope='europe',
            projection_type='mercator',
            center=dict(lat=48.5, lon=10),  # Center on Central Europe
            lataxis_range=[35, 65],  # Latitude bounds
            lonaxis_range=[-10, 30],  # Longitude bounds
            showland=True,
            landcolor='rgb(243, 243, 243)',
            showocean=True,
            oceancolor='rgb(255, 255, 255)',
            showcountries=True,
            countrycolor='rgb(204, 204, 204)',
        ),
        height=500,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)

