from enum import Enum


class Version(Enum):
    V2023_01 = 1
    MORE1 = 2
    MORE2 = 3
    MORE3 = 4


CURRENT_VERSION = Version.V2023_01

GENALPHA = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

# for select controls that use tags input by users
SELECT2_TAG_INDEX = {
    'article': [
        'articleCategory',
        'articleTag',
        'articleKeyword',
        'recipeCookingMethod',
        'recipeCuisine',
        'recipeCategory',
        'recipeSuitableForDiet',
    ],
}

DEFAULT_COLLECTIONS = [
    'articleCategory',
    'articleTag',
    'articleKeyword',
    'author',
    'pageCategory',
    'pageTag',
    'pageKeyword',
    'recipeCookingMethod',
    'recipeCategory',
    'recipeCuisine',
    'recipeSuitableForDiet',
    'techdocCategory',
    'techdocTag',
    'techdocKeyword',
    'website',
]
