# -*- coding: utf-8 -*-

import math
import cup

import linint

class linint_cup(cup):
    """
    Class to provide specialized cup,
    where model is made from linear interpolation
    between set of points

    Contains curves for both inner cup only
    """

    def __init__(self, fname):
        """
        Constructor

        Parameters
        ----------

        fname: string
            file name to read points
        """

        super(inner_cup, self).__init__(fname)

        self.init_from_file()

        self._zmax = self._Z1



