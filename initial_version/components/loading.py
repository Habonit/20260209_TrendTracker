import streamlit as st

def show_loading(message: str = "처리 중입니다..."):
    """
    로딩 스피너를 표시합니다. 
    Context Manager로 사용하여 'with' 문과 함께 사용할 수 있습니다.
    
    사용 예시:
    with show_loading("데이터를 가져오는 중..."):
        data = fetch_data()
    """
    return st.spinner(message)
