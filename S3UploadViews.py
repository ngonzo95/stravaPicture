import boto3
import os

def upload_views_to_s3():
	s3_client = boto3.client('s3')
	for filename in os.listdir('views'):
		if 'html' in filename:
			s3_client.upload_file("views/" + filename,
				"nicholas-gonzalez.com",
				filename,
				ExtraArgs={'ContentType': 'text/html'})
	


if __name__ == '__main__':
	upload_views_to_s3()