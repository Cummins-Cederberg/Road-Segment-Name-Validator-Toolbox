# -*- coding: utf-8 -*-

import arcpy


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Road Name Checking Toolbox"
        self.alias = "roadnamecheck"

        # List of tool classes associated with this toolbox
        self.tools = [RoadNameChecking]


class RoadNameChecking:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Fix intersecting road name If Incorrect"
        self.description = "Validates and replaces Name_1 or Name_12 only if intersecting roads suggest a better name"

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
        """The source code of the tool."""
        input_fc = parameters[0].valueAsText
        name_field = parameters[1].valueAsText
        name_1_field = parameters[2].valueAsText
        name_12_field = parameters[3].valueAsText

        arcpy.MakeFeatureLayer_management(input_fc, "roads_lyr")
        fields = ['OID@', 'SHAPE@', name_field, name_1_field, name_12_field]
        updated_count = 0

        with arcpy.da.UpdateCursor("roads_lyr", fields) as cursor:
            for row in cursor:
                oid, shape, name, name1, name12 = row
                updated = False

                # ==== Start Point ====
                start_geom = arcpy.PointGeometry(shape.firstPoint, shape.spatialReference)
                arcpy.SelectLayerByLocation_management("roads_lyr", "INTERSECT", start_geom)
                start_names = [r[0] for r in arcpy.da.SearchCursor("roads_lyr", [name_field]) if r[0] and r[0] != name]

                if start_names and (name1 != ", ".join(sorted(set(start_names)))):
                    row[3] = start_names[0] if len(start_names) == 1 else ", ".join(sorted(set(start_names)))
                    updated = True

                # ==== End Point ====
                end_geom = arcpy.PointGeometry(shape.lastPoint, shape.spatialReference)
                arcpy.SelectLayerByLocation_management("roads_lyr", "INTERSECT", end_geom)
                end_names = [r[0] for r in arcpy.da.SearchCursor("roads_lyr", [name_field]) if r[0] and r[0] != name]

                if end_names and (name12 != ", ".join(sorted(set(end_names)))):
                    row[4] = end_names[0] if len(end_names) == 1 else ", ".join(sorted(set(end_names)))
                    updated = True

                if updated:
                    cursor.updateRow(row)
                    updated_count += 1

        arcpy.Delete_management("roads_lyr")
        arcpy.AddMessage(f"✅ {updated_count} records updated where Name_1 and Name_12 both differed from Name.")
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
