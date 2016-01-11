#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import pygmsh as pg
import numpy as np

def generate():
    #-------------------------------------------------------------------------------------------------------------------
    coord = 1.
    
    domainShape = 'rectangular'
    leftDist = 1.
    rightDist = 3.
    topDist = 1.
    bottomDist = 1.
    
    charLength = 1e-2
    
    # Airfoil coordinates
    airfoilCoordinates = np.array([[1.000000,0.000000],
    [0.999023,0.000209],
    [0.996095,0.000832],
    [0.991228,0.001863],
    [0.984438,0.003289],
    [0.975752,0.005092],
    [0.965201,0.007252],
    [0.952825,0.009744],
    [0.938669,0.012538],
    [0.922788,0.015605],
    [0.905240,0.018910],
    [0.886092,0.022419],
    [0.865417,0.026096],
    [0.843294,0.029903],
    [0.819807,0.033804],
    [0.795047,0.037760],
    [0.769109,0.041734],
    [0.742094,0.045689],
    [0.714107,0.049588],
    [0.685258,0.053394],
    [0.655659,0.057071],
    [0.625426,0.060584],
    [0.594680,0.063897],
    [0.563542,0.066977],
    [0.532136,0.069789],
    [0.500587,0.072303],
    [0.469022,0.074486],
    [0.437567,0.076312],
    [0.406350,0.077752],
    [0.375297,0.078743],
    [0.344680,0.079180],
    [0.314678,0.079051],
    [0.285418,0.078355],
    [0.257025,0.077096],
    [0.229618,0.075287],
    [0.203313,0.072945],
    [0.178222,0.070096],
    [0.154449,0.066770],
    [0.132094,0.063005],
    [0.111248,0.058842],
    [0.091996,0.054325],
    [0.074415,0.049504],
    [0.058573,0.044427],
    [0.044532,0.039144],
    [0.032343,0.033704],
    [0.022051,0.028152],
    [0.013692,0.022531],
    [0.007292,0.016878],
    [0.002870,0.011224],
    [0.000439,0.005592],
    [0.000000,0.000000],
    [0.001535,-0.005395],
    [0.005015,-0.010439],
    [0.010421,-0.015126],
    [0.017725,-0.019451],
    [0.026892,-0.023408],
    [0.037880,-0.026990],
    [0.050641,-0.030193],
    [0.065120,-0.033014],
    [0.081257,-0.035451],
    [0.098987,-0.037507],
    [0.118239,-0.039185],
    [0.138937,-0.040493],
    [0.161004,-0.041444],
    [0.184354,-0.042054],
    [0.208902,-0.042343],
    [0.234555,-0.042335],
    [0.261221,-0.042058],
    [0.288802,-0.041541],
    [0.317197,-0.040817],
    [0.346303,-0.039923],
    [0.376013,-0.038892],
    [0.406269,-0.037757],
    [0.437099,-0.036467],
    [0.468187,-0.035009],
    [0.499413,-0.033414],
    [0.530654,-0.031708],
    [0.561791,-0.029917],
    [0.592701,-0.028066],
    [0.623264,-0.026176],
    [0.653358,-0.024269],
    [0.682867,-0.022360],
    [0.711672,-0.020466],
    [0.739659,-0.018600],
    [0.766718,-0.016774],
    [0.792738,-0.014999],
    [0.817617,-0.013284],
    [0.841253,-0.011637],
    [0.863551,-0.010068],
    [0.884421,-0.008583],
    [0.903777,-0.007191],
    [0.921540,-0.005900],
    [0.937637,-0.004717],
    [0.952002,-0.003650],
    [0.964576,-0.002708],
    [0.975305,-0.001896],
    [0.984145,-0.001222],
    [0.991060,-0.000691],
    [0.996020,-0.000308],
    [0.999004,-0.000077]]
    )
    
    # Scale airfoil to input coord
    airfoilCoordinates *= coord
    
    # Dat-file dimensions
    numPoints = airfoilCoordinates.shape[0]
    dimPoints = airfoilCoordinates.shape[1]
    
    # Move points from 1D or 2D space to 3D space
    if 0 < dimPoints < 3:
        airfoilCoordinates = np.hstack((airfoilCoordinates, np.zeros([numPoints, 3-dimPoints])))
    else:
        sys.exit('The airfoil dat-file should contain either 1, 2 or 3 columns.')
    
    # Instantiate geometry object
    geom = pg.Geometry()
    
    # Create line loop for airfoil
    airfoil = [geom.add_polygon_loop(airfoilCoordinates, charLength)]
    
    # Create line loop for numerical domain
    if domainShape == 'rectangular':
        domainCoordinates = np.zeros([4, 3])
        domainCoordinates[0, 0] = airfoilCoordinates[:, 0].min() - leftDist*coord
        domainCoordinates[0, 1] = airfoilCoordinates[:, 1].min() - bottomDist*coord
        domainCoordinates[1, 0] = airfoilCoordinates[:, 0].max() + rightDist*coord
        domainCoordinates[1, 1] = airfoilCoordinates[:, 1].min() - bottomDist*coord
        domainCoordinates[2, 0] = airfoilCoordinates[:, 0].max() + rightDist*coord
        domainCoordinates[2, 1] = airfoilCoordinates[:, 1].max() + topDist*coord
        domainCoordinates[3, 0] = airfoilCoordinates[:, 0].min() - leftDist*coord
        domainCoordinates[3, 1] = airfoilCoordinates[:, 1].max() + topDist*coord
    elif domainShape == 'elliptic':
        sys.exit('Elliptic domain is not yet implemented.')
    
    # Create surface for numerical domain with an airfoil-shaped hole
    geom.add_polygon(domainCoordinates, charLength, holes=airfoil)
    
    # Return geo-file code   
    return geom.get_code()
    
if __name__ == '__main__':
    print(generate())