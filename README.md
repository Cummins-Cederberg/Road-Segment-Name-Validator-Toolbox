# 🛣️ Road Name Checking Toolbox

A custom ArcGIS Python Toolbox for validating and updating road segment names based on spatial intersections. This tool compares road name fields (`Name_1` and `Name_12`) against the intersecting road names to correct potential discrepancies at the start and end points of each road segment.

---

## 📦 Features

- Automatically updates `Name_1` and `Name_12` fields if the intersecting road names suggest better values.
- Uses spatial logic to inspect road connectivity and naming consistency.
- Supports complex intersections with multiple connected roads.

---

## 🧰 Toolbox Overview

**Tool Name:** `Fix intersecting road name If Incorrect`  
**Toolbox Name:** `Road Name Checking Toolbox`

### 🔧 Parameters

| Parameter Name            | Description |
|--------------------------|-------------|
| `Input Road Feature Class` | The input polyline feature class representing roads. |
| `Road Name Field`          | The field that stores the main road name (e.g., `FULLNAME`, `STREETNAME`). |
| `Field for Start Road Name (Name_1)` | Field to be updated with road names at the **start** point of the road segment. |
| `Field for End Road Name (Name_12)` | Field to be updated with road names at the **end** point of the road segment. |

---

## 🚀 How It Works

1. For each road feature:
   - It checks the **start point** and **end point** of the geometry.
   - It finds all other roads that **intersect** at that point.
   - If the names of those intersecting roads differ from the current feature's name and `Name_1`/`Name_12`, the fields are updated.
2. The tool ensures that if multiple intersecting road names are found, the names are sorted and concatenated.

---


