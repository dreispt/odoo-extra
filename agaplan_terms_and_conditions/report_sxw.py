from osv import osv
import pooler
from report.report_sxw import report_sxw
from tools.safe_eval import safe_eval

import time
import base64
import logging

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    from pyPdf import PdfFileWriter, PdfFileReader
except ImportError:
    raise osv.except_osv(
        "agaplan_terms_and_conditions needs pyPdf",
        """To install the module "agaplan_terms_and_conditions" please ask your administrator to install the pyPdf package."""
    )


# We store the original function
openerp_create_single_pdf = report_sxw.create_single_pdf

def create_single_pdf(self, cr, uid, ids, data, report_xml, context=None):
    log = logging.getLogger('agaplan_terms_and_conditions')

    res = openerp_create_single_pdf(self, cr, uid, ids, data, report_xml, context)
    if report_xml.report_type != 'pdf':
        log.warn("report_type was not what we expected (%s) thus we return regular result.", report_xml.report_type)
        return res

    pool = pooler.get_pool(cr.dbname)

    # Check conditions to add or not
    rule_obj = pool.get('term.rule')
    if not rule_obj:
        # Module is not installed
        return res

    if not hasattr(report_xml, 'report_name'):
        # Likely means that the report_name was not found in ir.actions.report_xml
        # and a placeholder object is being created on the fly in report_sxw.py:426
        # Since we cannot extract and test report_name there we skip remarks.
        return res

    rule_ids = rule_obj.search(cr, uid, [
        ('report_name','=',report_xml.report_name),
    ])

    if not len(rule_ids):
        # No conditions should be added, return regular result
        return res

    valid_rules = []
    for rule in rule_obj.browse(cr, uid, rule_ids, context=context):
        log.debug("Checking rule %s for report %s, with data: %s",
                rule.term_id.name, report_xml.report_name, data)

        model_obj = self.getObjects(cr, uid, ids[0], context=context)
        if rule.company_id and hasattr(model_obj, 'company_id'):
            if rule.company_id.id != model_obj.company_id.id:
                log.debug("Company id's did not match !")
                continue
            else:
                log.debug("Company id's matched !")

        if rule.condition:
            env = {
                'object': model_obj,
                'report': report_xml,
                'data': data,
                'date': time.strftime('%Y-%m-%d'),
                'time': time,
                'context': context,
            }
            # User has specified a condition, check it and return res when not met
            if not safe_eval(rule.condition, env):
                log.debug("Term condition not met !")
                continue
            else:
                log.debug("Term condition met !")

        valid_rules += [ rule ]

    output = PdfFileWriter()
    reader = PdfFileReader( StringIO(res[0]) )

    for rule in valid_rules:
        if rule.term_id.mode == 'begin':
            att = PdfFileReader( StringIO(base64.decodestring(rule.term_id.pdf)) )
            map(output.addPage, att.pages)

    for page in reader.pages:
        output.addPage( page )
        for rule in valid_rules:
            if rule.term_id.mode == 'duplex':
                att = PdfFileReader( StringIO(base64.decodestring(rule.term_id.pdf)) )
                map(output.addPage, att.pages)

    for rule in valid_rules:
        if rule.term_id.mode == 'end':
            att = PdfFileReader( StringIO(base64.decodestring(rule.term_id.pdf)) )
            map(output.addPage, att.pages)

    buf = StringIO()
    output.write(buf)
    return (buf.getvalue(), report_xml.report_type)

report_sxw.create_single_pdf = create_single_pdf

# vim:sts=4:et
