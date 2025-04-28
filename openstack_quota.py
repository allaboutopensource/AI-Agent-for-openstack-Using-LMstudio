import openstack
import os
from dotenv import load_dotenv

load_dotenv()


def project_exists(target_project):
    conn = openstack.connect(cloud='openstack')
    conn2 = conn.connect_as(username = os.environ.get('OS_USERNAME'), password = os.environ.get('OS_PASSWORD'))
    global cloud2
    cloud2 = conn.connect_as_project('7b9b3c86a8ab4a6e9a1cdc8bb07ae190')
    global project
    project = cloud2.identity.find_project(target_project)
    if not project:
        print(f"Project '{target_project}' not found.")
        return
    else:
        print(f"Project '{target_project}' found.")
        return project.name, project.id 


def set_instance_quota(target_project , value):
    result = project_exists(target_project)
    if result is None:
        return
    print(f"Setting instance quota for project '{project.name}' to {value}")
    cloud2.set_compute_quotas(project.id, instances=int(value))



def set_volume_quota(target_project, value):
    result = project_exists(target_project)
    if result is None:
        return
    print(f"Setting volume quota for project '{project.name}' to {value}")
    cloud2.set_volume_quotas(project.id, volumes=int(value))



def increase_vcpu_quota(target_project, value):
    result = project_exists(target_project)
    if result is None:
        return
    print(f"Setting VCPU quota for project '{project.name}' to {value}")
    cloud2.set_compute_quotas(project.id, cores=int(value))
