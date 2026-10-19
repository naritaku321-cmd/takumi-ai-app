import streamlit as st
import os
from google import genai
from PIL import Image

st.set_page_config(
    page_title="農・醸の匠 AI - 現場の即時判断ツール",
    page_icon="🌾",
    layout="centered"
)

st.title("🌾 農・醸の匠 AI")
st.caption("公式技術指導データ × 現場画像解析による即時判断・診断システム")

with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Gemini API Key", type="password")
    st.markdown("---")
    st.markdown("※APIキーはGoogle AI Studioで無料取得できます。")

uploaded_file = st.file_uploader("📷 現場の写真（作物・病害虫・土壌など）をアップロード", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロードされた現場写真", use_column_width=True)

user_query = st.text_input("💬 相談内容・気になっている症状", value="葉に変な斑点が出てきたのですが、これは何ですか？")

if st.button("🔍 現場の匠AIに診断させる"):
    if not api_key:
        st.error("サイドバーにGemini APIキーを入力してください。")
    elif uploaded_file is None:
        st.warning("診断する画像をアップロードしてください。")
    else:
        with st.spinner("画像を解析し、公式技術データと照合中..."):
            try:
                client = genai.Client(api_key=api_key)
                context = """
                【公式技術指導指針データ】
                - いもち病の初期症状：葉に褐色の小さな斑点が出現。気温25度前後、多湿条件で急激に蔓延する。
                  対処法：発見次第、速やかな予防的散布が必要。放置すると減収に直結する。
                - 高温障害・水管理：出穂期前後は深水（5〜10cm）が基本だが、砂質土壌では根腐れ防止のため間断灌水に切り替える。
                """
                prompt = f"""
                あなたは熟練の専門指導員・匠の意思を受け継いだ、実用的な現場診断AIです。
                提供された【現場の写真】と【公式技術データ】に基づき、現場のワーカーに向けて「結論ファースト」で的確かつ妥協のないアドバイスを行ってください。

                【公式技術データ】
                {context}

                【現場からの相談内容】
                {user_query}

                以下の形式で出力してください：
                1. 【結論・今すぐ取るべき処置】（1〜2文で最も重要なアクションを明記）
                2. 【技術的根拠・公式データ】（なぜその処置が必要か、数値や条件を明記）
                3. 【プロの戒め・注意点】（初心者が陥りがちな見落としやリスク）
                """
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=[image, prompt]
                )
                st.success("診断が完了しました！")
                st.markdown("### 📋 診断・指示結果")
                st.write(response.text)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
