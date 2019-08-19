#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config 
from app import app
from os import environ as env
import os
import sys
from app.db import db,fs, ObjectId
from app.images import save_image

__author__ = 'icoz'

# if env.get('PhAS_PRODUCTION'):
#     app.run(host='0.0.0.0', port=80)
# else:

def load_images_from_dir(dir_name, top_level=False):
    img_ids = list()
    print(f"Working on loading images from dir '{dir_name}'")
    for fname in os.listdir(dir_name):
        if os.path.isdir(f"{dir_name}/{fname}"):
            ids = load_images_from_dir(f"{dir_name}/{fname}")
            if not top_level:
                for img_id in ids:
                    db.images.update_one({'_id': ObjectId(img_id)}, {"$push": {"tags": os.path.basename(dir_name)}})
            print(f"...continue in dir {dir_name}")
            img_ids += ids
        else:
            # try:
            if os.path.basename(fname).split('.')[1].lower() in ['jpg','jpeg']:
                print(f"loading file '{dir_name}/{fname}'")
                with open(f"{dir_name}/{fname}",'rb') as f:
                    f.__setattr__("filename", fname)
                    img_id = save_image(f)
                print(f"saved with id={img_id}")
                img_ids.append(img_id)
                if not top_level:
                    db.images.update_one({'_id': ObjectId(img_id)}, {"$push": {"tags": os.path.basename(dir_name)}})
    return img_ids
            # except:
                # print("except")

def main():
    print(db)
    if len(sys.argv) > 1:
        for dir_name in sys.argv[1:]:
            load_images_from_dir(dir_name, top_level=True)
    else:
        print(f"Usage: {sys.argv[0]} dir_name [dir_names...]")
    pass

if __name__ == '__main__':
    main()

