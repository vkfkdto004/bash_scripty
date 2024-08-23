#!/usr/bin/python3

import os
import subprocess

print('U-01: root 계정 원격접속 제한')

sshd_service_alive = False
telnet_service_alive = False

# SSH, Telnet 서비스 활성화 확인
sshd_service = subprocess.check_output('ps -ef | grep -v grep | grep sshd', shell=True, text=True)
if 'sshd' in sshd_service:
    sshd_service_alive = True
    print("SSH 서비스가 활성화 중입니다")

telnet_service = os.system("cat /etc/xinetd.d/telnet 2> /dev/null | grep 'disable=no'")
if bool(telnet_service):
    telnet_service_alive = True
    print("Telnet 서비스  활성화 중입니다\n")

# SSH서비스  진단  실시
print("#################SSH 서비스 진단 시작합니다.############################")
print("========================================================================")
dig_ssh_service = subprocess.check_output('cat /etc/ssh/sshd_config | grep -i "#permitrootlogin"', shell=True, text=True)   
if '#' in dig_ssh_service:
    print("\n####/etc/ssh/sshd_config####\n!!!!!!!설정이 취약합니다.!!!!!!!!!!!!!\n")
else:
    print("\n####/etc/ssh/sshd_config####\n!!!!!!!설정이 양호합니다.!!!!!!!!!!!!!\n")


# telnet 서비스 진단 실시
print("#################Telnet 서비스 진단 시작합니다.#########################")
print("========================================================================")
try:
    dig_telnet_service = subprocess.check_output('cat /etc/pam.d/login | grep -i "pam_securetty.so"', shell=True, text=True)
    print("\n####/etc/pam.d/login####\n!!!!!!!설정이 양호합니다.!!!!!!!!!!!!!\n")
except subprocess.CalledProcessError:
    print("\n####/etc/pam.d/login####\n!!!!!!!설정이 취약합니다.!!!!!!!!!!!!!\n")

# 사용자 선택권에 대한 코드를 추가해서 진행한다. -> 내부적으로 문제가 될 수가 있다.
# SSH, Telnet 조치 취하기
print("---------------SSH 서비스 취약점 조치 합니다.-------------------")
clear_ssh_service = subprocess.check_output('cat /etc/ssh/sshd_config | grep -i "#permitrootlogin"', shell=True, text=True) 
if 'prohibit-password' in clear_ssh_service:
    os.system('sed "s/#PermitRootLogin prohibit-password/PermitRootLogin No/g" /etc/ssh/sshd_config')


print("----------조치 완료했습니다. 다시 검사합니다---------------------")
dig_ssh_service = subprocess.check_output('cat /etc/ssh/sshd_config | grep -i "#permitrootlogin"', shell=True, text=True)   
if 'PermitrootLogin No' in dig_ssh_service:
    print("\n####/etc/ssh/sshd_config####\n!!!!!!!설정이 취약합니다.!!!!!!!!!!!!!\n")
else:
    print("\n####/etc/ssh/sshd_config####\n!!!!!!!설정이 양호합니다.!!!!!!!!!!!!!\n")
