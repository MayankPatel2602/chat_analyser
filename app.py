import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt

st.sidebar.header('Whatsapp Chat Analyzer')
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    # st.text(data)
    df = preprocessor.preprocessor(data)

    # st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user =  st.sidebar.selectbox("show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages,words,num_media,links = helper.fetch_stats(selected_user,df)
        st.title("Statics: ")

        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media Shared")
            st.title(num_media)
        with col4:
            st.header("Total links")
            st.title(links)

        #monthly timeline
        timeline = helper.timeline(selected_user,df)

        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation='vertical')

        st.title("Message Timeline")
        st.pyplot(fig)

        #activity map
        busy_day = helper.week_activity_map(selected_user,df)
        busy_month = helper.month_activity_map(selected_user,df)
        col1,col2 = st.columns(2)

        with col1:
            st.title("Most Busy Day")
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            plt.show()
            st.pyplot(fig)
        with col2:
            st.title("Most Busy Month")
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color = 'orange')
            plt.xticks(rotation='vertical')
            plt.show()
            st.pyplot(fig)
        #most Busy Users
        if selected_user == "Overall":
            st.title("Most Busy Users")
            x,new_df = helper.most_busy(df)
            fig,ax = plt.subplots()

            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color = 'red')
                plt.xticks(rotation = 'vertical')
                plt.show()
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        #wordcloud

        wc_df = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(wc_df)
        st.title('WorkCloud')
        st.pyplot(fig)

        #most common words

        most_common_df = helper.common_words(selected_user,df)

        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)



