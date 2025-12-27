import psutil
from core.base_plugin import BasePlugin

class SystemMonitor(BasePlugin):
    @property
    def name(self):
        return "System Health Monitor"

    @property
    def description(self):
        return "Checks CPU and RAM usage."

    def run(self):
        # בדיקה האם רצים בתוך Streamlit
        try:
            import streamlit as st
            is_gui = True
        except ImportError:
            is_gui = False

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        
        msg = f"CPU: {cpu}% | RAM: {ram}%"
        self.logger.info(msg)

        if is_gui:
            st.metric(label="CPU Usage", value=f"{cpu}%")
            st.metric(label="RAM Usage", value=f"{ram}%")
        else:
            print(f"\n[Monitor] {msg}\n")
