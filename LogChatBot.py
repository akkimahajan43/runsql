import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import pandas as pd
import os
import uuid
import time
from datetime import datetime

# ======================================================
# LOAD ENV VARIABLES
# ======================================================
load_dotenv()

# ======================================================
# STREAMLIT PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ======================================================
# PAGE TITLE
# ======================================================
st.title("🤖 AI Chatbot with CSV Logging")

# ======================================================
# INITIALIZE GROQ CLIENT
# ======================================================
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# ======================================================
# SESSION STATE
# ======================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# ======================================================
# DISPLAY CHAT HISTORY
# ======================================================
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ======================================================
# USER INPUT
# ======================================================
prompt = st.chat_input("Type your message here...")

# ======================================================
# PROCESS USER MESSAGE
# ======================================================
if prompt:

    # --------------------------------------------------
    # STORE USER MESSAGE
    # --------------------------------------------------
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # --------------------------------------------------
    # DISPLAY USER MESSAGE
    # --------------------------------------------------
    with st.chat_message("user"):
        st.markdown(prompt)

    # --------------------------------------------------
    # ASSISTANT RESPONSE AREA
    # --------------------------------------------------
    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        start_time = time.time()

        status = "Success"
        error_message = ""

        try:

            # ==========================================
            # API CALL
            # ==========================================
            response = client.chat.completions.create(

                model="llama-3.3-70b-versatile",

                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant"
                    },
                    *st.session_state.messages
                ],

                stream=False
            )

            # ==========================================
            # ASSISTANT RESPONSE
            # ==========================================
            assistant_reply = (
                response
                .choices[0]
                .message
                .content
            )

            response_placeholder.markdown(
                assistant_reply
            )

            # ==========================================
            # TOKEN USAGE
            # ==========================================
            prompt_tokens = (
                response
                .usage
                .prompt_tokens
            )

            completion_tokens = (
                response
                .usage
                .completion_tokens
            )

            total_tokens = (
                response
                .usage
                .total_tokens
            )

            # ==========================================
            # TOKEN PRICING
            # Update pricing as per model/provider
            # ==========================================
            input_price_per_million = 0.27
            output_price_per_million = 0.59

            # ==========================================
            # INPUT TOKEN COST
            # ==========================================
            prompt_cost_usd = round(
                (
                        prompt_tokens / 1_000_000
                ) * input_price_per_million,
                8
            )

            # ==========================================
            # OUTPUT TOKEN COST
            # ==========================================
            completion_cost_usd = round(
                (
                        completion_tokens / 1_000_000
                ) * output_price_per_million,
                8
            )

            # ==========================================
            # TOTAL COST
            # ==========================================
            total_cost_usd = round(
                prompt_cost_usd +
                completion_cost_usd,
                8
            )

        except Exception as e:

            assistant_reply = (
                "Error while generating response."
            )

            response_placeholder.error(
                assistant_reply
            )

            prompt_tokens = 0
            completion_tokens = 0
            total_tokens = 0
            estimated_cost = 0

            status = "Failed"

            error_message = str(e)

        # ==============================================
        # RESPONSE TIME
        # ==============================================
        end_time = time.time()

        response_time = round(
            end_time - start_time,
            2
        )

        # ==============================================
        # SAVE ASSISTANT MESSAGE
        # ==============================================
        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_reply
        })
        # ==============================================
        # WORD COUNT
        # ==============================================
        response_word_count = len(
            assistant_reply.split()
        )

        # ==============================================
        # SENTENCE COUNT
        # ==============================================
        response_sentence_count = len([
            sentence
            for sentence in assistant_reply
                .replace("?", ".")
                .replace("!", ".")
                .split(".")
            if sentence.strip()
        ])

        # ==============================================
        # CREATE LOG RECORD
        # ==============================================
        log_data = {

            # ------------------------------------------
            # TIMESTAMP
            # ------------------------------------------
            "timestamp":
                datetime.now(),

            "date":
                datetime.now().strftime("%Y-%m-%d"),

            "time":
                datetime.now().strftime("%H:%M:%S"),

            # ------------------------------------------
            # SESSION ID
            # ------------------------------------------
            "session_id":
                st.session_state.session_id,

            # ------------------------------------------
            # CHAT DATA
            # ------------------------------------------
            "user_input":
                prompt,

            "assistant_response":
                assistant_reply,

            # ------------------------------------------
            # RESPONSE ANALYTICS
            # ------------------------------------------
            "response_word_count":
                response_word_count,

            "response_sentence_count":
                response_sentence_count,

            # ------------------------------------------
            # TOKEN ANALYTICS
            # ------------------------------------------
            "prompt_tokens":
                prompt_tokens,

            "completion_tokens":
                completion_tokens,

            "total_tokens":
                total_tokens,

            # ------------------------------------------
            # COST ANALYTICS
            # ------------------------------------------
            "prompt_cost_usd":
                prompt_cost_usd,

            "completion_cost_usd":
                completion_cost_usd,

            "total_cost_usd":
                total_cost_usd,

            # ------------------------------------------
            # LATENCY ANALYTICS
            # ------------------------------------------
            "response_time_sec":
                response_time
        }

        # ==============================================
        # CREATE LOGS FOLDER
        # ==============================================
        log_folder = "logs"

        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        # ==============================================
        # DATE-WISE FILE NAME
        # ==============================================
        current_date = datetime.now().strftime(
            "%Y-%m-%d"
        )

        file_name = (
            f"{log_folder}/"
            f"chatbot_logs_{current_date}.csv"
        )

        # ==============================================
        # CONVERT TO DATAFRAME
        # ==============================================
        df = pd.DataFrame([log_data])

        # ==============================================
        # SAVE TO CSV
        # ==============================================
        if os.path.exists(file_name):

            df.to_csv(
                file_name,
                mode="a",
                header=False,
                index=False
            )

        else:

            df.to_csv(
                file_name,
                index=False
            )

