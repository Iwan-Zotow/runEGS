# -*- coding: utf-8 -*-
"""
Created on Thu May 28 19:02:57 2015

@author: Oleg.Krivosheev
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 07 12:12:35 2015

@author: Oleg.Krivosheev
"""

import unittest
import materials

class TestMaterials(unittest.TestCase):
    """
    Unit tests to check materials
    """
    
    def test_constructor(self):
        fname = "Materials.txt"
        
        mat = materials.materials(fname)
        
        self.assertTrue(mat.mats() != None)

    def test_constructor2(self):
        fname = "Materials.txt"
        
        mat = materials.materials(fname)
        
        self.assertTrue(len(mat) == 5)

    def test_constructor3(self):
        fname = "Materials.txt"
        
        mat = materials.materials(fname)

        for k in range(0, len(mat)):
            self.assertTrue(mat[k] != None)

    def test_constructor4(self):
        fname = "Materials.txt"
        
        mat = materials.materials(fname)

        for k in range(0, len(mat)):
            name, dens = mat[k]
            if k > 0:
                self.assertTrue(dens >= 0.0)
            else:
                self.assertTrue(dens < 0.0)


if __name__ == '__main__':
    unittest.main()
