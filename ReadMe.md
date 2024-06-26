# Instagram Influencer Analysis Project

## Overview
This project analyzes Instagram influencer metrics such as followers count, media count, and total likes over time. It provides insights into an influencer's engagement and popularity trends based on their Instagram posts.

## Requirements
To run this project locally, ensure you have Python installed along with the following dependencies:

- `requests`: For making HTTP requests to the Instagram Graph API.
- `matplotlib`: For plotting graphs.
- `seaborn`: For enhancing visualizations.
- `pandas`: For data manipulation and analysis.
- `streamlit`: For building interactive web applications.

Install these dependencies using the following command:
```bash
pip install -r requirements.txt
```


This project uses a .env file to store sensitive information like API tokens. Before running the application, create a .env file in the root directory of your project with the following structure:

- .env file

```bash
ACCESS_TOKEN=your_instagram_access_token
INSTAGRAM_USER_ID=your_instagram_user_id
```


## Running the Application

```bash
streamlit run app2.py
```