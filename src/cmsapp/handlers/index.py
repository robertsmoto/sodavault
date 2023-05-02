from .partial import CollectionPostHandler
from .document import GenericPostHandler
from .file import PostFileHandler
from .image import PostImageHandler, DeleteImageHandler
from .ingredient import PostIngredientsHandler
from .select2 import Select2ErrorHandler


DELETE_HANDLERS_INDEX = {
    'image': DeleteImageHandler,
}

POST_HANDLERS_INDEX = {
    'document': GenericPostHandler,
    'collections': GenericPostHandler,
    'article': GenericPostHandler,
    'article_collection': GenericPostHandler,
    'author': GenericPostHandler,
    'author_collection': GenericPostHandler,
    'file': PostFileHandler,
    'file_collection': CollectionPostHandler,
    'image': PostImageHandler,
    'image_collection': CollectionPostHandler,
    'ingredient_collection': PostIngredientsHandler,
    'recipe': GenericPostHandler,
    'recipe_collection': GenericPostHandler,
    'nutrition': GenericPostHandler,
    'website': GenericPostHandler,
    'website_collection': GenericPostHandler,
}

ERROR_HANDLERS_INDEX = {
    'document': Select2ErrorHandler,
    'collections': Select2ErrorHandler,
}
