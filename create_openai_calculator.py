"""
Generate Azure OpenAI Cost Calculator Excel file
Run this script to create the calculator in static/downloads/
"""
import openpyxl
from openpyxl.styles import Font, PatternFill
from pathlib import Path

# Create workbook
wb = openpyxl.Workbook()
if 'Sheet' in wb.sheetnames:
    del wb['Sheet']

# ==================== CALCULATOR SHEET ====================
ws = wb.create_sheet("Cost Calculator", 0)

# Styling
header_fill = PatternFill(start_color="0066CC", end_color="0066CC", fill_type="solid")
header_font = Font(color="FFFFFF", bold=True, size=12)
section_fill = PatternFill(start_color="E6F2FF", end_color="E6F2FF", fill_type="solid")
section_font = Font(bold=True, size=11)

# Set column widths
ws.column_dimensions['A'].width = 35
ws.column_dimensions['B'].width = 20
ws.column_dimensions['C'].width = 15

# Title
ws['A1'] = "Azure OpenAI Cost Calculator"
ws['A1'].font = Font(size=16, bold=True, color="0066CC")
ws.merge_cells('A1:C1')
ws['A2'] = "Calculate REAL production costs (not what Microsoft's calculator shows)"
ws['A2'].font = Font(size=10, italic=True)
ws.merge_cells('A2:C2')

# Input Section
ws['A4'] = "INPUT: Your Usage"
ws['A4'].fill = section_fill
ws['A4'].font = section_font
ws.merge_cells('A4:C4')

ws['A5'] = "1. Select Model"
ws['B5'] = "GPT-4o"
ws['C5'] = "(GPT-3.5, GPT-4, GPT-4o)"

ws['A6'] = "2. Monthly Input Tokens"
ws['B6'] = 1000000
ws['C6'] = "tokens"

ws['A7'] = "3. Monthly Output Tokens"
ws['B7'] = 1000000
ws['C7'] = "tokens"

ws['A8'] = "4. Using Fine-Tuned Model?"
ws['B8'] = "No"
ws['C8'] = "(Yes/No)"

# Pricing Section
ws['A10'] = "MODEL PRICING (per 1,000 tokens)"
ws['A10'].fill = section_fill
ws['A10'].font = section_font
ws.merge_cells('A10:C10')

pricing = [
    ("GPT-3.5-Turbo Input", 0.002, "$"),
    ("GPT-3.5-Turbo Output", 0.002, "$"),
    ("GPT-4o Input", 0.01, "$"),
    ("GPT-4o Output", 0.03, "$"),
    ("GPT-4 (8K) Input", 0.03, "$"),
    ("GPT-4 (8K) Output", 0.06, "$"),
]

for idx, (name, price, currency) in enumerate(pricing, 11):
    ws[f'A{idx}'] = name
    ws[f'B{idx}'] = price
    ws[f'C{idx}'] = currency

# Calculations
ws['A18'] = "CALCULATED COSTS"
ws['A18'].fill = header_fill
ws['A18'].font = header_font
ws.merge_cells('A18:C18')

ws['A19'] = "Token Costs (Input + Output)"
ws['B19'] = '=IF(B5="GPT-4o",(B6/1000)*B13+(B7/1000)*B14,IF(B5="GPT-3.5",(B6/1000)*B11+(B7/1000)*B12,(B6/1000)*B15+(B7/1000)*B16))'
ws['B19'].number_format = '$#,##0.00'
ws['C19'] = "$"

ws['A20'] = "Infrastructure Overhead"
ws['B20'] = 35
ws['B20'].number_format = '$#,##0.00'
ws['C20'] = "$"

ws['A21'] = "Fine-Tuning Hosting Fee"
ws['B21'] = '=IF(B8="Yes",1836,0)'
ws['B21'].number_format = '$#,##0.00'
ws['C21'] = "$"

ws['A22'] = "Retry/Error Overhead (15%)"
ws['B22'] = '=B19*0.15'
ws['B22'].number_format = '$#,##0.00'
ws['C22'] = "$"

ws['A24'] = "Microsoft's Calculator Shows:"
ws['A24'].font = Font(bold=True)
ws['B24'] = '=B19'
ws['B24'].number_format = '$#,##0.00'
ws['B24'].font = Font(size=12)

ws['A25'] = "Your ACTUAL Production Cost:"
ws['A25'].font = Font(bold=True, size=12)
ws['B25'] = '=B19+B20+B21+B22'
ws['B25'].number_format = '$#,##0.00'
ws['B25'].font = Font(size=14, bold=True, color="FF0000")

ws['A26'] = "The Gap:"
ws['A26'].font = Font(bold=True, size=12)
ws['B26'] = '=B25-B24'
ws['B26'].number_format = '$#,##0.00'
ws['B26'].font = Font(size=14, bold=True, color="FF0000")

ws['A27'] = "Cost Multiplier:"
ws['B27'] = '=B25/B24'
ws['B27'].number_format = '0.0"x"'
ws['B27'].font = Font(size=12, bold=True)

# ==================== INSTRUCTIONS SHEET ====================
ws_inst = wb.create_sheet("Instructions")
ws_inst['A1'] = "How to Use This Calculator"
ws_inst['A1'].font = Font(size=14, bold=True)

instructions = [
    "",
    "1. Go to the 'Cost Calculator' tab",
    "2. Enter your monthly token usage (input and output separately)",
    "3. Select your model (GPT-3.5, GPT-4o, or GPT-4)",
    "4. Indicate if you're using fine-tuning (Yes/No)",
    "",
    "The calculator shows:",
    "  - What Microsoft's calculator estimates",
    "  - Your ACTUAL production cost",
    "  - The gap between them",
    "",
    "Created by Azure-Noob.com",
    "For more: azure-noob.com/hub/finops",
    "",
    "© 2025 David Swann",
]

for idx, text in enumerate(instructions, 3):
    ws_inst[f'A{idx}'] = text

ws_inst.column_dimensions['A'].width = 80

# Save file
output_path = Path(__file__).parent / 'static' / 'downloads' / 'Azure_OpenAI_Cost_Calculator.xlsx'
output_path.parent.mkdir(parents=True, exist_ok=True)
wb.save(output_path)

print(f"✅ Calculator created: {output_path}")
print(f"📊 Sheets: Cost Calculator, Instructions")
