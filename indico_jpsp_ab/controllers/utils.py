from indico_jpsp_ab.utils import json_decode

def get_cookies_util(c) -> dict | None:
    return {
        'indico_session_http': c.get('indico_session_http')
    } if c else None


def get_settings_util(s) -> dict | None:

    # print(s)
    
    custom_fields = json_decode(s.custom_fields)

    contribution_fields = [
        dict(id=f.id, name=f.title)
        for f in s.event.contribution_fields
        if f.id in custom_fields
    ]

    return dict(
        api_key=s.api_key,
        api_url=s.api_url,
        pdf_page_width=s.pdf_page_width,
        pdf_page_height=s.pdf_page_height,
        custom_fields=contribution_fields,
        ab_session_h1=s.ab_session_h1,
        ab_session_h2=s.ab_session_h2,
        ab_contribution_h1=s.ab_contribution_h1,
        ab_contribution_h2=s.ab_contribution_h2
    ) if s else None


# pdf_page_width
# pdf_page_height
# ab_session_h1
# ab_session_h2
# ab_contribution_h1
# ab_contribution_p