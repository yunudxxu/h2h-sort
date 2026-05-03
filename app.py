import streamlit as st

st.set_page_config(page_title="H2H Song Sort", page_icon="🎵")

# 1. 초기 데이터 설정
if 'songs' not in st.session_state:
    st.session_state.songs = [
        "The Chase", "Butterflies", "STYLE", "Pretty Please", 
        "FOCUS", "Apple Pie", "Flutter", "Blue Moon", "RUDE!"
    ]
    st.session_state.groups = [[s] for s in st.session_state.songs]
    st.session_state.merged_groups = []
    st.session_state.left = []
    st.session_state.right = []
    st.session_state.current_merged = []
    st.session_state.finished = False

st.title("❤️ Hearts2Hearts Song Sort")

# 2. 정렬 프로세스 함수
def process_logic():
    if len(st.session_state.groups) <= 1 and not st.session_state.left and not st.session_state.right:
        st.session_state.finished = True
        return

    if not st.session_state.left and not st.session_state.right:
        if len(st.session_state.groups) >= 2:
            st.session_state.left = st.session_state.groups.pop(0)
            st.session_state.right = st.session_state.groups.pop(0)
            st.session_state.current_merged = []
        else:
            st.session_state.groups.extend(st.session_state.merged_groups)
            st.session_state.merged_groups = []
            # 재귀 대신 반복 처리를 위해 함수를 다시 부르지 않고 상태만 변경

# 3. 화면 렌더링
if not st.session_state.finished:
    process_logic()
    
    if st.session_state.finished:
        st.rerun() # 여기서 에러가 나면 아래 '결과 화면' 로직이 자동으로 실행됨
    else:
        st.write("### 다음 중 더 마음에 드는 곡은?")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(st.session_state.left[0], key="left_btn", use_container_width=True):
                st.session_state.current_merged.append(st.session_state.left.pop(0))
                if not st.session_state.left:
                    st.session_state.current_merged.extend(st.session_state.right)
                    st.session_state.right = []
                    st.session_state.merged_groups.append(st.session_state.current_merged)
                st.rerun() # 최신 버전 표준 명령어

        with col2:
            if st.button(st.session_state.right[0], key="right_btn", use_container_width=True):
                st.session_state.current_merged.append(st.session_state.right.pop(0))
                if not st.session_state.right:
                    st.session_state.current_merged.extend(st.session_state.left)
                    st.session_state.left = []
                    st.session_state.merged_groups.append(st.session_state.current_merged)
                st.rerun() # 최신 버전 표준 명령어
else:
    # 4. 결과 화면
    st.balloons()
    st.header("🏆 당신의 H2H 최애곡 순위")
    final_rank = st.session_state.groups[0]
    for i, song in enumerate(final_rank, 1):
        if i == 1:
            st.subheader(f"🥇 {i}위: {song}")
        elif i == 2:
            st.write(f"🥈 **{i}위**: {song}")
        elif i == 3:
            st.write(f"🥉 **{i}위**: {song}")
        else:
            st.write(f"{i}위: {song}")
    
    if st.button("다시 하기"):
        st.session_state.clear()
        st.rerun()