import glob
import contextlib
from PIL import Image
from contextlib import ExitStack
# filepaths
fp_in = "/out/rgb/rgb_*.jpg"
fp_out = "/out/videos/rgb.gif"

# use exit stack to automatically close opened images
with contextlib.ExitStack() as stack:

    # lazily load images
    imgs = (stack.enter_context(Image.open(f))
            for f in sorted(glob.glob(fp_in)))

    # extract  first image from iterator
    img = imgs.__next__()
    print(img)
    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
    img.save(fp=fp_out, format='GIF', append_images=imgs,
             save_all=True, duration=30, loop=0)