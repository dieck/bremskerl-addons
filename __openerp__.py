{
    "name": "Product-Customer related fields",
    "version": "1.0",
    "depends": ["product"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Custom",
    "description": """Add data relational to products and customers
    """,
    "init_xml": [],
    'update_xml': ["view/partner_view.xml",
                   "view/product_view.xml",
                   "view/product_partner_view.xml",
                   "security/ir.model.access.csv", ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}