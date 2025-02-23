import subprocess
import sys

# 定义执行 Shell 脚本的函数
def run_shell_script(script_path):
    try:
        # 使用 subprocess 执行 shell 脚本
        result = subprocess.run(['bash', script_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Script {script_path} executed successfully")
        print(result.stdout.decode())  # 打印脚本输出
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_path}")
        print(e.stderr.decode())  # 打印错误输出
        sys.exit(1)

# 运行第一个脚本
script1 = "/path/to/your/script1.sh"
print(f"Running {script1}...")
run_shell_script(script1)

# 运行第二个脚本
script2 = "/path/to/your/script2.sh"
print(f"Running {script2}...")
run_shell_script(script2)

print("Both scripts executed successfully.")
