import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.font_manager as fm
from matplotlib import rc

font_path = "NanumGothic-Regular.ttf"
font_prop = fm.FontProperties(fname=font_path)
rc('font', family=font_prop.get_name())  # 폰트를 Matplotlib에 적용

# Streamlit 앱 시작
st.title("대학교 정책 비교 도구")

# 기존 엑셀 파일 경로 정의
def get_file_path(filename):
    return filename  # 파일 경로를 현재 디렉토리에서 찾도록 설정

# 미리 정의된 파일 목록
file_options = {
    "A대학교 2023": "A대학교_2023.xlsx",
    "A대학교 2024": "A대학교_2024.xlsx",
    "B대학교 2023": "B대학교_2023.xlsx",
    "B대학교 2024": "B대학교_2024.xlsx",
}

# 사용자 파일 선택
st.sidebar.header("비교할 파일 선택")
file_1_name = st.sidebar.selectbox("첫 번째 파일 선택", options=file_options.keys())
file_2_name = st.sidebar.selectbox("두 번째 파일 선택", options=file_options.keys())

if file_1_name and file_2_name:
    file_1_path = get_file_path(file_options[file_1_name])
    file_2_path = get_file_path(file_options[file_2_name])

    # 데이터 로드
    df1 = pd.read_excel(file_1_path)
    df2 = pd.read_excel(file_2_path)

    # 데이터 확인
    st.subheader("첫 번째 데이터")
    st.dataframe(df1)

    st.subheader("두 번째 데이터")
    st.dataframe(df2)

    # 학과 선택
    departments = st.multiselect("비교할 학과 선택", options=df1["학과"].unique(), default=df1["학과"].unique())

    # 필터링
    df1_filtered = df1[df1["학과"].isin(departments)]
    df2_filtered = df2[df2["학과"].isin(departments)]

    # 데이터 비교
    st.subheader("데이터 비교")
    metric = st.selectbox("비교할 항목 선택", ["등록금", "장학금", "학생 수"])

    comparison_df = pd.DataFrame({
        "학과": df1_filtered["학과"],
        f"첫 번째 파일 {metric}": df1_filtered[metric].values,
        f"두 번째 파일 {metric}": df2_filtered[metric].values,
        "변화": df2_filtered[metric].values - df1_filtered[metric].values,
    })

    st.write(comparison_df)

    # 시각화
    st.subheader("변화 시각화")
    fig, ax = plt.subplots(figsize=(8, 6))
    comparison_df.set_index("학과")["변화"].plot(kind="bar", ax=ax)
    plt.title(f"{metric} 변화")
    plt.ylabel("변화량", labelpad=15, rotation=0, ha="center")
    plt.xlabel("학과", labelpad=15)
    ax.tick_params(axis='x', rotation=0)  # X축 레이블 가로로
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0f}'))  # Y축 숫자 포맷 설정
    st.pyplot(fig)

    # 정책 비교
    st.subheader("신규 정책 비교")
    policies_df = pd.DataFrame({
        "학과": df1_filtered["학과"],
        "첫 번째 파일 정책": df1_filtered["신규 정책"].values,
        "두 번째 파일 정책": df2_filtered["신규 정책"].values,
    })
    st.write(policies_df)
else:
    st.write("왼쪽 사이드바에서 두 개의 파일을 선택하세요.")
