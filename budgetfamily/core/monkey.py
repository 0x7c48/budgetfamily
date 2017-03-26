from flask.ext.admin.contrib.sqla import tools

tools.parse_like_term = lambda x: x
