from flask import Flask, render_template, json, Response, redirect, request, abort
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import json


class NameForm(FlaskForm):
    id = StringField('id', validators=[DataRequired()])
    url = StringField('图床链接', validators=[DataRequired()])
    author = StringField('画师')
    type = StringField('类型')
    title = StringField('标题')
    thumbnailBX = StringField('起始X坐标')
    thumbnailBY = StringField('起始Y坐标')
    thumbnailWidth = StringField('选取宽度(px)')
    thumbnailHeight = StringField('选取高度(px)')
    submit = SubmitField('提交')


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


def dictProcess(appendContent):
    form = NameForm()
    appendContent["url"] = form.url.data
    if form.thumbnailWidth.data != "" and form.thumbnailHeight.data != "":
        appendContent["thumbnailInfo"] = {
            "beginPointX": form.thumbnailBX.data,
            "beginPointY": form.thumbnailBY.data,
            "cutWidth": form.thumbnailWidth.data,
            "cutHeight": form.thumbnailHeight.data
        }
    appendContent["type"] = form.type.data
    appendContent["title"] = form.title.data
    appendContent["author"] = form.author.data


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

with open('gallery_list.json', encoding='utf-8') as f:
    gallery_JSON = json.load(f)


@app.route('/')
def index():
    return render_template('index.html', gallery_Json=gallery_JSON)


@app.route('/gallery_list')
def gallery_json():
    return json.dumps(gallery_JSON)


@app.route('/config')
@login_required
def configpage():
    form = NameForm()
    return render_template('commissionConfig.html', gallery_Json=gallery_JSON, form=form)


@app.route('/config', methods=['GET', 'POST'])
@login_required
def opForm():
    form = NameForm()
    if form.validate_on_submit():
        if form.submit.data:
            appendContent = {}
            if form.id.data != "New":
                appendContent["id"] = int(form.id.data) + 1
                dictProcess(appendContent)
                gallery_JSON["commissions"][int(form.id.data)] = appendContent
            else:
                appendContent["id"] = len(gallery_JSON["commissions"]) + 1
                dictProcess(appendContent)
                gallery_JSON["commissions"].append(appendContent)

            with open('gallery_list.json', 'w', encoding='utf-8') as f:
                json.dump(gallery_JSON, f, indent=4, ensure_ascii=False)
            return render_template('commissionConfig.html', gallery_Json=gallery_JSON, form=form)

        return ('', 204)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'username' and password == 'password':
            id = username.split('user')[0]
            user = User(id)
            login_user(user)
            return redirect(request.args.get("next"))
        else:
            return abort(401)
    else:
        return render_template('Login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('Logged Out')

@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')

@login_manager.user_loader
def load_user(userid):
    return User(userid)


if __name__ == '__main__':
    app.run()
