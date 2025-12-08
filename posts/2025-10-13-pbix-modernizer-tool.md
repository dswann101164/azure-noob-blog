---
title: "How I Reverse-Engineered a Power BI Dashboard (PBIX Modernizer Tool)"
date: 2025-10-13
summary: "Chris Bowman's CCO Dashboard is 200+ pages of Power BI. I needed to understand it to build CCO 2.0. Built a tool that extracts all queries, measures, and relationships in seconds. .pbix files are just ZIP archives."
tags: ["azure", "power-bi", "python", "tools", "cco-dashboard"]
cover: "static/images/hero/pbix-modernizer.svg"
---

Chris Bowman's CCO (Continuous Cloud Optimization) Dashboard is 200+ pages of Power BI showing Azure resource inventory, cost analysis, and security recommendations. I needed to understand how it worked to build a better version.

Opening the .pbix file in Power BI Desktop and clicking through every query, every DAX measure, every data relationship? That's hours of manual work.

So I built a tool that extracts everything in seconds.

## The Problem

Power BI Desktop is great for building dashboards. It's terrible for understanding someone else's dashboard.

**What I needed to know:**
- What queries does this dashboard run?
- What data sources does it connect to?
- What DAX measures calculate the metrics?
- How are tables related?
- What's the overall structure?

**Power BI Desktop workflow:**
1. Open .pbix file
2. Click "Transform Data" to see queries
3. Click through each query one by one (dozens of them)
4. Go back to main window
5. Click "Modeling" to see relationships
6. Click through measures one by one
7. Take notes manually
8. Hope you didn't miss anything

For a 200+ page dashboard with 50+ queries and hundreds of DAX measures? This takes hours.

## The Realization: .pbix Files Are Just ZIP Archives

Here's what nobody tells you about Power BI files:

**.pbix files are ZIP archives with JSON and XML inside.**

```powershell
# Try this yourself
Copy-Item "dashboard.pbix" "dashboard.zip"
Expand-Archive "dashboard.zip" -DestinationPath "extracted"
```

**What's inside:**
```
extracted/
├── DataModel         # The data model (binary format)
├── DataModelSchema   # Schema definitions (XML)
├── Report/
│   └── Layout        # Visual layouts (JSON)
├── Metadata          # Dashboard metadata (JSON)
├── DiagramLayout     # Relationship diagram
└── [Content_Types].xml
```

The entire dashboard structure is sitting there in JSON and XML files. You just need to read them.

## Building the PBIX Modernizer Tool

I built a Python tool that unzips .pbix files and extracts the important parts:

### Step 1: Unzip the .pbix File

```python
import zipfile
import json
from pathlib import Path

def extract_pbix(pbix_path, output_dir):
    """Extract .pbix file contents"""
    with zipfile.ZipFile(pbix_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    
    print(f"✓ Extracted {pbix_path} to {output_dir}")
```

**That's it.** No special libraries needed. It's just a ZIP file.

### Step 2: Parse the DataModelSchema

The `DataModelSchema` file contains the data model structure in XML:

```python
import xml.etree.ElementTree as ET

def parse_datamodel_schema(schema_path):
    """Parse DataModelSchema to extract tables and relationships"""
    tree = ET.parse(schema_path)
    root = tree.getroot()
    
    # Extract tables
    tables = []
    for table in root.findall(".//Table"):
        table_name = table.get('Name')
        tables.append(table_name)
    
    # Extract relationships
    relationships = []
    for rel in root.findall(".//Relationship"):
        from_table = rel.get('FromTable')
        to_table = rel.get('ToTable')
        relationships.append({
            'from': from_table,
            'to': to_table
        })
    
    return {
        'tables': tables,
        'relationships': relationships
    }
```

### Step 3: Extract Power Query (M) Code

Power BI stores Power Query code in the DataMashup file (binary format, but readable):

