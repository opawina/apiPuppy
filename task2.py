# Write a simple http api that implements following operations on in-memory db/collections:
#
# GET /vms
# [
#     {
#         "name": "vm1",     # NAME, not id of vm.
#         "volumes": [
#             1322,
#             ... all volumes CURRENTLY mounted to this vm
#         ]
#     },
#     ... all vms
# ]
#
# GET /volumes
# [
#     {
#         "id": 1322,
#         "vm_id": "asdkljasdlasjd"     # id of VM the volume is mounted to, or null
#         "past_mounts": [
#             "dslfjdffdsf",
#             ... set of all ids of vms excluding vm_id this volume was ever mounted to
#         ]
#     },
#     ... all volumes
# ]
#
# POST /unmount/<volume_id>
#
# Unmounts volume from vm, while marking the mount record as deleted or saving it elsewhere.
# 400 error if not mounted.
#
# POST /mount/<volume_id>/<vm_id>
#
# Mount volume to vm. 400 error if already mounted.
#
# Don't waste much time on http part, use in-built/stanrard library python data structures.
# Focus on state consistency.


from http import server
import json


class DB:

    """
    Data base imitator
    """

    def __init__(self):

        # id is unique
        self.vms = [
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
        # преобразуем для быстрого поиска по id
        self.vms_dict_id = {v["id"]: v for v in self.vms}

        # volume binding is many-to-many mapping, volume can be mounted to only one or zero vms.
        self.volume_mounts = [
            {
                "vm_id": "dasljdljsadlaj",
                "volume_id": 1489,
                "deleted": False
            },
            {
                "vm_id": "wklkljlasdks",
                "volume_id": 1548,
                "deleted": True
            },
            {
                "vm_id": "asdkljasdlasjd",
                "volume_id": 1548,
                "deleted": False
            }
        ]
        # преобразуем для быстрого поиска по id
        # self.volume_mounts_composite_id = {str(vm["volume_id"]) + "-" + vm["vm_id"]: vm for vm in self.volume_mounts}

        self.volumes = [
            {
                "id": 1233,
                "size": 12
            },
            {
                "id": 1487,
                "size": 100
            },
            {
                "id": 1489,
                "size": 228
            },
            {
                "id": 1337,
                "size": 42
            },
            {
                "id": 1548,
                "size": 200
            }
        ]
        # преобразуем для быстрого поиска по id
        self.volumes_dict_id = {v["id"]: v for v in self.volumes}


    def response(self, path):

        path = path.split('/')

        if path[1] == "vms":
            return self.get_vms()
        elif path[1] == "volumes":
            return self.get_volumes()
        elif path[1] == "unmount":
            return self.unmount(path)
        elif path[1] == "mount":
            return self.mount(path)


    def get_vms(self):

        data = []

        for vm in self.vms:

            data.append({
                "name": vm["name"],
                "volumes": [i["volume_id"] for i in self.volume_mounts if i["vm_id"] == vm["id"] and i["deleted"] is False]
            })

        return data


    def get_volumes(self):

        data = {}

        for iv in self.volumes:

            data[iv["id"]] = {
                "id": iv["id"],
                "vm_id": None,
                "past_mounts": []
            }

        for ivm in self.volume_mounts:

            if ivm["deleted"]:
                data[ivm["volume_id"]]["past_mounts"].append(ivm["vm_id"])
            else:
                data[ivm["volume_id"]]["vm_id"] = ivm["vm_id"]

        return list(data.values())


    def unmount(self, path):

        volume_id = int(path[2])

        # check if exists
        if not self.volumes_dict_id.get(volume_id):
            return 400, 'Resource not exists'

        for i, vm in enumerate(self.volume_mounts):

            if vm["volume_id"] == volume_id and vm["deleted"] is False:
                self.volume_mounts[i]["deleted"] = True
                return 200, "Unmount"
            else:
                return 400, "Not mount"


    def mount(self, path):

        volume_id, vm_id = int(path[2]), path[3]

        # check if exists
        if not self.volumes_dict_id.get(volume_id) or not self.vms_dict_id.get(vm_id):
            return 400, "Resource not exists"

        for i, vm in enumerate(self.volume_mounts):

            # check if already mount
            if vm["volume_id"] == volume_id and vm["deleted"] is False:
                if vm["deleted"] is False:
                    return 400, "Volume already busy"
                if vm["deleted"] is True:
                    self.volume_mounts[i]["deleted"] = True
                    return 200, "Past mount"

        # если такой связи не было добавляем
        self.volume_mounts.append({
            "vm_id": vm_id,
            "volume_id": volume_id,
            "deleted": False
        })
        return 200, "New mount"


if __name__ == "__main__":

    db = DB()
    print(json.dumps(db.response("/volumes"), indent=2))
    # print(json.dumps(db.response("/vms"), indent=2))

    print(json.dumps(db.response("/mount/1489/zxcmnzxmcnxzc"), indent=2))   # already busy
    print(json.dumps(db.response("/mount/1548/wklkljlasdks"), indent=2))   # past mount
    print(json.dumps(db.response("/mount/1337/wklkljlasdks"), indent=2))   # alredy busy
    print(json.dumps(db.response("/mount/1337/dasljdljsadlaj"), indent=2))   # alredy busy
    print(json.dumps(db.response("/mount/1487/dasljdljsadlaj"), indent=2))   # alredy busy

    print(json.dumps(db.response("/volumes"), indent=2))
    print(json.dumps(db.response("/vms"), indent=2))

    print(json.dumps(db.response("/unmount/1489"), indent=2))
    print(json.dumps(db.response("/unmount/1548"), indent=2))
    print(json.dumps(db.response("/unmount/2222"), indent=2))

    print(json.dumps(db.response("/volumes"), indent=2))
    print(json.dumps(db.response("/vms"), indent=2))



