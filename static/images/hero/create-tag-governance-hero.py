#!/usr/bin/env python3
"""
Generate hero image for tag governance post showing tag chaos
"""

def create_svg():
    return '''<svg width="1200" height="630" xmlns="http://www.w3.org/2000/svg">
  <!-- Background gradient -->
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1e3a8a;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1e40af;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <rect width="1200" height="630" fill="url(#bgGrad)"/>
  
  <!-- Title -->
  <text x="600" y="80" font-family="Arial, sans-serif" font-size="48" font-weight="bold" fill="#ffffff" text-anchor="middle">
    Tag Governance Gone Wrong
  </text>
  
  <!-- Tag chaos examples -->
  <g transform="translate(100, 150)">
    <!-- CostCenter chaos -->
    <text x="0" y="0" font-family="monospace" font-size="24" fill="#fbbf24" font-weight="bold">CostCenter:</text>
    <text x="0" y="35" font-family="monospace" font-size="18" fill="#f87171">78002566</text>
    <text x="200" y="35" font-family="monospace" font-size="18" fill="#f87171">9807566</text>
    <text x="400" y="35" font-family="monospace" font-size="18" fill="#f87171">CC-78002566</text>
    <text x="0" y="65" font-family="monospace" font-size="18" fill="#f87171">78OO2566</text>
    <text x="200" y="65" font-family="monospace" font-size="18" fill="#f87171">cost-center-78002566</text>
    <text x="600" y="65" font-family="monospace" font-size="18" fill="#f87171">78002566-prod</text>
    
    <!-- Environment chaos -->
    <text x="0" y="120" font-family="monospace" font-size="24" fill="#fbbf24" font-weight="bold">Environment:</text>
    <text x="0" y="155" font-family="monospace" font-size="18" fill="#f87171">Production</text>
    <text x="200" y="155" font-family="monospace" font-size="18" fill="#f87171">Prod</text>
    <text x="300" y="155" font-family="monospace" font-size="18" fill="#f87171">PROD</text>
    <text x="400" y="155" font-family="monospace" font-size="18" fill="#f87171">production</text>
    <text x="600" y="155" font-family="monospace" font-size="18" fill="#f87171">Vmware-Prod</text>
    
    <!-- Owner chaos -->
    <text x="0" y="210" font-family="monospace" font-size="24" fill="#fbbf24" font-weight="bold">Owner:</text>
    <text x="0" y="245" font-family="monospace" font-size="18" fill="#f87171">Data</text>
    <text x="100" y="245" font-family="monospace" font-size="18" fill="#f87171">data</text>
    <text x="200" y="245" font-family="monospace" font-size="18" fill="#f87171">Data Team</text>
    <text x="400" y="245" font-family="monospace" font-size="18" fill="#f87171">john.smith@company.com</text>
  </g>
  
  <!-- Stats box -->
  <rect x="50" y="480" width="1100" height="120" fill="#1e293b" opacity="0.9" rx="10"/>
  <text x="600" y="530" font-family="Arial, sans-serif" font-size="36" font-weight="bold" fill="#fbbf24" text-anchor="middle">
    247 Variations of the Same Cost Center
  </text>
  <text x="600" y="570" font-family="Arial, sans-serif" font-size="24" fill="#ffffff" text-anchor="middle">
    789 Resources • $2.3M in Untrackable Spending • 6 Hours/Month Wasted
  </text>
</svg>'''

if __name__ == '__main__':
    svg_content = create_svg()
    with open('azure-tag-governance.svg', 'w') as f:
        f.write(svg_content)
    print("✓ Created azure-tag-governance.svg")
