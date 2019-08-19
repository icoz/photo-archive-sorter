#!/usr/bin/env python3
# coding: utf8

from app import app
from app.db import db, fs, ObjectId
# from app import app, babel
# from app.forms import RequestForm, flash_form_errors
# from app.db import db, db_get_charts_list, db_get_chart, db_get_messages_stat, db_get_db_stat
from flask import request, render_template, redirect, url_for, flash, send_file
from app.images import save_image


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/surfer/by_date/<path:path>')
def surfer_date(path):
    return render_template('surfer_date.html', data=recs)


@app.route('/images/', defaults = {'skip':0})
@app.route('/images/skip/<int:skip>')
def list_images(skip):
    recs = db.images.find().skip(skip).limit(20)
    return render_template('images.html', data=recs, skip=skip)


@app.route('/image_file/<id>')
def image_file(id):
    img = db.images.find_one({"_id": ObjectId(id)})
    img_file = fs.get(img['fs_id'])
    return send_file(img_file, mimetype="image/jpeg")


@app.route('/image/<id>')
def image_info(id):
    recs = db.images.find_one({"_id": ObjectId(id)})
    # print(recs)
    similar = db.images.find({"phash": recs["phash"]}, {"_id": 1, "name": 1})
    return render_template('image_info.html', r=recs, similar=similar)

# https://stackoverflow.com/questions/35649770/how-to-upload-multiple-files-using-flask-in-python
# надо читать из FileStorage
# https://tedboy.github.io/flask/generated/generated/werkzeug.FileStorage.html


@app.route('/api/image/save', methods=['POST'])
def api_image_save():
    if request.method == 'POST':
        # pprint(request.form)
        # print("data_len=", len(request.data))
        # print("files_len=", len(request.files))
        # print("files = ", list(request.files.getlist("photos")))
        for file in request.files.getlist("photos"):
            # print(file.filename)
            save_image(file)

        return redirect(url_for("home"))
    # form = RequestForm.new()
    # if form.validate_on_submit():
    # img = request.args.get('chart')
    # for k in request.args:
    #     print(f"{k}: {request.args.get(k)}")
    return render_template("test.html", ra=request.args)
