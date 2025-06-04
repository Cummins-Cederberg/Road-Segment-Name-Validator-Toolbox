# Road-Segment-Name-Validator-Toolbox
ArcGIS Pro toolbox for validating and updating road segment names based on intersecting street names. Designed to assist in street network data by detecting mismatches and correcting start/end intersection names using spatial relationships.

## 🛣️ Road Segment Name Validation Toolbox
A custom ArcGIS Python toolbox (.pyt) that performs automation on road segment names by checking the consistency of intersecting road names at the start and end points of each road segment.

## 🔍 What It Does
This tool:

Takes a polyline feature class of road segments.

Compares each road segment's name with the names of intersecting roads at its start and end points.

If the same road name appears at both ends (indicating a potential error), it rechecks intersecting road names and updates accordingly.

Leaves values unchanged if the segment is a dead-end, circle, or curved continuation with no valid intersections.

## 📂 Input Parameters
Parameter	Description:

1. Input Road Feature Class -> Polyline shapefile or feature class representing split road segments.

2. Road Name Field -> Field containing the road segment's name (e.g., "Name").

3. Start Road Name Field (Name_1) -> Field to store or validate intersecting road name at the start of the segment.

4. End Road Name Field (Name_12) ->	Field to store or validate intersecting road name at the end of the segment.

## ✅ Rules Applied
If Name_1 == Name_12 (== Name), the tool checks actual intersections.

If no intersecting road names are found (e.g., at cul-de-sacs or road ends), Name_1 and Name_12 are set to the segment’s own Name.

If true intersections are found, the intersecting road names replace the existing Name_1 and Name_12 values.

## 🚀 Getting Started
Requirements
ArcGIS Pro

Python 3 (with ArcPy)

Your roads dataset should be split at intersections.

Usage
Add the .pyt file to your ArcGIS project.

Run the toolbox from the toolbox pane or script.

Input the parameters and let the tool validate road segment names.