# ======================================================
# SIDEBAR ANALYTICS
# ======================================================
with st.sidebar:

    st.header("📊 Chatbot Analytics")

    log_folder = "logs"

    if os.path.exists(log_folder):

        all_files = [
            os.path.join(log_folder, file)
            for file in os.listdir(log_folder)
            if file.endswith(".csv")
        ]

        if len(all_files) > 0:

            combined_df = pd.concat(
                [pd.read_csv(file) for file in all_files],
                ignore_index=True
            )

            # ------------------------------------------
            # TOTAL CONVERSATIONS
            # ------------------------------------------
            st.metric(
                "Total Conversations",
                len(combined_df)
            )

            # ------------------------------------------
            # TOTAL TOKENS
            # ------------------------------------------
            st.metric(
                "Total Tokens",
                int(
                    combined_df["total_tokens"].sum()
                )
            )

            # ------------------------------------------
            # TOTAL COST
            # ------------------------------------------
            st.metric(
                "Total Cost ($)",
                round(
                    combined_df[
                        "estimated_cost_usd"
                    ].sum(),
                    6
                )
            )

            # ------------------------------------------
            # AVG RESPONSE TIME
            # ------------------------------------------
            st.metric(
                "Avg Response Time (sec)",
                round(
                    combined_df[
                        "response_time_sec"
                    ].mean(),
                    2
                )
            )

            # ------------------------------------------
            # TOTAL SESSIONS
            # ------------------------------------------
            st.metric(
                "Unique Sessions",
                combined_df[
                    "session_id"
                ].nunique()
            )

            # ------------------------------------------
            # DOWNLOAD BUTTON
            # ------------------------------------------
            csv = combined_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="⬇ Download Logs",
                data=csv,
                file_name="chatbot_logs.csv",
                mime="text/csv"
            )

# ======================================================
# FOOTER
# ======================================================
st.markdown("---")
st.caption(
    "AI Chatbot with Token Usage, Cost Tracking & CSV Logging"
)