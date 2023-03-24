from svapi_py.api import SvApi
from svapi_py import processors
from django.conf import settings

CONF = settings.CONF


def navigation(request):
    # make a SODAvault Editor credentials, and use them for this request
    headers = {
        'Aid': CONF.get('svapi', {}).get('aid', ''),
        'Auth': CONF.get('svapi', {}).get('auth', ''),
        'Prefix': CONF.get('svapi', {}).get('prefix', ''),
        'Content-Type': 'application/json'
    }
    svapi = SvApi(request=request, headers=headers)
    # tech docs
    tech_docs, err = svapi.getMany('search', params={
        'docType': 'techdoc',
        'website': 'sodavault.com:rev',
        'sortby': 'docLexi:ASC',
    })
    forest = []
    if err == '':
        forest = processors.parent_child_list(tech_docs.get('Data', []))
    new_list = []
    for node in forest:
        new_list = processors.flatten_list(
            node, level=0, new_list=new_list)
    td_list = []
    for td in new_list:
        d = {}
        d['docID'] = td['docID']
        d['title'] = td['title']
        d['docType'] = td['docType']
        td_list.append(d)

    # pages
    pages, err = svapi.getMany('search', params={
        'docType': 'page',
        'sortby': 'docLexi:ASC',
    })
    if err == '':
        forest = processors.parent_child_list(pages.get('Data', []))

    new_list = []
    for node in forest:
        new_list = processors.flatten_list(
            node, level=0, new_list=new_list)

    page_list = []
    for page in new_list:
        d = {}
        d['docID'] = page['docID']
        d['title'] = page['title']
        d['docType'] = page['docType']
        page_list.append(d)

    main = {}
    # tech docs
    main['nav_docs'] = td_list
    # pages
    main['nav_pages'] = page_list
    print("### main", main, type(main))
    return main
