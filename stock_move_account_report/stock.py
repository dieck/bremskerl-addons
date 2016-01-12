# -*- coding: utf-8 -*-
from osv import fields, osv
import tools
import decimal_precision as dp

class view_stockmove_accountmove_report(osv.osv):
    _name = "view.stockmove.accountmove.report"
    _auto = False
       
    _columns = {
        "date": fields.date("Date"),
        "code":  fields.char('Reference', size=64),
        "name": fields.char('Name', size=128),
        "inv_qty": fields.float('Invoiced Quantity',  digits_compute=dp.get_precision('Product UoM')),
        "balance": fields.float('Balance', digits_compute=dp.get_precision('Account')),
        "acc_qty": fields.float('Account Quantity', digits=(16,2)),
        "inventory": fields.float('Total Inventory Value',  digits_compute=dp.get_precision('Account')),
        "diff": fields.float('Difference',  digits_compute=dp.get_precision('Account')),
    }
    
    def init(self, cr):
        try:
            tools.drop_view_if_exists(cr, 'view_stockmove_accountmove_report')
        except:
            cr.rollback() # allows next statement to pass correctly
        cr.execute("""
            CREATE OR REPLACE VIEW view_stockmove_accountmove_report AS 
 SELECT row_number() over (order by move_report.date) as id, move_report.date, move_report.code, move_report.name, sum(move_report.inv_qty) AS inv_qty, sum(move_report.balance) AS balance, sum(move_report.acc_qty) AS acc_qty, sum(move_report.inventory) AS inventory, sum(COALESCE(move_report.balance, 0.0) - COALESCE(move_report.inventory, 0.0)) AS diff
   FROM (        ( SELECT l.date, p.default_code AS code, p.name_template AS name, 0.0 AS inv_qty, sum(l.quantity) AS acc_qty, COALESCE(sum(l.debit - l.credit), 0.0) AS balance, 0.0 AS inventory
                   FROM product_product p
              LEFT JOIN account_move_line l ON p.id = l.product_id
             WHERE (p.id = l.product_id OR l.product_id IS NULL AND l.name::text ~~ (('['::text || p.default_code::text) || '] %'::text)) AND (l.account_id = (( SELECT account_account.id
                      FROM account_account
                     WHERE account_account.code::text = '5020'::text)) OR l.id IS NULL)
             GROUP BY l.date, p.default_code, p.name_template, l.account_id
             ORDER BY l.date DESC)
        UNION ALL 
                ( SELECT rsi.date::date AS date, p.default_code AS code, p.name_template AS name, sum(rsi.product_qty) AS inv_qty, 0.0 AS acc_qty, 0.0 AS balance, round(sum(rsi.value), 6) AS inventory
                   FROM product_product p
              LEFT JOIN report_stock_inventory rsi ON rsi.product_id = p.id
             WHERE rsi.location_type::text = 'internal'::text AND rsi.state::text = 'done'::text
             GROUP BY rsi.date, p.default_code, p.name_template
             ORDER BY rsi.date DESC)) move_report
  GROUP BY move_report.date, move_report.code, move_report.name
 HAVING sum(move_report.balance) <> 0.0 OR sum(move_report.inventory) IS NOT NULL AND round(sum(move_report.inventory), 2) <> 0.00
  ORDER BY move_report.code, move_report.date;
        """)
    
view_stockmove_accountmove_report()
