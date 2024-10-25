import pandas as pd
import joblib
from flask import Flask, request, render_template, redirect, url_for
from geopy.distance import geodesic
# Initialize Flask app
app = Flask(__name__,template_folder="../templates",static_folder="../static")

# Load the KMeans model from the joblib file
kmeans_model = joblib.load('../model/model.joblib')

# Load the CSV file with the existing users and study groups
csv_file = '../data/grouped_users.csv'
users_data = pd.read_csv(csv_file)

# Function to calculate match percentage based on topic interests
def calculate_match_percentage(user_topics, group_topics):
    if not group_topics:
        return 0
    matches = len(set(user_topics) & set(group_topics))
    total_user_topics = len(user_topics) if user_topics else 1  # Avoid division by zero
    return (matches / total_user_topics) * 100  # Percentage based on user topics


# Function to check availability match between user and group
# Function to check availability match between user and group (returns match percentages)
def availability_match(user_avail_days, user_avail_hours, group_avail_days, group_avail_hours):
    # Match for days
    days_match = len(set(user_avail_days) & set(group_avail_days))
    total_user_days = len(user_avail_days) if user_avail_days else 1  # Avoid division by zero
    days_percent = (days_match / total_user_days) * 100  # Percentage based on user's available days

    # Match for hours
    hours_match = len(set(user_avail_hours) & set(group_avail_hours))
    total_user_hours = len(user_avail_hours) if user_avail_hours else 1  # Avoid division by zero
    hours_percent = (hours_match / total_user_hours) * 100  # Percentage based on user's available hours

    return days_percent, hours_percent  # Return both percentages


def location_match(user_lat, user_lon, group_lat, group_lon):
    user_location = (user_lat, user_lon)
    group_location = (group_lat, group_lon)
    distance = geodesic(user_location, group_location).kilometers
    return distance

# Preprocess user input into the format required by the KMeans model
def preprocess_input(skill_level, topics, latitude, longitude, preferred_group_size, days, hours):
    # Encode skill level (assuming the model expects numerical encoding)
    skill_level_encoding = {'Beginner': 0, 'Intermediate': 1, 'Advanced': 2}
    skill_level_num = skill_level_encoding.get(skill_level, 0)

    # Convert the topics to a binary vector (1 for selected, 0 for not selected)
    topic_columns = ['Big Data', 'Data Analysis', 'Machine Learning', 'Python', 'SQL', 'Statistics']
    topics_vector = [1 if topic in topics else 0 for topic in topic_columns]

    # Encode preferred group size
    group_size_encoding = {'Small': 0, 'Medium': 1, 'Large': 2}
    preferred_group_size_num = group_size_encoding.get(preferred_group_size, 0)

#Convert hours to a binary vector
    hour_columns = ['Hour_0', 'Hour_1', 'Hour_2', 'Hour_3', 'Hour_4', 'Hour_5', 'Hour_6', 'Hour_7', 'Hour_8', 'Hour_9', 'Hour_10', 'Hour_11','Hour_12','Hour_13','Hour_14','Hour_15','Hour_16','Hour_17','Hour_18','Hour_19','Hour_20','Hour_21','Hour_22','Hour_23']
    hour_vector = [1 if hour in hours else 0 for hour in hour_columns]

    #Convert days to a binary vector
    day_columns = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_vector = [1 if day in days else 0 for day in day_columns]

    scaler = joblib.load("../model/scaler.joblib")
    lat_lon_scaled = scaler.transform([[latitude, longitude]])[0]  # Scale latitude and longitude

    print(lat_lon_scaled)
    # Combine skill level, topics, latitude, longitude, and preferred group size into a feature vector
    feature_vector = [latitude, longitude, skill_level_num, preferred_group_size_num] + topics_vector + hour_vector + day_vector
    print(feature_vector)
    return feature_vector

# Route for the home page (form submission)
@app.route('/')
def index():
    return render_template('form.html')

