#!/usr/bin/python3

import os
import subprocess

print('--------------------------U-02 패스워드 복잡성 설정 진단을 실시합니다.-------------------------\n')

def check_file(path, filename):
    try:
        file_check = subprocess.check_output(f'ls -al {path} 2> /dev/null', shell=True, text=True)        
        if filename in file_check:
            print(f'{path} 파일을 확인했습니다.')
            return True
        else:
            print(f'{path} 파일이 없습니다. os와 version을 다시 입력해주세요.')
            return False
    except subprocess.CalledProcessError:
        print(f'{path} 파일을 확인할 수 없습니다.\n')

def test():
# OS 및 버전 정보에 따른 파일 확인 로직
    os = input(str('os 정보를 입력해주세요: '))
    version = input(str('version: 정보를 입력해주세요(ubuntu는 .을 빼고 입력): '))
    need_check = False

    if os == "solaris" and version >= '10':
        solaria_check = check_file('/etc/default/passwd', 'passwd')
        if solaria_check:
            need_check = True
            return need_check
    elif os == "centos" and version >= '5' and version < '7':
        centos5_check = check_file('/etc/pam.d/system-auth', 'system-auth')
        if centos5_check:
            need_check = True
            return need_check
    elif os == "centos" and version >= '7':
        centos7_check = check_file('/etc/security/pwquality.conf', 'pwquality.conf')
        if centos7_check:
            need_check = True
            return need_check
    elif os == "ubuntu":
        ubuntu_check = check_file('/etc/security/pwquality.conf', 'pwquality.conf')
        if ubuntu_check:
            need_check = True
            return need_check
    else:
        print("지원되지 않는 OS 또는 버전입니다. os와 version을 다시 입력해주세요.")

# /etc/shadow 비밀번호가 설정되어 있는지 안되어 있는지 확인해야함

need_check = test()
# 패스워드 정책 설정
if need_check:
        print("================================================================================")
        print("아래는 확인하는 정책의 간단한 설명입니다.\n")
        print("lcredit: 최소 소문자 설정입니다. 최소 1자 이상 요구됩니다.")
        print("ucredit: 최소 대문자 설정입니다. 최소 1자 이상 요구됩니다.")
        print("dcredit: 최소 숫자 설정입니다. 최소 1자 이상 요구됩니다.")
        print("ocredit: 최소 특수문자 설정입니다. 최소 1자 이상 요구됩니다.")
        print("minlen: 최소 패스워드 길이 설정입니다. 최소 8자리 이상 요구됩니다.")
        print(" ")
        print(" ")
        print("=========================패스워드 설정을 확인합니다===============================" )      
        print("현재 설정되어 있는 항목들입니다.\n")
        confirm_setting = ['lcredit', 'ucredit', 'dcredit','ocredit','minlen']
        for setting in confirm_setting:
                command = f'cat /etc/security/pwquality.conf | grep "# {setting}"'
                try:
                        result = subprocess.check_output(command, shell=True, text=True)
                        print(f'현재 {setting} 항목이 설정되어 있지 않습니다.')
                except subprocess.CalledProcessError:
                        print(f'{setting} 항목은 설정이 올바르게 되어있습니다.')

print(" ")
