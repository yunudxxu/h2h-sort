import streamlit as st

st.set_page_config(page_title="H2H Song Sort", page_icon="🎵")

# 1. 노래 리스트
SONGS = [
    "The Chase", "Butterflies", "STYLE", "Pretty Please", 
    "FOCUS", "Apple Pie", "Flutter", "Blue Moon", "RUDE!"
]

# 2. 데이터 초기화 (정말 단순한 인덱스 기반 대결)
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.pool = [[s] for s in SONGS]
    st.session_state.merged = []
    st.session_state.left = []
    st.session_state.right = []
    st.session_state.temp_result = []
    st.session_state.game_over = False

st.title("❤️ Hearts2Hearts Song Sort")

# 3. 대결 로직 함수
def prepare_next_battle():
    # 더 이상 대결할 그룹이 없을 때
    if len(st.session_state.pool) < 2 and not st.session_state.left:
        if not st.session_state.merged: # 진짜 끝남
            st.session_state.game_over = True
        else: # 다음 라운드로 진행
            st.session_state.pool.extend(st.session_state.merged)
            st.session_state.merged = []
            prepare_next_battle()
    
    # 새로운 대결 쌍 설정
    if not st.session_state.left and not st.session_state.game_over:
        if len(st.session_state.pool) >= 2:
            st.session_state.left = st.session_state.pool.pop(0)
            st.session_state.right = st.session_state.pool.pop(0)
            st.session_state.temp_result = []

# 4. 화면 표시
if not st.session_state.game_over:
    prepare_next_battle()
    
    if st.session_state.game_over:
        st.rerun()
    else:
        st.write(f"### 다음 중 더 마음에 드는 곡은?")
        st.progress(len(st.session_state.merged) / (len(SONGS)//2 + 1)) # 진행도 표시
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(st.session_state.left[0], key="L", use_container_width=True):
                st.session_state.temp_result.append(st.session_state.left.pop(0))
                if not st.session_state.left:
                    st.session_state.temp_result.extend(st.session_state.right)
                    st.session_state.right = []
                    st.session_state.merged.append(st.session_state.temp_result)
                    st.session_state.left = [] # 대결 종료 표시
                st.rerun()

        with col2:
            if st.button(st.session_state.right[0], key="R", use_container_width=True):
                st.session_state.temp_result.append(st.session_state.right.pop(0))
                if not st.session_state.right:
                    st.session_state.temp_result.extend(st.session_state.left)
                    st.session_state.left = []
                    st.session_state.merged.append(st.session_state.temp_result)
                    st.session_state.left = [] # 대결 종료 표시
                st.rerun()
else:
    # 5. 결과 화면 (무조건 여기서만 뜸)
    st.balloons()
    st.header("🏆 당신의 H2H 최애곡 순위")
    
    # 최종 결과 리스트 추출
    final_list = st.session_state.pool[0] if st.session_state.pool else []
    
    for i, song in enumerate(final_list, 1):
        if i == 1: st.subheader(f"🥇 1위: {song}")
        elif i == 2: st.write(f"🥈 **2위**: {song}")
        elif i == 3: st.write(f"🥉 **3위**: {song}")
        else: st.write(f"{i}위: {song}")
    
    if st.button("다시 하기"):
        st.session_state.clear()
        st.rerun()