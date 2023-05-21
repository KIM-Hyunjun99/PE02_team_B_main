import os
import shutil



def delete():
    res_dir = "../res/"
    print('folder deleted')


    # res 폴더 내의 모든 파일과 디렉토리 삭제 (res 폴더 제외)
    for file_name in os.listdir(res_dir):
        file_path = os.path.join(res_dir, file_name)
        if file_name != "res" and os.path.isdir(file_path):
            shutil.rmtree(file_path)
        elif not os.path.isdir(file_path) and file_name != 'result will be save at this folder.txt':
            os.remove(file_path)
    return