import streamlit as st
import random

# 1. Cấu hình trang web game
st.set_page_config(page_title="Zombie Tsunami Game", page_icon="🧟", layout="centered")

# URL ảnh nền chuẩn Zombie Tsunami (đã tối ưu hóa hiển thị)
BACKGROUND_URL = "https://raw.githubusercontent.com/streamlit/app-examples/main/zombie_bg.jpg"
# Sử dụng trực tiếp ảnh thành phố Zombie Tsunami làm nền
IMAGE_BG_URL = "https://i.ibb.co/3s2mP4B/zombie-tsunami-bg.jpg" # Ảnh nền phong cách thành phố gốc

# 2. Cài đặt CSS để đổi NỀN TOÀN BỘ GAME thành ảnh Zombie Tsunami
st.markdown(
    f"""
    <style>
    /* Đổi hình nền chính của ứng dụng */
    .stApp {{
        background-image: url("https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=1600");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* Làm nền thẻ chứa nội dung tối lại chút để dễ đọc chữ */
    .main .block-container {{
        background-color: rgba(0, 0, 0, 0.75);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 0px 20px rgba(0, 255, 0, 0.3);
    }}

    /* Tùy chỉnh màu chữ và tiêu đề */
    h1, h2, h3, p, span {{
        color: #FFFFFF !important;
        text-shadow: 2px 2px 4px #000000;
    }}
    
    /* Thiết kế nút bấm phong cách Game */
    .stButton>button {{
        width: 100%;
        background-color: #2e7d32 !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border-radius: 10px !important;
        border: 2px solid #fff !important;
        padding: 10px !important;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background-color: #4caf50 !important;
        transform: scale(1.03);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Chèn thêm ảnh banner hình nền thành phố chuẩn Zombie Tsunami lên phía trên
st.image("https://i.ibb.co/68v8PZM/zombie-tsunami-city.jpg", use_column_width=True)

st.title("🧟 ZOMBIE TSUNAMI STREAMLIT")

# 3. Khởi tạo trạng thái game (Session State)
if "zombies" not in st.session_state:
    st.session_state.zombies = 5  # Bắt đầu với 5 zombie như trong ảnh gốc
    st.session_state.distance = 0
    st.session_state.coins = 0
    st.session_state.game_over = False
    st.session_state.log = ["Đàn Zombie 5 con bắt đầu tràn ra đường phố!"]
    st.session_state.current_event = None

# Hàm tạo sự kiện ngẫu nhiên trên đường
def generate_event():
    events = ["human", "car", "bus", "bomb", "pit", "coin_box"]
    weights = [0.35, 0.2, 0.1, 0.15, 0.1, 0.1]
    return random.choices(events, weights=weights)[0]

# 4. Bảng điểm và số lượng Zombie
col1, col2, col3 = st.columns(3)
col1.metric("🧟 Số Zombie", st.session_state.zombies)
col2.metric("🏃 Quãng đường", f"{st.session_state.distance}m")
col3.metric("🪙 Tiền xu", st.session_state.coins)

# Hiển thị đàn Zombie bằng Icon sinh động
zombie_icons = "🧟" * min(st.session_state.zombies, 20)
if st.session_state.zombies > 20:
    zombie_icons += f" (+{st.session_state.zombies - 20})"
st.subheader(f"Đội quân Zombie: {zombie_icons}")

st.divider()

# 5. Vòng lặp chơi game
if not st.session_state.game_over:
    if st.session_state.current_event is None:
        st.session_state.current_event = generate_event()

    event = st.session_state.current_event

    # --- Sự kiện 1: Gặp Người ---
    if event == "human":
        st.info("🚶 Bạn phát hiện một nhóm người dân trên cầu!")
        if st.button("🧟‍♂️ Cắn & Biến thành Zombie!"):
            st.session_state.zombies += 1
            st.session_state.distance += 10
            st.session_state.log.append("Cắn thành công 1 người (+1 Zombie, +10m)!")
            st.session_state.current_event = None
            st.rerun()

    # --- Sự kiện 2: Gặp Xe Hơi ---
    elif event == "car":
        st.warning("🚗 Một chiếc XE HƠI đỗ trên đường! (Cần 4 Zombie để lật)")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("💥 Lật xe!"):
                if st.session_state.zombies >= 4:
                    st.session_state.zombies += 2
                    st.session_state.distance += 15
                    st.session_state.coins += 5
                    st.session_state.log.append("Lật xe thành công! Thu phục 2 Zombie (+5 Xu)!")
                else:
                    st.session_state.zombies -= 1
                    st.session_state.log.append("Không đủ lực lật xe! Mất 1 Zombie!")
                st.session_state.current_event = None
                st.rerun()
        with col_b:
            if st.button("🦘 Nhảy qua xe"):
                st.session_state.distance += 10
                st.session_state.log.append("Nhảy qua xe hơi an toàn (+10m)!")
                st.session_state.current_event = None
                st.rerun()

    # --- Sự kiện 3: Gặp Xe Bus ---
    elif event == "bus":
        st.warning("🚌 Một chiếc XE BUS chật kín người! (Cần 8 Zombie để lật)")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("💥 Lật Xe Bus!"):
                if st.session_state.zombies >= 8:
                    st.session_state.zombies += 4
                    st.session_state.distance += 20
                    st.session_state.coins += 15
                    st.session_state.log.append("LẬT BUS THÀNH CÔNG! Thu phục 4 Zombie (+15 Xu)!")
                else:
                    st.session_state.zombies = max(0, st.session_state.zombies - 3)
                    st.session_state.log.append("Không đủ lượng! Bị xe bus đâm mất 3 Zombie!")
                st.session_state.current_event = None
                st.rerun()
        with col_b:
            if st.button("🦘 Nhảy né"):
                st.session_state.distance += 10
                st.session_state.log.append("Né xe bus an toàn (+10m)!")
                st.session_state.current_event = None
                st.rerun()

    # --- Sự kiện 4: Gặp Bom ---
    elif event == "bomb":
        st.error("💣 NGUY HIỂM! Bom đếm ngược giữa đường!")
        if st.button("🦘 Bấm nút NHẢY ngay!"):
            if random.random() > 0.2:
                st.session_state.distance += 15
                st.session_state.log.append("Nhảy né quả bom mượt mà (+15m)!")
            else:
                loss = random.randint(1, 2)
                st.session_state.zombies = max(0, st.session_state.zombies - loss)
                st.session_state.log.append(f"Vấp bom nổ! Mất {loss} Zombie!")
            st.session_state.current_event = None
            st.rerun()

    # --- Sự kiện 5: Gặp Hố Sâu ---
    elif event == "pit":
        st.error("🕳️ HỐ SÂU đứt đoạn cầu!")
        if st.button("🦘 Nhảy xa qua hố!"):
            st.session_state.distance += 10
            st.session_state.log.append("Đã nhảy an toàn qua hố sâu (+10m)!")
            st.session_state.current_event = None
            st.rerun()

    # --- Sự kiện 6: Nhặt Xu ---
    elif event == "coin_box":
        st.success("📦 Bạn thấy Hộp Xu trên đường!")
        if st.button("🪙 Nhặt Xu"):
            earned = random.randint(5, 20)
            st.session_state.coins += earned
            st.session_state.distance += 10
            st.session_state.log.append(f"Nhặt được {earned} coins!")
            st.session_state.current_event = None
            st.rerun()

    # Thua game
    if st.session_state.zombies <= 0:
        st.session_state.game_over = True
        st.rerun()

# 6. Màn hình Game Over
else:
    st.error("☠️ GAME OVER! Toàn bộ đàn Zombie của bạn đã gục ngã!")
    st.write(f"🏆 Tổng quãng đường: **{st.session_state.distance}m** | Tiền xu: **{st.session_state.coins} xu**")
    
    if st.button("🔄 Chơi lại game mới"):
        st.session_state.zombies = 5
        st.session_state.distance = 0
        st.session_state.coins = 0
        st.session_state.game_over = False
        st.session_state.log = ["Khởi động lại đàn Zombie!"]
        st.session_state.current_event = None
        st.rerun()

# 7. Nhật ký hành trình
st.divider()
st.subheader("📜 Nhật ký cuộc chạy")
for log_item in reversed(st.session_state.log[-5:]):
    st.write(f"- {log_item}")
