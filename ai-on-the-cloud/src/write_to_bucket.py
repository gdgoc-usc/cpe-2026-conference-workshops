from google.cloud import storage

bucket_name = 'ai-on-the-cloud-test'
weight_filename = 'mnist_cnn.pt'


# --- 3. Connect and Upload ---
print(f"Connecting to bucket: {bucket_name}...")


storage_client = storage.Client() 
bucket = storage_client.bucket(bucket_name)


blob = bucket.blob(weight_filename)
blob.upload_from_filename(weight_filename)

print(f"\n✅ SUCCESS! Weights uploaded to:")
print(f"gs://{bucket_name}/{weight_filename}")
