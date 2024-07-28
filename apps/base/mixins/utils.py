class RaiseExceptions:
    
    def raise_exceptions_if_necessary(self):
        for attr in self.attrs:
            if getattr(self, attr) is None:
                raise Exception(f'you need to set {attr}')

class RaiseAddExceptions(RaiseExceptions):
    
    attrs: list[str] = [
        'form_class',
        'template_name',
        'base_template_name',
        'add_form_template',
        'success_path',
    ]

class RaiseBulkDeleteExceptions(RaiseExceptions):
    
    attrs: list[str] = [
        'model',
        'hx_location_path',
        'hx_location_target',
    ]

class RaiseDeleteExceptions(RaiseExceptions):
        
    attrs: list[str] = [
        'class_name',
        'model',
        'template_name',
        'hx_location_path',
        'hx_location_target',
    ]

class RaiseListExceptions(RaiseExceptions):
    
    def raise_exceptions_if_necessary(self):
        
        print('dasdasdsadasdasdasdsad')
        
        if getattr(self.model, 'get_update_path') is None:
            raise Exception(
                f'you need to set get_update_path property in {self.model._meta.__class__}'
            )
        
        if getattr(self.model, 'get_delete_path') is None:
            raise Exception(
                f'you need to set get_delete_path property in {self.model._meta.__class__}'
            )
        return super().raise_exceptions_if_necessary()
    
    attrs: list[str] = [
        'model',
        'filter_class',
        'select_filter_class',
        'template_name',
        'index_template_name',
        'pagination_form',
        'pagination_form_attributes',
    ]

class RaiseUpdateExceptions(RaiseExceptions):
    
    attrs: list[str] = [
        'model',
        'form_class',
        'template_name',
        'base_template_name',
        'update_form_template',
        'success_path',
    ]
