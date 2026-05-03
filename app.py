import streamlit as st

st.set_page_config(page_title="H2H Song Sort", page_icon="🎵")

# 1. 초기 노래 리스트 설정
if 'songs' not in st.session_state:
    st.session_state.songs = [
        "The Chase", "Butterflies", "STYLE", "Pretty Please", 
        "FOCUS", "Apple Pie", "Flutter", "Blue Moon", "RUDE!"
    ]
    # 병합 정렬을 위한 초기 상태 (각 곡을 개별 리스트로 분리)
    st.session_state.groups = [[s] for s in st.session_state.songs]
    st.session_state.merged_groups = []
    st.session_state.left = []
    st.session_state.right = []
    st.session_state.current_merged = []
    st.session_state.finished = False

st.title("❤️ Hearts2Hearts Song Sort")

# 2. 정렬 로직 (버튼 클릭 시마다 실행)
def process():
    # 더 이상 합칠 그룹이 없고 대결 중인 그룹도 없으면 끝!
    if len(st.session_state.groups) <= 1 and not st.session_state.left and not st.session_state.right:
        st.session_state.finished = True
        return

    # 새로운 대결 쌍 만들기
    if not st.session_state.left and not st.session_state.right:
        if len(st.session_state.groups) >= 2:
            st.session_state.left = st.session_state.groups.pop(0)
            st.session_state.right = st.session_state.groups.pop(0)
            st.session_state.current_merged = []
        else:
            # 남은 그룹들을 다음 단계로 넘김
            st.session_state.groups.extend(st.session_state.merged_groups)
            st.session_state.merged_groups = []
            process()

# 3. 화면 표시
if not st.session_state.finished:
    process()
    if st.session_state.finished:
        st.balloons()
        st.success("✨ 당신의 취향 순위가 결정되었습니다!")
        final_list = st.session_state.groups[0]
        for i, song in enumerate(final_list, 1):
            st.write(f"### {i}위: {song}")
    else:
        st.write("### 다음 중 더 마음에 드는 곡은?")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(st.session_state.left[0], use_container_width=True):
                st.session_state.current_merged.append(st.session_state.left.pop(0))
                if not st.session_state.left:
                    st.session_state.current_merged.extend(st.session_state.right)
                    st.session_state.right = []
                    st.session_state.merged_groups.append(st.session_state.current_merged)
                st.rerun()

        with col2:
            if st.button(st.session_state.right[0], use_container_width=True):
                st.session_state.current_merged.append(st.session_state.right.pop(0))
                if not st.session_state.right:
                    st.session_state.current_merged.extend(st.session_state.left)
                    st.session_state.left = []
                    st.session_state.merged_groups.append(st.session_state.current_merged)
                st.rerun()
else:
    st.balloons()
    st.header("🏆 당신의 H2H 최애곡 순위")
    final_list = st.session_state.groups[0]
    for i, song in enumerate(final_list, 1):
        # 1등은 더 크게 강조!
        if i == 1:
            st.subheader(f"🥇 {i}위: {song}")
        else:
            st.write(f"**{i}위**: {song}")
    
    if st.button("다시 하기"):
        st.session_state.clear()
        st.rerun()