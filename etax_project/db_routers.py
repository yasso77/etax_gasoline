class ERPDBRouter:
    def db_for_read(self, model, **hints):
        if getattr(model._meta, 'app_label', None) == 'erp':
            return 'erp'
        return 'default'

    def db_for_write(self, model, **hints):
        if getattr(model._meta, 'app_label', None) == 'erp':
            return 'erp'
        return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'erp':
            return False  # ERP data is read-only
        return db == 'default'
