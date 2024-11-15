var aoi = ee.FeatureCollection("FAO/GAUL_SIMPLIFIED_500m/2015/level2")
            .filter(ee.Filter.eq('ADM2_NAME','Arkadias'));
            
Map.addLayer(aoi, {}, 'AOI - Arcadia');
Map.centerObject(aoi, 10);

var startDate = '2023-06-01';
var endDate = '2023-06-30';

// Applies scaling factors.
function applyScaleFactors(image) {
 // Scale and offset values for optical bands
 var opticalBands = image.select("SR_B.").multiply(0.0000275).add(-0.2);
 
 // Scale and offset values for thermal bands
 var thermalBands = image.select("ST_B.*").multiply(0.00341802).add(149.0);
 
 // Add scaled bands to the original image
 return image.addBands(opticalBands, null, true)
 .addBands(thermalBands, null, true);
}

function cloudMask(image) {
  // Define cloud shadow and cloud bitmasks (Bits 3 and 5)
  var cloudShadowBitmask = (1 << 3);
  var cloudBitmask = (1 << 5);

  // Select the Quality Assessment (QA) band for pixel quality information
  var qa = image.select('QA_PIXEL');

  // Create a binary mask to identify clear conditions (both cloud and cloud shadow bits set to 0)
  var mask = qa.bitwiseAnd(cloudShadowBitmask).eq(0)
                .and(qa.bitwiseAnd(cloudBitmask).eq(0));

  // Update the original image, masking out cloud and cloud shadow-affected pixels
  return image.updateMask(mask);
}
 
var image = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
              .filterBounds(aoi)
              .filterDate(startDate, endDate)
              .map(applyScaleFactors)
              .map(cloudMask)


print(image)

// Define visualization parameters for True Color imagery (bands 4, 3, and 2)
var visualization = {
  bands: ['SR_B4', 'SR_B3', 'SR_B2'],
  min: 0.0,
  max: 0.15,
};

var imagesList = image.toList(image.size()); 
var visualizeImages = function(index) {
  // Get each image from the list
  var image = ee.Image(imagesList.get(index)).clip(aoi);
  
  var date = image.date().format('YYYY-MM-dd').getInfo();
  print(date)
  
  var band10 = image.select('ST_B10').toFloat();
  var allBands = image.toFloat();

  // Define visualization parameters (adjust as needed)
  var visualization = {
    bands: ['SR_B4', 'SR_B3', 'SR_B2'],
    min: 0.0,
    max: 0.15,
  };

  // Add the image to the map
  Map.addLayer(image, visualization, 'Image from ' + date);
  // Export the image
  Export.image.toDrive({
  //image: band10.double(),
  image: allBands.double(),
  description: 'Landsat_Image_' + date, // Filename format
  scale: 30, // Scale in meters
  region: aoi, // Area of interest
  maxPixels: 1e13 // Set a max pixel limit (adjust if needed)
  });
};


var numberOfImages = imagesList.size();
for (var i = 0; i < numberOfImages.getInfo(); i++) {
  visualizeImages(i);
}

  
  
