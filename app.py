# import seaborn as sns
# import streamlit as st
# import matplotlib.pyplot as plt
# import preprocessor, helper
# from helper import most_common_words
#
# st.sidebar.title("ChatSense Chat Analyzer")
#
# uploaded_file = st.sidebar.file_uploader("Choose a file")
# if uploaded_file is not None:
#     # To read file as bytes:
#     bytes_data = uploaded_file.getvalue()
#     data = bytes_data.decode("utf-8")
#     # st.text(data)
#     df = preprocessor.preprocess(data)
#
#     # st.dataframe(df)
#
#     #fetch unique users
#     user_list = df['user'].unique().tolist()
#     user_list.remove('group_notification')
#     user_list.sort()
#     user_list.insert(0, "Overall")
#
#     selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
#
#     if st.sidebar.button("Show Analysis"):
#
#         st.title("Top Statistics")
#         # Stats Area
#         num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
#         col1, col2, col3, col4 = st.columns(4)
#
#         with col1:
#             st.header("Total Messages")
#             st.title(num_messages)
#         with col2:
#             st.header("Total Words")
#             st.title(words)
#         with col3:
#             st.header("Media Shared")
#             st.title(num_media_messages)
#         with col4:
#             st.header("Links Shared")
#             st.title(num_links)
#
#         # monthly timeline
#         st.title("Monthly Timeline")
#         timeline = helper.monthly_timeline(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.plot(timeline['time'], timeline['message'], color='green')
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)
#
#         # daily timeline
#         st.title("Daily Timeline")
#         daily_timeline = helper.daily_timeline(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)
#
#         # # activity map
#         st.title('Activity Map')
#         col1, col2 = st.columns(2)
#
#         with col1:
#             st.header("Most busy day")
#             busy_day = helper.week_activity_map(selected_user, df)
#             fig, ax = plt.subplots()
#             ax.bar(busy_day.index, busy_day.values, color='purple')
#             plt.xticks(rotation='vertical')
#             st.pyplot(fig)
#
#         with col2:
#             st.header("Most busy month")
#             busy_month = helper.month_activity_map(selected_user, df)
#             fig, ax = plt.subplots()
#             ax.bar(busy_month.index, busy_month.values, color='orange')
#             plt.xticks(rotation='vertical')
#             st.pyplot(fig)
#
#         st.title("Weekly Activity Map")
#         user_heatmap = helper.activity_heatmap(selected_user, df)
#         fig, ax = plt.subplots()
#         ax = sns.heatmap(user_heatmap)
#         st.pyplot(fig)
#
#
#         #finding the busiest users in the group(Group level)
#         if selected_user == "Overall":
#             st.title('Most Busy Users')
#             x, new_df = helper.most_busy_users(df)
#             fig, ax = plt.subplots()
#
#             col1, col2 = st.columns(2)
#
#             with col1:
#                 ax.bar(x.index, x.values, color='red')
#                 plt.xticks(rotation='vertical')
#                 st.pyplot(fig)
#             with col2:
#                 st.dataframe(new_df)
#
#         # WordCloud
#         st.title("Word Cloud")
#         df_wc = helper.create_wordCloud(selected_user, df)
#         fig, ax = plt.subplots()
#         plt.imshow(df_wc)
#         st.pyplot(fig)
#
#         #most common words
#         most_common_df = helper.most_common_words(selected_user, df)
#
#         fig, ax = plt.subplots()
#         ax.barh(most_common_df[0], most_common_df[1])
#         plt.xticks(rotation='vertical')
#
#         st.title("Most Common Words")
#         st.pyplot(fig)
#         # st.dataframe(most_common_df)
#
#         # emoji analysis
#         emoji_df = helper.emoji_helper(selected_user, df)
#         st.title("Emoji Analysis")
#
#         col1, col2 = st.columns(2)
#
#         with col1:
#             st.dataframe(emoji_df)
#         with col2:
#             fig, ax = plt.subplots()
#             ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
#             st.pyplot(fig)


import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import preprocessor, helper
import datetime
import time