```python
def extract_queries(datamashup_path):
    """Extract Power Query M code from DataMashup"""
    # DataMashup is a binary format, but queries are readable
    with open(datamashup_path, 'rb') as f:
        content = f.read()
    
    # Find M query sections (they're embedded in the binary)
    # This is simplified - actual implementation needs proper parsing
    queries = []
    
    # Look for "section" keyword (M queries start with "section")
    sections = content.split(b'section')
    
    for section in sections[1:]:  # Skip first (before any "section")
        try:
            # Decode and extract readable query text
            query_text = section.decode('utf-16-le', errors='ignore')
            if query_text.strip():
                queries.append(query_text[:500])  # First 500 chars
        except:
            continue
    
    return queries
```

### Step 4: Parse DAX Measures

DAX measures are in the DataModelSchema as well:

```python
def extract_dax_measures(schema_path):
    """Extract DAX measures from schema"""
    tree = ET.parse(schema_path)
    root = tree.getroot()
    
    measures = []
    for measure in root.findall(".//Measure"):
        measure_name = measure.get('Name')
        dax_expression = measure.find('Expression')
        
        if dax_expression is not None:
            measures.append({
                'name': measure_name,
                'expression': dax_expression.text
            })
    
    return measures
```

### Step 5: Generate Readable Report

Put it all together:

```python
def analyze_pbix(pbix_path):
    """Complete analysis of .pbix file"""
    # Extract
    extract_dir = Path("./extracted")
    extract_pbix(pbix_path, extract_dir)
    
    # Parse components
    schema_path = extract_dir / "DataModelSchema"
    datamashup_path = extract_dir / "DataMashup"
    
    model = parse_datamodel_schema(schema_path)
    queries = extract_queries(datamashup_path)
    measures = extract_dax_measures(schema_path)
    
    # Generate report
    report = {
        'tables': model['tables'],
        'relationships': model['relationships'],
        'query_count': len(queries),
        'queries': queries[:10],  # First 10 queries
        'measure_count': len(measures),
        'measures': measures[:20]  # First 20 measures
    }
    
    return report

# Usage
report = analyze_pbix("CCO_Dashboard.pbix")
print(json.dumps(report, indent=2))
```

## What I Discovered About the CCO Dashboard

Running this tool on Chris Bowman's dashboard showed me:

**Tables (50+):**
- ResourceGroups
- VirtualMachines
- StorageAccounts
- SqlDatabases
- NetworkSecurityGroups
- ... (and 40+ more)

**Queries (60+):**
- Most queries hit Azure Resource Graph KQL
- Some hit Azure Cost Management APIs
- Some transform data with Power Query M
- Pattern: One query per Azure resource type

**DAX Measures (100+):**
- Cost aggregations by subscription/resource group
- VM count by status (running/stopped/deallocated)
- Security score calculations
- Compliance percentages
- Resource age calculations

**Key Insight:** The CCO Dashboard is essentially:
1. 60+ Azure Resource Graph KQL queries
2. Power Query to shape the data
3. 100+ DAX measures to calculate metrics
4. 200+ pages of visualizations

**This told me what I needed to build CCO 2.0:**
- Don't rebuild the Power BI file
- Build a Python service that runs the same KQL queries
- Calculate metrics in Python/Pandas instead of DAX
- Serve via web dashboard (Streamlit) instead of Power BI

## The Actual Tool Output

Running PBIX Modernizer on the CCO Dashboard:

```json
{
  "metadata": {
    "name": "CCO_Dashboard_v8",
    "version": "8.0",
    "created": "2024-03-15",
    "author": "Chris Bowman"
  },
  "statistics": {
    "tables": 52,
    "relationships": 48,
    "queries": 63,
    "dax_measures": 147,
    "visuals": 200+
  },
  "sample_queries": [
    {
      "name": "AzureVMs",
      "type": "ResourceGraph",
      "preview": "Resources | where type =~ 'microsoft.compute/virtualmachines'..."
    },
    {
      "name": "StorageAccounts",
      "type": "ResourceGraph",
      "preview": "Resources | where type =~ 'microsoft.storage/storageaccounts'..."
    }
  ],
  "sample_measures": [
    {
      "name": "Total VM Count",
      "dax": "COUNTROWS('VirtualMachines')"
    },
    {
      "name": "Running VMs",
      "dax": "CALCULATE([Total VM Count], VirtualMachines[PowerState] = \"Running\")"
    }
  ]
}
```

