---
title: Extract KQL Queries from Azure Workbooks (Workbook → App Tool)
date: 2025-10-13
summary: 'An Azure Monitor workbook-driven app concept: turn your dashboards into
  lightweight tools for operators instead of static reports.'
tags:
- Azure
- KQL
- Monitoring
- Operations
- Python
- Streamlit
- Tools
- Workbooks
cover: static/images/hero/workbook-app-tool.svg
hub: governance
---
Billy York's Azure Inventory Workbook is comprehensive: 110 items tracking 200+ Azure services across compute, networking, PaaS, monitoring, and security. When I needed to enhance it, I hit a problem.

Azure Workbooks are JSON files with deeply nested structure. To understand what's inside—what queries run, what data gets displayed, how items connect—I'd need to click through 110+ items in Azure Portal. Each query buried in JSON. Each parameter block hidden in properties. Each text section wrapped in metadata.

Or I could spend three hours building a tool that parses it in 10 seconds.

I built the tool.

## The Problem with Azure Workbooks

Azure Workbooks are powerful: rich visualizations, interactive parameters, complex KQL queries across subscriptions. Microsoft uses them for everything from security dashboards to resource inventory.

But **understanding someone else's workbook is painful:**

**Azure Portal workflow:**
1. Open workbook in edit mode
2. Click first item
3. Try to figure out what it does
4. Click "Advanced Settings" to see the actual query
5. Copy query to notepad
6. Repeat 109 more times
7. Hope you didn't miss anything

**For Billy York's 110-item workbook?** That's hours of manual clicking and copying.

**What I needed:**
- See all 110 items at once
- Navigate between them quickly
- Extract all KQL queries in one shot
- Export everything for analysis
- Test queries locally without Portal

## The Realization: Workbooks Are Just JSON

Like .pbix files (which are ZIP archives), Azure Workbooks have a simple truth:

**Workbook files are JSON with a predictable structure.**

When you export a workbook from Azure Portal:

```json
{
  "items": [
    {
      "type": 1,
      "content": {
        "json": "## Azure Inventory Workbook\n### Change Log"
      }
    },
    {
      "type": 3,
      "content": {
        "query": "Resources | where type == 'microsoft.compute/virtualmachines'..."
      }
    },
    {
      "type": 9,
      "content": {
        "parameters": [...]
      }
    }
  ]
}
```

**Item types:**
- `1` = text/markdown
- `3` = KQL query
- `9` = parameters
- `10` = links
- `11` = groups
- `12` = metrics

The entire structure is sitting there in JSON. You just need to parse it.

## Building the Workbook → App Tool

I built a Streamlit app that turns workbook JSON into a navigable interface.

### The Core Parser

```python
def flatten_items(workbook: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract all items from workbook JSON with type, name, and content."""
    items = []
    raw_items = workbook.get("items") or workbook.get("graph") or []
    
    if isinstance(raw_items, list):
        for i, it in enumerate(raw_items):
            t = it.get("type") or it.get("content",{}).get("type")
            name = it.get("name") or it.get("content",{}).get("name") or it.get("title")
            items.append({"index": i, "type": t, "name": name, "raw": it})
    
    # Handle ARM template format (value array)
    if not items and isinstance(workbook.get("value"), list):
        for entry in workbook["value"]:
            props = entry.get("properties", {})
            items2 = props.get("serializedData") or props.get("items")
            if isinstance(items2, str):
                try:
                    items2 = json.loads(items2)
                except Exception:
                    items2 = []
            if isinstance(items2, list):
                for i, it in enumerate(items2):
                    t = it.get("type") or it.get("content",{}).get("type")
                    name = it.get("name") or it.get("content",{}).get("name")
                    items.append({"index": i, "type": t, "name": name, "raw": it})
    
    return items
```

**What this does:**
- Handles multiple workbook export formats
- Extracts type, name, and full content for each item
- Returns flat list for easy navigation

### Extracting KQL Queries

KQL queries hide in different places depending on the workbook version:

