import tempfile
import shutil

FILE_UPLOAD_DIR = '/cache/upload'

def handle_uploaded_file(source):
    #fd, filepath = tempfile.mkstemp(prefix=source.name, dir=FILE_UPLOAD_DIR)
    # with open(filepath, 'a') as dest:
        # shutil.copyfile(source, dest)
    # return filepath
    
    with open (source) as f:
        read_data = f.read()
    f.closed
    
    def __unicode__(self):
        return read_data