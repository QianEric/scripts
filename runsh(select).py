import subprocess

def run_shell_script(script_path):
    try:
        # 使用 subprocess.run 来执行Shell脚本
        result = subprocess.run(['bash', script_path], check=True, text=True, capture_output=True)
        print("脚本输出:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"运行脚本时出错: {e.stderr}")
    except FileNotFoundError:
        print("找不到脚本文件，请检查路径是否正确。")

def main():
    print("欢迎使用Python脚本管理器！")
    
    # 询问用户是否想要运行Shell脚本
    run_script = input("你想要运行Shell脚本吗？(y/n): ").strip().lower()

    if run_script == 'y':
        # 让用户输入脚本的路径
        script_path = input("请输入Shell脚本的完整路径: ").strip()
        run_shell_script(script_path)
    else:
        print("没有运行Shell脚本。")
    
if __name__ == "__main__":
    main()
    