"""
Copyright 2017 Neural Networks and Deep Learning lab, MIPT

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import random
from typing import List, Dict, Generator, Tuple, Any


class Dataset:
    def split(self, *args, **kwargs):
        pass

    def __init__(self, data: Dict[str, List[Tuple[Any, Any]]],
                 seed: int = None, shuffle: bool = True,
                 *args, **kwargs) -> None:
        r""" Dataiterator takes a dict with fields 'train', 'test', 'valid'. A list of samples (pairs x, y) is stored
        in each field.
        Args:
            data: list of (x, y) pairs. Each pair is a sample from the dataset. x as well as y can be a tuple
                of different input features.
            seed (int): random seed for data shuffling. Defaults to None
            shuffle: whether to shuffle data when batching (from config)
        """
        self.shuffle = shuffle

        rs = random.getstate()
        random.seed(seed)
        self.random_state = random.getstate()
        random.setstate(rs)

        self.train = data.get('train', [])
        self.valid = data.get('valid', [])
        self.test = data.get('test', [])
        self.split(*args, **kwargs)
        self.data = {
            'train': self.train,
            'valid': self.valid,
            'test': self.test,
            'all': self.train + self.test + self.valid
        }

    def batch_generator(self, batch_size: int, data_type: str = 'train',
                        shuffle: bool = None) -> Generator:
        r"""This function returns a generator, which serves for generation of raw
        (no preprocessing such as tokenization)
         batches
        Args:
            batch_size (int): number of samples in batch
            data_type (str): can be either 'train', 'test', or 'valid'
            shuffle (bool): whether to shuffle dataset before batching
        Returns:
            batch_gen (Generator): a generator, that iterates through the part (defined by data_type) of the dataset
        """
        if shuffle is None:
            shuffle = self.shuffle

        data = self.data[data_type]
        data_len = len(data)
        order = list(range(data_len))
        if shuffle:
            rs = random.getstate()
            random.setstate(self.random_state)
            random.shuffle(order)
            self.random_state = random.getstate()
            random.setstate(rs)

        for i in range((data_len - 1) // batch_size + 1):
            yield list(zip(*[data[o] for o in order[i * batch_size:(i + 1) * batch_size]]))

    def iter_all(self, data_type: str = 'train') -> Generator:
        r"""Iterate through all data. It can be used for building dictionary or
        Args:
            data_type (str): can be either 'train', 'test', or 'valid'
        Returns:
            samples_gen: a generator, that iterates through the all samples in the selected data type of the dataset
        """
        data = self.data[data_type]
        for x, y in data:
            yield (x, y)
