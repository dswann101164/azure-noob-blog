# Content Hub Definitions for Azure Noob Blog

HUBS = {
    'finops': {
        'slug': 'finops',
        'category': 'FinOps',
        'icon': '💰',
        'title': 'Azure FinOps at Scale',
        'subtitle': 'Real cost optimization and governance strategies for enterprise Azure environments managing 31,000+ assets.',
        'gradient_start': '#10b981',
        'gradient_end': '#059669',
        'philosophy_title': 'Why Most Azure Cost Management Fails',
        'philosophy_content': '''
            <p><strong>The harsh truth:</strong> Microsoft's native cost tools are designed for visibility, not action. Azure Cost Management shows you what you spent—but it doesn't tell you <em>why</em> you're spending it or <em>how</em> to fix it at scale.</p>
            
            <p>After managing 31,000 Azure resources at a regional bank, I've learned that successful FinOps requires three things Microsoft doesn't give you:</p>
            
            <ul style="margin: 1rem 0; padding-left: 2rem;">
                <li><strong>Business context in cost reports</strong> — Who approved this? What application is it for? What's the business owner?</li>
                <li><strong>Automated governance at scale</strong> — Tag enforcement, policy-driven resource management, and automatic remediation</li>
                <li><strong>KQL queries that connect the dots</strong> — Join cost data with resource metadata, tags, and business systems</li>
            </ul>
            
            <p>This hub contains the strategies, KQL queries, and governance frameworks I've built to make Azure FinOps actually work in production. No theory. Just battle-tested solutions.</p>
        ''',
        'sections': [
            {
                'title': '1. Foundations: Understanding Azure Costs',
                'icon': '📊',
                'description': 'Start here: how Azure billing actually works and why your reports are wrong.',
                'posts': [
                    'azure-cost-reports-business-reality',
                    'azure-costs-apps-not-subscriptions',
                    'azure-cost-management-is-confusing-but-you-can-tame-it',
                ]
            },
            {
                'title': '2. Governance at Scale',
                'icon': '🎯',
                'description': 'Tag strategies, policies, and automation for enterprise Azure.',
                'posts': [
                    'azure-resource-tags-guide',
                    'azure-chargeback-tags-model',
                    'azure-tag-governance-policy',
                    'tag-governance-247-variations',
                    'resource-tags-100k-problem',
                ]
            },
            {
                'title': '3. KQL for Cost Analysis',
                'icon': '🔍',
                'description': 'Join cost data with resource metadata and tags using KQL and Azure Resource Graph.',
                'posts': [
                    'kql-cheat-sheet-complete',
                    'azure-vm-inventory-kql',
                ]
            },
            {
                'title': '4. Cost Stories for Leadership',
                'icon': '🏛️',
                'description': 'How to talk about Azure spend with finance and executives.',
                'posts': [
                    'azure-cost-reporting-boardroom',
                    'azure-openai-pricing-real-costs',
                ]
            },
        ],
        'github_resources': [
            {
                'name': 'Enhanced Azure Inventory Workbook',
                'description': 'Complete resource inventory with cost analysis and compliance tracking.',
                'url': 'https://github.com/dswann101164/azure-inventory-workbook-enhanced',
            },
            {
                'name': 'CCO Dashboard Project',
                'description': 'Cloud Cost Optimization dashboard with FinOps metrics and business context.',
                'url': 'https://github.com/dswann101164/cco-dash-project',
            },
        ],
        'related_hubs': [
            {
                'slug': 'kql',
                'title': 'KQL Mastery',
                'icon': '🔍',
                'post_count': 6,
            },
            {
                'slug': 'governance',
                'title': 'Azure Governance',
                'icon': '🎯',
                'post_count': 7,
            },
            {
                'slug': 'monitoring',
                'title': 'Azure Monitoring',
                'icon': '📊',
                'post_count': 5,
            },
        ],
        'related_tags': ['FinOps', 'Cost', 'Azure', 'Governance', 'Tags'],
    },

    'kql': {
        'slug': 'kql',
        'category': 'KQL',
        'icon': '🔍',
        'title': 'KQL Queries for Production Azure',
        'subtitle': 'Master Kusto Query Language with real-world queries for Azure Resource Graph, Log Analytics, and Azure Monitor.',
        'gradient_start': '#7c3aed',
        'gradient_end': '#5b21b6',
        'philosophy_title': 'Why KQL is Hard (And How to Make it Easy)',
        'philosophy_content': '''
            <p><strong>The problem with KQL:</strong> Microsoft's documentation shows you <em>what's possible</em>, but not <em>what's useful</em>. You get syntax examples, not production queries.</p>
            
            <p>After writing thousands of KQL queries to manage enterprise Azure infrastructure, I've learned that effective KQL requires understanding three layers:</p>
            
            <ul style="margin: 1rem 0; padding-left: 2rem;">
                <li><strong>Data model awareness</strong> — Knowing which tables exist and how they connect (this is 80% of the battle).</li>
                <li><strong>Query patterns</strong> — Reusable templates for common scenarios (inventory, compliance, cost analysis).</li>
                <li><strong>Performance optimization</strong> — Making queries fast enough for dashboards and automation.</li>
            </ul>
            
            <p>This hub contains my complete KQL toolkit: from beginner fundamentals to advanced joins, aggregations, and performance tuning. Every query is tested in production Azure environments.</p>
        ''',
        'sections': [
            {
                'title': '1. KQL Fundamentals',
                'icon': '📚',
                'description': 'Core syntax, operators, and query structure.',
                'posts': [
                    'kql-cheat-sheet-complete',
                ]
            },
            {
                'title': '2. Resource Inventory Queries',
                'icon': '📦',
                'description': 'Find, count, and analyze Azure resources at scale.',
                'posts': [
                    'azure-vm-inventory-kql',
                    'azure-service-inventory-tool',
                ]
            },
            {
                'title': '3. Cost and Compliance Analysis',
                'icon': '💰',
                'description': 'Join cost data with resource metadata and tags.',
                'posts': [
                    'azure-cost-reports-business-reality',
                    'azure-resource-tags-guide',
                    'azure-cost-management-is-confusing-but-you-can-tame-it',
                ]
            },
            {
                'title': '4. Advanced Techniques',
                'icon': '🚀',
                'description': 'Performance tuning, multi-environment queries, and automation patterns.',
                'posts': [
                    'kql-multiple-systems',
                    'kql-query-library-git',
                    'azure-debugging-ai-rule',
                ]
            },
        ],
        'github_resources': [
            {
                'name': 'KQL Query Library (Coming Soon)',
                'description': 'Production-tested KQL queries for Azure Resource Graph and Log Analytics.',
                'url': 'https://github.com/dswann101164',
            },
            {
                'name': 'Enhanced Azure Inventory Workbook',
                'description': 'Inventory and governance workbook powered by KQL queries.',
                'url': 'https://github.com/dswann101164/azure-inventory-workbook-enhanced',
            },
        ],
        'related_hubs': [
            {
                'slug': 'finops',
                'title': 'FinOps',
                'icon': '💰',
                'post_count': 8,
            },
            {
                'slug': 'monitoring',
                'title': 'Azure Monitoring',
                'icon': '📊',
                'post_count': 6,
            },
            {
                'slug': 'governance',
                'title': 'Azure Governance',
                'icon': '🎯',
                'post_count': 7,
            },
        ],
        'related_tags': ['KQL', 'Azure', 'Queries', 'Resource Graph', 'Log Analytics'],
    },

    'governance': {
        'slug': 'governance',
        'category': 'Governance',
        'icon': '🎯',
        'title': 'Azure Governance at Scale',
        'subtitle': 'Enterprise governance strategies: tags, policies, RBAC, and compliance automation for 31,000+ resources.',
        'gradient_start': '#0078d4',
        'gradient_end': '#003d6b',
        'philosophy_title': 'Governance is a People Problem (Not a Tech Problem)',
        'philosophy_content': '''
            <p><strong>The governance trap:</strong> Teams implement Azure Policy, tag policies, and RBAC—then wonder why nobody follows them. The technical implementation was easy. Getting people to comply is the hard part.</p>
            
            <p>Managing 31,000+ Azure resources taught me that effective governance requires three layers:</p>
            
            <ul style="margin: 1rem 0; padding-left: 2rem;">
                <li><strong>Business buy-in</strong> — Tags and policies must solve business problems (showback, compliance, automation), not just "governance".</li>
                <li><strong>Automated enforcement</strong> — Make compliance the path of least resistance with deny policies, auto-tagging, and remediation.</li>
                <li><strong>Continuous measurement</strong> — KQL dashboards showing compliance trends, not just snapshots.</li>
            </ul>
            
            <p>This hub contains the governance frameworks, tag strategies, and policy patterns I've used to maintain compliance in enterprise Azure environments—without creating bureaucracy that teams ignore.</p>
        ''',
        'sections': [
            {
                'title': '1. Tag Strategy Fundamentals',
                'icon': '🏷️',
                'description': 'Design tag taxonomies that teams will actually use and finance can trust.',
                'posts': [
                    'azure-resource-tags-guide',
                    'azure-chargeback-tags-model',
                    'azure-tag-governance-policy',
                    'tag-governance-247-variations',
                    'resource-tags-100k-problem',
                ]
            },
            {
                'title': '2. Policy, Patching, and Automation',
                'icon': '⚙️',
                'description': 'Use Azure Policy, Update Manager, and automation to enforce standards instead of begging for them.',
                'posts': [
                    'azure-update-manager-reality-check',
                    'sccm-wsus-azure-update-manager-intune-confusion',
                    'azure-vm-automation-dependency-hell',
                    'pull-meta-from-arm',
                    'stop-reading-caf',
                ]
            },
            {
                'title': '3. Audit, Support, and Process Governance',
                'icon': '🧾',
                'description': 'Close audit gaps, fix ticketing reality, and make process part of governance instead of an afterthought.',
                'posts': [
                    'azure-audit-gap-nobody-talks-about',
                    'azure-support-ticket-reality',
                    'azure-service-inventory-tool',
                    'commenting-for-continuity',
                ]
            },
            {
                'title': '4. Hybrid & Azure Arc Governance',
                'icon': '🌉',
                'description': 'Extend Azure governance to VMware and on-prem servers with Azure Arc and a real CMDB strategy.',
                'posts': [
                    'azure-arc-ghost-registrations',
                    'azure-arc-private-lab',
                    'azure-arc-vcenter-implementation-guide',
                    'azure-cmdb-wrong-cloud-fixes-it',
                ]
            },
        ],
        'github_resources': [
            {
                'name': 'Azure Admin Workstation Setup',
                'description': 'Automated configuration for Azure governance and management tooling.',
                'url': 'https://github.com/dswann101164/azure-admin-workstation-setup',
            },
            {
                'name': 'Enhanced Azure Inventory Workbook',
                'description': 'Compliance tracking across subscriptions with governance metrics.',
                'url': 'https://github.com/dswann101164/azure-inventory-workbook-enhanced',
            },
        ],
        'related_hubs': [
            {
                'slug': 'finops',
                'title': 'FinOps',
                'icon': '💰',
                'post_count': 8,
            },
            {
                'slug': 'kql',
                'title': 'KQL Mastery',
                'icon': '🔍',
                'post_count': 7,
            },
            {
                'slug': 'monitoring',
                'title': 'Azure Monitoring',
                'icon': '📊',
                'post_count': 5,
            },
        ],
        'related_tags': ['Governance', 'Azure', 'Tags', 'Policy', 'Compliance'],
    },

    'monitoring': {
        'slug': 'monitoring',
        'category': 'Monitoring',
        'icon': '📊',
        'title': 'Azure Monitoring & Dashboards',
        'subtitle': 'Build production-ready dashboards, workbooks, and alerting for enterprise Azure infrastructure.',
        'gradient_start': '#f59e0b',
        'gradient_end': '#d97706',
        'philosophy_title': 'Dashboards Should Answer Questions (Not Raise Them)',
        'philosophy_content': '''
            <p><strong>The dashboard problem:</strong> Most Azure dashboards are "data dumps"—dozens of tiles showing metrics, logs, and alerts with no context. Nobody knows what's <em>actionable</em>.</p>
            
            <p>After building dashboards for Cloud NOC teams and executives, I've learned that effective monitoring requires three layers:</p>
            
            <ul style="margin: 1rem 0; padding-left: 2rem;">
                <li><strong>Purpose-driven design</strong> — Every dashboard answers a specific question ("What's down?", "What's expensive?", "What's non-compliant?").</li>
                <li><strong>Context over data</strong> — Show business impact, not just technical metrics. "3 VMs down" means nothing. "Payroll app offline" is actionable.</li>
                <li><strong>Automation-ready</strong> — Dashboards should trigger workflows, not just display numbers.</li>
            </ul>
            
            <p>This hub contains the dashboard patterns, workbook templates, and monitoring strategies I've used to build observability systems that teams actually use—from Cloud NOC to FinOps to security.</p>
        ''',
        'sections': [
            {
                'title': '1. Dashboard Fundamentals',
                'icon': '📺',
                'description': 'Design principles for effective Azure dashboards.',
                'posts': [
                    'azure-dashboards-cloud-noc',
                    'chris-bowman-dashboard',
                    'azure-reporting-role-microsoft-should-create',
                    'mcp-vs-powerbi-ai-what-actually-creates-dashboards',
                ]
            },
            {
                'title': '2. Azure Workbooks',
                'icon': '📊',
                'description': 'Build interactive, data-driven workbooks for deep analysis.',
                'posts': [
                    'modernizing-azure-workbooks',
                    'workbook-app-tool',
                    'azure-dashboard-rebranding-tool',
                ]
            },
            {
                'title': '3. Real-World Examples',
                'icon': '💼',
                'description': 'Production dashboard and tooling examples you can deploy today.',
                'posts': [
                    'azure-ipam-tool',
                    'azure-update-manager-reality-check',
                ]
            },
        ],
        'github_resources': [
            {
                'name': 'Chris Bowman Dashboard Model',
                'description': 'Enhanced Azure dashboard with business context and actionable insights.',
                'url': 'https://github.com/dswann101164/bowman-dashboard-model',
            },
            {
                'name': 'Enhanced Azure Inventory Workbook',
                'description': 'Complete resource inventory with cost, compliance, and monitoring data.',
                'url': 'https://github.com/dswann101164/azure-inventory-workbook-enhanced',
            },
            {
                'name': 'CCO Dashboard Project',
                'description': 'Cloud Cost Optimization dashboard with FinOps metrics.',
                'url': 'https://github.com/dswann101164/cco-dash-project',
            },
        ],
        'related_hubs': [
            {
                'slug': 'kql',
                'title': 'KQL Mastery',
                'icon': '🔍',
                'post_count': 7,
            },
            {
                'slug': 'finops',
                'title': 'FinOps',
                'icon': '💰',
                'post_count': 8,
            },
            {
                'slug': 'governance',
                'title': 'Azure Governance',
                'icon': '🎯',
                'post_count': 7,
            },
        ],
        'related_tags': ['Monitoring', 'Azure', 'Dashboards', 'Workbooks', 'KQL'],
    },
}


def get_hub_config(slug):
    """Get hub configuration by slug."""
    return HUBS.get(slug)


def get_all_hubs():
    """Get all hub configurations."""
    return HUBS


def get_hub_navigation():
    """Get hub navigation items for header menu and home page."""
    return [
        {
            'name': 'FinOps',
            'slug': 'finops',
            'url': '/hub/finops/',
            'icon': '💰',
            'title': 'FinOps',
            'tagline': 'Cost optimization and governance at enterprise scale',
        },
        {
            'name': 'KQL',
            'slug': 'kql',
            'url': '/hub/kql/',
            'icon': '🔍',
            'title': 'KQL Mastery',
            'tagline': 'Production-ready queries for Azure Resource Graph',
        },
        {
            'name': 'Governance',
            'slug': 'governance',
            'url': '/hub/governance/',
            'icon': '🎯',
            'title': 'Governance',
            'tagline': 'Tags, policies, and compliance automation',
        },
        {
            'name': 'Monitoring',
            'slug': 'monitoring',
            'url': '/hub/monitoring/',
            'icon': '📊',
            'title': 'Monitoring',
            'tagline': 'Dashboards and workbooks that answer questions',
        },
    ]
