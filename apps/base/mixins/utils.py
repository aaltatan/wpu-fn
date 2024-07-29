class HelperMixin:
    
    def get_model_class(self):
        
        if hasattr(self, 'model'):
            return self.model
        
        if not hasattr(self, 'form_class'):
            raise Exception('you need to set form_class')
        
        model_class = self.form_class._meta.model
        return model_class
    
    def get_app_name(self):
        
        model_class = self.get_model_class()
        app_name: str = model_class._meta.app_label
        
        return app_name
    
    def get_success_path(self):
        
        if hasattr(self, 'success_path'):
            return self.success_path
        
        app_name = self.get_app_name()
        return f'{app_name}:index'
    
    def get_hx_location_path(self):
        
        if hasattr(self, 'hx_location_path'):
            return self.hx_location_path
        
        app_name = self.get_app_name()
        return f'{app_name}:index'
    
    def get_hx_location_target(self):
        
        if hasattr(self, 'hx_location_target'):
            return self.hx_location_target
        
        app_name = self.get_app_name()
        return f'#{app_name}-table'
    
    def get_index_template_name(self):
        
        if hasattr(self, 'index_template_name'):
            return self.index_template_name
        
        app_name = self.get_app_name()
        
        return f'apps/{app_name}/index.html'