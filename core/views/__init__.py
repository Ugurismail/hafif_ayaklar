"""Lightweight package marker for core views.

Avoid importing view modules eagerly here; URLConfs should import the
specific submodules they need so startup cost stays bounded.
"""

