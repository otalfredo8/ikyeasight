"""
This module stores SQL queries as constants.
"""

GET_PARTNERS = """
    SELECT p.name, p.street, p.city, p.zip,
           p.partner_latitude as lat, p.partner_longitude as lon,
           c.code as country_code
    FROM res_partner p
    LEFT JOIN res_country c ON p.country_id = c.id
    WHERE p.active = True AND p.is_company = False;
"""
