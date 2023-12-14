import streamlit as st
import pathlib
from PIL import Image
from io import BytesIO

import google.generativeai as genai


from IPython.display import display

st.set_page_config(page_title="Geminate",page_icon="🤖")
with st.sidebar:
    st.subheader("How to use")
    st.markdown("""<span ><font size=2>1. Start by entering your Google API key.</font></span>""",unsafe_allow_html=True)
    st.markdown("""<span ><font size=2>2. To ask questions related to an image, Upload the image and proceed to ask questions related to the image</font></span>""",unsafe_allow_html=True)
    st.markdown("""<span ><font size=2>3. If you wish to chat without involving images, Simply remove any uploaded image and engage in a normal chat with Geminate.</font></span>""",unsafe_allow_html=True)
    google_api_key = st.text_input("Google API Key", key="chatbot_api_key", type="password")
    "[Get an Google API key](https://makersuite.google.com/app/apikey)"
    uploaded_file = st.file_uploader("Choose a image 📷", accept_multiple_files=False)
    if uploaded_file:
        img=uploaded_file.read()
        st.image(img,width=300)
    if st.button("Clear Chat History"):
        st.session_state.messages.clear()
        
    st.divider()
    st.markdown("""<span ><font size=2>Lets Connect!</font></span>""",unsafe_allow_html=True)
    "[Linkedin](https://www.linkedin.com/in/varun-sai-kanuri-089b34226/)" "  \t\t\t"  "[GitHub](https://github.com/varunsai-k)"
    
home_title="Geminate"
st.markdown(f"""# {home_title} <span style=color:#2E9BF5><font size=4>Beta</font></span>""",unsafe_allow_html=True)
st.caption("🚀 A streamlit chatbot powered by Google Gemini LLM")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    
if uploaded_file:
    image_data=uploaded_file.getvalue()
    image_file = BytesIO(image_data)
    image = Image.open(image_file)
    if prompt := st.chat_input():
            if not google_api_key:
                st.info("Please add your Google API key to continue.")
                st.stop()
            genai.configure(api_key=google_api_key)
            model = genai.GenerativeModel('gemini-pro-vision')
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            response=model.generate_content([prompt,image],stream=True)
            response.resolve()
            msg=response.text
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)    
    
else:
    
    if prompt := st.chat_input():
            if not google_api_key:
                st.info("Please add your Google API key to continue.")
                st.stop()
            genai.configure(api_key=google_api_key)
            model = genai.GenerativeModel('gemini-pro')
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            response=model.generate_content(prompt,stream=True)
            response.resolve()
            msg=response.text
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)
    

    
