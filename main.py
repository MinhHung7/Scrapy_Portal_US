from datetime import datetime, timedelta

# Your initial string
initial_time_str = "21:10:45"

# Convert the string to a datetime object
initial_time = datetime.strptime(initial_time_str, "%H:%M:%S")

# Add one hour to the datetime object
new_time = (datetime.strptime(initial_time_str, "%H:%M:%S") + timedelta(hours=1)).strftime("%H:%M:%S")

# Convert the new datetime object back to a string in the desired format
new_time_str = new_time.

print(new_time_str)
