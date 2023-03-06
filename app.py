#!/usr/bin/env python3

import streamlit as st
import requests
import threading

import server


def start_server():
    if not st.session_state['server_started']:
        # start API server
        threading.Thread(target=server.run_app).start()
        st.session_state['server_started'] = True


def render_gui():
    uploaded_file = st.file_uploader("Choose an RDF file.")

    if uploaded_file is not None:
        # st.write(document)
        st.write(uploaded_file)

        data = requests.post("http://localhost:5050/index", files={'file': uploaded_file}).json()
        st.write(data)

        query = st.text_input('Query', 'list all regions')
        answer = requests.get("http://localhost:5050/query", params={'id': data['id'], 'query': query}).json()
        st.write(answer)


if __name__ == '__main__':
    st.session_state['server_started'] = False
    start_server()
    render_gui()
