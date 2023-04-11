import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

minData = (len(pd.read_csv('Data/DanielWalkingHand.csv')) // 500) * 500
#char_walking = pd.read_csv('Data/CharWalkingHand.csv')
#nile_walking = pd.read_csv('Data/NileWalkingHand.csv')
#dan_walking = pd.read_csv('Data/DanielWalkingHand.csv')

#char_walking = pd.read_csv('Data/CharWalkingHand.csv', nrows = minData)
#char_jumping = pd.read_csv('Data/CharJumpingHand.csv', nrows = minData)
char_jumping = pd.read_csv('Data/CharJumpingHand.csv')
nile_jumping = pd.read_csv('Data/NileJumpingHand.csv')
dan_jumping = pd.read_csv('Data/DanielJumpingHand.csv')
#rows_per_seg = 500
#segment_nums = np.arange(len(char_walking))
#char_walking['segment'] = np.repeat(segment_nums, rows_per_seg)[:len(char_walking)]
#segment_0 = char_walking.groupby('segment').get_group(0)


# Create pandas dataframes for each member's data
#walkAcc1, walkTime1 = char_walking['Absolute acceleration (m/s^2)'], char_walking['Time (s)']
#walkAcc2, walkTime2 = nile_walking['Absolute acceleration (m/s^2)'], nile_walking['Time (s)']
#walkAcc3, walkTime3 = dan_walking['Absolute acceleration (m/s^2)'], dan_walking['Time (s)']

jumpAcc1, jumpTime1 = char_jumping['Absolute acceleration (m/s^2)'], char_jumping['Time (s)']
jumpAcc2, jumpTime2 = nile_jumping['Absolute acceleration (m/s^2)'], nile_jumping['Time (s)']
jumpAcc3, jumpTime3 = dan_jumping['Absolute acceleration (m/s^2)'], dan_jumping['Time (s)']

# Plot the acceleration versus time data for each person
#plt.plot(walkTime1, walkAcc1, label='Char')
#plt.plot(walkTime2, walkAcc2, label='Nile')
#plt.plot(walkTime3, walkAcc3, label='Dan')

#plt.plot(segment_0['Time (s)'], segment_0['Absolute acceleration (m/s^2)'], label='Char')
plt.plot(jumpTime1, jumpAcc1, label='Char')
plt.plot(jumpTime2, jumpAcc2, label='Nile')
plt.plot(jumpTime3, jumpAcc3, label='Dan')

# Add labels and legend to the plot
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s^2)')
#plt.title('Acceleration versus Time (Walking)')
plt.title('Acceleration versus Time (Jumping)')
plt.legend()

# Show the plot
plt.show()

