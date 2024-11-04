# /////////////////////////////////////////////////////////////
# 
# 
# Rotina para alterar NEXT HOP da rotas da VPC quando o IP primário do NLB mudar.
# 
# 
# /////////////////////////////////////////////////////////////

from ibm_vpc import VpcV1 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator 
from os import environ

# apikey = environ.get('IBMCLOUD_API_KEY')

apikey = <APIKEY>

authenticator = IAMAuthenticator(apikey)
service = VpcV1(authenticator=authenticator)
service.set_service_url('https://br-sao.iaas.cloud.ibm.com/v1')

# variáveis de entrada
lb_id = "r042-7c84dec4-074d-4e3f-b349-1cfa621bf142"
vpc_id="r042-6b497e29-403d-4e01-a4c0-889f229d2cef"
routing_table_id="r042-b2787c7a-4d4c-4884-ade3-a16dcfa37fd2"

# pega IPs primário e secundário do NLB
def getNLBIps():
    prymary_ip = service.get_load_balancer(lb_id).get_result()["private_ips"][0]["address"]
    secondery_ip = service.get_load_balancer(lb_id).get_result()["private_ips"][1]["address"]
    return prymary_ip, secondery_ip

# faz uma lista com os IDs das rotas
def routesIdList():
    routes_lenght = len(service.get_vpc_routing_table(vpc_id=vpc_id, id=routing_table_id).get_result()["routes"])
    id_routes_list = []
    for i in range(routes_lenght):
        route_id = service.get_vpc_routing_table(vpc_id=vpc_id, id=routing_table_id).get_result()["routes"][i]["id"]
        id_routes_list.append(route_id)
    return id_routes_list, routes_lenght

# atualiza o next hop caso ele for diferente do IP primário do NLB
def updateNextHop(routes_lenght, id_routes_list, primary_ip,secondery_ip):
    for i in range(routes_lenght):
        next_hop = service.get_vpc_routing_table_route(vpc_id, routing_table_id, id_routes_list[i]).get_result()["next_hop"]["address"]
        route_patch_model = {
                "next_hop": {
                    "address": primary_ip
            }}
        if next_hop == secondery_ip:
            service.update_vpc_routing_table_route(vpc_id, routing_table_id, id_routes_list[i],route_patch=route_patch_model)

def main():
    primary_ip, secondery_ip = getNLBIps()
    id_routes_list, routes_lenght = routesIdList()  
    updateNextHop(routes_lenght, id_routes_list, primary_ip, secondery_ip)

main()












