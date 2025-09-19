import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="ARGO Ocean Data Assistant",
    # page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern chat interface
st.markdown("""

<style>

    .stApp {
    background-color: #E6F6F3 !important;  /* Light Aqua */
    }

    /* THEME VARIABLES */
    :root {{
        --bg-color: #E6F6F3;
        --body-text-color: #355C7D;
        --container-bg: #ffffff;
        --container-border: #e2e8f0;
        --user-bubble-bg: #90C7E8;
        --user-bubble-text: #ffffff;
        --bot-bubble-bg: #ffffff;
    }}

    [data-theme="dark"] {{
        --bg-color: #0f172a; /* Slate 900 */
        --body-text-color: #cbd5e1; /* Slate 300 */
        --header-gradient: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); /* Indigo/Violet */
        --container-bg: #1e293b; /* Slate 800 */
        --container-border: #334155; /* Slate 700 */
        --user-bubble-bg: #4f46e5;
        --user-bubble-text: #ffffff;
        --bot-bubble-bg: #334155; /* Slate 700 */
    }}

    /* Apply theme to body */
    body {{
        background-color: var(--bg-color);
        color: var(--body-text-color);
    }}

    /* Basic Resets & Hiding Streamlit elements */
    .stDeployButton, .stDecoration {{ display: none; }}
    /* The line that hid the header and arrow has been REMOVED from here */
    .block-container {{ padding-top: 2rem; padding-bottom: 2rem; }}

    /* Header */
    .header {{
        background: none;
        padding: 0;
        margin-bottom: 2rem;
        text-align: left;
    }}
    .header h1 {{ margin: 0; font-size: 2.2rem; font-weight: 700; color: #355C7D;}}
    .header p {{ margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem; }}

    /* Chat container */
    .chat-container {{
        background: var(--container-bg);
        border-radius: 12px;
        border: 1px solid var(--container-border);
    }}

    /* Messages area */
    .messages-area {{
        padding: 1.5rem 2rem;
        display: flex;
        flex-direction: column;
    }}
    .messages-area {{
        min-height: 300px;
        justify-content: center;
    }}
    .messages-area-active {{
        justify-content: flex-start;
    }}

    /* Message bubble styling */
    .message {{ margin-bottom: 1.5rem; }}
    .user-message {{ display: flex; justify-content: flex-end; }}
    .bot-message {{ display: flex; justify-content: flex-start; }}
    .message-bubble {{ max-width: 70%; padding: 1rem 1.25rem; border-radius: 18px; word-wrap: break-word; }}
    .user-bubble {{ background: var(--user-bubble-bg); color: var(--user-bubble-text); border-bottom-right-radius: 6px; }}
    .bot-bubble {{ background: #C2E9F0 !important; border: 1px solid #90C7E8 !important; border-bottom-left-radius: 6px; color: #355C7D !important; }}

    /* Input area styling */
    .input-area {{
        padding: 1rem 2rem;
        background: var(--container-bg);
        border-top: 1px solid var(--container-border);
        border-radius: 0 0 12px 12px;
    }}
    .stTextInput > div > div > input {{
        border-radius: 25px; border: 2px solid #C2E9F0 !important; padding: 0.75rem 1.25rem; font-size: 1rem; transition: all 0.2s;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: #90C7E8; box-shadow: 0 0 0 3px rgba(144, 199, 232, 0.2);
    }}
    .stButton > button {{
        background: #90C7E8 !important; color: white !important; border: none; border-radius: 25px; padding: 0.75rem 2rem; font-weight: 600; transition: all 0.2s;
    }}
    .stButton > button:hover {{
        background-color: #355C7D !important; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(53, 92, 125, 0.3);
    }}

    /* Visualization container styling */
    .viz-container {{
        background: white; border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border: 1px solid #90C7E8 !important;
    }}

    /* Apply theme to sidebar */
    [data-testid="stSidebar"] > div:first-child {{
        background-color: #C2E9F0 !important;
        border-right: none;
    }}
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
         color: var(--body-text-color);
    }}
</style>

""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'show_welcome' not in st.session_state:
    st.session_state.show_welcome = True

# Header
st.markdown("""
<div class="header">
    <h1>FloatChat</h1>
    <p>Explore oceanographic data through natural language queries • Powered by AI</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with sample queries
with st.sidebar:
    st.markdown("### *Quick Start Queries*")
    st.markdown("Click any query below to try it:")
    
    if st.button("Temperature Profiles\n\n*Show me temperature profiles near the equator in March 2023*", 
               key="temp_query", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Show me temperature profiles near the equator in March 2023"})
        st.session_state.show_welcome = False
        st.rerun()
    
    if st.button("Nearest Floats\n\n*What are the nearest ARGO floats to latitude 15°N, longitude 65°E?*", 
               key="location_query", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "What are the nearest ARGO floats to latitude 15°N, longitude 65°E?"})
        st.session_state.show_welcome = False
        st.rerun()
    
    if st.button("Salinity Analysis\n\n*Analyze salinity variations in the Indian Ocean during monsoon season*", 
               key="salinity_query", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Analyze salinity variations in the Indian Ocean during monsoon season"})
        st.session_state.show_welcome = False
        st.rerun()
    
    st.markdown("---")
    st.markdown("### *Data Sources*")
    st.markdown("""
    - *ARGO Float Network* - Global ocean profiling
    - *Temperature & Salinity* - CTD measurements 
    - *Real-time Data* - Updated continuously
    """)
    
    st.markdown("---")
    st.markdown("### *About*")
    st.markdown("""
    This AI assistant helps you explore ARGO oceanographic data using natural language queries. 
    
    *Features:*
    - Natural language processing
    - Interactive visualizations  
    - Global ocean coverage
    - Real-time data access
    """)

# Sample queries for welcome screen - removed from main content

# Mock data for demonstration
def generate_mock_argo_data():
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    data = {
        'date': np.random.choice(dates, 100),
        'latitude': np.random.uniform(-60, 60, 100),
        'longitude': np.random.uniform(20, 120, 100),
        'temperature': np.random.uniform(2, 30, 100),
        'salinity': np.random.uniform(32, 38, 100),
        'depth': np.random.uniform(0, 2000, 100),
        'float_id': [f'ARGO_{i:04d}' for i in np.random.randint(1000, 9999, 100)]
    }
    return pd.DataFrame(data)

def create_temperature_plot():
    df = generate_mock_argo_data()
    fig = px.scatter_mapbox(
        df, lat="latitude", lon="longitude", color="temperature",
        size="depth", hover_data=["float_id", "salinity"],
        color_continuous_scale="RdYlBu_r",
        size_max=15, zoom=2,
        mapbox_style="open-street-map",
        title="ARGO Float Temperature Distribution"
    )
    fig.update_layout(height=500, margin=dict(l=0, r=0, t=40, b=0))
    return fig

def create_depth_profile():
    depths = np.arange(0, 2000, 50)
    temp = 25 * np.exp(-depths/500) + np.random.normal(0, 0.5, len(depths))
    salinity = 34 + 2 * np.exp(-depths/800) + np.random.normal(0, 0.1, len(depths))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=temp, y=-depths, mode='lines+markers', 
                            name='Temperature (°C)', line=dict(color='red', width=3)))
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=salinity, y=-depths, mode='lines+markers',
                             name='Salinity (PSU)', line=dict(color='blue', width=3)))
    
    fig.update_layout(
        title="Temperature-Depth Profile",
        xaxis_title="Temperature (°C)",
        yaxis_title="Depth (m)",
        height=400,
        showlegend=True
    )
    
    return fig, fig2

