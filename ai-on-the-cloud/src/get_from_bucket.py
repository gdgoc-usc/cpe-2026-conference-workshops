
import torch.nn as nn
from google.cloud import storage
from the_net import Net

FILE_NAME = 'mnist_cnn.pt'

# Prompt user for bucket name
BUCKET_NAME = input("Enter your GCS bucket name: ").strip()

if not BUCKET_NAME:
    print("❌ Error: Bucket name cannot be empty.")
    exit(1)

print(f"Connecting to bucket: {BUCKET_NAME}...")

# The storage client automatically uses the VM's built-in credentials!
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)
blob = bucket.blob(FILE_NAME)

print(f"Downloading {FILE_NAME}...")
blob.download_to_filename(FILE_NAME)
print("✅ Download complete!")