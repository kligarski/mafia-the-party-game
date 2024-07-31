from django.conf import settings

def reactjs_assets_paths(request):
    staticfiles_base = settings.STATICFILES_BASE
    build_files = settings.REACT_JS_BUILD_DIR / "assets"
    
    return {
        "reactjs_assets_js_paths":[str(x.relative_to(staticfiles_base)) for x in build_files.glob("*.js")],
        "reactjs_assets_css_paths":[str(x.relative_to(staticfiles_base)) for x in build_files.glob("*.css")],
    }
