import os
import numpy as np
import pandas as pd
from skimage import io
from torch.utils.data import Dataset

class CelebA(Dataset):
    def __init__(self, dataset_path, train=True, download=False,
                 transform=None, random_state=42, train_size=100_000, 
                 test_size=20_000):
        self.random_state = random_state
        self.dataset_path = os.path.join(dataset_path)
        self.image_files = np.array(os.listdir(self.dataset_path))
        self.train_size = train_size
        self.test_size = test_size
        self.transform = transform
        
        np.random.seed(random_state)
        np.random.shuffle(self.image_files)

        if train:
            self.image_files = self.image_files[:train_size]
        else:
            self.image_files = self.image_files[-test_size:]

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_name = os.path.join(self.dataset_path,
                                self.image_files[idx])
        image, target = io.imread(img_name), 0

        if self.transform:
            image = self.transform(image)

        return image, target
    
    
class DSprites(Dataset):
    def __init__(self, dataset_path, train=True, download=False,
                 transform=None, random_state=42, train_size=600_000,
                 test_size=100_000):
        self.random_state = random_state
        self.dataset_path = dataset_path
        images = np.load(os.path.join(dataset_path,
                'dsprites_ndarray_co1sh3sc6or40x32y32_64x64.npz'))['imgs']
        self.images = images[..., None] * 255
        self.train_size = train_size
        self.test_size = test_size
        self.transform = transform
        
        np.random.seed(random_state)
        np.random.shuffle(self.images)
        
        if train:
            self.images = self.images[:train_size]
        else:
            self.images = self.images[-test_size:]
        
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        image, target = self.images[idx], 0
        
        if self.transform:
            image = self.transform(image)
        
        return image, target