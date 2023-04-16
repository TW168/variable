import streamlit as st

# Set the page width and height
st.set_page_config(
    page_title="Home",
    page_icon=":smiley:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add some content to the page
st.write("# My Demo App")
st.write("Hello, world!")

# Use CSS styles to center the content
st.markdown(
    """
    <style>
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Wrap the content in a div with the "center" class
st.markdown('<div class="center">', unsafe_allow_html=True)

# Add the content inside the centered div
st.write("This content will be centered.")

# Close the centered div
st.markdown('</div>', unsafe_allow_html=True)
