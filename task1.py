# Write a simple http server that on GET request to / writes json list of the following structure to body:
#
# [
#     {
#         "name": "some_vm_name",	# name, not id
#         "interfaces": [
#             "48:7c:07:4f:de:5d",
#             "bb:2b:c0:38:e4:7d",
#             ... all macs of this vm interfaces.
#         ]
#     },
#     ... all vms
# ]
#
# Try to minimize both time and memory required for the response construction.


from http import server
import json


def DB():

    """
    Data base imitator
    """

    # id is unique
    vms = [
        {
            "name": "vm1",
            "id": "asdkljasdlasjd"
        },
        {
            "name": "vm2",
            "id": "dasljdljsadlaj"
        },
        {
            "name": "vm3",
            "id": "wqeoiqwueiowu"
        },
        {
            "name": "vm4",
            "id": "zxcmnzxmcnxzc"
        },
        {
            "name": "vm2",
            "id": "wklkljlasdks"
        }
    ]
    interfaces = [
        {
            "vm_id": "wklkljlasdks",
            "mac": "8d:5a:c0:dc:ed:28"
        },
        {
            "vm_id": "ldewskdsalsad",
            "mac": "90:2b:c7:46:a7:e5"
        },
        {
            "vm_id": "asdkljasdlasjd",
            "mac": "9c:1d:bc:97:0d:70"
        },
        {
            "vm_id": "dasljdljsadlaj",
            "mac": "04:8e:9b:9f:3f:01"
        },
        {
            "vm_id": "zxcmnzxmcnxzc",
            "mac": "8d:5a:c0:dc:ed:28"
        },
        {
            "vm_id": "dasljdljsadlaj",
            "mac": "08:6a:2b:e6:6d:67"
        },
        {
            "vm_id": "dasljdljsadlaj",
            "mac": "d0:23:14:b8:c6:52"
        }
    ]

    # собираем ответ
    mapped_data = {}

    # создаем перечень всех vms
    for iv in vms:

        vms_name = iv["name"]
        vms_id = iv["id"]

        if not mapped_data.get(vms_id):
            mapped_data[vms_id] = {
                "name": vms_name,
                "interfaces": []
            }

    for ii in interfaces:

        if not mapped_data.get(ii["vm_id"]):
            mapped_data[ii["vm_id"]] = {
                "name": "_no_vms_name",
                "interfaces": [ii["mac"]]
            }
        else:
            mapped_data[ii["vm_id"]]["interfaces"].append(ii["mac"])

    return list(mapped_data.values())


class HTTPProc(server.SimpleHTTPRequestHandler):

    def do_GET(self):

        if self.path == '/':

            print()
            print(self.client_address)
            print(self.path)

            self.send_response(200)
            self.send_header('Content-Type', 'application\json')
            self.end_headers()
            self.wfile.write(json.dumps(DB()).encode())

        # elif self.path == '/q':
        #
        #     print()
        #     print(self.client_address)
        #     print(self.path)
        #
        #     self.send_response(201)
        #     self.send_header('content-typeqqqqqqqqqq', 'text\html')
        #     self.end_headers()


class HTTPServ:

    def __init__(self, HOST, PORT):

        self.handler = HTTPProc

        self.serv = server.HTTPServer(
            (HOST, PORT),
            self.handler
        )


    def run(self):

        self.serv.serve_forever()
        print('Server run...')


if __name__ == '__main__':
    serv = HTTPServ('localhost', 33221)
    serv.run()
