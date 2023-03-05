from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtCore import QVariant

from qgis.core import Qgis
from qgis.core import QgsVectorLayer, QgsPoint, QgsVectorDataProvider
from qgis.core import QgsFeature
from qgis.core import (
    QgsGeometry,
    QgsGeometryCollection,
    QgsPoint,
    QgsPointXY,
    QgsWkbTypes,
    QgsProject,
    QgsFeatureRequest,
    QgsVectorLayer,
    QgsDistanceArea,
    QgsUnitTypes,
    QgsCoordinateTransform,
    QgsCoordinateReferenceSystem,
    QgsField,
)
from qgis.gui import (
    QgsVertexMarker,
)

from .point import Point
from .pickets import Pickets


class LayerProps():
    def __init__(self, iface):
        self.__iface = iface
        self.__canvas = self.__iface.mapCanvas()
        self.__layer = iface.activeLayer()
        self.__layer_name_curr = self.__layer.name()
        self.__layer_name_true = self.__layer.dataProvider().subLayers()[0].split('!!::!!')[1]
        self.__layer_type = self.__layer.geometryType()

    def layer(self):
        return self.__layer

    def name_current(self):
        return self.__layer_name_curr

    def name_true(self):
        return self.__layer_name_true

    def type(self):
        return self.__layer_type

    def is_linestring(self):
        if self.__layer_type == 1:
            return True
        return False

    def selected_features(self):
        return self.__layer.selectedFeatures()

    def selected_features_geometry(self):
        markers = []
        features = self.__layer.selectedFeatures()
        for feature in features:
            for part in feature.geometry().asMultiPolyline():
                for pnt in part:
                    m = QgsVertexMarker(self.__canvas)
                    m.setCenter(pnt)
                    m.setColor(QColor(0, 255, 0))
                    m.setIconSize(7)
                    markers.append(m)
                    # print(pnt)

        for m in markers:
            self.__canvas.scene().removeItem(m)

    def features_is_linestring(self):
        features = self.__layer.selectedFeatures()
        for feature in features:
            # refer to all attributes
            print(feature.attributes())  # results in [3, 'Group 1', 4.6]

    def get_points(self):
        points = []
        features = self.__layer.selectedFeatures()
        for feature in features:
            for part in feature.geometry().asMultiPolyline():
                for pnt in part:
                    points.append(Point(pnt.y(), pnt.x()))
        return points

    def PK(self):
        pickets = Pickets(self.get_points());
        pickets.get();

        # create layer
        vl = QgsVectorLayer("Point?crs=epsg:28473", "temporary_points", "memory")
        pr = vl.dataProvider()

        # add fields
        pr.addAttributes([QgsField("name", QVariant.String),
                          QgsField("age", QVariant.Int),
                          QgsField("size", QVariant.Double)])
        vl.updateFields()  # tell the vector layer to fetch changes from the provider

        for pk in pickets.get():
            # add a feature
            fet = QgsFeature()
            fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(pk.point.east, pk.point.north)))
            fet.setAttributes([pk.name, 2, 0.3])
            pr.addFeatures([fet])

        # update layer's extent when new features have been added
        # because change of extent in provider is not propagated to the layer
        vl.updateExtents()
        QgsProject.instance().addMapLayer(vl)

        # for f in vl.getFeatures():
        #     print("Feature:", f.id(), f.attributes(), f.geometry().asPoint())
        # print(pickets);