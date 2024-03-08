import mimetypes
import os


def fileUpload(request):
    if 'cert' not in request.files:
        return 'No cert part in the request'

    file = request.files['cert']

    if file.filename == '':
        return 'No selected file'

    try:
        # save it to the folder
        upload_folder = 'static/uploads'
        file.save( upload_folder + '/' + file.filename)
        # Determine the file type
        file_type, encoding = mimetypes.guess_type(os.path.join(upload_folder, file.filename))
        new_filename = 'myfile123' + '.' + file_type.split('/')[1]
        file_path = os.path.join(upload_folder, new_filename)
        os.rename(os.path.join(upload_folder, file.filename), file_path)
        return 'File uploaded successfully'
    except Exception as e:
        return str(e)