# Set page configuration for Streamlit app
st.set_page_config(
    page_title="ChatSense Chat Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Logo - styled 'CS' with red and white colors using HTML & CSS
st.sidebar.markdown(
    """
    <div style="background-color:#B22222; padding:15px; text-align:center; border-radius:8px; margin-bottom:10px;">
        <span style="color:white; font-weight:bold; font-size:32px; font-family:monospace;">C</span>
        <span style="color:#B22222; background:white; font-weight:bold; font-size:32px; font-family:monospace; padding:0 6px; border-radius:4px;">S</span>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar title and description
st.sidebar.title("🧠 ChatSense Chat Analyzer")
st.sidebar.markdown("Upload your WhatsApp chat export text file and explore insightful analytics! 🚀")

# Initialize session state
if "show_analysis" not in st.session_state:
    st.session_state["show_analysis"] = False


# File uploader to upload WhatsApp chat .txt file
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["txt"])


# Check if a file is uploaded
if uploaded_file is not None:
    # Read uploaded file bytes and decode to string
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # Preprocess raw chat data into a DataFrame
    # df = preprocessor.preprocess(data)

    with st.spinner("Analyzing your chat..."):
        df = preprocessor.preprocess(data)
        time.sleep(1)  # optional: simulate delay


    # Fetch unique users from chat excluding 'group_notification'
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")  # Add 'Overall' option for aggregate analysis

    # Dropdown to select user or overall chat analysis
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    # Button triggers analysis display
    # When button is clicked, set session state to True
    if st.sidebar.button("Show Analysis"):
        st.session_state["show_analysis"] = True

    #  Only show analysis if session state is True
    if st.session_state["show_analysis"]:

        # Top statistics section
        st.markdown("## 📊 Top Statistics")
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        # Display key metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💬 Total Messages", f"{num_messages}")
        col2.metric("📝 Total Words", f"{words}")
        col3.metric("🖼️ Media Shared", f"{num_media_messages}")
        col4.metric("🔗 Links Shared", f"{num_links}")

        # Monthly timeline plot inside expandable container
        with st.expander("📅 Monthly Timeline"):
            timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(12, 4))
            ax.plot(timeline['time'], timeline['message'], color='green', marker='o')
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)

        # Daily timeline plot inside expandable container
        with st.expander("📅 Daily Timeline"):
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(12, 4))
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black', marker='o')
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)

        # Activity Map section showing busiest day and month
        st.markdown("## 🔥 Activity Map")
        col1, col2 = st.columns(2)

        # Most busy day bar chart
        with col1:
            st.subheader("📅 Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Most busy month bar chart
        with col2:
            st.subheader("📆 Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Weekly activity heatmap visualization
        st.markdown("## 📅 Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(12, 4))
        sns.heatmap(user_heatmap, cmap='YlGnBu', linewidths=0.5, linecolor='gray', ax=ax)
        st.pyplot(fig)

        # Show most busy users only if overall analysis selected
        if selected_user == "Overall":
            st.markdown("## 👥 Most Busy Users")
            x, new_df = helper.most_busy_users(df)
            col1, col2 = st.columns([3, 2])

            # Bar chart for top users
            with col1:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation=45)
                st.pyplot(fig)

            # Dataframe with percentages of user activity
            with col2:
                st.dataframe(new_df.style.highlight_max(axis=0))

        # Word Cloud section
        st.markdown("## ☁️ Word Cloud")
        df_wc = helper.create_wordCloud(selected_user, df)

        # Display word cloud if available, else show warning
        if df_wc is not None:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.imshow(df_wc)
            ax.axis('off')
            st.pyplot(fig)
        else:
            st.warning("😕 No sufficient words found to generate a Word Cloud for this user.")

        # Most common words bar chart
        st.markdown("## 📝 Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        if most_common_df.empty:
            st.warning("😕 No common words found for this user.")
        else:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.barh(most_common_df[0], most_common_df[1], color='teal')
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Emoji analysis section
        st.markdown("## 😀 Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)
        with col1:
            # Display emoji dataframe or warning if empty
            if emoji_df.empty:
                st.warning("😕 No emojis found for this user.")
            else:
                st.dataframe(emoji_df)
        with col2:
            # Display pie chart of top emojis if data is available
            if not emoji_df.empty:
                fig, ax = plt.subplots(figsize=(5, 5))
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f%%", startangle=140, colors=sns.color_palette("pastel"))
                st.pyplot(fig)


        # ---- DOWNLOAD CSV ----
        st.markdown("## 📥 Download Stats")
        user_df = df[df['user'] == selected_user] if selected_user != "Overall" else df
        csv = user_df.to_csv(index=False)
        st.download_button("Download Raw Chat Data as CSV", data=csv, file_name='chat_data.csv', mime='text/csv')


# import datetime

if uploaded_file is not None:
    # ... all your analysis code here ...

    # Footer at the end of the app
    current_year = datetime.datetime.now().year
    st.markdown(
        f"""
        <hr>
        <p style='text-align:center; font-size:14px; color:gray;'>
            Made with ❤️ by Kush Gupta | © {current_year}
        </p>
        """,
        unsafe_allow_html=True
    )
else:
    st.info("👈 Please upload a WhatsApp chat export `.txt` file to get started.")

    # Optional: show footer even if no file uploaded
    current_year = datetime.datetime.now().year
    st.markdown(
        f"""
        <hr>
        <p style='text-align:center; font-size:14px; color:gray;'>
            Made with ❤️ by Kush Gupta | © {current_year}
        </p>
        """,
        unsafe_allow_html=True
    )