```python
def extract_kql(item: Dict[str, Any]) -> Optional[str]:
    """Extract KQL query from item, handling multiple schema formats."""
    c = item.get("raw", {}).get("content", {})
    
    if isinstance(c, dict):
        # Direct query string
        if "query" in c and isinstance(c["query"], str):
            return c["query"]
        
        # Nested query object
        if "query" in c and isinstance(c["query"], dict) and "query" in c["query"]:
            return c["query"]["query"]
        
        # Versioned query format
        if "versionedQuery" in c and isinstance(c["versionedQuery"], dict):
            if "query" in c["versionedQuery"]:
                return c["versionedQuery"]["query"]
        
        # JSON-wrapped query
        if "json" in c and isinstance(c["json"], dict) and "query" in c["json"]:
            return c["json"]["query"]
    
    # Queries array (some workbooks)
    q = c.get("queries") if isinstance(c, dict) else None
    if isinstance(q, list) and q:
        first = q[0]
        if isinstance(first, dict) and "query" in first:
            return first["query"]
    
    return None
```

**The challenge:** Microsoft changed the workbook schema over time. This parser handles all common formats.

### The Bug I Had to Fix

Initial version crashed on Billy York's workbook:

```
AttributeError: 'int' object has no attribute 'lower'
```

**The problem:** I assumed `type` was always a string like `"query"`. Billy York's workbook uses **numeric type codes** like `3` for queries, `9` for parameters.

**The fix:**

```python
# Item type mappings (numeric → readable)
WORKBOOK_ITEM_TYPES = {
    1: "text",
    3: "query",
    9: "parameters",
    10: "links",
    11: "group",
    12: "metrics"
}

def normalize_type(raw_type: Any) -> str:
    """Convert workbook type (int or string) to normalized lowercase string."""
    if raw_type is None:
        return "unknown"
    if isinstance(raw_type, int):
        return WORKBOOK_ITEM_TYPES.get(raw_type, f"type{raw_type}")
    if isinstance(raw_type, str):
        return raw_type.lower()
    return str(raw_type).lower()

def get_type_display(raw_type: Any) -> str:
    """Get human-readable type name for display."""
    normalized = normalize_type(raw_type)
    if isinstance(raw_type, int):
        return f"{WORKBOOK_ITEM_TYPES.get(raw_type, f'type{raw_type}')} ({raw_type})"
    return normalized
```

Now `type: 3` displays as `"query (3)"` and parses correctly.

### The Streamlit Interface

```python
import streamlit as st

st.set_page_config(page_title="Azure Workbook → App", layout="wide")
st.title("📒 Azure Monitor Workbook → App")

# File upload
uploaded = st.file_uploader("Upload an Azure Monitor Workbook JSON", type=["json"])

if not uploaded:
    st.info("Upload a workbook export (JSON).")
    st.stop()

# Parse workbook
workbook = load_workbook_json(uploaded.getvalue())
items = flatten_items(workbook)

st.success(f"Parsed {len(items)} item(s) from the workbook.")

# Sidebar navigation
with st.sidebar:
    st.markdown("### Items")
    def format_item(i):
        item = items[i]
        type_display = get_type_display(item.get('type'))
        name = item.get('name') or '(unnamed)'
        return f"{i}: {type_display} — {name}"
    
    idx = st.selectbox("Jump to item", list(range(len(items))), format_func=format_item)

# Display current item
current = items[idx]
itype = normalize_type(current.get('type'))

if "query" in itype or itype == "3":
    q = extract_kql(current)
    if q:
        st.code(q, language="kusto")
        # Optional: Execute query if workspace ID provided
        if run_queries and workspace_id:
            df = try_run_kql(workspace_id, q)
            if df is not None and not df.empty:
                st.dataframe(df.head(500), use_container_width=True)
```

**Key features:**
- Sidebar shows all 110 items with types
- Jump to any item instantly
- Display KQL queries with syntax highlighting
- Optionally execute queries (requires Log Analytics workspace ID)

### Export Functionality

