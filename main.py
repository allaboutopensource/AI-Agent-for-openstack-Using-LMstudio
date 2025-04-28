from openstack_quota import set_instance_quota,set_volume_quota,increase_vcpu_quota
from ai_agent import process_quota_request
import json 


def main():
    user_input = input("🗣 What would you like to do with OpenStack cloud? ")
    parsed = process_quota_request(user_input)
    print(f"Parsed JSON: {parsed}")
    if parsed:
        action = parsed.get("action")
        resource_type = parsed.get("resource_type")
        target_project = parsed.get("target_project")
        value = parsed.get("value")

        if action == "set_quota" and resource_type == "instances":
            set_instance_quota(target_project, value)
            print(f"Quota for {resource_type} in project {target_project} has been set to {value}.")
        elif action == "set_quota" and resource_type == "volumes":
            set_volume_quota(target_project, value)
            print(f"Quota for {resource_type} in project {target_project} has been set to {value}.")
        elif action == "set_quota" and resource_type == "vcpus":
            increase_vcpu_quota(target_project, value)
            print(f"VCPU quota for project {target_project} has been increased to {value}.")
        else:
            print("Invalid action or resource type of kind volumes")
        
if __name__ == "__main__":
    main()
