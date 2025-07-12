import streamlit as st
import requests

st.title("🧪 WasteWise AI - Chat Tester")

# Input for item_id and message
item_id = st.text_input("Item ID", value="WMBE8D91")
message = st.text_area("Your Question", placeholder="Ask something about this item...")

if st.button("Send to AI"):
    if not item_id or not message:
        st.warning("Please enter both Item ID and a question.")
    else:
        try:
            with st.spinner("Contacting WasteWise AI..."):
                response = requests.post(
                    "http://localhost:8000/chat",
                    json={"item_id": item_id, "message": message}
                )
                data = response.json()

                # ✅ Log response to terminal
                print("🧠 AI Raw Response:", data)

                st.success("✅ AI Response:")
                st.write(data.get("reply", "No reply returned."))
        except Exception as e:
            st.error(f"❌ Request failed: {e}")
