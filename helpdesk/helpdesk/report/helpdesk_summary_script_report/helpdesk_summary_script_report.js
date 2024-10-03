// Copyright (c) 2024, Your Company
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Helpdesk Summary Script Report"] = {
    filters: [
        {
            fieldname: "created_from",
            label: __("Created From"),
            fieldtype: "Date",
            default: frappe.datetime.add_days(frappe.datetime.nowdate(), -15),
            reqd: 1,
        },
        {
            fieldname: "created_to",
            label: __("Created To"),
            fieldtype: "Date",
            default: frappe.datetime.nowdate(),
            reqd: 1,
        },
        {
            fieldname: "created_by",
            label: __("Created By"),
            fieldtype: "Link",
            options: "User",
        },
        {
            fieldname: "agent",
            label: __("HD Agent"),
            fieldtype: "Link",
            options: "HD Agent",
        },
        {
            fieldname: "type",
            label: __("Ticket Type"),
            fieldtype: "Link",
            options: "HD Ticket Type",
        },
        {
            fieldname: "status",
            label: __("HD Ticket Status"),
            fieldtype: "Select",
            options: [
                { label: __("Open"), value: "Open" },
                { label: __("Replied"), value: "Replied" },
                { label: __("Resolved"), value: "Resolved" },
                { label: __("Closed"), value: "Closed" },
            ],
        },
        {
            fieldname: "work_status",
            label: __("Work Status"),
            fieldtype: "Select",
            options: [
                { label: __("En Cours"), value: "En Cours" },
                { label: __("En Attente"), value: "En Attente" },
                { label: __("Annulé"), value: "Annulé" },
            ],
        },
        {
            fieldname: "source",
            label: __("HD Source of the Problem"),
            fieldtype: "Link",
            options: "HD Source of the problem",
        },
        {
            fieldname: "cause",
            label: __("HD Cause of Problem"),
            fieldtype: "Link",
            options: "HD Cause of problem",
        },
        {
            fieldname: "resolution",
            label: __("HD Resolution of Problem"),
            fieldtype: "Link",
            options: "HD Resolution of problem",
        },
        {
            fieldname: "team",
            label: __("HD Team"),
            fieldtype: "Link",
            options: "HD Team",
        },
    ]
};
