# Content Hub Definitions for Azure Noob Blog

HUBS = {
    'finops': {
        'slug': 'finops',
        'category': 'FinOps',
        'icon': '💰',
        'title': 'Azure FinOps Complete Guide: Cost Management When Subscriptions Are Security Boundaries',
        'subtitle': 'Enterprise Azure cost allocation, tagging governance, and chargeback models for regulated environments managing 31,000+ resources across 44 subscriptions.',
        'gradient_start': '#10b981',
        'gradient_end': '#059669',
        'philosophy_title': 'What is Azure FinOps (Real Definition)',
        'philosophy_content': '''
            <p><strong>Short Answer:</strong> Azure FinOps is cost visibility + allocation + governance for cloud spending. In regulated industries (banking, healthcare), this means building custom solutions because Microsoft's native tools assume you control your subscription structure—which regulated enterprises never do. Subscriptions serve as security boundaries, not cost centers, breaking Microsoft's cost allocation model.</p>
            
            <h3 style="margin: 1.5rem 0 0.75rem 0; font-size: 1.1rem; font-weight: 600;">Why Azure FinOps is harder than AWS FinOps</h3>
            
            <p><strong>AWS approach:</strong> Consolidated billing with cost allocation tags that work universally across accounts.</p>
            
            <p><strong>Azure reality:</strong> Security boundaries = subscription boundaries = cost reporting nightmare. You can't consolidate billing across subscriptions in regulated environments, making application-level cost tracking require custom KQL queries and tag governance.</p>
            
            <p><strong>Real impact:</strong> Organizations spend more on allocation tooling than they save in optimization because Azure Cost Management can't answer "What does Application X cost across 6 subscriptions?"</p>
            
            <h3 style="margin: 1.5rem 0 0.75rem 0; font-size: 1.1rem; font-weight: 600;">What breaks at enterprise scale</h3>
            
            <ul style="margin: 1rem 0; padding-left: 2rem;">
                <li><strong>Azure Cost Management shows subscription costs, not application costs</strong> — Finance wants "Payroll app monthly cost." Azure shows "Production subscription $47K." These don't align.</li>
                <li><strong>Resource tagging fails without enforcement</strong> — Teams deploy resources without tags. Six months later, finance can't allocate $200K in untagged spend.</li>
                <li><strong>Chargeback models nobody accepts</strong> — IT creates allocation formulas finance rejects because they don't match budget authority or GL accounts.</li>
            </ul>
            
            <p>This hub contains the cost allocation strategies, tag governance frameworks, and KQL queries I've built to make Azure FinOps work in enterprise environments where subscriptions are security boundaries, not billing units.</p>
        ''',
        'sections': [
            {
                'title': '1. Foundations: Understanding Azure Costs',
                'icon': '📊',
                'description': 'Start here: how Azure billing actually works and why your reports are wrong.',
                'posts': [
                    'azure-finops-complete-guide',
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

    'arc': {
        'slug': 'arc',
        'category': 'Azure Arc',
        'icon': '🌉',
        'title': 'Azure Arc at Enterprise Scale',
        'subtitle': 'Extend Azure management to VMware, on-prem servers, and multi-cloud infrastructure. Real governance, inventory, and Arc deployment patterns.',
        'gradient_start': '#8b5cf6',
        'gradient_end': '#6d28d9',
        'philosophy_title': 'Azure Arc is Not "Cloud Extension" — It\'s Inventory Unification',
        'philosophy_content': '''
            <p><strong>The Arc misconception:</strong> Organizations deploy Azure Arc thinking it will "extend Azure Policy to on-prem servers." Then they discover 64% of their Arc registrations are ghost VMs that don\'t exist, governance dashboards are wrong, and nobody knows what\'s actually managed.</p>
            
            <p>After managing Azure Arc at scale for VMware environments with 850+ VMs, I\'ve learned that Arc success requires three things Microsoft doesn\'t emphasize:</p>
            
            <ul style="margin: 1rem 0; padding-left: 2rem;">
                <li><strong>Inventory reconciliation first</strong> — Arc registrations must sync with your CMDB or VMware inventory, or governance data is fiction.</li>
                <li><strong>Ghost registration cleanup</strong> — VMs get deleted but Arc registrations persist, wrecking compliance reports and cost tracking.</li>
                <li><strong>Private Link architecture</strong> — Public internet Arc connectivity creates firewall complexity and security risk in regulated environments.</li>
            </ul>
            
            <p>This hub contains the Arc implementation guides, inventory reconciliation strategies, and governance patterns I\'ve built to make Azure Arc actually work in enterprise VMware and hybrid environments.</p>
        ''',
        'sections': [
            {
                'title': '0. Enterprise Scale Overview',
                'icon': '🏢',
                'description': 'Complete enterprise Arc deployment guide covering all 6 major problems Microsoft doesn\'t document.',
                'posts': [
                    'azure-arc-enterprise-scale-problems',
                ]
            },
            {
                'title': '1. Arc Fundamentals & Implementation',
                'icon': '🚀',
                'description': 'Deploy Azure Arc to VMware vCenter and on-prem servers with proper governance from day one.',
                'posts': [
                    'azure-arc-vcenter-implementation-guide',
                    'azure-arc-private-lab',
                ]
            },
            {
                'title': '2. Arc Inventory & Ghost Registration Management',
                'icon': '👻',
                'description': 'Detect and clean up Arc ghost registrations that wreck governance and compliance reporting.',
                'posts': [
                    'azure-arc-ghost-registrations',
                    'azure-cmdb-wrong-cloud-fixes-it',
                ]
            },
            {
                'title': '3. Hybrid Networking & DNS for Arc',
                'icon': '🔌',
                'description': 'Connect on-prem infrastructure to Azure with Private Link and hybrid DNS patterns.',
                'posts': [
                    'private-endpoint-dns-hybrid-ad',
                    'azure-migrate-enterprise-hybrid',
                ]
            },
        ],
        'github_resources': [
            {
                'name': 'Arc Ghost Registration Detector',
                'description': 'Python script to reconcile Azure Arc inventory against VMware RVTools exports.',
                'url': 'https://github.com/dswann101164',
            },
            {
                'name': 'Azure Arc Lab Terraform',
                'description': 'Complete Azure Arc lab environment with Private Link and vCenter integration.',
                'url': 'https://github.com/dswann101164',
            },
        ],
        'related_hubs': [
            {
                'slug': 'governance',
                'title': 'Azure Governance',
                'icon': '🎯',
                'post_count': 7,
            },
            {
                'slug': 'migration',
                'title': 'Migration',
                'icon': '☁️',
                'post_count': 6,
            },
            {
                'slug': 'monitoring',
                'title': 'Monitoring',
                'icon': '📊',
                'post_count': 5,
            },
        ],
        'related_tags': ['Azure Arc', 'Hybrid', 'VMware', 'Governance', 'Inventory'],
    },

    'automation': {
        'slug': 'automation',
        'category': 'Automation',
        'icon': '⚡',
        'title': 'Azure Automation at Scale',
        'subtitle': 'PowerShell scripts, Logic Apps, IPAM tools, and automation patterns for enterprise Azure operations.',
        'gradient_start': '#ef4444',
        'gradient_end': '#b91c1c',
        'philosophy_title': 'Automation Isn\'t About Writing Scripts — It\'s About Eliminating Repetitive Decisions',
        'philosophy_content': '''
            <p><strong>The automation trap:</strong> Teams write PowerShell scripts for every repetitive task, then wonder why their "automation" requires constant maintenance and breaks when Azure changes. Scripts automate actions, but they don\'t automate <em>decisions</em>.</p>
            
            <p>After automating operations across 31,000+ Azure resources, I\'ve learned that sustainable automation requires three layers:</p>
            
            <ul style="margin: 1rem 0; padding-left: 2rem;">
                <li><strong>Tool consolidation first</strong> — Stop building custom scripts for every problem. Most operational needs have existing tools (IPAM, inventory, dashboard generators).</li>
                <li><strong>Logic Apps over scheduled scripts</strong> — Event-driven automation scales better than cron jobs running PowerShell. Let Azure trigger your automation, not the clock.</li>
                <li><strong>Self-service over tickets</strong> — The best automation eliminates the need for humans to approve routine requests.</li>
            </ul>
            
            <p>This hub contains the automation tools, PowerShell patterns, and Logic App workflows I\'ve built to reduce operational overhead in enterprise Azure environments. Every tool here eliminates repetitive work, not just speeds it up.</p>
        ''',
        'sections': [
            {
                'title': '1. Infrastructure Automation Tools',
                'icon': '🔧',
                'description': 'Production-ready tools for Azure inventory, IPAM, and resource management.',
                'posts': [
                    'azure-service-inventory-tool',
                    'azure-ipam-tool',
                    'pull-meta-from-arm',
                ]
            },
            {
                'title': '2. Logic Apps & Event-Driven Automation',
                'icon': '🔄',
                'description': 'Replace scheduled scripts with event-driven workflows that scale.',
                'posts': [
                    'four-logic-apps-every-azure-admin-needs',
                ]
            },
            {
                'title': '3. PowerShell & Script Modernization',
                'icon': '💻',
                'description': 'Migrate from PowerShell 5.1 to 7.x and fix automation dependency hell.',
                'posts': [
                    'powershell-7-enterprise-migration',
                    'azure-vm-automation-dependency-hell',
                    'azure-scripts-break-server-2025',
                ]
            },
            {
                'title': '4. Dashboard & Workbook Automation',
                'icon': '📊',
                'description': 'Generate dashboards and workbooks programmatically instead of clicking through the portal.',
                'posts': [
                    'workbook-app-tool',
                    'azure-dashboard-rebranding-tool',
                    'pbix-modernizer-tool',
                ]
            },
        ],
        'github_resources': [
            {
                'name': 'Azure Service Inventory Script',
                'description': 'PowerShell script to export complete Azure resource inventory across all subscriptions.',
                'url': '/static/downloads/Get-AzureServiceInventory.ps1',
            },
            {
                'name': 'Azure IPAM Tool',
                'description': 'IP address management across Azure subscriptions with conflict detection.',
                'url': 'https://github.com/dswann101164',
            },
        ],
        'related_hubs': [
            {
                'slug': 'governance',
                'title': 'Azure Governance',
                'icon': '🎯',
                'post_count': 7,
            },
            {
                'slug': 'monitoring',
                'title': 'Monitoring',
                'icon': '📊',
                'post_count': 5,
            },
            {
                'slug': 'kql',
                'title': 'KQL Mastery',
                'icon': '🔍',
                'post_count': 7,
            },
        ],
        'related_tags': ['Automation', 'PowerShell', 'Logic Apps', 'Tools', 'IPAM'],
    },

    'ai': {
        'slug': 'ai',
        'category': 'AI',
        'icon': '🤖',
        'title': 'Azure AI & OpenAI at Scale',
        'subtitle': 'Azure OpenAI pricing, AI Foundry implementation, RAG patterns, and the future of AI-assisted Azure operations.',
        'gradient_start': '#ec4899',
        'gradient_end': '#9333ea',
        'philosophy_title': 'AI Won\'t Replace Azure Admins — It Will Reveal Who\'s Actually Good At Their Job',
        'philosophy_content': '''
            <p><strong>The AI panic:</strong> Azure admins worry that AI will eliminate their jobs. The reality is more nuanced: AI will automate the tasks bad admins rely on (clicking through the portal, copy-pasting from Stack Overflow) while amplifying what good admins already do (understanding systems, debugging complex issues, architecting solutions).</p>
            
            <p>After implementing Azure OpenAI and AI Foundry in production, I\'ve learned that enterprise AI requires three layers Microsoft doesn\'t emphasize:</p>
            
            <ul style="margin: 1rem 0; padding-left: 2rem;">
                <li><strong>Cost reality first</strong> — Azure OpenAI looks cheap until you hit production scale. $50K/month AI bills are common without proper governance.</li>
                <li><strong>RAG complexity</strong> — Retrieval-Augmented Generation isn\'t "just add a vector database." It\'s data governance, chunk strategies, and embedding model selection.</li>
                <li><strong>Role transformation</strong> — AI creates new roles (AI Admin, Prompt Engineer, RAG Architect) while eliminating manual work from existing ones.</li>
            </ul>
            
            <p>This hub contains the Azure OpenAI pricing models, AI Foundry implementation patterns, and career guidance I\'ve learned from deploying AI at enterprise scale. Real costs, real patterns, and real career advice.</p>
        ''',
        'sections': [
            {
                'title': '1. Azure OpenAI Cost Reality',
                'icon': '💸',
                'description': 'Understand Azure OpenAI pricing before your $50K bill arrives.',
                'posts': [
                    'azure-openai-pricing-real-costs',
                ]
            },
            {
                'title': '2. AI Foundry & RAG Implementation',
                'icon': '🏭',
                'description': 'Deploy Azure AI Foundry with Terraform and implement RAG patterns that work in production.',
                'posts': [
                    'azure-ai-foundry-terraform',
                    'azure-ai-foundry-rag-enterprise-reality',
                ]
            },
            {
                'title': '3. AI-Assisted Azure Operations',
                'icon': '🤖',
                'description': 'Use AI to enhance Azure administration without eliminating the human.',
                'posts': [
                    'ai-azure-admins-gap',
                    'azure-ai-collaboration-gap',
                    'mcp-vs-powerbi-ai-what-actually-creates-dashboards',
                ]
            },
            {
                'title': '4. Career & Future of Azure Admin',
                'icon': '🚀',
                'description': 'How AI changes Azure administration roles and what to learn next.',
                'posts': [
                    'will-ai-replace-azure-administrators-by-2030',
                    'the-ai-admin',
                    'three-ai-roles',
                    'gartner-ai-forecast-azure-admin',
                ]
            },
        ],
        'github_resources': [
            {
                'name': 'Azure AI Foundry Terraform Module',
                'description': 'Complete Terraform module for deploying Azure AI Foundry with proper governance.',
                'url': 'https://github.com/dswann101164',
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
                'slug': 'automation',
                'title': 'Automation',
                'icon': '⚡',
                'post_count': 8,
            },
            {
                'slug': 'governance',
                'title': 'Azure Governance',
                'icon': '🎯',
                'post_count': 7,
            },
        ],
        'related_tags': ['AI', 'OpenAI', 'Azure AI Foundry', 'Machine Learning', 'Career'],
    },

    'migration': {
        'slug': 'migration',
        'category': 'Migration',
        'icon': '☁️',
        'title': 'Enterprise Migration Reality',
        'subtitle': 'Pre-migration planning, licensing compliance, ROI reality checks, and lessons learned from real-world Azure migrations at scale.',
        'gradient_start': '#06b6d4',
        'gradient_end': '#0891b2',
        'philosophy_title': 'Most Migrations Fail Before They Start',
        'philosophy_content': '''
            <p><strong>The migration trap:</strong> Organizations design Azure landing zones, engage consultants, and deploy Azure Migrate—then discover 6 months in that nobody knows which applications they own, who maintains them, or whether they should even migrate.</p>
            
            <p>After managing migrations at enterprise scale, I've learned that successful migrations require three things Microsoft doesn't tell you:</p>
            
            <ul style="margin: 1rem 0; padding-left: 2rem;">
                <li><strong>Organizational readiness</strong> — Know what you own, who owns it, and where the installation media is BEFORE touching Azure Migrate.</li>
                <li><strong>Licensing compliance</strong> — Azure Hybrid Benefit can save money or trigger $50K+ audit penalties. The difference is documentation.</li>
                <li><strong>Rationalization first</strong> — 20-40% of applications should be retired, not migrated. Discover this on day 1, not month 18.</li>
            </ul>
            
            <p>This hub contains the pre-migration checklists, licensing guides, and failure patterns I've learned from real enterprise migrations. No theory. Just what actually determines whether migrations succeed or fail.</p>
        ''',
        'sections': [
            {
                'title': '1. Pre-Migration Planning',
                'icon': '📋',
                'description': 'The 55-question assessment that prevents $2M budget overruns.',
                'posts': [
                    'cloud-migration-reality-check',
                    'application-migration-checklist-azure',
                    'why-most-azure-migrations-fail',
                ]
            },
            {
                'title': '2. Migration ROI & Financial Reality',
                'icon': '💰',
                'description': 'Why finance\'s ROI calculation is wrong and what actually changes.',
                'posts': [
                    'azure-migration-roi-wrong',
                    'azure-hybrid-benefit-50k',
                    'azure-migration-yard-sale-rolloff',
                ]
            },
            {
                'title': '3. Execution & Lessons Learned',
                'icon': '🚀',
                'description': 'Real migration patterns, failures, and what works in production.',
                'posts': [
                    'azure-migrate-enterprise-hybrid',
                    'powershell-7-enterprise-migration',
                ]
            },
        ],
        'github_resources': [
            {
                'name': 'Application Migration Questionnaire',
                'description': '55-question Excel template for application assessment.',
                'url': '/static/downloads/Application_Questionnaire_Template_v2.xlsx',
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
                'slug': 'governance',
                'title': 'Azure Governance',
                'icon': '🎯',
                'post_count': 7,
            },
        ],
        'related_tags': ['Migration', 'Azure', 'Cloud Migration', 'Licensing', 'Planning'],
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
        {
            'name': 'Migration',
            'slug': 'migration',
            'url': '/hub/migration/',
            'icon': '☁️',
            'title': 'Migration',
            'tagline': 'Enterprise migration planning and execution reality',
        },
        {
            'name': 'Azure Arc',
            'slug': 'arc',
            'url': '/hub/arc/',
            'icon': '🌉',
            'title': 'Azure Arc',
            'tagline': 'Extend Azure management to VMware and on-prem at scale',
        },
        {
            'name': 'Automation',
            'slug': 'automation',
            'url': '/hub/automation/',
            'icon': '⚡',
            'title': 'Automation',
            'tagline': 'PowerShell, Logic Apps, and tools that eliminate repetitive work',
        },
        {
            'name': 'AI & OpenAI',
            'slug': 'ai',
            'url': '/hub/ai/',
            'icon': '🤖',
            'title': 'AI & OpenAI',
            'tagline': 'Azure OpenAI pricing, AI Foundry, and the future of AI-assisted Azure ops',
        },
    ]
