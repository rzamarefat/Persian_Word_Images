from glob import glob
from PIL import Image, ImageFont, ImageDraw
import os
from uuid import uuid1
import numpy as np
from tqdm import tqdm

config = {
  "path_to_farsi_text_data": "./farsi_data/farsi_sents.txt",
  "root_path_to_farsi_fonts": "./farsi_fonts/*",
  
  "root_path_to_generated_text_images": "./text_images/",
  
  "number_of_text_images_per_word": 1,
}


def get_words():
    with open(config["path_to_farsi_text_data"]) as h:
        sents = [l.replace("\n", "") for l in h.readlines()]
    
    words = []
    for s in sents:
        s = s.split(" ")
        
        for w in s:
            if not(w in words):
                words.append(w)
                
    return words

def generate():
    words = get_words()
    fonts = [f for f in sorted(glob(config["root_path_to_farsi_fonts"]))]
    
    print(f"Number of unique words in the data: {len(words)}")
    print(f"Number of fonts: {len(fonts)}")
    
    
    for w in tqdm(words):
        for f in fonts:
            font = ImageFont.truetype(f, 20)
            text_w, text_l = font.getsize(w)
            
            img = np.zeros([text_w + 10, text_l + 10,3],dtype=np.uint8)
            img.fill(255)
            img = Image.fromarray(img)
            #img = Image.new('RGB', (text_w + 10, text_l + 10))
            bg_w, bg_h = img.size
            draw = ImageDraw.Draw(img)
            draw.text(((bg_w - text_w) / 2, (bg_h - text_l) / 2),w,(0,0,0),font=font)
            
            
            name_of_generated_text_image = str(uuid1())[0:8]
            img.save(os.path.join(config["root_path_to_generated_text_images"], f"{name_of_generated_text_image}.jpg"))
            with open(os.path.join(config["root_path_to_generated_text_images"], f"{name_of_generated_text_image}.txt"), "a+") as h:
                h.seek(0)
                h.writelines(w)
        
if __name__ == "__main__":
    generate()