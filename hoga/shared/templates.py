import jinjax
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="hoga/templates")
templates.env.add_extension(jinjax.JinjaX)
catalog = jinjax.Catalog(jinja_env=templates.env)
catalog.add_folder("templates/components")