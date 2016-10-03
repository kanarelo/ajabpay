from flask import request, render_template, jsonify, url_for, redirect, g

from ajabpay.index import app, db
from ajabpay.app.models import *
from ajabpay.app.utils import requires_auth

def parse_resource(resource):
    if resource is None:
        return

    if not ('resource_type' in resource and 'event_type' in resource):
         return

    if resource['resource_type'] not in ('sale', 'invoices', 'dispute', 'authorization_consent_revoked'):
        return

    if resource['resource_type'] == 'sale':
        if resource['event_type'] == 'PAYMENT.SALE.DENIED':
            pass
        elif resource['event_type'] == 'PAYMENT.SALE.PENDING':
            pass #update_sale_status(resource['resource'])
        elif resource['event_type'] == 'PAYMENT.SALE.REFUNDED':
            pass
        elif resource['event_type'] == 'PAYMENT.SALE.REVERSED':
            pass
        elif resource['event_type'] == 'PAYMENT.SALE.COMPLETED':
            pass
        else:
            return

        update_sale_status(resource['resource'], 
            event_type=resource['event_type'], 
            webhook_id=resource['id'], 
            summary=resource['summary'])
    elif resource['resource_type'] == 'invoices':
        if resource['event_type'] == 'INVOICING.INVOICE.CANCELLED':
            pass
        elif resource['event_type'] == 'INVOICING.INVOICE.PAID':
            pass
        elif resource['event_type'] == 'INVOICING.INVOICE.REFUNDED':
            pass
        
        update_invoice_status(resource['resource'], 
            event_type=resource['event_type'], 
            webhook_id=resource['id'], 
            summary=resource['summary'])
    elif resource['resource_type'] == 'dispute':
        if resource['event_type'] == 'CUSTOMER.DISPUTE.CREATED':
            pass
        elif resource['event_type'] == 'CUSTOMER.DISPUTE.RESOLVED':
            pass
        elif resource['event_type'] == 'INVOICING.INVOICE.REFUNDED':
            pass
        else:
            return
        
        update_dispute_status(resource['resource'], 
            event_type=resource['event_type'], 
            webhook_id=resource['id'], 
            summary=resource['summary'])
    elif resource['resource_type'] == 'authorization_consent_revoked':
        if resource['event_type'] == 'IDENTITY.AUTHORIZATION-CONSENT.REVOKED':
            pass
        else:
            return

        update_profile_status(resource['resource'], 
            event_type=resource['event_type'], 
            webhook_id=resource['id'], 
            summary=resource['summary'])

@app.route('/services/pp/webhooks', methods=['GET', 'POST'])
def webhook():
    '''
    https://gist.github.com/kanarelo/2400ed991718d23180ec424721c55ce0
    '''
    pass