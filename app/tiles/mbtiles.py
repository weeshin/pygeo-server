from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
import sqlite3
import os

router = APIRouter()

# Define the fixed database path
DB_PATH = os.path.realpath(r"D:\\johor\\Segamat-bukit bujang\\mbtiles\\2b-tiles.mbtiles")
DB_PATH = os.path.realpath(r"D:\\johor\\Segamat-bukit bujang\\mbtiles\\2b-tiles-12-22.mbtiles")
DB_PATH = os.path.realpath(r"D:\\teeh-teh-mbtiles\\tee-teh-17-23-engine.mbtiles")

@router.get("/tiles")
def get_tile(z: int = Query(..., alias="z"),
             x: int = Query(..., alias="x"),
             y: int = Query(..., alias="y")):
    
    # Ensure the file exists
    if not os.path.isfile(DB_PATH):
        raise HTTPException(status_code=404, detail="Database not found or access denied.")

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Query the tiles table
        query = """
        SELECT zoom_level, tile_column, tile_row, tile_data
        FROM tiles
        WHERE zoom_level = ? AND tile_column = ? AND tile_row = ?
        """
        cursor.execute(query, (z, x, y))
        result = cursor.fetchone()

        if result:
            zoom_level, tile_column, tile_row, tile_data = result
            return Response(content=tile_data, media_type="image/png")
        else:
            raise HTTPException(status_code=404, detail="Tile not found.")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        if conn:
            conn.close()
