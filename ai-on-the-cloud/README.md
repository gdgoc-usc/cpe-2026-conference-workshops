# AI on the Cloud
The repository that contains all the programms used in the RACCETCON pre-conference workshops.

## Directory Structure
```
src
├── app.py
├── config.json
├── for_workshop.ipynb
├── full_notebook.ipynb
├── get_from_bucket.py
├── helper.py
├── mnist_cnn.pt
├── requirements.txt
├── the_net.py
└── write_to_bucket.py
```

### app.py
The script that loads the model weights and launches the gradio UI.

### config.json
Not used in any script. But compiled for reference.

### for_workshop.ipynb
The notebook that was used in the workshop

### full_notebook.ipynb
The full notebook with train, testing, and saving the weights.

### helper.py
Helper functions with the train and test loaders.

### requirements.txt
requirements file used to install the packages with `pip install -r requirements.txt`

### the_net.py
The neural network defined with Pytorch.

### write_to_bucket.py
saves the weights to the Google Cloud bucket.

### get_from_bucket.py
retrieves the weight from the Google Cloud bucket.

## Deployment Process
**1. Install Required Packages**
```bash
pip install -r requirements.txt
```
**2. Run Notebook**
Click on the <img src="media/image-7.png" style="vertical-align:middle" height="20"> button.

![alt text](media/image-8.png)
**3. Creating the bucket**

Search `bucket` and click on <img src="media/image-4.png" style="vertical-align:middle" height="20">

![alt text](media/image-3.png)

Click on `create`.
![alt text](media/image-5.png)

Then write your own bucket name. Remember this for later.
![alt text](media/image-6.png)

**3. Saving the weights to Google Cloud**
Replace the `bucket_name` variable with your bucket name that you just made in `write_to_bucket.py`.

**4. Creating Virtual Machine**
Search Virtual Machine and then click on VM Instances.
![alt text](media/image-9.png)

Enable the API.
![alt text](media/image-10.png)


Create a new VM instance with <img src="media/image-12.png" style="vertical-align:middle" height="20">

![alt text](media/image-11.png)


Pick this specific machine configuration.
![alt text](media/image-13.png)

Click on change.
![alt text](media/image-14.png)

Change the storage size to 30GiB
![alt text](media/image-15.png)

Then, click on *create* on the bottom.

**5. Setup the Machine**

Click on the SSH button on the right.
![alt text](media/image-16.png)

Install git and the relevant packages by typing.
```bash
sudo apt install git python3 python3-venv python3-pip -y
```
![alt text](media/image-17.png)

Clone the Github repo.
```bash
git clone https://github.com/gdgoc-usc/cpe-2026-conference-workshops.git
```
![alt text](media/image-18.png)

CD to the directory as follows
```bash
cd cpe-2026-conference-workshops/ai-on-the-cloud/src/
```


Run `get_from_bucket.py` and enter the bucket name you entered earlier.

Finally, run the `app.py` script.

## References

1. L. Deng, "The MNIST Database of Handwritten Digit Images for Machine Learning Research [Best of the Web]," in IEEE Signal Processing Magazine, vol. 29, no. 6, pp. 141-142, Nov. 2012, doi: 10.1109/MSP.2012.2211477.
keywords: {Machine learning}


2. Official Pytorch MNIST Example: [link](https://github.com/pytorch/examples/tree/main/mnist)