import os
import errno

def generate_file_tree(directory, prefix="", level=0, max_depth=2):
    """生成给定目录的格式化文件树字符串，限制深度到 max_depth。"""
    # 如果超过最大深度，不再递归
    if level > max_depth:
        return ""
    
    # 获取目录中的所有条目
    try:
        entries = sorted(os.listdir(directory))
    except PermissionError:
        return f"{prefix}└── [权限被拒绝]"
    except OSError as e:
        return f"{prefix}└── [错误: {e}]"
    
    tree = []
    for i, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "
        
        # 添加当前条目
        tree.append(f"{prefix}{connector}{entry}")
        
        # 如果是目录且未超过最大深度，则递归
        if os.path.isdir(path) and level < max_depth:
            new_prefix = prefix + ("    " if is_last else "│   ")
            tree.append(generate_file_tree(path, new_prefix, level + 1, max_depth))
    
    return "\n".join(filter(None, tree))

def main():
    # 从用户输入获取目录路径或使用当前目录
    directory = input("请输入目录路径（按 Enter 使用当前目录）：").strip()
    if not directory:
        directory = os.getcwd()
    
    # 规范化并验证目录路径
    directory = os.path.abspath(directory)
    
    # 检查目录是否存在
    if not os.path.exists(directory):
        print(f"错误：目录 '{directory}' 不存在")
        return
    
    # 检查是否为目录
    if not os.path.isdir(directory):
        print(f"错误：'{directory}' 不是一个目录")
        return
    
    # 检查读取权限
    if not os.access(directory, os.R_OK):
        print(f"错误：没有 '{directory}' 的读取权限")
        return
    
    # 生成并打印文件树
    root_name = os.path.basename(directory) + "/"
    tree = f"{root_name}\n{generate_file_tree(directory)}"
    print(tree)
    
    # 保存到文件
    output_file = "file_tree.txt"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(tree)
        print(f"\n文件树已保存到 {output_file}")
    except OSError as e:
        print(f"错误：无法写入 {output_file}：{e}")

if __name__ == "__main__":
    main()
