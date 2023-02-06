from django.apps import apps
import importlib


def get_url_names():
    """
    It imports all the urls from all the apps in the project and returns a list of dictionaries with the
    url name and route
    :return: A list of dictionaries.
    """

    list_of_url_names = list()
    list_of_all_urls = list()
    for name, app in apps.app_configs.items():
        mod_to_import = f"{name}.urls"
        try:
            urls = getattr(importlib.import_module(mod_to_import), "urlpatterns")
            # urls = importlib.import_module(mod_to_import)
            # pprint(urls)
            list_of_all_urls.extend(urls)
        except ImportError as ex:
            # is an app without urls
            pass
    for url in list_of_all_urls:
        list_of_url_names.append(
            {
                "name": url.name,
                "route": url.pattern._route,
            }
        )

    return list_of_url_names