import logging
import apie

class resource(apie.Endpoint):
    def __init__(this, name="API Endpoint for any Resource"):
        super().__init__(name)

        this.staticKWArgs.append('operations')
        

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
        return this.executor.ProcessEndpoint(this.operations[this.next[0]], this.request, predecessor=this, next=this.next)