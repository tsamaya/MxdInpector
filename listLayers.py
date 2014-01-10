#-------------------------------------------------------------------------------
# Name:        main module
# Purpose:
#
# Author:      aferrand
#
# Created:     08/01/2014
# Copyright:   (c) aferrand 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy, sys, os

# default enconding
ENCODING = "iso-8859-15"

# not available
NA = "n.a."

# not defined
ND = "n.d."

def main():
    mxdFile = arcpy.GetParameterAsText(0)
    if( not os.path.isfile(mxdFile) ):
        mxdFile = "CURRENT"

    mxd = arcpy.mapping.MapDocument(mxdFile)

    df = arcpy.mapping.ListDataFrames(mxd)[0]

    filename = '%s_layer-description.txt' % (os.path.basename(mxd.filePath)[:-4])

    try:
        file = open(filename,'w')
        print "file encoding:" + str(file.encoding)

        print >>file, entete()
        for lyr in arcpy.mapping.ListLayers(mxd, '', df):
            if not lyr.isGroupLayer:
                print >>file, printLayerDescription(lyr)
            else:
            	print >>file, lyr.name

        print 'Create layer-description in %s' % (os.path.abspath(filename))

    finally:
        file.close()
        del mxd

def entete():
    return "Layer name,Data type,Feature type,Spatial Reference,Geometry,Spatial Index, Layer visibility,max Scale,min Scale,Group layer,Definition query,Labels,DataSource"

def printLayerDescription(layer):
    print layer.longName

    retour = '';
    # layer name
    retour+= layer.name.encode(ENCODING,"ignore")
    #retour+= layer.name
    #retour+= layer.name
    retour+=','

    fc = layer.dataSource
    desc = None
    sr = None
    try:
        desc = arcpy.Describe(fc)
        sr = desc.spatialReference
    except arcpy.ExecuteError:
        msg =arcpy.getGetMessages(2)

    try:
        # data type
        retour+= desc.dataType.encode(ENCODING,"ignore") + " " + desc.dataElementType.encode(ENCODING,"ignore")
    except:
        retour+= NA
    retour+=','

    try:
        # feature type
        if( hasattr(desc, "featureType")):
            retour+= desc.featureType.encode(ENCODING,"ignore")
        else:
            retour+= ND
    except:
        retour+= NA
    retour+=','

    try:
        # spatial ref
        retour+= sr.name.encode(ENCODING, "ignore")
    except:
        retour+= NA
    retour+=','

    try:
        # Geometry
        if( hasattr(desc, "shapeType")):
            retour+= desc.shapeType.encode(ENCODING, "ignore")
        else:
            retour+= ND
    except:
        retour+= NA
    retour+=','

    try:
        # spatial index
        if( hasattr(desc, "hasSpatialIndex")):
            retour+= str(desc.hasSpatialIndex)
        else:
            retour+= ND
    except:
        retour+= NA
    retour+=','

    # Layer visibility
    if( layer.supports("visible")):
        retour+= str(layer.visible)
    else:
        retour+= ND
    retour+=','

    # max Scale
    if( hasattr(layer, "minScale")):
        retour+= str(layer.minScale)
    else:
        retour+= ND
    retour+=','

    # min Scale
    if( hasattr(layer, "minScale")):
        retour+= str(layer.minScale)
    else:
        retour+= ND
    retour+=','

    # Group layer
    retour+= layer.longName.encode(ENCODING, "ignore")
    #retour+= layer.longName
    retour+=','

    # Definition query
    if( layer.supports("definitionQuery")):
        retour+= "\"" + layer.definitionQuery.replace('\\n', ' ').encode(ENCODING) + "\""
    else:
        retour+= ND
    retour+=','

    # Labels
    if( layer.supports("showLabels")):
        retour+= str(layer.showLabels)
    else:
        retour+= ND
    retour+=','

    # Labels
    retour+= str(layer.dataSource)
    retour+=','

    return retour

if __name__ == '__main__':
    main()
