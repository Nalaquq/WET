# import modules
import arcpy
from arcpy import env
from arcpy.sa import *
from arcpy.ia import *

# Step 1: Set workspace
arcpy.env.workspace = (
    r"C:\Users\Jon\Documents\ArcGIS\Projects\Nalaquq\nativeallotments.gdb"
)

# Step 2: Adjust sampling resolution interval in meters. Adjust direction of
# analysis with "2" for a vertical search, or "1" for a horizontal one, 3 for SWNE, 4 for NWSE
interval = "10 meters"
direction = 2

# Step 3: Specify old and new coastline file locations
oldcoast = "old"
newcoast = "new"

# Step 4: Specify final outputs locations
distance = "region9"
statistics = "statisticsregion9"

# temporary files
points = "points"
bothcoasts = "bothcoasts"
lines = "lines"
bothpoints1 = "bothpoints1"
bothpoints2 = "bothpoints2"

# merge both coasts
arcpy.management.Merge([oldcoast, newcoast], bothcoasts)

# Create temporary points for alignment and assign coordinates
arcpy.GeneratePointsAlongLines_management(oldcoast, points, "DISTANCE", interval)
arcpy.management.CalculateGeometryAttributes(
    points, [["x", "POINT_X"], ["y", "POINT_Y"]]
)

# Create an ID field to be assigned to each bisecting line
arcpy.management.AddField(points, "idforjoin", "LONG")
arcpy.management.CalculateField(points, "idforjoin", "$feature.OBJECTID", "ARCADE")

if direction == 1:
    # Create paired coordinates 1000m west and east to create bisecting lines. Adjust distance as needed below
    arcpy.management.AddField(points, "xW", "DOUBLE")
    arcpy.management.AddField(points, "xE", "DOUBLE")
    arcpy.management.AddField(points, "yW", "DOUBLE")
    arcpy.management.AddField(points, "yE", "DOUBLE")
    arcpy.management.CalculateField(points, "xW", "$feature.x - 1000", "ARCADE")
    arcpy.management.CalculateField(points, "yW", "$feature.y", "ARCADE")
    arcpy.management.CalculateField(points, "xE", "$feature.x + 1000", "ARCADE")
    arcpy.management.CalculateField(points, "yE", "$feature.y", "ARCADE")

    # Generate bisecting lines
    arcpy.management.XYToLine(
        points, lines, "xW", "yw", "xE", "yE", "PLANAR", "idforjoin"
    )
elif direction == 2:
    # Create paired coordinates 1000m north and south to create bisecting lines. Adjust distance as needed below
    arcpy.management.AddField(points, "xN", "DOUBLE")
    arcpy.management.AddField(points, "xS", "DOUBLE")
    arcpy.management.AddField(points, "yN", "DOUBLE")
    arcpy.management.AddField(points, "yS", "DOUBLE")
    arcpy.management.CalculateField(points, "xN", "$feature.x", "ARCADE")
    arcpy.management.CalculateField(points, "yN", "$feature.y + 1000", "ARCADE")
    arcpy.management.CalculateField(points, "xS", "$feature.x", "ARCADE")
    arcpy.management.CalculateField(points, "yS", "$feature.y - 1000", "ARCADE")

    # Generate bisecting lines
    arcpy.management.XYToLine(
        points, lines, "xN", "yN", "xS", "yS", "PLANAR", "idforjoin"
    )
elif direction == 3:
    # Create paired coordinates 1000m southwest and northeast to create bisecting lines. Adjust distance as needed below
    arcpy.management.AddField(points, "xW", "DOUBLE")
    arcpy.management.AddField(points, "xE", "DOUBLE")
    arcpy.management.AddField(points, "yW", "DOUBLE")
    arcpy.management.AddField(points, "yE", "DOUBLE")
    arcpy.management.CalculateField(points, "xW", "$feature.x - 1000", "ARCADE")
    arcpy.management.CalculateField(points, "yW", "$feature.y - 1000", "ARCADE")
    arcpy.management.CalculateField(points, "xE", "$feature.x + 1000", "ARCADE")
    arcpy.management.CalculateField(points, "yE", "$feature.y + 1000", "ARCADE")

    # Generate bisecting lines
    arcpy.management.XYToLine(
        points, lines, "xW", "yw", "xE", "yE", "PLANAR", "idforjoin"
    )
elif direction == 4:
    # Create paired coordinates 1000m northwest and southeast to create bisecting lines. Adjust distance as needed below
    arcpy.management.AddField(points, "xW", "DOUBLE")
    arcpy.management.AddField(points, "xE", "DOUBLE")
    arcpy.management.AddField(points, "yW", "DOUBLE")
    arcpy.management.AddField(points, "yE", "DOUBLE")
    arcpy.management.CalculateField(points, "xW", "$feature.x - 1000", "ARCADE")
    arcpy.management.CalculateField(points, "yW", "$feature.y + 1000", "ARCADE")
    arcpy.management.CalculateField(points, "xE", "$feature.x + 1000", "ARCADE")
    arcpy.management.CalculateField(points, "yE", "$feature.y - 1000", "ARCADE")

    # Generate bisecting lines
    arcpy.management.XYToLine(
        points, lines, "xW", "yw", "xE", "yE", "PLANAR", "idforjoin"
    )

else:
    print("Process failed, please try a different direction")

# Generate points on old and new coastline where the lines bisect them. Convert
# from multipoint to normal points
arcpy.analysis.PairwiseIntersect([bothcoasts, lines], bothpoints1, "", "", "POINT")
arcpy.management.FeatureToPoint(bothpoints1, bothpoints2)

# Generate lines to measure distance between both coasts
arcpy.management.PointsToLine(bothpoints2, distance, "idforjoin")
arcpy.management.CalculateGeometryAttributes(
    distance, [["LengthM", "LENGTH"]], "METERS"
)

# Generate a table summarising the coastline change
arcpy.analysis.Statistics(
    distance,
    statistics,
    [
        ["LengthM", "MIN"],
        ["LengthM", "MAX"],
        ["LengthM", "MEAN"],
        ["LengthM", "MEDIAN"],
    ],
)

# Delete temporary files
arcpy.management.Delete(points)
arcpy.management.Delete(bothcoasts)
arcpy.management.Delete(lines)
arcpy.management.Delete(bothpoints1)
arcpy.management.Delete(bothpoints2)

arcpy.management.Delete(points)
arcpy.management.Delete(bothcoasts)
arcpy.management.Delete(lines)
arcpy.management.Delete(bothpoints1)
arcpy.management.Delete(bothpoints2)
