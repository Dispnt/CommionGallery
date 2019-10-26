from flask import Flask, render_template, json,request
from datetime import timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from PIL import Image
import urllib.request
import io
import base64
import json

class NameForm(FlaskForm):
    url = StringField('图床链接', validators=[DataRequired()])
    author = StringField('画师')
    type = StringField('类型')
    title = StringField('标题')
    thumbnailBX = StringField('起始X坐标')
    thumbnailBY = StringField('起始Y坐标')
    thumbnailWidth = StringField('选取宽度(px)')
    thumbnailHeight = StringField('选取高度(px)')
    submit = SubmitField('提交')

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

with open('gallery_list.json',encoding='utf-8') as f:
    gallery_JSON = json.load(f)

@app.route('/gallery_list')
def gallery_json():
    return json.dumps(gallery_JSON)

@app.route('/')
def index():
    return render_template('index.html', gallery_Json=gallery_JSON)

@app.route('/config')
def configpage():
    form = NameForm()
    return render_template('commissionConfig.html', gallery_Json=gallery_JSON,form=form)

@app.route('/config',methods=['GET','POST'])
def opForm():
    form = NameForm()
    if form.validate_on_submit():
        if form.submit.data:
            url = form.url.data
            author = form.author.data
            type = form.type.data
            title = form.title.data
            description = form.title.data
            beginPointX = form.thumbnailBX.data
            beginPointY = form.thumbnailBY.data
            thumbnailWidth = form.thumbnailWidth.data
            thumbnailHeight = form.thumbnailHeight.data
            appendContent = {
                "id": len(gallery_JSON["commissions"])+1,
                "url": url,
                "thumbnailInfo": {
                    "beginPointX": beginPointX,
                    "beginPointY": beginPointY,
                    "cutWidth": thumbnailWidth,
                    "cutHeight": thumbnailHeight
                },
                "title": title,
                "author": author,
                "type": type,
                "description": description
            }
            appendContent2 = {
                "id": 41,
                "url": url,
                "thumbnailInfo": {
                    "beginPointX": beginPointX,
                    "beginPointY": beginPointY,
                    "cutWidth": thumbnailWidth,
                    "cutHeight": thumbnailHeight
                },
                "title": title,
                "author": author,
                "type": type,
                "description": description
            }
            gallery_JSON["commissions"][4] = appendContent2
            # gallery_JSON["commissions"].append(appendContent)
            with open('gallery_list.json', 'w') as f:
                json.dump(gallery_JSON, f, indent=4)
            return render_template('commissionConfig.html', gallery_Json=gallery_JSON, form=form)
        return ('', 204)

if __name__ == '__main__':
    app.run()
