# model.py
import torch
import torch.nn as nn

class TrainedTTSModel(nn.Module):
    def __init__(self):
        super(TrainedTTSModel, self).__init__()
        self.layer = nn.Linear(10, 1)  # Example layer (modify according to your model's structure)

    def forward(self, x):
        return self.layer(x)
