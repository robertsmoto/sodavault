from docsapp.models import Doc
from django.conf import settings


def breadcrumb_processor(self, doc_slug='missing', context=None, *args, **kwargs):

    # PLEASE READ
    ######################
    ######################
    # This is as complicated as you make it
    # Add doc_slug into the url conf
    # A record in the docs app will be crated
    # Modify the record in the docs app to your liking
    # Add breadcrumb records to the docapp.objects
    # variable order does matter so be careful with input
    # it is helpful to name the doc_slug the same as the url namespace
    ######################
    ######################

#     if settings.SITE_ID == 1:
        # url = "https://www.swim.express"
    # elif settings.SITE_ID == 2:
        # url = "https://www.blogfromprague.com"
    # elif settings.SITE_ID == 3:
        # url = "https://www.media.goodbyechlorine.com"
    # else:
#         url = "https://SOMETHINGELSE"

    url = "https://sodavault.com"

    if doc_slug != 'missing':
        doc = Doc.objects.get_or_create(
            slug=doc_slug
        )
        doc_q = doc[0]
        doc_t = doc[1]
        # print('doc_q :: ', doc_q, type(doc_q))
        # print('doc_t :: ', doc_t)

        breadcrumbs = []

        if doc_t is False and doc_q.breadcrumbs.exists():
            position = 1
            for breadcrumb in doc_q.breadcrumbs.all():
                breadcrumbs_dict = {}
                breadcrumbs_dict['url'] = url
                breadcrumbs_dict['position'] = position

                if breadcrumb.name == 'post_list':
                    breadcrumbs_dict['name'] = self.kwargs['post_type'] + ' ' + 'list'
                    # print('************ self.kwargs post_type :: ', self.kwargs['post_type'])
                elif breadcrumb.name == 'topic_name':
                    breadcrumbs_dict['name'] = self.kwargs['topic_name']
                elif breadcrumb.name == 'interest_name':
                    breadcrumbs_dict['name'] = self.kwargs['interest_name']
                elif breadcrumb.name == 'h1':
                    breadcrumbs_dict['name'] = context['metadata']['h1']
                elif breadcrumb.name == 'archive_year':
                    breadcrumbs_dict['name'] = 'year: ' + str(self.kwargs['year'])
                elif breadcrumb.name == 'archive_month':
                    breadcrumbs_dict['name'] = 'month: ' + str(self.kwargs['month'])
                elif breadcrumb.name == 'archive_day':
                    breadcrumbs_dict['name'] = 'day: ' + str(self.kwargs['day'])
                else:
                    breadcrumbs_dict['name'] = breadcrumb.name

                breadcrumbs_dict['namespace'] = breadcrumb.url_namespace
                # useful addions for use in template
                # # post_type used to differentiate post types in breadcrumbs
                # if 'post_type' in self.kwargs:
                #     breadcrumbs_dict['post_type'] = self.kwargs['post_type']

                # handle varible cases
                if breadcrumb.url_variables:
                    # make list from breadcrum.url_variables
                    url_variables_list = [
                        x.strip()
                        for x in breadcrumb.url_variables.split("|")
                    ]
                    # iterate and put them in dict
                    variable_counter = 1
                    for var in url_variables_list:
                        var_key = "var" + str(variable_counter)
                        var_value = self.kwargs[var]
                        breadcrumbs_dict[var_key] = var_value
                        variable_counter += 1

                breadcrumbs.append(breadcrumbs_dict)
                position += 1
        else:
            breadcrumbs = [{'name': '## new slug added to doc, please add data ##'}]

    else:
        breadcrumbs = [{'name': 'url extra context missing'}]
    return breadcrumbs
