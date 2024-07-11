from google.cloud import storage
from typing import Any

def get_article_files(bucket_name: str,
                      storage: Any):
    storage_client = storage
    #bucket = storage_client.get_bucket(bucket_name)
    file_list = storage_client.list_blobs(bucket_name)
    list_file = [file.name for file in file_list]
    return list_file

def download_article_from_gcs(GCS_BUCKET:str,
                              storage_client:Any,
                              file_name:str,
                              directory:str):
    bucket = storage_client.get_bucket(GCS_BUCKET)
    blob = bucket.blob(file_name)
    path_to_tmp_file = directory + '/' + file_name
    blob.download_to_filename(path_to_tmp_file)
    return path_to_tmp_file
