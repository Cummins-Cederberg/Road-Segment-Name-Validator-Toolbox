# -*- coding: utf-8 -*-

import arcpy


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Road Segment Name Validation Toolbox"
        self.alias = "roadsegmenttools"

        # List of tool classes associated with this toolbox
        self.tools = [CheckRoadNames]


class CheckRoadNames:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Check Segment Road Names"
        self.description = "alidates road segment names by comparing them to intersecting street names at segment start and end points."

    def getParameterInfo(self):
        """Define the tool parameters."""
        params = []

        input_fc = arcpy.Parameter(
            displayName="Input Road Feature Class",
            name="input_fc",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")

        name_field = arcpy.Parameter(
            displayName="Road Name Field",
            name="name_field",
            datatype="Field",
            parameterType="Required",
            direction="Input")
        name_field.parameterDependencies = ["input_fc"]

        name_1_field = arcpy.Parameter(
            displayName="Field for Start Road Name (Name_1)",
            name="name_1_field",
            datatype="Field",
            parameterType="Required",
            direction="Input")
        name_1_field.parameterDependencies = ["input_fc"]

        name_12_field = arcpy.Parameter(
            displayName="Field for End Road Name (Name_12)",
            name="name_12_field",
            datatype="Field",
            parameterType="Required",
            direction="Input")
        name_12_field.parameterDependencies = ["input_fc"]

        params.extend([input_fc, name_field, name_1_field, name_12_field])
        return params



    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        roads_fc = parameters[0].valueAsText
        name_field = parameters[1].valueAsText
        name_1_field = parameters[2].valueAsText
        name_12_field = parameters[3].valueAsText

        arcpy.MakeFeatureLayer_management(roads_fc, "roads_lyr")

        fields = ['OID@', 'SHAPE@', name_field, name_1_field, name_12_field]

        with arcpy.da.UpdateCursor("roads_lyr", fields) as cursor:
            for row in cursor:
                oid, shape, name, name1, name12 = row

                # Only proceed if Name_1 == Name_12
                if not (name1 == name12):
                    continue

                start_geom = arcpy.PointGeometry(shape.firstPoint, shape.spatialReference)
                end_geom = arcpy.PointGeometry(shape.lastPoint, shape.spatialReference)

                # Intersecting road names at start (excluding itself)
                arcpy.SelectLayerByLocation_management("roads_lyr", "INTERSECT", start_geom)
                start_names = [r[0] for r in arcpy.da.SearchCursor("roads_lyr", [name_field]) if r[0] != name]

                # Intersecting road names at end (excluding itself)
                arcpy.SelectLayerByLocation_management("roads_lyr", "INTERSECT", end_geom)
                end_names = [r[0] for r in arcpy.da.SearchCursor("roads_lyr", [name_field]) if r[0] != name]

                # Condition 1: Both ends have NO other intersecting street — assume dead-end/circle
                if not start_names and not end_names:
                    row[3] = name
                    row[4] = name
                    cursor.updateRow(row)
                    continue

                # Condition 2: Segment is likely a curve (no new road names intersected)
                if not start_names and not end_names:
                    continue  # skip updating Name_1 and Name_12

                # Otherwise: update Name_1 and Name_12 with actual intersecting roads
                row[3] = ", ".join(sorted(set(start_names))) if start_names else ""
                row[4] = ", ".join(sorted(set(end_names))) if end_names else ""
                cursor.updateRow(row)

        arcpy.Delete_management("roads_lyr")
        arcpy.AddMessage("✅ Updated intersecting street names where necessary.")
        return


    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
