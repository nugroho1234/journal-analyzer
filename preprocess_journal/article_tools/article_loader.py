from google.cloud import storage
from typing import Any

def get_article_files(bucket_name: str,
                      storage: Any):
    storage_client = storage
    #bucket = storage_client.get_bucket(bucket_name)
    file_list = storage_client.list_blobs(bucket_name)
    list_file = [file.name for file in file_list]
    return list_file