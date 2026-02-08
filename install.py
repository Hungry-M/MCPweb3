#!/usr/bin/env python3
"""
TRONMCP 一键安装脚本

用法:
    python install.py

功能:
    1. 创建虚拟环境
    2. 安装依赖
    3. 安装 tronmcp 命令
    4. 自动运行 onboard 配置向导
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def detect_python_command():
    """自动检测可用的 Python 命令"""
    # 尝试常见的 Python 命令
    python_commands = ['python', 'python3', 'py']
    
    for cmd in python_commands:
        try:
            # 检查命令是否存在
            result = subprocess.run(
                f'"{cmd}" --version',
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return cmd
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue
    
    # 如果都没找到，返回默认的 python
    print("  ⚠️  未检测到 python/python3/py 命令，将使用 'python'")
    return 'python'


def run_command(cmd, description, capture_output=False):
    """运行命令并显示进度"""
    print(f"  ⏳ {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=capture_output,
            text=True,
            timeout=300,
        )
        if result.returncode == 0:
            print(f"  ✅ {description}完成")
            return True
        else:
            print(f"  ❌ {description}失败: {result.stderr if capture_output else '返回码 ' + str(result.returncode)}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  ❌ {description}超时")
        return False
    except Exception as e:
        print(f"  ❌ {description}异常: {e}")
        return False


def main():
    print("\n" + "="*60)
    print("  🐙 TRONMCP 一键安装")
    print("="*60 + "\n")

    # 显示 TRON logo
    logo = r"""
  ████████╗██████╗  ██████╗ ███╗   ██╗
  ╚══██╔══╝██╔══██╗██╔═══██╗████╗  ██║
     ██║   ██████╔╝██║   ██║██╔██╗ ██║
     ██║   ██╔══██╗██║   ██║██║╚██╗██║
     ██║   ██║  ██║╚██████╔╝██║ ╚████║
     ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
"""
    print(f"  {logo}")

    project_dir = Path(__file__).parent.resolve()
    venv_dir = project_dir / ".venv"

    # Step 1: 检测 Python 命令
    print("📋 Step 1/4: 检测 Python 环境")
    python_cmd = detect_python_command()
    print(f"  ✅ 使用命令: {python_cmd}")
    
    # 获取 Python 版本
    try:
        result = subprocess.run(
            f'"{python_cmd}" --version',
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        python_version = result.stdout.strip() if result.stdout else result.stderr.strip()
        print(f"  ✅ {python_version}")
    except Exception as e:
        print(f"  ❌ 无法获取 Python 版本: {e}")
        sys.exit(1)
    
    # 检查 Python 版本是否 >= 3.10
    if sys.version_info < (3, 10):
        print("  ❌ 需要 Python 3.10 或更高版本")
        sys.exit(1)
    print()

    # Step 2: 创建虚拟环境
    print("📦 Step 2/4: 创建虚拟环境")
    if venv_dir.exists():
        print(f"  ⏳ 虚拟环境已存在，跳过创建")
    else:
        if not run_command(f'"{python_cmd}" -m venv "{venv_dir}"', "创建虚拟环境"):
            sys.exit(1)
    print()

    # Step 3: 安装依赖
    print("🔧 Step 3/4: 安装依赖包")
    if platform.system() == "Windows":
        pip_cmd = f'"{venv_dir}/Scripts/pip.exe"'
    else:
        pip_cmd = f'"{venv_dir}/bin/pip"'

    # 升级 pip
    if not run_command(f'{pip_cmd} install --upgrade pip', "升级 pip", capture_output=True):
        print("  ⚠️  pip 升级失败，继续安装...")

    # 安装项目（包含所有依赖）
    if not run_command(f'{pip_cmd} install -e "{project_dir}"', "安装 tron-mcp-server", capture_output=True):
        print("  ⚠️  安装失败，请检查错误信息")
        sys.exit(1)
    print()

    # Step 4: 完成
    print("🎉 Step 4/4: 安装完成！\n")
    print("="*60)
    print("  下一步：")
    print("="*60)
    print()
    print("  1️⃣  激活虚拟环境并运行配置向导：")
    if platform.system() == "Windows":
        print(f'     {project_dir}\\.venv\\Scripts\\Activate.ps1')
        print(f'     tronmcp onboard')
    else:
        print(f'     source {project_dir}/.venv/bin/activate')
        print(f'     tronmcp onboard')
    print()
    print("  2️⃣  或者直接运行（已自动配置）：")
    if platform.system() == "Windows":
        print(f'     {project_dir}\\.venv\\Scripts\\tronmcp.exe onboard')
    else:
        print(f'     {project_dir}/.venv/bin/tronmcp onboard')
    print()
    print("="*60)
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 安装已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 安装失败: {e}")
        sys.exit(1)
