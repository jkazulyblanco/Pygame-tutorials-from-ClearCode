# 01 # setup | # 02 # Draw axes | # 03 # Add Graphs  
# 04 # Customizing Graphs | # 05 # Adding Text |
# 06 # Styling |

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
fig.patch.set_facecolor('darkorange') # 06 #
font_style = {'color':'tab:grey', 'family':'fantasy', 'weight':'bold'}
font_style2 = {'color':'lightgreen', 'family':'fantasy', 'weight':'bold'}

# Ratings ========================================
# 02 # Draw axes box for graphs, size = inches
ax_rating = fig.add_axes([0.05,0.05,0.9,0.35]) # 02 #
ax_rating.bar(x= seasons, height= ratings) # 03 #
# 04 #
ax_rating.set_xticks([0,9,19,29]) # seasons to show
ax_rating.set_ylim(3,9) # Rating to show
ax_rating.set_title('Random Ratings', fontdict= font_style)
# 05 #
ax_rating.text(1, 8, 'Golden Age', size= 16, bbox= {'fc':'purple', 'ec':'red'}, fontdict= font_style)
ax_rating.text(25, 4, 'Zombie Simpsons', size= 16, bbox= {'fc':'purple', 'ec':'red'}, fontdict= font_style2)

# Views ==========================================
ax_views = fig.add_axes([0.05,0.45,0.9,0.5]) # 02 #
ax_views.plot(years, views, linewidth= 4, solid_capstyle= 'round') # 03, 06 #
# 04 #
ax_views.set_xticks([]) # empty
ax_views.set_title('Random Views (in millions)', fontdict= font_style)
# 05 # axes.text(location,content)
ax_views.text(1988, 26, '1989', fontdict= font_style) 
ax_views.text(2018, 10, '2018', fontdict= font_style)

 # 06 # Styling
for axes in [ax_views, ax_rating]:
    axes.set_facecolor('yellow')
    axes.tick_params(colors= 'lightgreen', labelsize= 12, width= 2)
    # line box axes color
    for side in ['bottom', 'top', 'left', 'right']:
        axes.spines[side].set_color('tab:red')
        axes.spines[side].set_linewidth(2)

plt.show() # 01 #

# to save pic
# plt.savefig('random Simpson', facecolor = 'darkorange')




