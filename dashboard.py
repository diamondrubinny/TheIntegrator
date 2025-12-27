import streamlit as st
import json
import os
import time
from core.plugin_manager import PluginManager
from core.logger import setup_logger

st.set_page_config(page_title="The Integrator", page_icon="🔗", layout="wide")

st.title("🔗 The Integrator")
st.markdown("### AI-Powered Automation Hub")

@st.cache_resource
def load_system():
    logger = setup_logger()
    try:
        with open('config/settings.json', 'r') as f:
            config = json.load(f)
    except:
        config = {}
    manager = PluginManager(config, logger)
    return manager, logger

manager, logger = load_system()
# גילוי פלאגינים כל פעם מחדש כדי לתמוך ב-AI שיוצר אותם
manager.discover_plugins()
plugins = manager.get_plugins()

with st.sidebar:
    st.header("Tools Menu")
    if plugins:
        names = [p.name for p in plugins]
        selection = st.radio("Select Tool:", names)
    else:
        st.warning("No plugins found.")
        selection = None
    
    if st.button("Reload System 🔄"):
        st.cache_resource.clear()
        st.rerun()

if selection:
    plugin = next(p for p in plugins if p.name == selection)
    st.markdown("---")
    st.subheader(f"Running: {plugin.name}")
    st.caption(plugin.description)
    
    # אזור הרצה
    container = st.container(border=True)
    with container:
        plugin.run()

# לוגים
st.markdown("---")
with st.expander("System Logs"):
    if os.path.exists('logs'):
        files = sorted([os.path.join('logs', f) for f in os.listdir('logs')], key=os.path.getctime, reverse=True)
        if files:
            with open(files[0], 'r') as f:
                st.text(f.read())
