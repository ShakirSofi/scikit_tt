# -*- coding: utf-8 -*-

from unittest import TestCase
import scikit_tt.data_driven.perron_frobenius as pf
import numpy as np
import os
import scipy.io as io


class TestSLIM(TestCase):

    def setUp(self):
        """Consider triple- and quadruple well potentials for testing"""

        # set tolerance for errors
        self.tol = 1e-10

        # load transition lists
        directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.transitions_2d = io.loadmat(directory + '/examples/data/TripleWell2D_500.mat')["indices"]
        self.transitions_3d = io.loadmat(directory + '/examples/data/QuadrupleWell3D_25x25x25_100.mat')["indices"]

    def test_perron_frobenius_2d(self):
        """test for perron_frobenius_2d"""
    
        # construct transition operator in TT format
        operator = pf.perron_frobenius_2d(self.transitions_2d, [50, 50], 500)

        # construct full operator
        operator_full = np.zeros([50,50,50,50])
        for i in range(self.transitions_2d.shape[1]):
            [x_1, y_1, x_2, y_2] = self.transitions_2d[:,i] - 1
            operator_full[x_2, y_2, x_1, y_1] += 1
        operator_full *= 1/500

        # compute error
        error = np.abs(operator.full()-operator_full).sum()
               
        # check if error is smaller than tolerance         
        self.assertLess(error, self.tol)

    def test_perron_frobenius_3d(self):
        """test for perron_frobenius_3d"""
    
        # construct transition operator in TT format
        operator = pf.perron_frobenius_3d(self.transitions_3d, [25, 25, 25], 100)

        # construct full operator
        operator_full = np.zeros([25,25,25,25,25,25])
        for i in range(self.transitions_3d.shape[1]):
            [x_1, y_1, z_1, x_2, y_2, z_2] = self.transitions_3d[:, i] - 1
            operator_full[x_2, y_2, z_2, x_1, y_1, z_1] += 1
        operator_full *= 1/100

        # compute error
        error = np.abs(operator.full()-operator_full).sum()
               
        # check if error is smaller than tolerance         
        self.assertLess(error, self.tol)