```python
# Extract all KQL queries
kql_rows = []
for it in items:
    k = extract_kql(it)
    if k:
        type_display = get_type_display(it.get('type'))
        kql_rows.append({
            "index": it["index"], 
            "type": type_display,
            "name": it.get("name") or "(unnamed)", 
            "query": k
        })

kql_df = pd.DataFrame(kql_rows)

# CSV export
st.download_button(
    "📥 Download all KQL to CSV", 
    kql_df.to_csv(index=False).encode("utf-8"), 
    "workbook_kql.csv", 
    "text/csv"
)

# Markdown export
md = io.StringIO()
md.write(f"# Workbook: {uploaded.name}\n\n")
md.write(f"**Items:** {len(items)}\n")
md.write(f"**KQL Queries:** {len(kql_rows)}\n\n")

for i, it in enumerate(items):
    type_display = get_type_display(it.get('type'))
    name = it.get('name') or '(unnamed)'
    md.write(f"## Item {i}: {type_display} — {name}\n\n")
    
    txt = extract_text(it)
    q = extract_kql(it)
    
    if txt:
        md.write(txt + "\n\n")
    if q:
        md.write("```kusto\n" + q + "\n```\n\n")
    
    md.write("---\n\n")

st.download_button(
    "📥 Download as Markdown", 
    md.getvalue().encode("utf-8"), 
    "workbook_export.md", 
    "text/markdown"
)
```

## Real-World Result: Billy York's Workbook