# Route for assigning a user to study groups
@app.route('/assign_user', methods=['POST'])
def assign_user():
    name = request.form['name']
    skill_level = request.form['skill_level']
    selected_topics = request.form.getlist('topics')
    selected_days = request.form.getlist('days')  # Get days the user is available
    selected_hours = request.form.getlist('hours')  # Get hours the user is available
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])
    preferred_group_size = request.form['preferred_group_size']

    # Step 1: Preprocess the user input into the format required by KMeans
    feature_vector = preprocess_input(skill_level, selected_topics, latitude, longitude, preferred_group_size, selected_days, selected_hours)

    # Step 2: Predict the cluster for the new user
    predicted_cluster = kmeans_model.predict([feature_vector])[0]
    print(predicted_cluster)

    # Step 3: Filter the users in the predicted cluster
    cluster_data = users_data[users_data['Cluster'] == predicted_cluster]

    # Step 4: Find matching groups based on topics and availability
    matched_groups = []
    # Step 3: Find unique study groups in the predicted cluster
    # Step 3: Find unique study groups in the predicted cluster
    unique_groups = cluster_data['Study_Group'].unique()

    # Step 4: Compare the user with each group (not each user)
    for group_name in unique_groups:
        group_data = cluster_data[cluster_data['Study_Group'] == group_name]
        
        # Get the most common topics in the group
        group_topics = []
        for topics in group_data['Topics_of_Interest']:
            group_topics.extend(topics.split(","))
        group_topics = list(set(group_topics))  # Get unique topics in the group
        
        # Get the most common available days and hours
        group_avail_days = []
        for days in group_data['Days_Available']:
            group_avail_days.extend(days.split(","))
        group_avail_days = list(set(group_avail_days))  # Get unique available days in the group
        
        group_avail_hours = []
        for hours in group_data['Hours_Available']:
            group_avail_hours.extend(hours.split(","))
        group_avail_hours = list(set(group_avail_hours))  # Get unique available hours in the group

        # Get the average location (latitude and longitude) of the group
        group_lat = group_data['Latitude'].mean()
        group_lon = group_data['Longitude'].mean()

        # Compare the new user with the aggregated group data
        topic_match_percent = calculate_match_percentage(selected_topics, group_topics)
        day_match_percent, hour_match_percent = availability_match(selected_days, selected_hours, group_avail_days, group_avail_hours)
        location_distance = location_match(latitude, longitude, group_lat, group_lon)

        # Combine the matching scores
        combined_match = (topic_match_percent * 0.6) + ((day_match_percent + hour_match_percent) / 2 * 0.3) + (1 / (1 + location_distance) * 0.1)        
        # Add the group and its match percentage to the list of matched groups
        matched_groups.append({
        'group_name': group_name,
        'topic_match': round(topic_match_percent, 2),
        'day_match': round(day_match_percent, 2),
        'hour_match': round(hour_match_percent, 2),
        'match_percent': round(combined_match, 2)  # Total match percentage
        })


    # Step 5: Sort groups by match percentage in descending order
    matched_groups = sorted(matched_groups, key=lambda x: x['match_percent'], reverse=True)
    
    print(matched_groups)

    # Step 6: Return the results to the user (all matched groups)
    return render_template('results.html', matched_groups=matched_groups, name=name, skill_level=skill_level, topics=selected_topics, days=selected_days, hours=selected_hours, latitude=latitude, longitude=longitude,preferred_group_size=preferred_group_size, cluster_id=predicted_cluster)

# Route to handle the user joining a study group
@app.route('/join_group', methods=['POST'])
def join_group():
    # Get the user's information from the form
    group_name = request.form["group_name"]
    name = request.form['name']
    skill_level = request.form['skill_level']
    selected_topics = request.form.getlist('topics')
    selected_days = request.form.getlist('days')
    selected_hours = request.form.getlist('hours')
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])
    preferred_group_size = request.form['preferred_group_size']
    group_name = request.form['group_name']
    cluster_id = request.form['cluster_id']

    global users_data

    print(list(selected_days))
    # Create a new row for the user with the joined group
    new_user = {
        'UserID': len(users_data) + 1,  # Assign a new user ID
        'Cluster': cluster_id,  # We are not clustering here but you can use clustering logic if needed
        'Skill_Level': skill_level,
        'Study_Group': group_name,
        'Latitude': latitude,
        'Longitude': longitude,
        'Preferred_Group_Size': preferred_group_size,
        'Days_Available': ','.join(selected_days),
        'Hours_Available': ','.join(selected_hours),
        'Topics_of_Interest': ','.join(selected_topics)
    }

    # Add the new user to the DataFrame
    new_user_df = pd.DataFrame([new_user])  # Create a DataFrame from the new user data
    users_data = pd.concat([users_data, new_user_df], ignore_index=True)  # Concatenate the new row to the existing DataFrame

    # Save the updated data to the CSV file
    users_data.to_csv(csv_file, index=False)

    # Redirect to the homepage or another page after joining the group
    return redirect(url_for('group_page', group_name=group_name, cluster_id=cluster_id))


# Route to display users in a study group by group name and cluster ID
@app.route('/group')
def group_page():
    # Get group name and cluster ID from query parameters
    group_name = request.args.get('group_name')
    cluster_id = request.args.get('cluster_id')

    print(users_data[users_data['Study_Group'] == group_name])
    # Filter users who belong to the specified group and cluster
    group_members = users_data[(users_data['Study_Group'] == group_name) & (users_data['Cluster'] == float(cluster_id))]

    # Render the template with the group members' data
    return render_template('group.html', group_name=group_name, cluster_id=cluster_id, group_members=group_members.to_dict(orient='records')) 


# Run the Flask app
if __name__ == '__main__':
    app.run(port=3000)
