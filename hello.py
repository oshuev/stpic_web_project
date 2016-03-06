
def wsgi_application(environ, start_response):
	status = '200 OK'
	headers = [
		('Content-Type', 'text/plain')
	]

	body = environ['QUERY_STRING'].replace('&', '\r\n')

 	start_response(status, headers)
	return [body]