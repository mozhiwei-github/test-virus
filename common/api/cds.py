from common.log import log
from common.utils import send_request
from common.contants import ServerHost

"""容器调度服务相关api接口"""


def set_kvm_state_api(ip):
    """
    修改虚拟机任务状态接口
    @param ip: kvm虚拟机ip地址
    @return:
    """
    url = f"{ServerHost.CDS.value}/api/v1/kvm/state"

    data = {"ip": ip}

    res = send_request(url, data=data)

    if res.status_code != 200:
        log.log_error(f"修改虚拟机状态失败, status_code: {res.status_code}", log_only=True)
        return False

    res_data = res.json()
    if not res_data or res_data["ret"] != 0:
        log.log_error(f"修改虚拟机状态失败, res: {res.text}", log_only=True)
        return False

    return True


def kvm_image_sync_api(ip, case_id, case_name, case_username):
    """
    虚拟机镜像同步接口
    @param ip: kvm虚拟机ip地址
    @param case_id: 测试用例ID
    @param case_name: 测试用例名称
    @param case_username: 测试用例触发用户
    @return:
    """
    url = f"{ServerHost.CDS.value}/api/v1/kvm/image/sync"

    data = {
        "ip": ip,
        "case_id": case_id,
        "case_name": case_name,
        "case_username": case_username,
    }

    res = send_request(url, data=data)

    if res.status_code != 200:
        log.log_error(f"启动虚拟机镜像同步失败, status_code: {res.status_code}", log_only=True)
        return False

    res_data = res.json()
    if not res_data or res_data["ret"] != 0:
        log.log_error(f"启动虚拟机镜像同步失败, res: {res.text}", log_only=True)
        return False

    return True
