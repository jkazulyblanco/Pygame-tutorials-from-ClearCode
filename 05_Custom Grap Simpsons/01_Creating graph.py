# 01 # setup | # 02 # Draw axes | # 03 # Add Graphs  
# 04 # Customizing Graphs | # 05 # Adding Text |

#▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀

# 01 #
import matplotlib.pyplot as plt
import random

# Data ===========================================
seasons = [f'Season {i}' for i in range(1, 31)]
years   = [i for i in range(1989,2019)]
ratings = []
views   = []

# 01 # fill each list with 30 random float ranges
for i in range(0,30):
    r = round(random.uniform(3.5,8.4),1)
    v = round(random.uniform(7.0,28.0),1)
    ratings.append(r)
    views.append(v)
# Sort lists form largest to smallest    
ratings = sorted(ratings, key= float, reverse= 1)
views = sorted(views, key= float, reverse= 1)

# General ========================================
fig = plt.figure(figsize= (13,6.5)) # 02 # 

# Ratings ========================================
# 02 # Draw axes box for graphs, size = inches
ax_rating = fig.add_axes([0.05,0.05,0.9,0.35]) # 02 #
ax_rating.bar(x= seasons, height= ratings) # 03 #
# 04 #
ax_rating.set_xticks([0,9,19,29]) # seasons to show
ax_rating.set_ylim(3,9) # Rating to show
ax_rating.set_title('Random Ratings')
# 05 #
ax_rating.text(1, 8, 'Golden Age', bbox= {})
ax_rating.text(25, 4, 'Zombie Simpsons', bbox= {})

# Views ==========================================
ax_views = fig.add_axes([0.05,0.45,0.9,0.5]) # 02 #
ax_views.plot(years, views) # 03 #
# 04 #
ax_views.set_xticks([]) # empty
ax_views.set_title('Random Views (in millions)')
# 05 #
ax_views.text(1988, 26, '1989') 
ax_views.text(2018, 10, '2018') 

plt.show() # 01 #

# axes.text(location,content) # 05 #


