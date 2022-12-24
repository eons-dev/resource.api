import logging
import apie
import eons

class resource(apie.Endpoint):
	def __init__(this, name="API Endpoint for any Resource"):
		super().__init__(name)

		this.staticKWArgs.append('operations')

		# Everything that can change a resource's implementation should be specified somewhere in apie, not in the request.
		# By prepending this.name, we can have multiple resources which use very similar args (e.g. external url).
		this.fetchFrom = [
			'this',
			'args',
			'precursor_name_prepended',
			'executor_name_prepended',
			'environment_name_prepended',
			'precursor',
			'executor',
			'environment',
		]


	# Required Endpoint method. See that class for details.
	def GetHelpText(this):
		return '''\
Resources represent data structures which can be manipulated. The means of manipulating such data are called "operations".
Each resource must specify a map of operations and their associated implementations. For example, a CRUD resource might have:
operations = {
	'create': 'create_implementation_database',
	'read': 'read_implementation_database',
	'update': 'update_implementation_database',
	'delete': 'create_implementation_database'
}
Each implementation is injected into the apie list of Endpoints to process directly after *this and before the specified operation.
Only the specified operations will be allowed.
'''


	def ValidateStaticArgs(this):
		if (this.staticArgsValid):
			return
		
		super().ValidateStaticArgs()
		
		this.allowedNext = this.operations.keys()


	# Override CallNext to process the implementation before the associated operation
	def CallNext(this):
		if (not this.next):
			return None

		if (this.GetExecutor() is None):
			raise eons.InvalidNext(f"{this.name} has no executor and cannot execute next ({this.next}).")

		toCall = this.operations[this.next[0]].split('/')
		for i, endpoint in enumerate(toCall):
			if (i == len(toCall)-1):
				break
			cachedEndpoint = None
			if (endpoint not in this.GetExecutor().cachedFunctors):
				cachedEndpoint = this.GetExecutor().GetRegistered(endpoint, "api")
				this.GetExecutor().cachedFunctors[endpoint] = cachedEndpoint
			else:
				cachedEndpoint = this.GetExecutor().cachedFunctors[endpoint]
			if (cachedEndpoint is None):
				raise apie.APIError(f"Could not get {endpoint} while processing request for {this.name}/{this.next[0]}")
			cachedEndpoint.allowedNext.append(toCall[i+1])

		this.next = toCall + this.next

		next = this.next.pop(0)
		if (not this.ValidateNext(next)):
			raise eons.InvalidNext(f"Failed to validate {next}")

		return this.GetExecutor().ProcessEndpoint(next, this.request, precursor=this, next=this.next)


	# Enable Fetching values prepended with the name of *this.
	# This makes it possible to specify "first_name_arg" and "second_name_arg" independently (as opposed to both being just "arg")
	def fetch_location_precursor_name_prepended(this, varName, default, fetchFrom, attempted):
		return this.fetch_location_precursor(f"{this.name}_{varName}", default, fetchFrom, attempted)

	# Enable Fetching values prepended with the name of *this.
	# This makes it possible to specify "first_name_arg" and "second_name_arg" independently (as opposed to both being just "arg")
	def fetch_location_executor_name_prepended(this, varName, default, fetchFrom, attempted):
		return this.fetch_location_executor(f"{this.name}_{varName}", default, fetchFrom, attempted)

	# Enable Fetching values prepended with the name of *this.
	# This makes it possible to specify "first_name_arg" and "second_name_arg" independently (as opposed to both being just "arg")
	def fetch_location_environment_name_prepended(this, varName, default, fetchFrom, attempted):
		return this.fetch_location_environment(f"{this.name}_{varName}", default, fetchFrom, attempted)

