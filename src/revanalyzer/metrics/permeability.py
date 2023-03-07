import numpy as np
import os
from .basic_metric import BasicMetric


class Permeability(BasicMetric):
    def __init__(self, all_directions=True):
        super().__init__(vectorizer=None)
        self.metric_type = 's'
        if all_directions:
            self.directional = True
