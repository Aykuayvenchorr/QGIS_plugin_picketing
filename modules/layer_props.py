from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtCore import QVariant

from qgis.core import Qgis
from qgis.core import QgsFeature
from qgis.core import (
    QgsGeometry,
    QgsGeometryCollection,
    QgsPoint,
    QgsPointXY,
    QgsProject,
    QgsFeatureRequest,
    QgsVectorLayer,
    QgsDistanceArea,
    QgsUnitTypes,
    QgsField,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform
)


from qgis.gui import (
    QgsVertexMarker,
)

from .point import Point
from .pickets import Pickets


class LayerProps:
    def __init__(self, iface, distance: float, prefix: str, crs_target: str):
        self.__iface = iface
        self.__canvas = self.__iface.mapCanvas()
        self.__layer = iface.activeLayer()
        self.__layer_name_curr = self.__layer.name()
        self.__layer_name_true = self.__layer.dataProvider().subLayers()[0].split('!!::!!')[1]
        self.__layer_type = self.__layer.geometryType()
        self.distance = distance;
        self.prefix = prefix;
        self.crs_target = crs_target

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

    def convert_crs(self, point, crs_target_):
        """Метод, преобразующий исходные координаты точек из системы координат слоя в целевую СК"""
        crs = str(self.__layer.crs()).split(': ')[1].split('>')[0]
        crsSrc = QgsCoordinateReferenceSystem(crs)  # WGS 84
        # crsDest = QgsCoordinateReferenceSystem(str(crs_target_))  # WGS 84 / UTM zone 33N

        # crsSrc = QgsCoordinateReferenceSystem("EPSG:4326")  # WGS 84
        crsDest = QgsCoordinateReferenceSystem(crs_target_)  # WGS 84 / UTM zone 33N

        # transformContext = QgsProject.instance().transformContext()
        tform = QgsCoordinateTransform(crsSrc, crsDest, QgsProject.instance())
        # xform = QgsCoordinateTransform(crsSrc, crsDest, transformContext)
        #
        # forward transformation: src -> dest
        print(point)
        pt1 = tform.transform(QgsPointXY(point.x(), point.y()))
        print("Transformed point:", pt1)
        # Если выбирать географическую СК (в градусах), то пересчета не будет
        return pt1

    def get_points(self):
        points = []
        features = self.__layer.selectedFeatures()
        for feature in features:
            for part in feature.geometry().asMultiPolyline():
                for pnt in part:
                    # transform CRS: CRS_layer -> CRS_target
                    # print(pnt.x())
                    pnt = self.convert_crs(pnt, self.crs_target)
                    points.append(Point(pnt.y(), pnt.x()))
        return points

    def PK(self):
        pickets = Pickets(self.get_points(), self.distance, self.prefix);
        pickets.get()

        # create layer
        # layer.crs()
        crs = str(self.__layer.crs()).split(': ')[1].split('>')[0]
        crs_str = "Point?crs="+crs
        # print(crs_str)
        crs_trg = "Point?crs="+str(self.crs_target)
        # print(crs_trg)
        # Создание временного слоя в целевой СК
        vl = QgsVectorLayer(crs_trg, "temporary_points", "memory")
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
        # print(pickets)