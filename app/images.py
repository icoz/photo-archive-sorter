#!/usr/bin/env python3
# coding: utf8
from app.db import db, fs, ObjectId
from app.photohash import average_hash, open_img, phash
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS                                                                                                                                                        
from hashlib import sha256
from pprint import pprint


def find_similar(phash):
    similar = db.images.find({"phash": phash.asString()},{"_id": 1})


def save_image(file=None):
    image_data = file.read()    # get raw data
    file_length = len(image_data)
    img = Image.open(file)      # open image
    hash = sha256(image_data).hexdigest()
    phash_v = average_hash(img)
    # phash_v = phash(img)
# get EXIF (if it's JPEG?)
    exif = img.getexif()
# get EXIF
    exif_data = { TAGS[k]: exif[k] for k in exif if TAGS[k] not in ["MakerNote","UserComment"]}
# make metadata to file
    file_data = {
        "name": file.filename,
        # "fs_id": file_id,
        "size": file_length,
        "exif": exif_data,
        "sha256": hash,
        "phash": phash_v.asString(),
    }
    # pprint(file_data)
    q_res = db.images.find_one({"sha256": hash})
    if q_res: #if we have this one... del(then link this meta to it)
        # print(q_res)
        # file_id = q_res['fs_id']
        #no need to save it at all! 
        # хранять не надо, но вернем имеющийся id, 
        # как правило для добавления тегов
        return q_res['_id']    
    else: # we have no such files
# Save data to GRIDFS
        with fs.new_file(content_type="image/jpeg") as f:
            file_id = f._id # remember file_id before file is closed.
            f.write(image_data)
    file_data['fs_id'] = file_id
    # search similar phashes
    q_res = db.images.find({"phash": phash_v.asString()},{"_id": 1})
    # print("similar by phash (delta=0): ", q_res.count())
    file_data['similar'] = list(map(lambda x: ObjectId(x['_id']), q_res))
# save it to DB.
    image_id = db.images.insert(file_data)
    for img_upd_id in file_data['similar']:
        db.images.update_one({"_id": ObjectId(img_upd_id)}, {"$push": {"similar": ObjectId(image_id)}})
        # pprint(f"{img_upd_id} updated")
    return image_id
