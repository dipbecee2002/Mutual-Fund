import streamlit as st
from mftool import Mftool
import pandas as pd
from PIL import Image
import base64

# Initialize Mftool instance
mf = Mftool()

# Streamlit page configuration
st.set_page_config(page_title="Investment Dashboard", layout="wide")

# Paths for sliding header images
image_paths = ["resources/b1.png", "resources/b2.png", "resources/b3.png", "resources/b4.png", "resources/b5.png", "resources/b6.png", "resources/b7.png"]

# Function to encode images for HTML display
def get_base64_image(img_path):
    """Convert image to base64 format for embedding in HTML."""
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Prepare base64 images for the slider
base64_images = [get_base64_image(img) for img in image_paths]

# Slider HTML with JavaScript for sliding functionality
slider_html = f"""
<div style="display:flex; justify-content:center; align-items:center; position:relative; width:100%; max-height:500px; overflow:hidden;">
    <img id="slider-image" src="data:image/png;base64,{base64_images[0]}" style="width:100%; max-height:500px; object-fit:cover; transition:1.5s; cursor:pointer;" onclick="changeImage()">
</div>

<script>
    const images = {base64_images};
    let currentIndex = 0;

    function changeImage() {{
        currentIndex = (currentIndex + 1) % images.length;
        const sliderImage = document.getElementById("slider-image");
        sliderImage.src = "data:image/png;base64," + images[currentIndex];
    }}
</script>
"""

# Display the sliding header
st.markdown(slider_html, unsafe_allow_html=True)

# Title and Subtitle
st.title("Welcome to Investment Dashboard")
st.subheader("Manage, Analyze, and Learn about Mutual Funds and Insurance")

# Sidebar navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["MF Details", "Login", "Investment", "Blog", "Insurance Details"])

# Tabs for Mutual Fund and Insurance Details
tab1, tab2 = st.tabs(["Mutual Fund Details", "Insurance Details"])

# Mutual Fund Details Tab
with tab1:
    st.header("Mutual Fund Details")
    search_query = st.text_input("Enter Mutual Fund Scheme Name or Code", "")

    if search_query:
        try:
            # Search mutual fund schemes by name or code
            all_schemes = mf.get_scheme_codes()
            matched_schemes = {
                code: name
                for code, name in all_schemes.items()
                if search_query.lower() in name.lower()
            }

            if matched_schemes:
                st.subheader("Matched Schemes:")
                st.write(pd.DataFrame(list(matched_schemes.items()), columns=["Scheme Code", "Scheme Name"]))

                # Select a scheme for more details
                selected_scheme = st.selectbox(
                    "Select a scheme to view details", list(matched_schemes.keys())
                )

                if selected_scheme:
                    # Fetch scheme details
                    scheme_details = mf.get_scheme_details(selected_scheme)

                    # Extract required fields
                    scheme_data = {
                        "Fund House": scheme_details.get("fund_house", "N/A"),
                        "Scheme Type": scheme_details.get("scheme_type", "N/A"),
                        "Scheme Category": scheme_details.get("scheme_category", "N/A"),
                        "Scheme Code": scheme_details.get("scheme_code", "N/A"),
                        "Scheme Name": scheme_details.get("scheme_name", "N/A"),
                        "Scheme Start Date": scheme_details.get("scheme_start_date", "N/A"),
                        "NAV Value": scheme_details.get("nav", "N/A"),
                    }

                    # Display details in table format
                    st.subheader(f"Details for Scheme Code: {selected_scheme}")
                    st.table(pd.DataFrame([scheme_data]))

                    # Section for plotting NAV values
                    st.subheader("NAV Value Over Time")

                    try:
                        # Fetch historical NAV data
                        nav_history = mf.get_scheme_historical_nav(selected_scheme)

                        # Sanitize and convert NAV data to a DataFrame with formatted date
                        nav_data = []
                        for date, nav_value in nav_history.items():
                            try:
                                nav_data.append(
                                    {
                                        "Date": pd.to_datetime(date, format="%d-%m-%Y").strftime("%d/%m/%Y"),
                                        "NAV": float(nav_value),
                                    }
                                )
                            except ValueError:
                                # Skip invalid entries
                                continue

                        if nav_data:
                            nav_df = pd.DataFrame(nav_data)

                            # Convert date column to datetime for plotting
                            nav_df["Date"] = pd.to_datetime(nav_df["Date"], format="%d/%m/%Y")

                            # Display the NAV history in a table
                            st.subheader("NAV History Table")
                            st.table(nav_df)

                            # Plot NAV over time
                            st.subheader("NAV Value Plot")
                            st.line_chart(nav_df.set_index("Date")["NAV"], use_container_width=True)
                        else:
                            st.warning("No valid historical NAV data available for this scheme.")
                    except Exception as e:
                        st.error(f"Error fetching NAV history: {e}")
            else:
                st.warning("No matching schemes found.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Insurance Details Tab
with tab2:
    st.header("Insurance Details")
    st.subheader("Explore and Manage Insurance Policies")
    st.write("This section is under development. It will include features for comparing insurance policies, calculating premiums, and tracking your insurance portfolio.")

# Functionality: Login
if menu == "Login":
    st.header("Login Page")
    st.subheader("User Authentication")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin":  # Replace with actual authentication logic
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password.")

# Functionality: Investment
if menu == "Investment":
    st.header("Investment Dashboard")
    st.subheader("Track and Manage Investments")
    st.write("This section can be expanded to include features like tracking investment portfolios, analyzing growth, and making recommendations.")

# Functionality: Blog
if menu == "Blog":
    st.header("Investment Blog")
    st.subheader("Latest Articles and Insights")
    st.write("Coming soon: A blog platform with articles on investment strategies, mutual fund tips, and financial planning.")

# Functionality: Insurance Details in Sidebar
if menu == "Insurance Details":
    st.header("Insurance Details")
    st.subheader("Explore and Manage Insurance Policies")
    st.write("This section is under development. It will include features for comparing insurance policies, calculating premiums, and tracking your insurance portfolio.")
