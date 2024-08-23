#!/usr/bin/python3

import os
import subprocess
import platform

print('-------------------계정 잠금 임계값 설정 진단 프로그램------------------')

def detect_os():
    os_name = platform.system()
    os_version = platform.release()
    os_release= subprocess.check_output('cat /etc/os-release | grep -i pretty | cut -d "=" -f 2', shell=True, text=True)
    print(f"현재 OS: {os_release}, {os_name}, {os_version}")
    return os_name, os_version

solaris_faillock = 'etc/default/login'
solaris5_9_faillock = '/etc/security/policy.conf'
ubuntu_faillock = '/etc/pam.d/common-auth'
aix_faillock = '/etc/security/user'
hp_ux_faillock = '/tcb/files/auth/system/default'
hp_ux11_faillock = '/etc/default/security'


current_os_name, current_os_version = detect_os()

while True:
    print('\n운영체제를 선택해주세요: ')
    print('1. Solaris')
    print('2. Solaris 5.9')
    print('3. Ubuntu')
    print('4. AIX')
    print('5. HP-UX')
    print('6. HP-UX 11')
    print('0. Go back (종료)')

    try:
        select_os = int(input('Enter the os number(0 to go back): '))
        if select_os == 0:
            break

        if select_os == 1:
            print(f"Solaris의 faillock 파일 경로: {solaris_faillock}")
            try:
                solaris_check = subprocess.check_output(f'cat {solaris_faillock}  | grep -i "# retries"', shell=True, text=True)
                if '#' in faillock_check:
                    print('설정이 취약합니다.')
            except subprocess.CalledProcessError:
                    print("###설정이 양호합니다")
            break
        elif select_os == 2:
            print(f"Solaris 5.9의 faillock 파일 경로: {solaris5_9_faillock}")
            try:
                solaris5_check = subprocess.check_output(f'cat {solaris5_9_faillock}  | grep -i "lock_after_retries"', shell=True, text=True)
                if 'YES' in solaris5_check:
                    print('###설정이 양호합니다.')
            except subprocess.CalledProcessError:
                    print("설정이 취약합니다")
            break
        elif select_os == 3:
            print(f"Ubuntu의 faillock 파일 경로: {ubuntu_faillock}")
            try:
                ubuntu_check = subprocess.check_output(f'cat {ubuntu_faillock}  | grep -i "faillock"', shell=True, text=True)
                if 'faillock.so' in ubuntu_check:
                    print('###설정이 양호합니다.')
            except subprocess.CalledProcessError:
                    print("설정이 취약합니다")
            break
        elif select_os == 4:
            print(f"AIX의 faillock 파일 경로: {aix_faillock}")
            try:
                aix_check = subprocess.check_output(f'cat {aix_faillock}  | grep -i "loginretries"', shell=True, text=True)
                if 'loginretries' in aix_check:
                    print('###설정이 양호합니다.')
            except subprocess.CalledProcessError:
                    print("설정이 취약합니다")
            break
        elif select_os == 5:
            print(f"HP-UX의 faillock 파일 경로: {hp_ux_faillock}")
            try:
                hp_check = subprocess.check_output(f'cat {hp_ux_faillock}  | grep -i "u_maxtries"', shell=True, text=True)
                if 'u_maxtries' in hp_check:
                    print('###설정이 양호합니다.')
            except subprocess.CalledProcessError:
                    print("설정이 취약합니다")
            break
        elif select_os == 6:
            print(f"HP-UX 11의 faillock 파일 경로: {hp_ux11_faillock}")
            try:
                hp_11_check = subprocess.check_output(f'cat {hp_ux11_faillock}  | grep -i "auth_maxtries"', shell=True, text=True)
                if 'AUTH_MAXTRIES' in hp_11_check:
                    print('###설정이 양호합니다.')
            except subprocess.CalledProcessError:
                    print("설정이 취약합니다")
            break
        else:
            print("다시 선택해주세요.")

    except ValueError:
        print("숫자를 입력해주세요.")
