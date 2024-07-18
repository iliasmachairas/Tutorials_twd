from qgis.core import QgsProject, QgsLayout, QgsLayoutItemMap, QgsLayoutItemPicture, QgsLayoutExporter
from qgis.gui import QgisInterface
from qgis.utils import iface
import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem

print(os.getcwd())

input_directory = "F:\Tutorials\Layout_plot_qgis\individual_prefectures_2100"
qgis_project_directory = "F:\Tutorials\Layout_plot_qgis\projects_qgis"
style_prefecture_path = r"F:\Tutorials\Layout_plot_qgis\styles\styles_prefecture.qml"
style_indiv_prefecture_path = r"F:\Tutorials\Layout_plot_qgis\styles\styles_individual_prefecture.qml"
export_images_directory = r"F:\Tutorials\Layout_plot_qgis\Export_images"
export_pdf_directory = r"F:\Tutorials\Layout_plot_qgis\Export_pdf"

# Loop through each shapefile in the directory
for filename in os.listdir(input_directory):
    if filename.endswith(".shp"):
        # Construct the full path to the shapefile
        filepath = os.path.join(input_directory, filename)
        filename_without_extension = os.path.splitext(os.path.basename(filename))[0]
        print(filename_without_extension)

        # project code
        project_name = f"QGIS_Project_{filename_without_extension}.qgz"
        # path_project = r"C:\Users\Ilias\Downloads\Layout_plot_qgis\project_path\project.qgs"
        path_project = os.path.join(qgis_project_directory, project_name)
        # image
        image_name = f"image_{filename_without_extension}.png"
        path_image = os.path.join(export_images_directory, image_name)
        # pdf
        pdf_name = f"{filename_without_extension}.pdf"
        path_pdf = os.path.join(export_pdf_directory, pdf_name)        

        
        project = QgsProject.instance()
        project.setTitle(project_name)
    
        urlWithParams = 'type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0&crs=EPSG3857'
        rlayer = QgsRasterLayer(urlWithParams, 'OpenStreetMap', 'wms')  
        print(rlayer.crs())
        if rlayer.isValid():
            project.addMapLayer(rlayer)
        else:
            print('invalid layer')
            print(rlayer.error().summary()) 

        # # adding perifereies
        path_shp = "F:\Tutorials\Layout_plot_qgis\periphereies (1)\periphereies\periphereies.shp"
        # path_shp = r"C:\Users\Ilias\Downloads\Layout_plot_qgis\periphereies (1)\periphereies\periphereies.shp"
        prefectures = QgsVectorLayer(path_shp, 'prefectures', 'ogr')
        prefectures.loadNamedStyle(style_prefecture_path)
        
        if not prefectures.isValid():
            print("Layer failed to load!")
        else:
            QgsProject.instance().addMapLayer(prefectures)


        individual_prefecture = QgsVectorLayer(filepath,str(filename_without_extension), 'ogr')
        if not individual_prefecture.isValid():
            print("Layer failed to load!")
        else:
            QgsProject.instance().addMapLayer(individual_prefecture)
        print(individual_prefecture.id)
        individual_prefecture.loadNamedStyle(style_indiv_prefecture_path)
        

        layout_name = f"Layout_{filename_without_extension}"
        layout_manager = project.layoutManager()
        layout = QgsPrintLayout(project)
        layout.setName(layout_name)
        layout.initializeDefaults()
        layout_manager.addLayout(layout)


        # Set page size
        layout.pageCollection().page(0).setPageSize('A4', QgsLayoutItemPage.Portrait)
        # Create map item
        map_item = QgsLayoutItemMap(layout)
        map_item.setRect(20, 20, 210, 220)
        map_item.setExtent(prefectures.extent())
        layout.addLayoutItem(map_item)
        map_item.refresh()
        map_item.setFrameEnabled(True)
        map_item.setFrameStrokeColor(QColor(Qt.black))  # Set border color
        # locking style in layout
        map_item.storeCurrentLayerStyles()
        map_item.setKeepLayerSet(True)
        map_item.setKeepLayerStyles(True)

        
        ## adding legend 
        legend = QgsLayoutItemLegend(layout)
        layout.addLayoutItem(legend)
        legend.setFrameEnabled(True)
        legend.setFrameStrokeWidth(QgsLayoutMeasurement(0.3))
        legend.setTitle('Legend')
        legend.attemptMove(QgsLayoutPoint(120, 225, QgsUnitTypes.LayoutMillimeters))
        legend.attemptResize(QgsLayoutSize(60, 40, QgsUnitTypes.LayoutMillimeters))
        
        
        # adding image
        layoutItemPicture = QgsLayoutItemPicture(layout)
        layoutItemPicture.setResizeMode(QgsLayoutItemPicture.Zoom)
        layoutItemPicture.setMode(QgsLayoutItemPicture.FormatRaster)
        layoutItemPicture.setPicturePath(r"F:\Tutorials\Layout_plot_qgis\north_3.PNG")
        dim_image_original = [1443, 1453]
        new_dim = [i * 0.20 for i in dim_image_original]
        layoutItemPicture.attemptMove(QgsLayoutPoint(5, 5, QgsUnitTypes.LayoutMillimeters))
        layoutItemPicture.attemptResize(QgsLayoutSize(*new_dim, QgsUnitTypes.LayoutPixels))
        layout.addLayoutItem(layoutItemPicture)
        
        # Projection Setting 
        project.setCrs(QgsCoordinateReferenceSystem(2100))
        
        
        # Attention: crs should be defined before the integration of scalebar 
        ### adding scale-bar 
        scalebar = QgsLayoutItemScaleBar(layout)
        scalebar.setStyle('Line Ticks Up')
        scalebar.setUnits(QgsUnitTypes.DistanceKilometers)
        scalebar.setNumberOfSegments(3)
        scalebar.setNumberOfSegmentsLeft(0)
        scalebar.setUnitsPerSegment(75)
        scalebar.setLinkedMap(map_item)
        scalebar.setUnitLabel('km')
        scalebar.setFont(QFont ('Arial',14))
        scalebar.update()
        layout.addLayoutItem(scalebar)
        scalebar.attemptMove(QgsLayoutPoint(5, 160, QgsUnitTypes.LayoutMillimeters))
        
        
        # adding text 
        title = QgsLayoutItemLabel(layout)
        title.setText(filename_without_extension)
        title.setFont(QFont("Arial", 20))
        title.adjustSizeToText()
        title.setHAlign(Qt.AlignHCenter)
        layout.addLayoutItem(title)
        title.attemptMove(QgsLayoutPoint(120, 210, QgsUnitTypes.LayoutMillimeters))

        # saving QGIS project
        project.write(path_project)
        
        # Exporting to png images
        exporter = QgsLayoutExporter(layout)
        settings = QgsLayoutExporter.ImageExportSettings()
        ######### settings.cropToContents = True  # Set to True if you want to crop to the contents
        settings.dpi = 300  # Set your desired DPI
        result = exporter.exportToImage(path_image, settings)

        # Exporting to pdf
        exporter.exportToPdf(path_pdf, QgsLayoutExporter.PdfExportSettings())
        
        project.clear()
        

        



    
