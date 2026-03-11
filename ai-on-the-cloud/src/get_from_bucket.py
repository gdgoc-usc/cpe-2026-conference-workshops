
import torch.nn as nn
from google.cloud import storage
from the_net import Net

BUCKET_NAME = 'your-bucket-name'
FILE_NAME = 'mnist_cnn.pt'


print(f"Connecting to bucket: {BUCKET_NAME}...")

# The storage client automatically uses the VM's built-in credentials!
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)
blob = bucket.blob(FILE_NAME)

print(f"Downloading {FILE_NAME}...")
blob.download_to_filename(FILE_NAME)
print("✅ Download complete!")