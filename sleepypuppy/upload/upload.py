#     Copyright 2015 Netflix, Inc.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
from flask import request, send_from_directory
from werkzeug import secure_filename
from sleepypuppy import app, csrf_protect
import os
from PIL import Image
from flask import Response

# Only allow png extensions, which is the filetype we generate using HTML5
# canvas.
ALLOWED_EXTENSIONS = set(['png'])


def allowed_file(filename):
    """
    Method to filter out bad filenames and prevent dir traversal.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@csrf_protect.exempt
@app.route('/up', methods=['GET', 'POST'])
def upload_file():
    """
    Store filename by timestamp and resize file for thumbnail.
    """
    response = Response()

    size = 256, 256
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # Prevent dir traversal/NUL byte injection
            filename = secure_filename(file.filename)

            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            im = Image.open(
                os.path.join(app.config['UPLOAD_FOLDER'], filename))
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(app.config['UPLOAD_FOLDER'] + '/small_' + filename, "PNG")
            _upload_to_s3(filename)
            _upload_to_s3('small_{}'.format(filename))
    return response


def _upload_to_s3(filename):
    """
    If configured, store screenshots in S3
    """
    if not app.config.get('UPLOAD_SCREENSHOTS_TO_S3', False):
        return

    import boto
    from boto.s3.key import Key
    conn = boto.connect_s3()
    b = conn.get_bucket(app.config['S3_BUCKET'])
    k = Key(b)
    k.key = '{}/{}'.format(
        app.config.get('S3_FILES_PREFIX', 'sleepypuppy'),
        filename
    )
    k.set_contents_from_filename(
        "{}/{}".format(
            app.config['UPLOAD_FOLDER'],
            filename
        )
    )
    os.remove(
        "{}/{}".format(
            app.config['UPLOAD_FOLDER'],
            filename
        )
    )


def _correct_s3_url(url):
    # bucket names containing periods break the *.s3.amazonaws.com SSL cert
    # so rewrite the URL.
    # https://bad.bucket.name.s3.amazonaws.com/sleepypuppy/...
    # ->
    # https://s3.amazonaws.com/bad.bucket.name/sleepypuppy/...
    url = url.replace('https://', '')
    bucket_name = url.split("s3.amazonaws.com/")[0][:-1]
    bucket_path = url.split("s3.amazonaws.com/")[1]
    return 'https://s3.amazonaws.com/{}/{}'.format(
        bucket_name,
        bucket_path
    )


@app.route('/up/<filename>')
def uploaded_file(filename):
    """
    Route to retrieve screenshot when requested.
    """
    if app.config.get('UPLOAD_SCREENSHOTS_TO_S3', False):
        import boto
        from flask import redirect
        conn = boto.connect_s3()
        url = conn.generate_url(
            expires_in=long(60 * 60 * 2),  # 2 hour expiry
            method='GET',
            bucket=app.config['S3_BUCKET'],
            key='{}/{}'.format(
                app.config.get('S3_FILES_PREFIX', 'sleepypuppy'),
                filename
            ),
            query_auth=True
        )
        url = _correct_s3_url(url)
        return redirect(url, 302)
    else:
        return send_from_directory(
            app.config['UPLOAD_FOLDER'],
            filename
        )
