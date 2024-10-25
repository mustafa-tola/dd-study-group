import pandas as pd
from collections import Counter

# Load the data
def load_clustered_data(file_path):
    """Load the clustered data."""
    data = pd.read_csv(file_path)
    return data

# Find top 3 topics for each cluster
def get_top_topics_per_cluster(data, cluster_id, topic_columns):
    """Return the top 3 topics of interest for the specified cluster."""
    cluster_data = data[data['Cluster'] == cluster_id]
    
    # Count the number of students interested in each topic
    topic_counts = Counter()
    for topic in topic_columns:
        topic_counts[topic] = cluster_data[topic].sum()
    
    # Get the top 3 topics based on the frequency
    top_3_topics = [topic for topic, _ in topic_counts.most_common(3)]
    return top_3_topics

# Merge topic, days, and hours into a single column
def merge_columns(row, topic_columns, day_columns, hour_columns):
    """Merge topics, days, and hours into a single string for each user."""
    # Concatenate topics the user is interested in
    topics = [topic for topic in topic_columns if row[topic] == 1]
    merged_topics = ','.join(topics) if topics else "No Topics"

    # Concatenate days the user is available
    days = [day for day in day_columns if row[day] == 1]
    merged_days = ','.join(days) if days else "No Days"

    # Concatenate hours the user is available
    hours = [str(hour) for hour in hour_columns if row[hour] == 1]
    merged_hours = ','.join(hours) if hours else "No Hours"

    return merged_topics, merged_days, merged_hours

# Assign students to study groups based on top topics
def assign_students_to_groups(data, cluster_id, top_3_topics, topic_columns, day_columns, hour_columns):
    """Assign students in a cluster to study groups based on top 3 topics."""
    cluster_data = data[data['Cluster'] == cluster_id].copy()
    cluster_data['Study_Group'] = None  # Add a new column for study group assignment
    
    # Assign students to groups based on their interest in the top topics
    for idx, row in cluster_data.iterrows():
        for i, topic in enumerate(top_3_topics):
            if row[topic] == 1:  # If the student is interested in this topic
                cluster_data.at[idx, 'Study_Group'] = f'Group_{topic}'  # Assign to Group based on topic
                break  # Stop once a student is assigned to one group

        # If the student has no interest in the top 3 topics, assign to a default group
        if pd.isna(cluster_data.at[idx, 'Study_Group']):
            cluster_data.at[idx, 'Study_Group'] = 'Group_3'  # Default group

        # Merge topics, days, and hours into single columns
        merged_topics, merged_days, merged_hours = merge_columns(row, topic_columns, day_columns, [f'Hour_{i}' for i in range(24)])

        # Store the merged data in the appropriate columns
        cluster_data.at[idx, 'Topics_of_Interest'] = merged_topics
        cluster_data.at[idx, 'Days_Available'] = merged_days
        cluster_data.at[idx, 'Hours_Available'] = merged_hours
    return cluster_data

# Save the final data with study group assignments
def save_grouped_data_to_csv(grouped_data, output_path):
    """Save the final grouped data to a CSV file."""
    grouped_data.drop(['Big Data','Data Analysis','Machine Learning','Python','SQL','Statistics','Hour_0','Hour_1','Hour_2','Hour_3','Hour_4','Hour_5','Hour_6','Hour_7','Hour_8','Hour_9','Hour_10','Hour_11','Hour_12','Hour_13','Hour_14','Hour_15','Hour_16','Hour_17','Hour_18','Hour_19','Hour_20','Hour_21','Hour_22','Hour_23','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],axis=1,inplace=True)    
    grouped_data.to_csv(output_path, index=False)
    print(f"Grouped data saved to {output_path}")

# Main function to execute the entire process
def create_study_groups(input_csv, output_csv):
    # Step 1: Load the clustered data
    data = load_clustered_data(input_csv)
    
    # Define the topic columns and availability columns (days and hours)
    topic_columns = ['Big Data', 'Data Analysis', 'Machine Learning', 'Python', 'SQL', 'Statistics']
    day_columns = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hour_columns = [f'Hour_{i}' for i in range(24)]
    
    # Final dataframe to store the grouped data
    final_grouped_data = pd.DataFrame()

    # Step 2: For each cluster, find the top 3 topics and assign students to groups
    for cluster_id in data['Cluster'].unique():
        print(f"Processing Cluster {cluster_id}...")
        
        # Step 3: Get the top 3 topics for this cluster
        top_3_topics = get_top_topics_per_cluster(data, cluster_id, topic_columns)
        print(f"Top 3 topics for Cluster {cluster_id}: {top_3_topics}")
        
        # Step 4: Assign students in this cluster to study groups based on the top topics and merge the columns
        clustered_data_with_groups = assign_students_to_groups(data, cluster_id, top_3_topics, topic_columns, day_columns, hour_columns)
        
        # Step 5: Append the grouped data for this cluster to the final dataframe
        final_grouped_data = pd.concat([final_grouped_data, clustered_data_with_groups])
    
    # Step 6: Save the final grouped data to a CSV file
    save_grouped_data_to_csv(final_grouped_data, output_csv)

# Run the process
input_csv = "../data/output.csv"  # Path to input file (clustered data)
output_csv = "../data/grouped_users.csv"   # Path to output file (grouped users)

create_study_groups(input_csv, output_csv)
