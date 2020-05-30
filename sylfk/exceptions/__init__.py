class SYLFkException(object):
	"""docstring for SYLFk"""
	def __init__(self, code='',message='Error'):
		self.code=code
		self.message = message
	def __str__(self):
		return self.message

class EndpiontExistsError(SYLFkException):
	"""docstring for EndpiontExistsError"""
	def __init__(self, message='Endpoint exists'):
		super(EndpiontExistsError,self).__init__(message)

class URLExistsError(SYLFkException):
	"""docstring for URLExistsError
"""
	def __init__(self, message='URL exists'):
		super(URLExistsError, self).__init__(message)
		
		
		