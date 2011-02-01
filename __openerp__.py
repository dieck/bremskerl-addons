{
    "name": "Add production lot in manufactoring order views",
    "version": "1.0",
    "depends": ["mrp"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Custom",
    "description": """Add production lot in manufactoring order views
        Tab 'Consumed products' / 'Products to consume',
        Tab 'Finished products' / 'Products to finish'
    """,
    "init_xml": [],
    'update_xml': ["view/mrp_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}