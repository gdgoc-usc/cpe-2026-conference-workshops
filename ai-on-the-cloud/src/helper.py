import torch
import torch.nn.functional as F
from torchvision import transforms
import numpy as np
from pathlib import Path

from the_net import Net


LOG_INTERVAL = 10
_MODEL = None

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


def _get_model():
    global _MODEL
    if _MODEL is None:
        model_path = Path(__file__).with_name("mnist_cnn.pt")
        if not model_path.exists():
            raise FileNotFoundError(f"Model weights not found at {model_path}")

        model = Net()
        state_dict = torch.load(model_path, map_location="cpu")
        model.load_state_dict(state_dict)
        model.eval()
        _MODEL = model
    return _MODEL


def predict_digit(sketch):
    # Gradio Sketchpad can return either raw numpy data or a dictionary payload.
    if isinstance(sketch, dict):
        img = sketch.get("composite")
    else:
        img = sketch

    if img is None:
        return {str(i): 0.0 for i in range(10)}

    if len(img.shape) > 2:
        img = img[:, :, 0]

    img = img.astype(np.float32)
    if img.max() > 1.0:
        img = img / 255.0

    # Match MNIST convention (white digit on black background).
    if float(np.mean(img)) > 0.5:
        img = 1.0 - img

    img_tensor = torch.tensor(img, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
    img_tensor = F.interpolate(img_tensor, size=(28, 28), mode="bilinear", align_corners=False)
    img_tensor = (img_tensor - 0.1307) / 0.3081

    model = _get_model()
    with torch.no_grad():
        output = model(img_tensor)
        probabilities = torch.softmax(output[0], dim=0)

    return {str(i): float(probabilities[i].item()) for i in range(10)}