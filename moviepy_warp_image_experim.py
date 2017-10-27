#!./venv/bin/python

"""
Description of the video:
Mimic of Star Wars' opening title. A text with a (false)
perspective effect goes towards the end of space, on a
background made of stars. Slight fading effect on the text.

"""

import numpy as np
from skimage import transform as tf

from moviepy.editor import *
from moviepy.video.tools.drawing import color_gradient
# import imageio
import matplotlib
# imageio.plugins.ffmpeg.download()
print(matplotlib)

# RESOLUTION

w = 720
h = w*9/16 # 16/9 screen
moviesize = w,h



# THE RAW TEXT
txt = "\n".join([
"A long time ago, in a faraway galaxy,",
"there lived a prince and a princess",
"who had never seen the stars, for they",
"lived deep underground.",
"",
"Many years before, the prince's",
"grandfather had ventured out to the",
"surface and had been burnt to ashes by",
"solar winds.",
"",
"One day, as the princess was coding",
"and the prince was shopping online, a",
"meteor landed just a few megameters",
"from the couple's flat."
])


# Add blanks
txt = 10*"\n" +txt + 10*"\n"


# CREATE THE TEXT IMAGE

stars = ImageClip('stars.jpg')
# clip_txt = TextClip(txt,color='white', align='West',fontsize=25,
#                     font='Arial', method='label')


# SCROLL THE TEXT IMAGE BY CROPPING A MOVING AREA

txt_speed = 100
fl = lambda gf,t : gf(t)[int(txt_speed*t):int(txt_speed*t)+h,:]
moving_img= stars.fl(fl, apply_to=['mask'])


# ADD A VANISHING EFFECT ON THE TEXT WITH A GRADIENT MASK

# grad = color_gradient(moving_img.size,p1=(0,2*h/3),
#                 p2=(0,h/4),col1=0.0,col2=1.0)
# gradmask = ImageClip(grad,ismask=True)
# fl = lambda pic : np.minimum(pic,gradmask.img)
# moving_img.mask = moving_img.fl_image(fl)


# WARP THE TEXT INTO A TRAPEZOID (PERSPECTIVE EFFECT)

def trapzWarp(pic,cx,cy,ismask=False):
    """ Complicated function (will be latex packaged as a fx) """
    Y,X = pic.shape[:2]
    src = np.array([[0,0],[X,0],[X,Y],[0,Y]])
    dst = np.array([[cx*X,cy*Y],[(1-cx)*X,cy*Y],[X,Y],[0,Y]])
    tform = tf.ProjectiveTransform()
    tform.estimate(src,dst)
    im = tf.warp(pic, tform.inverse, output_shape=(Y,X))
    return im if ismask else (im*255).astype('uint8')

fl_im = lambda pic : trapzWarp(pic,0.2,0.2)
# fl_mask = lambda pic : trapzWarp(pic,0.1,0.5, ismask=True)
warped_img= moving_img.fl_image(fl_im)
# warped_img.mask = warped_img.fl_image(fl_mask)


# BACKGROUND IMAGE, DARKENED AT 60%


stars_darkened = stars.fl_image(lambda pic: (0.6*pic).astype('int16'))


# COMPOSE THE MOVIE

# final = CompositeVideoClip([
#          stars_darkened,
#          warped_img.set_pos(('center','bottom'))],
#          size = moviesize)

final = warped_img

# WRITE TO A FILE

final.set_duration(10).write_videofile("starworms.mp4", fps=5)

# This script is heavy (30s of computations to render 8s of video)



"""=====================================================================

    CODE FOR THE VIDEO TUTORIAL

  We will now code the video tutorial for this video.
  When you think about it, it is a code for a video explaining how to
  make another video using some code (this is so meta !).
  This code uses the variables of the previous code (it should be placed
  after that previous code to work).

====================================================================="""
