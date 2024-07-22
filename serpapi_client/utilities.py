# -*- coding: utf-8 -*-

# typing
from typing import Dict, List

'''
Build search query

'''
def advanced_search_options(args: Dict) -> str:
    '''
    Builds advanced search options based on the provided arguments.

    :param args: Dictionary containing the command line arguments and options.
    :return: A formatted query string with advanced search options.
    '''
    before = args.get('before', '')
    after = args.get('after', '')

    advanced_search = {
        'before': before,
        'after': after
    }

    response = [
        f'{k}:{v}' for k, v in advanced_search.items() if v
    ]

    return ' '.join(response)
        
def search_query(args: Dict) -> str:
    '''
    Builds the search query string based on the command line arguments.

    :param args: Dictionary containing the command line arguments and options.
    :return: A formatted query string.
    '''
    q = args.get('q', '')
    advanced_search = advanced_search_options(args)

    return f'{q} {advanced_search}'.strip()


'''
Select SerpAPI parameters

'''
def select_serpapi_parameters(args: Dict) -> Dict:
    '''
    Filters the command line arguments to include only the default SerpAPI
    parameters.

    :param args: Dictionary containing the command line arguments and options.
    :return: A dictionary containing only the relevant SerpAPI parameters.
    '''
    default_serpapi_parameters = [
        'q',
        'google_domain',
        'gl',
        'hl',
        'cr',
        'lr'
    ]

    # filter and return only the relevant SerpAPI parameters
    params = {
        k: v for k, v in args.items() if k in default_serpapi_parameters and v 
    }

    # add new parameters
    params['engine'] = 'google'
    params['start'] = 0
    params['num'] = 100

    return params

'''
Extract relevant keys from SerpAPI response

'''
def extract_results_keys(data: List[Dict], result_type: str) -> List[Dict]:
    '''
    Filters the SerpAPI response data to include only entries with 'link'
    containing 'video', and returns a list of dictionaries with specified
    default keys.

    :param data: List of dictionaries containing the SerpAPI response data.
    :param result_type: Type of SerpAPI response: 'search_result' or
        'image_result'
    :return: A list of dictionaries, each containing the specified default
        keys from the SerpAPI response.
    '''
    key_mapping = {
        'search_result': [
            'source',
            'title',
            'snippet',
            'link',
            'thumbnail',
            'video_link',
            'snippet_highlighted_words',
            'displayed_link'
        ],
        'image_result': [
            'source',
            'thumbnail',
            'title',
            'link',
            'serpapi_related_content_link'
        ]
    }

    selected_keys = key_mapping.get(result_type, [])

    # filter data to include only entries with 'link' containing 'video'
    d = [i for i in data if 'link' in i and 'video' in i['link']]

    # return list of dictionaries with specified default keys
    return [
        {
            k: i[k] for k in selected_keys if k in i
        } for i in d
    ]

'''
Extract relevant keys from related content
'''
def extract_related_content_keys(data: List[Dict]) -> List[Dict]:
    '''
    Filters related content data and returns a list of dictionaries with
    specified default keys.

    :param data: List of dictionaries containing related content data.
    :return: A list of dictionaries, each containing the specified default
        keys for the related content.
    '''
    key_mapping = [
        'source',
        'link',
        'thumbnail',
        'title'
    ]

    # return list of dictionaries with specified default keys
    return [
        {
            k: i[k] for k in key_mapping if k in i
        } for i in data
    ]
