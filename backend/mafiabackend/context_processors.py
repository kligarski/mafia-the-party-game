from django.conf import settings

def frontend_assets_paths(request):
    staticfiles_base = settings.STATICFILES_BASE
    build_files = settings.FRONTEND_BUILD_DIR / "assets"
    
    return {
        "frontend_assets_js_paths":[str(x.relative_to(staticfiles_base)) for x in build_files.glob("*.js")],
        "frontend_assets_css_paths":[str(x.relative_to(staticfiles_base)) for x in build_files.glob("*.css")],
    }
