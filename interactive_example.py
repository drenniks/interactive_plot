import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from PIL import Image

from matplotlib import rc
rc('font', size=18)

#List of paths to images
files = []
path = 'output_plots/'
for i in os.listdir(path):
    files.append(path + str(i))

#Scatter data
xx = np.random.randn(1, 20)[0]
yy = np.random.randn(1, 20)[0]

#Names for scatter points
names=[]
for i in range(len(xx)):
    names.append(str(i))

#Scatter point color
x=np.random.randn(1, 20)[0]

#Plotting xx and yy
norm = plt.Normalize(np.min(xx),np.max(xx))
cmap = plt.cm.viridis
fig, ax = plt.subplots(figsize=(10,8))
sc = plt.scatter(xx, yy, c=x, cmap=cmap, norm=norm, label='Scatter')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()
fig.colorbar(sc, label='Random')

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))

annot.set_visible(False)

def create_collage(width, height, listofimages):
	#Credit to Hugo on stackoverflow ( https://stackoverflow.com/questions/35438802/making-a-collage-in-pil )
    cols = 2
    rows = 2
    thumbnail_width = width//cols
    thumbnail_height = height//rows
    size = thumbnail_width, thumbnail_height
    new_im = Image.new('RGB', (width, height))
    ims = []
    for p in listofimages:
        im = Image.open(p)
        im.thumbnail(size)
        ims.append(im)
    i = 0
    x = 0
    y = 0
    for col in range(cols):
        for row in range(rows):
            new_im.paste(ims[i], (x, y))
            i += 1
            y += thumbnail_height
        x += thumbnail_width
        y = 0
    new_im.show()

#Credit to ImportanceOfBeingErnest on stackoverflow ( https://stackoverflow.com/questions/7908636/possible-to-make-labels-appear-when-hovering-over-a-point-in-matplotlib )
def update_annot(ind):
    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "{}".format(" ".join([names[n] for n in ind["ind"]]))
    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor(cmap(norm(x[ind["ind"][0]])))
    annot.get_bbox_patch().set_alpha(0.4)

def click(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        x_pos = float(event.xdata)
        y_pos = float(event.ydata)
        print('You clicked at position: ', (round(x_pos, 3), round(y_pos, 3)))
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
            print('Pulling up plots: ')
            for i in files:
                print('\t', i)
            create_collage(2000,2000, files)
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

fig.canvas.mpl_connect('button_press_event', click)
plt.show()

