# Study Group Matching System - MVP

## Overview

This project is a **Flask-based web application** that facilitates the creation and management of study groups. Users can join groups based on their availability, skill level, topics of interest, and geographic location. The application uses a **KMeans clustering model** to group users and match them to the most suitable study groups based on common topics, availability, and proximity. The application also allows users to create new study groups.

## Key Features

- **Intelligent Session Matching**: Match users to relevant study groups based on availability, skill level, and topics of interest.
- **Cluster-based Grouping**: A KMeans clustering algorithm is used to group users based on similarities (topics, location, etc.).
- **Join Study Groups**: Users can join existing study groups or create new ones.
- **Centralized CSV Data Storage**: User data, group assignments, and availability are stored in a CSV file.
- **Dynamic User Interface**: A web-based UI built using HTML, CSS, and Flask to display study groups and allow user interactions.

## Tech Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML, CSS, Bootstrap
- **Machine Learning Model**: KMeans clustering (Scikit-learn)
- **Data Storage**: CSV (Comma-separated values)
- **Deployment**: Render.com (or any free deployment platform)
- **Other Libraries**: Geopy (for calculating geographic distance), Gunicorn (for production server)

## Setup Guide

### Local Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mustafa-tola/dd-study-group.git
   cd study-group-mvp
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Mac/Linux
   venv\Scripts\activate  # For Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application Locally**:
   ```bash
   python app.py
   ```

5. **Access the Application**:
   Open your web browser and visit `http://127.0.0.1:3000/` to access the application.

## Usage Guide

### Joining a Study Group

1. Fill in the **User Form** with your details (name, skill level, topics of interest, availability, location, and preferred group size).
2. Submit the form to view **matched study groups**.
3. Join one of the suggested study groups based on the calculated match percentage.

### Viewing Group Members

Once you join a group, you can view the **members** of that group by visiting the group page.

## Machine Learning Model: KMeans Clustering

### Overview

The **KMeans** algorithm is used to cluster users based on:

- **Topics of Interest**: Subjects like Machine Learning, Python, etc.
- **Availability**: Days and hours the user is available.
- **Geographic Location**: Latitude and Longitude of the user.

The model is pre-trained and assigns new users to clusters based on these features.

### Model File

- The trained model is saved as `model.joblib` and loaded by the Flask app to predict clusters for new users.

## API Endpoints

### 1. Home Page (Form Submission)

- **URL**: `/`
- **Method**: `GET`
- **Description**: Displays the form for user input.

### 2. Assign User to Group

- **URL**: `/assign_user`
- **Method**: `POST`
- **Description**: Predicts the cluster for the user and displays relevant study groups.

### 3. Join Study Group

- **URL**: `/join_group`
- **Method**: `POST`
- **Description**: Saves the user's details into the selected group and updates the CSV file.

### 4. View Group Members

- **URL**: `/group?group_name=GroupName&cluster_id=ClusterID`
- **Method**: `GET`
- **Description**: Displays the members of a specific study group.

## Future Roadmap

- **Expand Group Creation**: Allow group leaders to invite users.
- **User Authentication**: Implement login and registration for returning users.
- **Improved Matching Algorithm**: Add weights based on user preferences for location, time, or skill level.
- **Real-time Chat Integration**: Allow group members to communicate in real-time.
- **Advanced Model Tuning**: Fine-tune the clustering model based on user feedback and engagement.

## Troubleshooting

### Common Issues:

2. **Model Not Loading**:
   - Ensure the `model.joblib` and `scaler.joblib` files are present in the `model/` directory.

3. **Form Data Not Saving**:
   - Ensure the CSV path is correctly specified and the user data is appended properly.

---

