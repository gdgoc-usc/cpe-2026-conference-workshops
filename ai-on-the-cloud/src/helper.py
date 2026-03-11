import torch
import torch.nn.functional as F
from torchvision import transforms
import numpy as np


LOG_INTERVAL = 10

def get_preprocessing_pipeline():
    return transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])

    
def train_processor(model, device, train_loader, optimizer, epoch, is_dry_run=False):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % LOG_INTERVAL == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))
            if is_dry_run:
                break


def test_processor(model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))


def predict_digit(sketch, model):
    def fn(sketch):
        # Extract the image from Gradio's dictionary format
        if isinstance(sketch, dict):
            img = sketch['composite']
        else:
            img = sketch
            
        # Isolate the 2D array if Gradio adds extra dimensions
        if len(img.shape) > 2:
            img = img[:, :, 0]
            
        # IMPORTANT: Invert colors if the background is white to match MNIST
        if np.mean(img) > 127:
            img = 255 - img
            
        # Normalize the image to match the PyTorch training transformations
        img = img.astype(np.float32) / 255.0
        img = (img - 0.1307) / 0.3081
        
        # Convert to PyTorch tensor and add batch/channel dimensions: (1, 1, 28, 28)
        img_tensor = torch.tensor(img).unsqueeze(0).unsqueeze(0)
        
        model.eval() # Set model to evaluation mode
        with torch.no_grad(): # Turn off gradient tracking for inference
            output = model(img_tensor)
            # Apply softmax to get percentages (probabilities)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)
            
        # Return a dictionary of labels (0-9) and their confidence scores
        return {str(i): probabilities[i].item() for i in range(10)}
    return fn