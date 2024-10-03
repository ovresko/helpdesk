import frappe
from datetime import datetime, timedelta


def execute(filters=None):
    if not filters:
        filters = {}

    # Default values for filters
    created_from = filters.get(
        'created_from', (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d'))
    created_to = filters.get('created_to', datetime.now().strftime('%Y-%m-%d'))
    created_by = filters.get('created_by')
    agent = filters.get('agent')
    type_ = filters.get('type')
    status = filters.get('status')
    work_status = filters.get('work_status')
    source = filters.get('source')
    cause = filters.get('cause')
    resolution = filters.get('resolution')
    team = filters.get('team')
    

    # Base query
    query = """
    SELECT
        a.name,
        a.creation AS created,
        a.subject,
        a.ticket_type,
        a.status,
        a.custom_work_status AS work_status,
        a.custom_hd_cause_of_problem AS cause,
        a.custom_hd_source_of_the_problem AS source,
        a.custom_hd_resolution_of_problem AS resolution,
        CONCAT(
            FLOOR(TIMESTAMPDIFF(SECOND, a.creation, a.resolution_date) / 86400), ' days, ',
            MOD(FLOOR(TIMESTAMPDIFF(SECOND, a.creation, a.resolution_date) / 3600), 24), ' hours, ',
            MOD(FLOOR(TIMESTAMPDIFF(SECOND, a.creation, a.resolution_date) / 60), 60), ' minutes'
        ) AS a1,
        ROUND(TIMESTAMPDIFF(SECOND, a.creation, a.resolution_date) / 3600, 2) AS a1_h,
        a.resolution_date AS a2,
        CONCAT(
            FLOOR((TIMESTAMPDIFF(SECOND, a.creation, a.resolution_date) - (a.total_hold_time * 86400)) / 86400), ' days, ',
            MOD(FLOOR((TIMESTAMPDIFF(SECOND, a.creation, a.resolution_date) - (a.total_hold_time * 86400)) / 3600), 24), ' hours, ',
            MOD(FLOOR((TIMESTAMPDIFF(SECOND, a.creation, a.resolution_date) - (a.total_hold_time * 86400)) / 60), 60), ' minutes'
        ) AS a3,
        ROUND((TIMESTAMPDIFF(SECOND, a.creation, a.resolution_date) - (a.total_hold_time * 86400)) / 3600, 2) AS a3_h,
        a.feedback_rating AS a4,
        CONCAT(
            FLOOR((TIMESTAMPDIFF(SECOND, a.creation, a.resolution_date) + (a.total_hold_time * 86400)) / 86400), ' days, ',
            MOD(FLOOR((TIMESTAMPDIFF(SECOND, a.creation, a.resolution_date) + (a.total_hold_time * 86400)) / 3600), 24), ' hours, ',
            MOD(FLOOR((TIMESTAMPDIFF(SECOND, a.creation, a.resolution_date) + (a.total_hold_time * 86400)) / 60), 60), ' minutes'
        ) AS a5,
        ROUND((TIMESTAMPDIFF(SECOND, a.creation, a.resolution_date) + (a.total_hold_time * 86400)) / 3600, 2) AS a5_h
    FROM
        `tabHD Ticket` a
    WHERE
        a.docstatus = 0
        AND a.creation BETWEEN %(created_from)s AND %(created_to)s
    """

    # Append filters to the query
    if created_by:
        query += " AND a.owner = %(created_by)s"
    if agent:
        query += " AND a.custom_agent = %(agent)s"
    if type_:
        query += " AND a.ticket_type = %(type)s"
    if status:
        query += " AND a.status = %(status)s"
    if work_status:
        query += " AND a.custom_work_status = %(work_status)s"
    if source:
        query += " AND a.custom_hd_source_of_the_problem = %(source)s"
    if cause:
        query += " AND a.custom_hd_cause_of_problem = %(cause)s"
    if resolution:
        query += " AND a.custom_hd_resolution_of_problem = %(resolution)s"
    if team:
        query += " AND a.agent_group = %(team)s"

    

    query += " ORDER BY a.creation;"

    # Prepare the filters for SQL execution
    sql_filters = {
        'created_from': created_from,
        'created_to': created_to,
        'created_by': created_by,
        'agent': agent,
        'type': type_,
        'status': status,
        'work_status': work_status,
        'source': source,
        'cause': cause,
        'resolution':resolution,
        'team':team,
    }

    # Execute the query
    data = frappe.db.sql(query, sql_filters, as_dict=True)

    return get_columns(), data


def get_columns():
    return [
        {"fieldname": "name", "label": "Name", "fieldtype": "Link",
            "options": "HD Ticket", "width": 100},
        {"fieldname": "created", "label": "Created",
            "fieldtype": "Datetime", "width": 150},
        {"fieldname": "subject", "label": "Subject",
            "fieldtype": "Data", "width": 200},
        {"fieldname": "ticket_type", "label": "Ticket Type",
            "fieldtype": "Link", "options": "HD Ticket Type", "width": 150},
        {"fieldname": "status", "label": "Status",
            "fieldtype": "Data", "width": 100},
        {"fieldname": "work_status", "label": "Work Status",
            "fieldtype": "Data", "width": 100},
        {"fieldname": "cause", "label": "Cause", "fieldtype": "Link",
            "options": "HD Cause of problem", "width": 200},
        {"fieldname": "source", "label": "Source", "fieldtype": "Link",
            "options": "HD Source of the problem", "width": 200},
        {"fieldname": "resolution", "label": "Resolution", "fieldtype": "Link",
            "options": "HD Resolution of problem", "width": 200},
        {"fieldname": "a1", "label": "Durée de Résolution",
            "fieldtype": "Data", "width": 150},
        {"fieldname": "a1_h",
            "label": "Durée de Résolution (Heures)", "fieldtype": "Float", "width": 150},
        {"fieldname": "a2", "label": "Date de Résolution",
            "fieldtype": "Datetime", "width": 150},
        {"fieldname": "a3", "label": "Durée de Traitement Sans Attente",
            "fieldtype": "Data", "width": 150},
        {"fieldname": "a3_h",
            "label": "Durée de Traitement Sans Attente (Heures)", "fieldtype": "Float", "width": 150},
        {"fieldname": "a4", "label": "Évaluation des Retours",
            "fieldtype": "Float", "width": 100},
        {"fieldname": "a5", "label": "Durée de Traitement Avec Attente",
            "fieldtype": "Data", "width": 150},
        {"fieldname": "a5_h",
            "label": "Durée de Traitement Avec Attente (Heures)", "fieldtype": "Float", "width": 150}
    ]
