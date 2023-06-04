from pprint import pprint

from django.contrib import admin


admin.site.site_header = 'Ponto2 . Bordado industrial'
admin.site.site_title = 'Ponto2 . Bordado industrial'
admin.site.index_title = 'Central de controle'
admin.AdminSite.original_get_app_list = admin.AdminSite.get_app_list


def get_app_list(self, request, app_label=None):
    app_list = admin.AdminSite.original_get_app_list(
        self, request, app_label=app_label
    )
    # Sort the models by admin_order attribute or alphabetically
    # within each app.
    for app in app_list:
        app['models'].sort(
            key=lambda x: (
                x['model'].admin_order
                if hasattr(x['model'], 'admin_order')
                else x['name']
            )
        )
    return app_list


admin.AdminSite.get_app_list = get_app_list
