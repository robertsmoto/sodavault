from enum import Enum


class Version(Enum):
    V2023_01 = 1
    MORE1 = 2
    MORE2 = 3
    MORE3 = 4


CURRENT_VERSION = Version.V2023_01

ARTICLE = 'article'
ARTICLEAUTHOR = 'article_author'
ARTICLECATEGORY = 'article_category'
ARTICLEKEYWORD = 'article_keyword'
ARTICLETAG = 'article_tag'
ARTICLEWEBSITE = 'article_website'
AUTHOR = 'author'
COMPONENT = 'component'
CUSTOMER = 'customer'
DETAIL = 'detail'
DOCUMENT = 'document'
DOCUMENTAUTHOR = 'document_author'
DOCUMENTCATEGORY = 'document_category'
DOCUMENTKEYWORD = 'document_keyword'
DOCUMENTTAG = 'document_tag'
IMAGE = 'image'
JOURNAL = 'journal'
JOURNALCATEGORY = 'journal_category'
JOURNALKEYWORD = 'journal_keyword'
JOURNALTAG = 'journal_tag'
LOCATION = 'location'
ORDER = 'order'
PAGE = 'page'
PAGEAUTHOR = 'page_author'
PAGECATEGORY = 'page_category'
PAGEKEYWORD = 'page_keyword'
PAGETAG = 'page_tag'
PART = 'part'
PERSON = 'person'
PRODUCT = 'product'
PRODUCTBRAND = 'product_brand'
PRODUCTCATEGORY = 'product_category'
PRODUCTDEPARTMENT = 'product_department'
PRODUCTKEYWORD = 'product_keyword'
PRODUCTTAG = 'product_tag'
