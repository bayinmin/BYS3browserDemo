from flask import Flask, render_template, request, make_response
import boto3, botocore
import random

ACCESS_KEY = 'DUMMY'
SECRET_KEY = 'DUMMY'

GOTO_BUCKET_LISTING_PAGE = "<a href=\"\\..\\..\\\"> Go to index </a>"

app = Flask(__name__)
app.secret_key = 'random string'

client = boto3.client(
    's3',
    aws_access_key_id= ACCESS_KEY,
    aws_secret_access_key= SECRET_KEY,
    # aws_session_token=SESSION_TOKEN,
)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = 'some_secret'

#Restrict uploadable file types
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Dummy error message         
def print_exception_homepage(e):
    return "Error Occurred --> " + str(e) + GOTO_BUCKET_LISTING_PAGE

# List All Buckets  
@app.route('/')
def buckets():
    response = client.list_buckets()
    print type(response['Buckets'])
    return render_template('index.html', buckets=response['Buckets'])

# Get Specific Bucket
@app.route('/bucket/<bid>', methods=['GET', 'POST'])
def get_bucket(bid):
    if request.method == 'POST':
    # # check if the post request has the file part
        upload_bid = request.form['bid']
        if 'file' not in request.files:
            return "no file part"
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return "no selected file"
        if file and allowed_file(file.filename):
            file_name = str(random.randint(1, 100)) + "_" + file.filename
            client.upload_fileobj(file, upload_bid, file_name)
            return "File successfully uploaded" + GOTO_BUCKET_LISTING_PAGE
    else:
        s3 = boto3.resource('s3')
        file_list = []
        try:
            bucket = s3.Bucket(bid)
            for key in bucket.objects.all():
                file_list.append(key.key)
            return render_template('get_bucket.html', bucket_content=file_list, bid=bid)
        except botocore.exceptions.ClientError as e:
            return print_exception_homepage(e)

# Download file from the bucket
@app.route('/bucket/<bid>/download/<filename>', methods=['GET', 'POST'])
def download_file_from_bucket(bid,filename):
    s3 = boto3.client('s3')
    with open(filename, 'wb') as data:
        s3.download_fileobj(bid, filename, data)
        
    f = open(filename, 'r')
    response = make_response(f.read())
    response.headers["Content-Disposition"] = "attachment; filename=" + filename
    
    return response
    return filename + "has been downloaded. check in folder." + GOTO_BUCKET_LISTING_PAGE   

# Delete the file within the bucket    
@app.route('/bucket/<bid>/delete/<filename>', methods=['GET', 'POST'])
def delete_file_from_bucket(bid,filename):
    s3 = boto3.resource('s3')
    try:
        bucket = s3.Bucket(bid)
        for key in bucket.objects.all():
            if key.key == filename:
                key.delete()
                return "Successfully deleted the file " + GOTO_BUCKET_LISTING_PAGE
            else:
                return "File not found " + GOTO_BUCKET_LISTING_PAGE
        return "Error Occured" + GOTO_BUCKET_LISTING_PAGE
    except botocore.exceptions.ClientError as e:
        return print_exception_homepage(e)

# Create the bucket   
@app.route('/bucket/create', methods=['GET', 'POST'])
def create_bucket():
    if request.method == 'POST':
        if len(request.form['bid']) > 0:
            try:
                response = client.create_bucket(Bucket=request.form['bid'])
                return "successfully created the bucket" + GOTO_BUCKET_LISTING_PAGE
            except botocore.exceptions.ClientError as e:
                return print_exception_homepage(e)  
        else:
            return "Enter valid bucket name"
    else:
        return render_template('create_bucket.html', bucket_content="this is bucket content")
    

# Delete the bucket
@app.route('/bucket/<bid>/delete')
def delete_bucket(bid):
    s3 = boto3.resource('s3')
    try:
        bucket = s3.Bucket(bid)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()
        return "Successfully deleted the bucket" + GOTO_BUCKET_LISTING_PAGE
    except botocore.exceptions.ClientError as e:
        return print_exception_homepage(e)

# Rename existing specific bucket 
@app.route('/bucket/<bid>/rename', methods=['GET', 'POST'])
def rename_bucket(bid):
    if request.method == 'POST':
        cur_bid = request.form['current_bid']
        new_bid = request.form['new_bid']
        if len(cur_bid) > 0 and len(new_bid) > 0 and cur_bid != new_bid:
            try:
                # create new bucket
                response = client.create_bucket(Bucket=new_bid)
                s3 = boto3.resource('s3')
                src = s3.Bucket(cur_bid)
                # copy over all the files
                for k in src.objects.all():
                    print str(k.key)
                    copy_source = {
                        'Bucket': cur_bid,
                        'Key': k.key
                    }
                    s3.meta.client.copy(copy_source, new_bid, k.key)
                # delete old bucket
                for key in src.objects.all():
                    key.delete()
                src.delete()
                return "Successfully renamed the bucket. " + GOTO_BUCKET_LISTING_PAGE
            except botocore.exceptions.ClientError as e:
                return print_exception_homepage(e)  
        else:
            return "Enter valid bucket name"
    else:
        return render_template('rename_bucket.html', bid=bid)

if __name__== '__main__':
	app.run(debug=True)



