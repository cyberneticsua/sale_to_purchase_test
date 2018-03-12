# -*- coding: utf-8 -*-
{
    "name" : "Sale to Purchase order",
    "version" : "1.0",
    'summary': """ This module brings users to create a purchase order while doing sale order.""",
    'category': 'Sales Management',
    'author': 'zerokool ?',
    'website': '',
    "depends" : ['sale','purchase', ],
    'data': ['views/sale_order_inherit.xml',
            'views/sale_order_tab.xml'],
    'images': ['static/description/banner1.jpg',
               'static/description/banner2.jpg',
               'static/description/banner3.jpg'],
    'license': 'LGPL-3',
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}