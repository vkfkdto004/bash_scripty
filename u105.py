#!/usr/bin/python3

import os
import subprocess

#wheel 그룹 찾기 /etc/group -> 그룹에 사용자가 있는지 확인 -> 4750 파일 권한
# pam.d. 파일 확인(주석이 제거되어 있는지,

# /etc/group에 wheel 그룹이 존재하는지 확인
print('\n------------/etc/group 내에 wheel 그룹이 존재하는지 확인-------------------')
wheel_group = "/etc/group"

try:
    group_check = subprocess.check_output(f'cat {wheel_group} | grep -i "wheel"', shell=True, text=True)
    if 'wheel' in group_check:
        group_user = (os.popen(f'cat {wheel_group} | grep -i "wheel" | cut -d ":" -f 4').read())
        print('wheel group에 존재한 유저 목록:', group_user)

except subprocess.CalledProcessError:
    print("wheel 그룹이 없습니다.")

# 파일 권한 확인
print('\n============/usr/bin/su 파일에 대한 권한을 확인합니다=======================')
try:
    su_priv = subprocess.check_output('ls -al /usr/bin/su', shell=True, text=True)
    if '-rwsr-x---' in su_priv:
        print("양호합니다.")
    else:
        print("취약점이 발견되었습니다. 권한을 수정해주세요.")
except subprocess.CalledProcessError:
    print("/usr/bin/su 가 존재하지 않습니다.")


# /etc/pam.d/su 파일에 설정이 어떻게 되어있는지 확인.
print('\n-----------/etc/pam.d/su 파일에 대한 설정을 확인합니다-------------------------')
try:
    pam_su = subprocess.check_output('cat /etc/pam.d/su | grep -i "pam_wheel.so" | head -1', shell=True, text=True)
    if '#' in pam_su:
        print('취약점이 발견되었습니다. 주석을 해제하고 활성화 시켜주세요.')
    else:
        print(pam_su)
        print('양호합니다')
except subprocess.CalledProcessError:
    print("출력 결과가 잘못되었습니다.")

print(" ")
