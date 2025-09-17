import streamlit as st
import requests
import time


st.markdown("<h1 style='text-align: center; color: red;'>HR Policy Chatbot 🤖</h1>", unsafe_allow_html=True)
st.title("Ask a question about our HR policy and get a detailed answer with sources.🤖")
st.write("How can i help you..")

# Initialize chat history in Streamlit's session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Write Your query here.."):
  
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    
    with st.spinner("Thinking..."):
        try:
            # Send POST request to your backend API
            api_url = "http://127.0.0.1:5000/query"
            payload = {"question": prompt}
            response = requests.post(api_url, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes

            # Parse the JSON response
            data = response.json()
            answer = data.get("answer", "No answer found.")
            sources = data.get("sources", [])

            # Format the response with the answer and sources
            full_response = answer
            if sources:
                full_response += "\n\n**Sources:**"
                for i, source in enumerate(sources):
                    full_response += f"\n- Chunk {i+1}: {source['text']}"

        except requests.exceptions.ConnectionError:
            full_response = "Connection Error: The backend API is not running. Please make sure your `app.py` server is active in a separate terminal."
        except Exception as e:
            full_response = f"An error occurred: {e}"

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})