import torch
from google.cloud import storage
from the_net import Net


model = Net()

# --- 1. Save the PyTorch model weights locally ---
weight_filename = 'mnist_cnn.pt'
torch.save(model.state_dict(), weight_filename)
print(f"Saved weights locally as {weight_filename}")

# --- 2. Define the target bucket ---
# ⚠️ Attendees MUST replace this string with the exact name they created in the console!
bucket_name = "REPLACE_WITH_YOUR_BUCKET_NAME" 

# --- 3. Connect and Upload ---
print(f"Connecting to bucket: {bucket_name}...")

# Workbench automatically handles the authentication and project mapping
storage_client = storage.Client() 
bucket = storage_client.bucket(bucket_name)

# Create a blob (the destination file) and upload the local file
blob = bucket.blob(weight_filename)
blob.upload_from_filename(weight_filename)

print(f"\n✅ SUCCESS! Weights uploaded to:")
print(f"gs://{bucket_name}/{weight_filename}")
