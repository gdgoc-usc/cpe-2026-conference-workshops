import torch
from google.cloud import storage
from the_net import Net


model = Net()


weight_filename = 'mnist_cnn.pt'
torch.save(model.state_dict(), weight_filename)
print(f"Saved weights locally as {weight_filename}")


bucket_name = "REPLACE_WITH_YOUR_BUCKET_NAME" 

# --- 3. Connect and Upload ---
print(f"Connecting to bucket: {bucket_name}...")


storage_client = storage.Client() 
bucket = storage_client.bucket(bucket_name)


blob = bucket.blob(weight_filename)
blob.upload_from_filename(weight_filename)

print(f"\n✅ SUCCESS! Weights uploaded to:")
print(f"gs://{bucket_name}/{weight_filename}")
