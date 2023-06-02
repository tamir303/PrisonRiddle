import matplotlib.pyplot as plt

def calculate_success_probability(num_prisoners):
    # Your logic to calculate the success probability based on the number of prisoners goes here
    # This can be based on a specific strategy or algorithm you have in mind

    # For demonstration purposes, let's assume a simple linear relationship
    success_probability = 1 / num_prisoners
    
    return success_probability

# Generate data points for the graph
def show_graph(num_prisoners_range):
    plt.clf()  # Clear the previous plot
    success_probabilities = [calculate_success_probability(num) for num in num_prisoners_range]
    # Plot the graph
    plt.plot(num_prisoners_range, success_probabilities)
    plt.xlabel('Number of Prisoners')
    plt.ylabel('Probability of Prisoner Success')
    plt.title('Prisoner Success Probability vs. Number of Prisoners')
    plt.grid(True)
    plt.show()

def create_success_graph(games):
    plt.clf()  # Clear the previous plot
    success_count = sum(int(games[game].isSuccess) for game in games if games[game].isSuccess)
    fail_count = len(games) - success_count
    
    # Create a bar chart with two columns
    plt.bar(['Success', 'Fail'], [success_count, fail_count], color=['green', 'red'])
    plt.xlabel('Outcome')
    plt.ylabel('Number of Games')
    plt.title('Games Success Graph')
    
    # Add text labels for each column
    plt.text('Success', success_count, str(success_count), ha='center', va='bottom')
    plt.text('Fail', fail_count, str(fail_count), ha='center', va='bottom')
    
    # Display the graph
    plt.show()