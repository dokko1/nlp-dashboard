from .constants import colors
from pathlib import Path
import base64

def construct_styled_component(tag, index, input1, colored, input2):
    html = f"""
    <{tag}>
        {input1}
        <span style='background-color: {colors[index]}'>
            {colored}
        </span>
        {input2}
    </{tag}>
    """

    return html

def construct_horizontal_star(count):
    star_img = img_to_html('./img/full.png')
    star_imgs = ''
    for i in range(int(count)):
        star_imgs += star_img
    
    # add half star if needed
    half_star = img_to_html('./img/half.png')
    if (count-int(count)>=0.5 and count-int(count)<1):
        star_imgs += half_star

    # put star_imgs into format
    html = f"""
    <div style='display: flex'>
        <div style='flex-direction: row'>
            {star_imgs}
        </div>
    </div>
    """
    return html

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' width='20' height='20'>".format(
      img_to_bytes(img_path)
    )
    return img_html