#!/usr/bin/env python3
#20250403
# -*- coding: utf-8 -*-
"""
根据目录结构和类继承关系生成文件列表
功能说明见原始脚本注释
"""

import os
import re
import argparse
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Union

USE_ABSOLUTE = True  # 是否使用绝对路径
AGENT_ORDER = ["intf", "interface", "transaction", "monitor", "driver", "sequencer", "seqr", "agent"]
ENV_ORDER = ["model", "scoreboard", "env"]


# --------------------- 路径配置 ---------------------
def get_directory_paths(script_dir: str, core_type: str) -> Dict[str, str]:
    """获取各目录绝对路径"""
    base_dir = os.path.abspath(os.path.join(script_dir, ".."))
    return {
        "design_file": os.path.join(base_dir, "..", "design_file", f"{core_type}"),
        "testbench": os.path.join(base_dir, "verif", "testbench"),
        "hdl_top": os.path.join(base_dir, "verif", "testbench", "hdl_top"),
        "sequences": os.path.join(base_dir, "verif", "testbench", "sequences"),
        "vseqs": os.path.join(base_dir, "verif", "testbench", "vseqs"),
        "tests": os.path.join(base_dir, "verif", "testbench", "tests"),
        "agent": os.path.join(base_dir, "verif", "agent"),
        "env": os.path.join(base_dir, "verif", "env"),
        "filelists": os.path.join(base_dir, "filelists")
    }


# --------------------- 核心功能 ---------------------
class FileProcessor:
    """文件处理与拓扑排序类"""

    def __init__(self, folder_type: Optional[str] = None):
        self.folder_type = folder_type
        self.class_map: Dict[str, str] = {}
        self.file_info: Dict[str, Tuple[Optional[str], Optional[str], Optional[str]]] = {}

    def extract_class_info(self, file_path: str) -> Tuple[Optional[str], Optional[str]]:
        """提取类继承关系"""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception:
            return (None, None)

        match = re.search(r'class\s+(\w+)\s+extends\s+(\w+)', content, re.IGNORECASE)
        return (match.group(1), match.group(2)) if match else (None, None)

    def process_files(self, file_paths: List[str]) -> None:
        """预处理所有文件信息"""
        for fp in file_paths:
            cls_name, parent_cls = self.extract_class_info(fp)
            func = self._extract_function_tag(fp) if self.folder_type else None
            self.file_info[fp] = (cls_name, parent_cls, func)
            if cls_name:
                self.class_map[cls_name] = fp

    def _extract_function_tag(self, file_path: str) -> Optional[str]:
        """提取文件功能标签"""
        filename = os.path.basename(file_path)
        result = filename.rsplit('_', 1)[-1].rsplit('.', 1)[0]
        return result if result else None

    def build_dependency_graph(self) -> Tuple[Dict[str, List[str]], Dict[str, int]]:
        """构建依赖关系图"""
        graph = defaultdict(list)
        in_degree = {fp: 0 for fp in self.file_info}

        for fp, (_, parent, _) in self.file_info.items():
            if parent and parent in self.class_map:
                parent_fp = self.class_map[parent]
                graph[parent_fp].append(fp)
                in_degree[fp] += 1

        return graph, in_degree

    def topological_sort(self, file_paths: List[str]) -> List[str]:
        """执行拓扑排序"""
        graph, in_degree = self.build_dependency_graph()
        sorted_files = []

        # 初始化零入度节点
        zero_degree = [fp for fp in file_paths if in_degree[fp] == 0]
        zero_degree.sort(key=self._sort_key)

        while zero_degree:
            current = zero_degree.pop(0)
            sorted_files.append(current)

            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    zero_degree.append(neighbor)
                    zero_degree.sort(key=self._sort_key)

        # 处理循环依赖
        if len(sorted_files) < len(file_paths):
            remaining = [fp for fp in file_paths if fp not in sorted_files]
            remaining.sort(key=self._sort_key)
            sorted_files.extend(remaining)

        return sorted_files

    def _sort_key(self, file_path: str) -> tuple:
        """定义排序规则"""
        _, _, func = self.file_info[file_path]
        filename = os.path.basename(file_path)

        if self.folder_type == "agent" and func:
            order = AGENT_ORDER.index(func) if func in AGENT_ORDER else 100
            return (order, filename)
        elif self.folder_type == "env" and func:
            order = ENV_ORDER.index(func) if func in ENV_ORDER else 100
            return (order, filename)
        return (0, filename)


# --------------------- 文件生成 ---------------------
def generate_f_file(target_dir: str, output_path: str, use_absolute: bool) -> None:
    """生成单个目录的.f文件"""
    if not os.path.isdir(target_dir):
        print(f"目录 {target_dir} 不存在，跳过生成 {output_path}")
        return

    # 过滤并排序文件
    files = []
    for dirpath, dirnames, filenames in os.walk(target_dir):
        for f in filenames:
            if not f.endswith(".f"):
                files.append(os.path.join(dirpath, f))
    # files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f)) and not f.endswith(".f")]

    processor = FileProcessor()
    full_paths = [os.path.join(target_dir, f) for f in files]
    processor.process_files(full_paths)
    sorted_files = processor.topological_sort(full_paths)

    # 写入文件
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            for fp in sorted_files:
                f.write(f"{os.path.abspath(fp)}\n" if use_absolute else f"{os.path.basename(fp)}\n")
        print(f"生成文件列表：{output_path}")
    except Exception as e:
        print(f"写入文件 {output_path} 失败: {e}")


def generate_tc_filelist(dirs: Dict[str, str], use_absolute: bool) -> None:
    """生成总文件列表"""
    output_path = os.path.join(dirs["filelists"], "tc_filelist.f")
    lines = []

    # 添加design.f引用
    design_f = os.path.join(dirs["design_file"], "design_file.f")
    lines.append(f"-f {_format_path(design_f, dirs['filelists'], use_absolute)}")

    # 处理各目录文件
    for folder in ["hdl_top", "agent", "env"]:
        processor = FileProcessor(folder_type=folder if folder in ("agent", "env") else None)
        files = _collect_files(dirs[folder])
        processor.process_files(files)
        sorted_files = processor.topological_sort(files)
        lines.extend([_format_path(fp, dirs["filelists"], use_absolute) for fp in sorted_files])

    # 添加其他.f文件引用
    for section in ["sequences", "vseqs", "tests"]:
        f_path = os.path.join(dirs[section], f"{section}.f")
        if os.path.exists(f_path):
            lines.append(f"-f {_format_path(f_path, dirs['filelists'], use_absolute)}")

    # 写入总文件
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"生成总文件列表：{output_path}")
    except Exception as e:
        print(f"写入 {output_path} 失败: {e}")


# --------------------- 辅助函数 ---------------------
def _collect_files(directory: str) -> List[str]:
    """收集目录下所有非.f文件"""
    files = []
    for root, _, filenames in os.walk(directory):
        for fn in filenames:
            if not fn.endswith(".f"):
                files.append(os.path.join(root, fn))
    return files


def _format_path(path: str, base: str, absolute: bool) -> str:
    """格式化路径输出"""
    return os.path.abspath(path) if absolute else os.path.relpath(path, base)


# --------------------- 主程序 ---------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--core_type", type=str, required=True)
    args = parser.parse_args()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    directories = get_directory_paths(script_dir, args.core_type)

    # 生成各子目录.f文件
    for section in ["design_file", "sequences", "tests", "vseqs"]:
        generate_f_file(directories[section], os.path.join(directories[section], f"{section}.f"), USE_ABSOLUTE)

    # 生成总文件列表
    generate_tc_filelist(directories, USE_ABSOLUTE)
