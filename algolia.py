"""
Algolia Search Plugin for Pelican
=================================

This plugin uploads an Algolia search index
"""

# http://docs.getpelican.com/en/3.7.1/plugins.html
from pelican import signals
from algoliasearch import algoliasearch

import hashlib


def create_article_index(generator):
    algolia_index_name = generator.settings.get('ALGOLIA_INDEX_NAME')
    print("Generating Algolia index '%s' for %d articles..." % (algolia_index_name, len(generator.articles)))
    algolia_app_id = generator.settings.get('ALGOLIA_APP_ID')
    algolia_admin_api_key = generator.settings.get('ALGOLIA_ADMIN_API_KEY')

    client = algoliasearch.Client(algolia_app_id, algolia_admin_api_key)
    index = client.init_index(algolia_index_name)

    for article in generator.articles:
        print("Indexing article: '%s'" % article.title)
        data = {'title': article.title, 'slug': article.slug, 'url': article.url, 'tags': [],
                'content': article.content, 'category': article.category}
        for tag in getattr(article, 'tags', []):
            data['tags'].append(tag.name)

        object_id = hashlib.sha256(str(article.slug).encode('utf-8')).hexdigest()
        index.add_object(data, object_id)
        print("Added Algolia object...%s" % object_id)

    print("Articles have been indexed.")


def create_page_index(generator):
    algolia_index_name = generator.settings.get('ALGOLIA_INDEX_NAME')
    print("Generating Algolia index '%s' for %d pages..." % (algolia_index_name, len(generator.pages)))

    algolia_app_id = generator.settings.get('ALGOLIA_APP_ID')
    algolia_admin_api_key = generator.settings.get('ALGOLIA_ADMIN_API_KEY')

    client = algoliasearch.Client(algolia_app_id, algolia_admin_api_key)
    index = client.init_index(algolia_index_name)

    for page in generator.pages:
        print("Indexing page: '%s'" % page.title)
        data = {'title': page.title, 'slug': page.slug, 'url': page.url, 'tags': [], 'content': page.content,
                'category': page.category}
        for tag in getattr(page, 'tags', []):
            data['tags'].append(tag.name)

        object_id = hashlib.sha256(str(page.slug).encode('utf-8')).hexdigest()
        index.add_object(data, object_id)
        print("Added Algolia object...%s" % object_id)

    print("Pages have been indexed.")


def register():
    signals.article_generator_finalized.connect(create_article_index)
    signals.page_generator_finalized.connect(create_page_index)
