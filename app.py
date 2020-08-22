from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField
from flask_uploads import patch_request_class, configure_uploads, UploadSet, IMAGES, DATA, TEXT, ARCHIVES
## pip install Flask-Reuploaded

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisasecret'
patch_request_class(app, 25 * 1024 * 1024) # (n * 1024 * 1024) bytes
app.config['UPLOADED_UPLOADS_DEST'] = 'uploads/'

uploads = UploadSet('uploads', IMAGES + DATA + TEXT + ARCHIVES)
configure_uploads(app, uploads)


class MyForm(FlaskForm):
    image = FileField('image')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    if form.validate_on_submit():
        filename = uploads.save(form.image.data)
        return '<h1>'+uploads.url(filename)+'</h1>'

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)