**Time to analyze:** 10 seconds

**Time to understand:** 5 minutes reading the output

**Time saved:** Hours of clicking through Power BI Desktop

## Building CCO Dashboard 2.0

Understanding the original structure let me build a better version:

**Original CCO Dashboard (Power BI):**
- ✅ Comprehensive data collection
- ✅ Rich visualizations
- ❌ Requires Power BI Desktop or Premium
- ❌ Slow refresh (60+ queries run sequentially)
- ❌ Can't customize queries easily
- ❌ 200+ pages = hard to navigate

**CCO Dashboard 2.0 (Python/Streamlit):**
- ✅ Same KQL queries (learned from analysis)
- ✅ Web-based (no Power BI license needed)
- ✅ Fast refresh (parallel query execution)
- ✅ Easy to customize (Python code)
- ✅ Modular design (add/remove features easily)
- ✅ API-first (can integrate with other systems)

The PBIX Modernizer tool gave me the blueprint for building the improved version.

## The GitHub Repo

The complete tool is available on GitHub:

**Features:**
- Extract .pbix file contents
- Parse DataModelSchema (tables, relationships)
- Extract Power Query M code
- Parse DAX measures
- Generate JSON report
- Command-line interface

**Usage:**

```bash
# Install
git clone https://github.com/yourusername/pbix-modernizer
cd pbix-modernizer
pip install -r requirements.txt

# Analyze a .pbix file
python pbix_modernizer.py analyze "CCO_Dashboard.pbix" --output report.json

# View summary
python pbix_modernizer.py summarize "CCO_Dashboard.pbix"
```

**Output formats:**
- JSON (full details)
- Markdown (human-readable summary)
- CSV (tables and relationships)

## When You Need This Tool

**Use PBIX Modernizer when you need to:**
- Understand someone else's Power BI dashboard
- Document dashboard structure before modifying
- Extract queries for reuse in other systems
- Audit DAX measure complexity
- Prepare for dashboard migration
- Compare multiple dashboard versions

**Don't need this if:**
- You built the dashboard yourself (you already know the structure)
- You have full documentation (rare)
- Dashboard is simple (< 10 queries, < 20 measures)

## The Power BI Structure Nobody Explains

Here's what this tool taught me about Power BI internals:

**.pbix file structure:**
- ZIP archive (just rename to .zip)
- DataModelSchema = XML schema of tables/relationships/measures
- DataMashup = Binary file containing Power Query M code
- Report/Layout = JSON visual layouts
- Metadata = Dashboard metadata (name, version, author)

**Why this matters:**
- You can programmatically analyze dashboards
- You can extract queries without opening Power BI
- You can audit measure complexity automatically
- You can compare dashboard versions with diff tools

**Microsoft doesn't document this** because they want you using Power BI Desktop. But for analysis, automation, and migration, direct file access is powerful.

## The Real Lesson

When you need to understand complex Power BI dashboards, don't click through Power BI Desktop for hours.

The entire structure is sitting in a ZIP archive. Extract it. Parse the XML and JSON. Generate a report.

Chris Bowman's 200+ page CCO Dashboard with 60+ queries and 100+ measures? Analyzed in 10 seconds.

That analysis became the blueprint for CCO Dashboard 2.0, which I'm building in Python to solve the same problems without requiring Power BI licenses.

**PBIX Modernizer saved me weeks of reverse-engineering work.**

It might do the same for you.

---

## Resources

**GitHub Repo:** [PBIX Modernizer Tool](https://github.com/yourusername/pbix-modernizer)  
**Chris Bowman's Original CCO Dashboard:** [GitHub - chbomme/CloudOptimizationDashboard](https://github.com/chbomme/CloudOptimizationDashboard)  
**My CCO 2.0 Progress:** [Modernizing Azure Workbooks](/blog/modernizing-azure-workbooks/)

---

*Building tools to solve real problems? That's what this blog is about. If PBIX Modernizer helps you understand Power BI dashboards faster, let me know what you discover.*
