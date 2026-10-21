import streamlit as st
import random

# Cấu hình trang web game
st.set_page_config(page_title="Zombie Tsunami Streamlit", page_icon="🧟", layout="centered")

st.title("🧟 ZOMBIE TSUNAMI: STREAMLIT RUNNER")

# 1. Khởi tạo dữ liệu trò chơi (Session State)
if "zombies" not in st.session_state:
    st.session_state.zombies = 1
    st.session_state.distance = 0
    st.session_state.coins = 0
    st.session_state.game_over = False
    st.session_state.log = ["Bắt đầu hành trình với 1 Zombie cô đơn..."]
    st.session_state.current_event = None

# Hàm tạo sự kiện ngẫu nhiên trên đường đi
def generate_event():
    events = ["human", "car", "bus", "bomb", "pit", "coin_box"]
    weights = [0.35, 0.2, 0.1, 0.15, 0.1, 0.1]
    return random.choices(events, weights=weights)[0]

# 2. Bảng thông số (Dashboard)
col1, col2, col3 = st.columns(3)
col1.metric("🧟 Đàn Zombie", st.session_state.zombies)
col2.metric("🏃 Quãng đường", f"{st.session_state.distance}m")
col3.metric("🪙 Tiền xu", st.session_state.coins)

# Hiển thị đàn zombie bằng Biểu tượng
zombie_display = "🧟" * min(st.session_state.zombies, 25)
if st.session_state.zombies > 25:
    zombie_display += f" (+{st.session_state.zombies - 25})"
st.subheader(f"Đội quân: {zombie_display}")

st.divider()

# 3. Xử lý vòng lặp chơi
if not st.session_state.game_over:
    if st.session_state.current_event is None:
        st.session_state.current_event = generate_event()

    event = st.session_state.current_event

    # --- Sự kiện 1: Gặp Người ---
    if event == "human":
        st.info("🚶 Phát hiện 1 người dân đang đứng trên đường!")
        if st.button("🧟‍♂️ Cắn & Biến thành Zombie!"):
            st.session_state.zombies += 1
            st.session_state.distance += 10
            st.session_state.log.append("Đã cắn 1 người! Đàn Zombie tăng thêm 1 (+10m)!")
            st.session_state.current_event = None
            st.rerun()

    # --- Sự kiện 2: Gặp Xe Hơi ---
    elif event == "car":
        st.warning("🚗 Một chiếc XE HƠI ngáng đường! (Cần ít nhất 4 Zombie để lật)")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("💥 Lật xe!"):
                if st.session_state.zombies >= 4:
                    st.session_state.zombies += 2
                    st.session_state.distance += 15
                    st.session_state.coins += 5
                    st.session_state.log.append("Lật xe thành công! Thu phục thêm 2 Zombie (+5 Xu)!")
                else:
                    st.session_state.zombies -= 1
                    st.session_state.log.append("Không đủ lực! Xe tông trúng mất 1 Zombie!")
                st.session_state.current_event = None
                st.rerun()
        with col_b:
            if st.button("🦘 Nhảy né"):
                st.session_state.distance += 10
                st.session_state.log.append("Đã nhảy an toàn qua xe hơi (+10m)!")
                st.session_state.current_event = None
                st.rerun()

    # --- Sự kiện 3: Gặp Xe Bus ---
    elif event == "bus":
        st.warning("🚌 Một chiếc XE BUS đông đúc! (Cần ít nhất 8 Zombie để lật)")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("💥 Lật xe Bus!"):
                if st.session_state.zombies >= 8:
                    st.session_state.zombies += 4
                    st.session_state.distance += 20
                    st.session_state.coins += 15
                    st.session_state.log.append("LẬT BUS THÀNH CÔNG! Thu phục thêm 4 Zombie (+15 Xu)!")
                else:
                    st.session_state.zombies = max(0, st.session_state.zombies - 3)
                    st.session_state.log.append("Thất bại! Bị xe bus đâm mất 3 Zombie!")
                st.session_state.current_event = None
                st.rerun()
        with col_b:
            if st.button("🦘 Nhảy né"):
                st.session_state.distance += 10
                st.session_state.log.append("Né xe bus thành công (+10m)!")
                st.session_state.current_event = None
                st.rerun()

    # --- Sự kiện 4: Gặp Bom ---
    elif event == "bomb":
        st.error("💣 NGUY HIỂM! Một quả BOM phía trước!")
        if st.button("🦘 Bật nhảy nhanh!"):
            if random.random() > 0.25:
                st.session_state.distance += 15
                st.session_state.log.append("Nhảy qua bom an toàn (+15m)!")
            else:
                loss = random.randint(1, 2)
                st.session_state.zombies = max(0, st.session_state.zombies - loss)
                st.session_state.log.append(f"Vấp phải bom nổ! Mất {loss} Zombie!")
            st.session_state.current_event = None
            st.rerun()

    # --- Sự kiện 5: Gặp Hố Sâu ---
    elif event == "pit":
        st.error("🕳️ HỐ SÂU nguy hiểm!")
        if st.button("🦘 Nhảy xa qua hố!"):
            st.session_state.distance += 10
            st.session_state.log.append("Nhảy qua hố thành công (+10m)!")
            st.session_state.current_event = None
            st.rerun()

    # --- Sự kiện 6: Nhặt Hộp Xu ---
    elif event == "coin_box":
        st.success("📦 Bạn nhặt được một Hộp Tiền Xu!")
        if st.button("🪙 Nhặt Xu"):
            earned = random.randint(5, 20)
            st.session_state.coins += earned
            st.session_state.distance += 10
            st.session_state.log.append(f"Nhặt thành công {earned} Tiền xu!")
            st.session_state.current_event = None
            st.rerun()

    # Thua game khi số Zombie = 0
    if st.session_state.zombies <= 0:
        st.session_state.game_over = True
        st.rerun()

# 4. Màn hình Game Over
else:
    st.error("☠️ GAME OVER! Đàn Zombie của bạn đã bị tiêu diệt hoàn toàn!")
    st.write(f"🏆 Thành tích: **{st.session_state.distance}m** | Tiền xu: **{st.session_state.coins} xu**")
    
    if st.button("🔄 Chơi lại từ đầu"):
        st.session_state.zombies = 1
        st.session_state.distance = 0
        st.session_state.coins = 0
        st.session_state.game_over = False
        st.session_state.log = ["Bắt đầu lại hành trình!"]
        st.session_state.current_event = None
        st.rerun()

# 5. Nhật ký hoạt động
st.divider()
st.subheader("📜 Nhật ký hành trình")
for log_item in reversed(st.session_state.log[-5:]):
    st.write(f"- {log_item}")
