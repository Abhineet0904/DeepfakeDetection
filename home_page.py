import base64
import pandas as pd
import plotly.express as px
import streamlit as st
from st_pages import Page, show_pages

st.set_page_config(page_title="About", page_icon="ℹ️")
st.title("**Deepfake Detection 🕵️‍♂️**")

with open("media/background.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.header("Understanding Deepfakes : Creation, Impact and Detection")

st.subheader("What are Deepfakes?")
st.write(
    "Deepfakes are synthetic media in which a person's likeness is digitally manipulated "
    "using artificial intelligence (AI) and deep learning techniques to create realistic yet fake "
    "videos, images, or audio. These are often used to imitate real people, sometimes convincingly."
)

st.subheader("How are Deepfakes Created?")
st.write(
    "Deepfakes are generated using deep learning algorithms, particularly Generative Adversarial Networks (GANs). "
    "These models train on large datasets of real videos/images to generate realistic fakes. The process includes:"
)
st.markdown(
    """
    - **Data Collection** : Gathering videos and images of the target person.
    - **Training AI Model** : Using AI techniques like GANs or autoencoders to learn facial features and expressions.
    - **Face Mapping & Synthesis** : Applying the trained model to superimpose the fake likeness onto another person.
    - **Post-Processing** : Refining and enhancing to make the fake media indistinguishable from real content.
    """
)
st.write("")

st.video("media/dynamic_video.mp4")
st.caption(
    "This is an example of Dynamic video Static audio. Source : https://youtu.be/lnUbEPFlgKA?si=VTswxXODM7c0RpzU")
st.subheader("")

st.subheader("Advantages and Disadvantages of Deepfakes")
col1, col2 = st.columns(2)
with col1:
    st.write("**Advantages**")
    st.markdown(
        """
        - Used in the entertainment industry for visual effects.
        - Helps create realistic dubbing in movies.
        - Can be used for historical recreations or educational purposes.
        """
    )
with col2:
    st.write("**Disadvantages**")
    st.markdown(
        """
        - Used for spreading misinformation and fake news.
        - Can damage reputations and be used for identity theft.
        - Increases risks of fraud, scams, and political manipulation.
        """
    )
st.write("")

st.subheader("The Impact of Deepfakes on Society")
st.write(
    """
    Deepfakes pose a significant threat by spreading misinformation, influencing elections,
    damaging reputations, and eroding trust in media. Fake political speeches and news have
    led to severe consequences worldwide.

    **Some alarming trends in deepfake misuse are :**
    - The number of deepfake videos online has been doubling approximately every six months. In 2023, an estimated 500,000 deepfake videos were shared on social media worldwide.
    - Deepfake fraud incidents increased by 1,740% in North America in 2022.
    - Asia-Pacific experienced a 1,530% rise in deepfake fraud in 2022.
    """
)

with st.expander("___Deepfake Timeline___"):
    timeline_data = pd.DataFrame({
        "Event": [
            "Obama Buzzfeed Deepfake",
            "Jim Acosta Doctored Video",
            "Jennifer Lawrence - Buscemi Deepfake",
            "David Beckham Anti-Malaria Deepfake",
            "World Leaders 'Imagine' Deepfake",
            "Dali Museum Deepfake",
            "Bill Hader Impression Deepfake",
            "Nancy Pelosi Doctored Video",
            "Mark Zuckerberg Deepfake",
            "Joe Rogan Audio/Visual Deepfake",
            "Moon Landing Deepfake",
            "Queen Christmas Deepfake",
            "Tom Cruise Deepfake",
            "Pennsylvania Cheerleader case",
            "Anthony Bourdain Documentary"
        ],
        "Date": [
            "2018-04-17",
            "2018-11-17",
            "2019-01-14",
            "2019-04-09",
            "2019-04-12",
            "2019-05-13",
            "2019-05-16",
            "2019-05-22",
            "2019-06-07",
            "2019-11-24",
            "2020-07-20",
            "2020-12-25",
            "2021-02-22",
            "2021-03-12",
            "2021-07-16"
        ],
        "Category": [
            "Mouth Swap Deepfake",
            "Synthetic Media",
            "Face Swap Deepfake",
            "Puppet Deepfake",
            "Puppet Deepfake",
            "Puppet Deepfake",
            "Face Swap Deepfake",
            "Synthetic Media",
            "Mouth Swap Deepfake",
            "Face Swap Deepfake",
            "Puppet Deepfake",
            "Puppet Deepfake",
            "Face Swap Deepfake",
            "Unknown",
            "Audio Deepfake"
        ]
    })

    timeline_data["Date"] = pd.to_datetime(timeline_data["Date"])

    fig_timeline = px.scatter(
        timeline_data,
        x="Date",
        y="Event",
        color="Category",
        title="Timeline of Major Deepfake Events",
        labels={"Date": "Year"},
        size_max=15
    )

    fig_timeline.update_layout(
        xaxis=dict(
            type="date",
            tickformat="%Y-%m-%d"
        ),
        yaxis=dict(
            categoryorder="array",
            categoryarray=timeline_data.sort_values("Date", ascending=False)["Event"].tolist()
        )
    )

    st.plotly_chart(fig_timeline)
st.write("")

st.subheader("How to Detect Deepfakes?")
st.markdown(
    """
    Deepfakes can be detected using various techniques:
    - **Visual Artifacts**: Blurry edges, inconsistent lighting, or unnatural facial expressions.
    - **Audio Analysis**: Lip-sync mismatches, unnatural pauses, and robotic intonations.
    - **Metadata Inspection**: Checking the digital footprint of media files.
    - **AI Detection Tools**: Deep learning models trained to spot deepfake patterns.
    """
)
st.write("")

st.subheader("AI Models for Deepfake Detection")
st.markdown(
    """
    Several AI models are developed to counter deepfakes:
    - **XceptionNet** : A deep learning model trained specifically for deepfake detection.
    - **MesoNet** : Designed for spotting manipulated facial features.
    - **EfficientNet** : Utilized for deepfake detection due to its optimized performance in image classification.
    - **ResNet** : Used to analyze facial inconsistencies in deepfake videos.
    """
)
st.write("")

st.write(
    "With ongoing advancements, researchers are constantly improving AI-based solutions to combat the risks of deepfake misuse.")

show_pages(
    [
        Page("home_page.py", "About", "ℹ️"),
        Page("Webpages/signin_page.py", "Signin", "🔑"),
        Page("Webpages/engine.py", "Engine", "🕵️‍"),
        Page("Webpages/verification.py", "Verification", "✅‍"),
        Page("Webpages/contact_page.py", "Contact", "📤")
    ]
)