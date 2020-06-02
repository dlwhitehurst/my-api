from src.models.init import initialize

##
# API Routes
##
def api(http, api):
  
	# Response
  def response(version, name, para={}):
    
    crud = api[version]
    auth = http.authenticate(lambda arg : crud.db.read(crud.db.config['schema']['parent'], arg))

    if version in api:
      output, code = getattr(crud, name)(http.request, para)

      if auth and 'id' in auth:
        result = output(auth)

        if 'error' in result:
          return http.response(result['error'], result['code'])
        else:
          return http.response(result, code)
      else:
        return http.response(auth)
    else:
      return http.response({'error': 'Invalid API Version'}, 400)

  @http.flask.route('/api/<string:version>/init', methods=['GET'])
  def init(version):
    return initialize(http, api[version].db)

	# Add Person
  @http.flask.route('/api/<string:version>/persons', methods=['POST'])
  def addUser(version):
    return response(version, 'addUser')

	# Get Persons
  @http.flask.route('/api/<string:version>/users', methods=['GET'])
  def getUsers(version):
    return response(version, 'getUsers')

	# Get Person
  @http.flask.route('/api/<string:version>/users/<string:id>', methods=['GET'])
  def getUser(version, id):
    return response(version, 'getUser', {'id': id})

	# Update Person
  @http.flask.route('/api/<string:version>/users/<string:id>', methods=['PUT'])
  def updateUser(version, id):
    return response(version, 'updateUser', {'id': id})

	# Delete Person
  @http.flask.route('/api/<string:version>/users/<string:id>', methods=['DELETE'])
  def deleteUser(version, id):
    return response(version, 'deleteUser', {'id': id})

	# Get addresses
  @http.flask.route('/api/<string:version>/users/<string:id>/addresses', methods=['GET'])
  def getAddresses(version, id):
    return response(version, 'getAddresses', {'id': id})

	# Get address
  @http.flask.route('/api/<string:version>/users/<string:id>/addresses/<string:key>', methods=['GET'])
  def getAddress(version, id, key):
    return response(version, 'getAddress', {'id': id, 'key': key})

	# Add address
  @http.flask.route('/api/<string:version>/users/<string:id>/addresses', methods=['POST'])
  def addAddress(version, id):
    return response(version, 'addAddress', {'id': id})

	# Update address
  @http.flask.route('/api/<string:version>/users/<string:id>/addresses/<string:key>', methods=['PUT'])
  def updateAddress(version, id, key):
    return response(version, 'updateAddress', {'id': id, 'key': key})

	# Delete address
  @http.flask.route('/api/<string:version>/users/<string:id>/addresses/<string:key>', methods=['DELETE'])
  def deleteAddress(version, id, key):
    return response(version, 'deleteAddress', {'id': id, 'key': key})