# Chat container
chat_container = st.container()

with chat_container:
    if st.session_state.show_welcome and not st.session_state.messages:
        # Welcome screen with compact height and search bar higher up
        st.markdown("""
        <div class="chat-container">
            <div class="messages-area">
                <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%; padding: 1rem;">
                    <div style="width: 100%; max-width: 600px; margin-bottom: 1.5rem;">
        """, unsafe_allow_html=True)
        
        # Create input form for welcome screen
        with st.form(key="welcome_chat_form", clear_on_submit=True):
            col1, col2 = st.columns([5, 1])
            
            with col1:
                user_input = st.text_input(
                    "Message",
                    placeholder="Ask me about ARGO float data, ocean temperatures, salinity profiles...",
                    label_visibility="collapsed"
                )
            
            with col2:
                submitted = st.form_submit_button("Send", use_container_width=True)
        
        # --- ADDED FOOTER AND CLOSING DIVS FOR WELCOME SCREEN ---
        st.markdown("""
                    </div>
                    <div style="text-align: center; font-size: 0.8rem; margin-top: 1.5rem; color: #355C7D; opacity: 0.7;">
                        <p style="margin-bottom: 0.2rem;">ARGO Ocean Data Assistant • Built for oceanographic research • Powered by AI & Streamlit</p>
                        <p>This demo uses simulated data. Connect your ARGO database for real-time analysis.</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        # --- END OF ADDITION ---
        
    
    else:
        # Chat messages with dynamic container
        chat_class = "chat-container-active" if st.session_state.messages else "chat-container"
        messages_class = "messages-area-active" if st.session_state.messages else "messages-area"
        
        st.markdown(f'<div class="{chat_class}"><div class="{messages_class}">', unsafe_allow_html=True)
        
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="message user-message">
                    <div class="message-bubble user-bubble">{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="message bot-message">
                    <div class="message-bubble bot-bubble">{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show visualizations if present
                if "visualization" in message:
                    if message["visualization"] == "temperature_map":
                        st.plotly_chart(create_temperature_plot(), use_container_width=True)
                    elif message["visualization"] == "depth_profile":
                        fig1, fig2 = create_depth_profile()
                        col1, col2 = st.columns(2)
                        with col1:
                            st.plotly_chart(fig1, use_container_width=True)
                        with col2:
                            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown('</div></div>', unsafe_allow_html=True)

# Input area - only show when in chat mode (not welcome mode)
# Input area - only show when in chat mode (not welcome mode)
if not (st.session_state.show_welcome and not st.session_state.messages):
    st.markdown('<div class="input-area">', unsafe_allow_html=True)

    # Create input form
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "Message",
                placeholder="Ask me about ARGO float data, ocean temperatures, salinity profiles...",
                label_visibility="collapsed"
            )
        
        with col2:
            submitted = st.form_submit_button("Send", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # --- ADDED FOOTER AFTER THE CHAT INPUT ---
    st.markdown("""
    <div style="text-align: center; font-size: 0.8rem; margin-top: 1.5rem; color: #355C7D; opacity: 0.7;">
        <p style="margin-bottom: 0.2rem;">ARGO Ocean Data Assistant • Built for oceanographic research • Powered by AI & Streamlit</p>
        <p>This demo uses simulated data. Connect your ARGO database for real-time analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    # --- END OF ADDITION ---

# Process user input
if submitted and user_input:
    st.session_state.show_welcome = False
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Simulate AI processing
    with st.spinner("Analyzing your query..."):
        time.sleep(1)  # Simulate processing time
    
    # Generate response based on query
    response = ""
    visualization = None
    
    if any(word in user_input.lower() for word in ["temperature", "temp", "thermal"]):
        response = """Based on your query about temperature data, I've analyzed the ARGO float measurements. The temperature profiles show clear seasonal and depth variations. Here's what I found:

• *Surface temperatures* range from 15-28°C in the specified region
• *Thermocline depth* varies between 50-150m depending on location
• *Deep water temperatures* remain stable around 2-4°C below 1000m

I've generated a temperature distribution map showing ARGO float locations and their measurements."""
        visualization = "temperature_map"
        
    elif any(word in user_input.lower() for word in ["salinity", "salt"]):
        response = """Here's the salinity analysis from ARGO float data:

• *Surface salinity* values range from 33.5-37.2 PSU
• *Halocline characteristics* show distinct patterns at 100-200m depth
• *Regional variations* are influenced by precipitation and evaporation patterns

The depth profiles reveal interesting salinity stratification patterns."""
        visualization = "depth_profile"
        
    elif any(word in user_input.lower() for word in ["bgc", "biochemical", "bio-geo"]):
        response = """BGC (Bio-Geo-Chemical) ARGO float analysis reveals:

• *Chlorophyll-a concentrations* peak at subsurface maxima (40-80m depth)
• *Dissolved oxygen* shows clear oxygen minimum zones
• *pH levels* indicate carbonate system dynamics
• *Nitrate profiles* demonstrate nutrient cycling patterns

The data suggests active biological processes in the euphotic zone with distinct biogeochemical provinces."""
        
    elif any(word in user_input.lower() for word in ["nearest", "location", "float"]):
        response = """Found 12 active ARGO floats within 200km of your specified coordinates:

*Nearest floats:*
• ARGO_2901847 - 15.2°N, 64.8°E (23km away) - Last profile: 2 days ago
• ARGO_2902134 - 14.7°N, 65.3°E (45km away) - Last profile: 5 days ago  
• ARGO_2901923 - 15.6°N, 65.1°E (67km away) - Last profile: 1 day ago

All floats are transmitting normally with complete T/S profiles to 2000m depth."""
        
    else:
        response = """I understand you're interested in ARGO oceanographic data. I can help you with:

• *Temperature and salinity profiles* at specific locations and times
• *BGC parameter analysis* including oxygen, chlorophyll, and nutrients  
• *Float trajectory mapping* and data availability
• *Comparative analysis* between different regions or time periods
• *Data export* in various formats (NetCDF, CSV, ASCII)

Could you be more specific about what oceanographic parameters you'd like to explore?"""
    
    # Add bot response
    bot_message = {"role": "assistant", "content": response}
    if visualization:
        bot_message["visualization"] = visualization
    
    st.session_state.messages.append(bot_message)
    st.rerun()
