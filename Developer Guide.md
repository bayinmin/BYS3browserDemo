
# BYS3browserDemo Developer Guide

This is the POC/Demo version to show how Amazon aws S3 could be used with python Flask backend. This application is for demo only and not suitable for production use.

# Framework

1. python Flask - version 0.12.2
2. AWS S3 - Account

# Dependencies

1. Python -> pthon 2.7.x base for python flask
2. Virtualenv -> virtual python enviroment if needed
3. boto3 -> for S3 CRUD API


# Dependencies Installation

This app was developed in OSX environment. The setup maybe slightly varies on different platform.

1. Install python 2.7.x
2. Install pip
3. Install Flask with pip. It is the developer choice whether to install virtualenv or python virtual environment. 

   Reference: https://gist.github.com/dineshviswanath/af72af0ae2031cd9949f
4. Install boto3 with pip. Current version of this s3browser, the key are hardcoded in the application.

   Reference: https://boto3.readthedocs.io/en/latest/guide/quickstart.html
5. While installing boto3 and if you come across “six” library problem, refer to the following solutions.

   Reference: https://stackoverflow.com/questions/31900008/oserror-errno-1-operation-not-permitted-when-installing-scrapy-in-osx-10-11
   
   #### Fix six library problem 
   `sudo -H pip install boto3 --upgrade --ignore-installed six`

# Step to launch application

1. Download the application folder from github
2. Make sure you have the following amazon account setting satisfied:
	2.1 Valid amazon aws account
	2.2 Create non root s3 test account user with limited rights. Use strong password for this s3 test account.
	2.3 Create group policy to allow "AmazonS3FullAccess". This is potentially dangerous and remove the access rights as soon as the testing is done
	2.4 Assign s3 test account user to newly created access group
	2.5 Generate access key and secret key
3. Locate the app.py in the application folder. Edit the file to input the valid access key and secret key of your own
4. Open Terminal/Command Prompt and navigate to the application folder
5. type "python app.py" and the server should start to run on port 5000 as default
6. Open Web Browser and navigate to http://localhost:5000/. The s3 browser home page should be showing.


# Further improvement point

1. Not hardcoding the S3 keys in the source code. To shift to environmental variable
2. Perform proper input validations
3. Improve of UI and Navigation
4. More stringent error handlings
