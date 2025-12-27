import os
import re
from core.base_plugin import BasePlugin
from openai import OpenAI

class AIArchitect(BasePlugin):
    @property
    def name(self):
        return "🤖 AI Plugin Architect"

    @property
    def description(self):
        return "Generates new tools automatically using AI."

    def run(self):
        try:
            import streamlit as st
        except ImportError:
            print("AI Architect is only available in GUI mode.")
            return

        st.info("Describe a tool you need, and I will write the code for it.")
        
        col1, col2 = st.columns(2)
        with col1:
            filename = st.text_input("Tool Name (English, e.g., 'currency_converter'):")
        with col2:
            description = st.text_input("Description (What should it do?):")
            
        if st.button("Generate & Install Tool 🚀"):
            if not filename or not description:
                st.error("Please fill all fields.")
                return
            
            api_key = self.config.get('openai_api_key')
            if not api_key or "YOUR" in api_key:
                st.error("Please set your OpenAI API Key in config/settings.json")
                return

            with st.spinner("AI is coding..."):
                try:
                    code = self.generate_code(api_key, description, filename)
                    self.save_plugin(filename, code)
                    st.success(f"Plugin '{filename}.py' created! Please refresh the page.")
                    with st.expander("View Generated Code"):
                        st.code(code, language='python')
                except Exception as e:
                    st.error(f"Error: {e}")

    def generate_code(self, api_key, prompt, name):
        client = OpenAI(api_key=api_key)
        system_prompt = """
        You are a Python expert. Write a class inheriting from 'core.base_plugin.BasePlugin'.
        Rules:
        1. Imports: `from core.base_plugin import BasePlugin` plus any libraries needed.
        2. Class name must be CamelCase based on the filename.
        3. Implement `name`, `description`, and `run(self)`.
        4. In `run`, use `try-except` blocks.
        5. Detect if running in Streamlit (`import streamlit as st`) for UI output, otherwise use print.
        6. Return ONLY raw python code. No markdown formatting.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create a plugin named '{name}' that does: {prompt}"}
            ]
        )
        content = response.choices[0].message.content
        return re.sub(r"```python|```", "", content).strip()

    def save_plugin(self, filename, code):
        clean_name = "".join(x for x in filename if x.isalnum() or x == "_").lower()
        path = os.path.join("plugins", f"{clean_name}.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
