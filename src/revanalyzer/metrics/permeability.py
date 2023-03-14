# -*- coding: utf-8 -*-
"""Definition of Permeability metric."""

import numpy as np
import os
from .basic_metric import BasicMetric


class Permeability(BasicMetric):
    """
    Class describing porosity metric.
    """
    def __init__(self, all_directions=True):
        """
        **Input:**
        all_directions (bool): flag indicating if generation over 3 flow directions was done by external generator.
                               It must be False, if in generator function parameter 'directions' = 'x', 'y' or 'z'. 
                               It must be True, if 'directions' = 'all'. Default: True.
        """
        super().__init__(vectorizer=None)
        self.metric_type = 's'
        if all_directions:
            self.directional = True
