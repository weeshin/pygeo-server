import unittest
from unittest.mock import patch, MagicMock
from osgeo import gdal
from app.wms.common import WMSBaseServiceHandle

class TestWMSBaseServiceHandle(unittest.TestCase):
    @patch("your_module.gdal.Open")  # Mock gdal.Open
    @patch("your_module.gdal.Translate")  # Mock gdal.Translate
    def test_GetMap(self, mock_translate, mock_open):
        # Arrange
        geotiff_path = "test_data/input.tif"
        bbox = "100000,200000,300000,400000"
        width = 256
        height = 256
        crs = "EPSG:32647"
        output_format = "image/png"
        
        # Mock dataset returned by gdal.Open
        mock_dataset = MagicMock()
        mock_open.return_value = mock_dataset

        # Mock Translate behavior
        mock_translate.return_value = MagicMock()

        # Act
        result = WMSBaseServiceHandle.GetMap(
            geotiff_path, bbox, width, height, crs, format=output_format
        )

        # Assert
        mock_open.assert_called_once_with(geotiff_path)  # Ensure gdal.Open was called correctly
        mock_translate.assert_any_call(
            "output_clipped.tif",
            mock_dataset,
            projWin=(100000, 400000, 300000, 200000),  # xmin, ymax, xmax, ymin
            width=width,
            height=height,
            format="GTiff"
        )  # Ensure Translate for GeoTIFF was called
        mock_translate.assert_any_call(
            "output_clipped.png",
            mock_translate.return_value,
            format="PNG"
        )  # Ensure Translate for PNG was called

        # Check the result
        self.assertEqual(result, "output_clipped.png")