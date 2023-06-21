import os
import shutil
from common.log import log
from common.utils import try_import

SMBConnection = try_import('smb.SMBConnection', 'SMBConnection')

"""smb操作"""


class Samba(object):
    def __init__(self, server_ip, username, password, port=445):
        self.conn = SMBConnection(username, password, "", server_ip, is_direct_tcp=True)
        assert self.conn.connect(server_ip, port)

    def download_dir(self, service_name, dir_path, target_path):
        """
        递归下载目录下所有文件
        @param service_name: 路径的共享文件夹的名称
        @param dir_path: 相对于service_name的路径
        @param target_path: 下载目标路径
        @return:
        """
        file_info_list = []
        full_dir_name = os.path.join(service_name, dir_path)

        if os.path.exists(target_path):
            shutil.rmtree(target_path)
        # 创建目标下载目录
        os.makedirs(target_path)

        try:
            for f in self.conn.listPath(service_name, dir_path):
                if f.filename in ['.', '..']:
                    continue

                filepath = os.path.join(dir_path, f.filename)
                target_filepath = os.path.join(target_path, f.filename)
                # 如果为文件夹则再进入该文件夹递归下载
                if f.isDirectory:
                    sub_download_result, sub_file_info_list = self.download_dir(service_name, filepath, target_filepath)
                    file_info_list.extend(sub_file_info_list)
                    if not sub_download_result:
                        return sub_download_result, file_info_list
                else:
                    try:
                        with open(target_filepath, "wb") as t:
                            self.conn.retrieveFile(service_name, filepath, t)

                        file_info_list.append({
                            "filepath": target_filepath,
                            "filename": f.filename,
                        })
                    except Exception as e:
                        log.log_error(f"smb download failed, file: {full_dir_name}, err: {e}", attach=False, need_assert=False)
                        return False, file_info_list

        except Exception as e:
            log.log_error(f"smb download failed, dir: {full_dir_name}, err: {e}", attach=False, need_assert=False)
            return False, file_info_list

        return True, file_info_list
