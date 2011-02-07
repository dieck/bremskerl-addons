{
    "name": "Purchase Order View Currency",
    "version": "1.0",
    "depends": ["purchase"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Sales & Purchases",
    "description": """
    Adds currency to Purchase Order List view
    """,
    "init_xml": [],
    'update_xml': [
                   "view/purchase_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}