import pandas as pd

def calculate_loss_wrt_topic(data):
    """Calculate the overall loss with respect to the topics (study group assignment)."""
    # Calculate the loss for "Group_3" (default group)
    reduced_data = data[data["Study_Group"] == "Group_3"]
    overall_loss = len(reduced_data) / len(data)
    print("Overall Loss wrt topic (Group_3):", overall_loss)
    return overall_loss

def calculate_loss_per_cluster(data):
    """Calculate the loss with respect to topics for each cluster."""
    clusters = data['Cluster'].unique()  # Get unique clusters
    cluster_losses = {}

    for cluster_id in clusters:
        # Filter the data for the specific cluster
        cluster_data = data[data["Cluster"] == cluster_id]

        # Calculate the loss for Group_3 in the cluster
        reduced_cluster_data = cluster_data[cluster_data["Study_Group"] == "Group_3"]
        cluster_loss = len(reduced_cluster_data) / len(cluster_data)
        cluster_losses[cluster_id] = cluster_loss

        print(f"Loss wrt topic for Cluster {cluster_id}: {cluster_loss}")

    return cluster_losses

def assess_model_loss(input_csv):
    """Load the grouped user data and assess loss with respect to each cluster and overall."""
    # Load the data
    data = pd.read_csv(input_csv)

    # Step 1: Calculate the overall loss (as you did before)
    overall_loss = calculate_loss_wrt_topic(data)

    # Step 2: Calculate the loss for each cluster
    cluster_losses = calculate_loss_per_cluster(data)

    return overall_loss, cluster_losses

# Run the assessment
input_csv = "../data/grouped_users.csv"  # Path to input file (grouped data)
overall_loss, cluster_losses = assess_model_loss(input_csv)
