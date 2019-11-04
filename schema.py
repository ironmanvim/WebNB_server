from graphene import ObjectType, String, NonNull, Field, Schema
from helpers import execute, Client, clients, IDError
import threading
import uuid


class CloseKernel(ObjectType):
    id = String()
    output = String()

    def resolve_output(source, info):
        client_id = source.id
        try:
            clients[client_id].close_client()
            clients.pop(client_id)
            return "The Instance is Terminated Successfully"
        except KeyError:
            return "The Instance may already Terminated"


class GetKernel(ObjectType):
    id = String()

    def resolve_id(source, info):
        unique_id = str(uuid.uuid1())
        clients[unique_id] = Client([], unique_id)
        clients[unique_id].start()
        print(clients)
        return unique_id


class Result(ObjectType):
    output = String()
    error = String()


class Python(ObjectType):
    code = Field(String, default_value="")
    result = Field(Result)
    id = Field(String, required=True)

    def resolve_result(source, info):
        clients[source.id].push_code(source.code)
        result = clients[source.id].get_result()
        return result


class Execute(ObjectType):
    python = Field(Python, code=String(), required=True)
    id = Field(String)

    def resolve_python(source, info, code=""):
        if source.id in clients.keys():
            return Python(code=code, id=source.id)
        else:
            raise IDError(f"This ID({source.id}) may be Exhausted. Try to get a new Kernel Instance.")


class Query(ObjectType):
    execute = Field(Execute, id=String(required=True), required=True)
    get_kernel_instance = Field(GetKernel)
    close_kernel_instance = Field(CloseKernel, id=String(required=True))

    def resolve_execute(source, info, id):
        return Execute(id=id)

    def resolve_get_kernel_instance(source, info):
        return GetKernel()

    def resolve_close_kernel_instance(source, info, id):
        return CloseKernel(id=id)


schema = Schema(query=Query)
