# flask sql alchemy requires the first part of the db url to be
# postgresql:// but the url provided by heroku is postgres://
# so I add the 'ql' as a fix
def fix_db_url(db_url):
    return db_url[0 : db_url.find(":")] + "ql" + db_url[db_url.find(":") :]