Running the tool on [Billy York's Azure Inventory Workbook](https://github.com/scautomation/Azure-Inventory-Workbook):

**Input:** `template.json` (213 KB)

**Output:**
```
✅ Parsed 110 item(s) from the workbook.
✅ Found 41 KQL queries in workbook.
```

**Extracted structure:**

```markdown
# Workbook: template.json

**Items:** 110
**KQL Queries:** 41

---

## Item 2: text (1) — Change Log

## Azure Inventory Workbook
### Change Log

|Version|Description|
|---|---|
|v1.1.1| Initial Release - October 2020 - BY
|v2.0.2 | Added VM state, fixed WVD Details - Feb 2022 - BY

---

## Item 9: query (3) — Azure Compute Summary

```kusto
Resources | where type == "microsoft.compute/virtualmachines"
| extend vmState = tostring(properties.extended.instanceView.powerState.displayStatus)
| extend vmState = iif(isempty(vmState), "VM State Unknown", (vmState))
| summarize count() by vmState
```

---

## Item 15: query (3) — Azure Compute Overview

```kusto
Resources 
| where type == "microsoft.compute/virtualmachines"
| extend vmID = tolower(id)
| extend osDiskId= tolower(tostring(properties.storageProfile.osDisk.managedDisk.id))
| join kind=leftouter(resources
    | where type =~ 'microsoft.compute/disks'
    | where properties !has 'Unattached'
    | project timeCreated, OS, osSku, osDiskSizeGB, osDiskId) on osDiskId
| join kind=leftouter(resources
    | where type =~ 'microsoft.compute/availabilitysets'
    | mv-expand VirtualMachine=properties.virtualMachines
    | project AvailabilitySetID = id, vmID, FaultDomainCount) on vmID
...
```
```

**CSV export:** All 41 queries with index, type, name, and full query text.

**Time to parse:** 10 seconds  
**Time to understand structure:** 5 minutes reading the Markdown  
**Time saved vs manual Portal clicking:** Hours

## What This Enabled

### Enhanced Billy York's Workbook

Original workbook: 50 Azure resource types  
Enhanced version: 200+ resource types  

**The tool let me:**
1. **Extract all existing queries** - see what resources were already tracked
2. **Identify patterns** - understand the query structure Billy used
3. **Add new resource types** - following the same patterns
4. **Test queries locally** - verify before deploying
5. **Document everything** - exported Markdown served as reference

[Read about the enhancement here →](/blog/modernizing-azure-workbooks/)

### Built Custom Workbooks

Using the extracted queries as templates:
- Created security-focused workbook (NSG rules, exposed endpoints)
- Built cost analysis workbook (unattached resources, stopped VMs)
- Developed compliance tracking workbook (tagging, policy violations)

**Pattern:** Extract queries from existing workbooks → modify → deploy new workbooks

### Migrated Workbooks to Code

For complex scenarios, converted workbook queries to Python scripts:
- Extracted all queries using this tool
- Rewrote as Python using Azure SDK
- Automated daily reports
- Integrated with alerting systems

## Optional: Execute Queries

The tool can actually **run the KQL queries** if you provide a Log Analytics workspace ID:

```python
def try_run_kql(workspace_id: str, query: str) -> Optional[pd.DataFrame]:
    """Execute KQL query against Log Analytics workspace."""
    if not AZURE_AVAILABLE or not workspace_id or not query:
        return None
    
    try:
        cred = DefaultAzureCredential(exclude_shared_token_cache_credential=True)
        client = LogsQueryClient(credential=cred)
        resp = client.query_workspace(workspace_id, query, timespan=None)
        
        if not resp.tables:
            return pd.DataFrame()
        
        t = resp.tables[0]
        cols = [c.name for c in t.columns]
        rows = [list(r) for r in t.rows]
        return pd.DataFrame(rows, columns=cols)
    except Exception as e:
        st.warning(f"KQL execution failed: {e}")
        return None
```

**Use cases:**
- Test query modifications before deploying
- Validate query results locally
- Debug complex queries without Portal
- Quick data exploration

**Requirements:**
- Azure authentication (`az login` or DefaultAzureCredential)
- Log Analytics workspace ID
- Toggle enabled in sidebar

## When You Need This Tool

**Use Workbook → App when you need to:**
- Understand someone else's workbook structure
- Extract all KQL queries for reuse
- Document workbook contents
- Enhance existing workbooks
- Migrate workbooks to code
- Debug complex queries locally

**Don't need this if:**
- You built the workbook yourself (you already know the structure)
- Workbook is simple (< 10 items, basic queries)
- Just viewing results (use Azure Portal)

## Comparison to PBIX Modernizer

Similar concept, different Azure file format:

| Feature | PBIX Modernizer | Workbook → App |
|---------|----------------|----------------|
| **Input** | Power BI .pbix files (ZIP) | Azure Workbook JSON |
| **Extracts** | DAX measures, M queries, tables | KQL queries, parameters, content |
| **Format** | XML/JSON inside ZIP | Pure JSON |
| **Type codes** | String types | Numeric + string types |
| **Query language** | DAX + Power Query M | KQL (Kusto) |
| **Execute queries** | No (requires Power BI) | Yes (with workspace ID) |
| **Use case** | Understand Power BI dashboards | Understand Azure Workbooks |

**Both solve the same problem:** Extract and analyze Azure/BI files without clicking through slow UI.

## The GitHub Repo

The complete tool is available on GitHub:

**Features:**
- Upload workbook JSON (drag and drop)
- Parse all items (text, queries, parameters, groups, metrics)
- Navigate via sidebar
- Syntax-highlighted KQL display
- Optional query execution
- Export to CSV (all queries)
- Export to Markdown (full structure)
- Handles numeric and string type codes

**Usage:**

```bash
# Install
git clone https://github.com/yourusername/workbook_app
cd workbook_app
pip install -r requirements.txt

# Run locally
streamlit run streamlit_workbook_app.py

# Opens http://127.0.0.1:8502
# Upload your workbook JSON
```

**No Azure credentials required** unless you want to execute queries.

## The Real Lesson

When you need to understand complex Azure files (workbooks, ARM templates, policies), don't click through the Portal for hours.

The structure is sitting in JSON. Extract it. Parse it. Analyze it.

Billy York's 110-item workbook with 41 complex KQL queries? **Parsed in 10 seconds.** Full structure exported to Markdown. All queries in CSV. Ready for enhancement.

**This tool saved weeks of manual work** during workbook enhancement and migration projects.

It might do the same for you.

---

## Resources

**GitHub Repo:** [Azure Workbook → App Tool](https://github.com/yourusername/workbook_app)  
**Billy York's Original Workbook:** [Azure Inventory Workbook](https://github.com/scautomation/Azure-Inventory-Workbook)  
**My Enhancement:** [Modernizing Azure Workbooks](/blog/modernizing-azure-workbooks/)  
**Similar Tool:** [PBIX Modernizer](/blog/pbix-modernizer-tool/) (for Power BI files)

---

*Building tools to solve real Azure problems? That's what this blog is about. If Workbook → App helps you understand workbooks faster, let me know what you discover.*