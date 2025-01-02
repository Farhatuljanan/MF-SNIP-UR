# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 10:39:14 2024

@author: fjanan
"""

import matplotlib.pyplot as plt
import numpy as np

# Create some data
#x = np.linspace(0, 10, 100)
x=[20, 40, 60]
## Network 1

y1 = [116.77, 116.77, 116.77]
y2 = [105.55, 84.86, 63.9]
y3 = [115.20, 114.96, 114.05]
y4=[114.56, 112.06, 109.14]
y5=[114.56, 112.08, 109.23]
plt.figure(figsize=(10, 8))
plt.plot(x, y1, marker='o', linestyle='-', label='Max flow')
plt.plot(x, y2, marker='s', linestyle='None', label='MFNIP')
plt.plot(x, y3,marker='^', linestyle='None', label='MFNIP interdiction plan in MF-SNIP-UR')
plt.plot(x, y4, marker='v', linestyle='None',label='MF-SNIP-UR before restructuring')
plt.plot(x, y5, marker='D', linestyle='None', label='MF-SNIP-UR')

plt.xticks([20, 40, 60])
# Add labels and title
plt.xlabel('Budget')
plt.ylabel('Flow')
plt.title('Budget vs. Flow in Network 1')

# Add a legend to differentiate the lines
plt.legend()

# Show the plot
plt.show()


## Network 2

y1=[111.89,111.89,111.89]
y2=[85.91, 60.12,36.89]
y3=[110.18,108.91,106.59]
y4=[109.03, 103.81, 99.62]
y5=[109.03, 104.40, 100.62]
plt.figure(figsize=(10, 8))
plt.plot(x, y1, marker='o', linestyle='-', label='Max flow')
plt.plot(x, y2, marker='s', linestyle='None', label='MFNIP')
plt.plot(x, y3,marker='^', linestyle='None', label='MFNIP interdiction plan in MF-SNIP-UR')
plt.plot(x, y4, marker='v', linestyle='None',label='MF-SNIP-UR before restructuring')
plt.plot(x, y5, marker='D', linestyle='None', label='MF-SNIP-UR')

plt.xticks([20, 40, 60])
# Add labels and title
plt.xlabel('Budget')
plt.ylabel('Flow')
plt.title('Budget vs. Flow in Network 2')

# Add a legend to differentiate the lines
plt.legend()

# Show the plot
plt.show()


## Network 3

y1=[114.44,114.44,114.44]
y2=[97.25, 74.93, 55.88]
y3=[113.96, 112.58, 111.83]
y4=[111.22, 107.55, 103.57]
y5=[111.22, 107.56, 104.03]
plt.figure(figsize=(10, 8))
plt.plot(x, y1, marker='o', linestyle='-', label='Max flow')
plt.plot(x, y2, marker='s', linestyle='None', label='MFNIP')
plt.plot(x, y3,marker='^', linestyle='None', label='MFNIP interdiction plan in MF-SNIP-UR')
plt.plot(x, y4, marker='v', linestyle='None',label='MF-SNIP-UR before restructuring')
plt.plot(x, y5, marker='D', linestyle='None', label='MF-SNIP-UR')

plt.xticks([20, 40, 60])
# Add labels and title
plt.xlabel('Budget')
plt.ylabel('Flow')
plt.title('Budget vs. Flow in Network 3')

# Add a legend to differentiate the lines
plt.legend()

# Show the plot
plt.show()

## Network 4

y1=[110.55,110.55,110.55]
y2=[98.36, 70.83, 51.47]
y3=[109.77, 108.51, 108.52]
y4=[108.50, 105.48, 101.95]
y5=[108.50, 105.48, 101.96]

plt.figure(figsize=(10, 8))
plt.plot(x, y1, marker='o', linestyle='-', label='Max flow')
plt.plot(x, y2, marker='s', linestyle='None', label='MFNIP')
plt.plot(x, y3,marker='^', linestyle='None', label='MFNIP interdiction plan in MF-SNIP-UR')
plt.plot(x, y4, marker='v', linestyle='None',label='MF-SNIP-UR before restructuring')
plt.plot(x, y5, marker='D', linestyle='None', label='MF-SNIP-UR')

plt.xticks([20, 40, 60])
# Add labels and title
plt.xlabel('Budget')
plt.ylabel('Flow')
plt.title('Budget vs. Flow in Network 4')

# Add a legend to differentiate the lines
plt.legend()

# Show the plot
plt.show()


## Network 5

y1=[118.28,118.28,118.28]
y2=[108.57, 88.25, 68.47]
y3=[113.43, 116.24, 115.60]
y4=[116.54, 113.95, 111.13]
y5=[116.59, 114.03, 111.16]
# Plot multiple lines on the same graph
#plt.plot(x, y1, label='Max flow')
plt.figure(figsize=(10, 8))
plt.plot(x, y1, marker='o', linestyle='-', label='Max flow')
plt.plot(x, y2, marker='s', linestyle='None', label='MFNIP')
plt.plot(x, y3,marker='^', linestyle='None', label='MFNIP interdiction plan in MF-SNIP-UR')
plt.plot(x, y4, marker='v', linestyle='None',label='MF-SNIP-UR before restructuring')
plt.plot(x, y5, marker='D', linestyle='None', label='MF-SNIP-UR')

plt.xticks([20, 40, 60])
# Add labels and title
plt.xlabel('Budget')
plt.ylabel('Flow')
plt.title('Budget vs. Flow in Network 5')

# Add a legend to differentiate the lines
plt.legend()

# Show the plot
plt.show()

