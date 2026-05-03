import streamlit as st

st.set_page_config(page_title="H2H Song Sort", page_icon="🎵")

# 세션 상태 초기화
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

def process():
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
            process()

if not st.session_state.finished:
    process()
    if st.session_state.finished:
        st.balloons()
        st.header("🏆 당신의 H2H 최애곡 순위")
        final_list = st.session_state.groups[0]
        for i, song in enumerate(final_list, 1):
            if i == 1: st.subheader(f"🥇 {i}위: {song}")
            else: st.write(f"**{i}위**: {song}")
    else:
        st.write("### 다음 중 더 마음에 드는 곡은?")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(st.session_state.left[0], key="btn1", use_container_width=True):
                st.session_state.current_merged.append(st.session_state.left.pop(0))
                if not st.session_state.left:
                    st.session_state.current_merged.extend(st.session_state.right)
                    st.session_state.right = []
                    st.session_state.merged_groups.append(st.session_state.current_merged)
                st.experimental_rerun() # 구버전 환경에서도 돌아가도록 수정

        with col2:
            if st.button(st.session_state.right[0], key="btn2", use_container_width=True):
                st.session_state.current_merged.append(st.session_state.right.pop(0))
                if not st.session_state.right:
                    st.session_state.current_merged.extend(st.session_state.left)
                    st.session_state.left = []
                    st.session_state.merged_groups.append(st.session_state.current_merged)
                st.experimental_rerun() # 구버전 환경에서도 돌아가도록 수정
else:
    st.balloons()
    st.header("🏆 당신의 H2H 최애곡 순위")
    final_list = st.session_state.groups[0]
    for i, song in enumerate(final_list, 1):
        if i == 1: st.subheader(f"🥇 {i}위: {song}")
        else: st.write(f"**{i}위**: {song}")
    
    if st.button("다시 하기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()