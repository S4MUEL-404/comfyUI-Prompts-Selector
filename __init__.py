import os

# 获取当前节点文件所在的目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")

class PromptSelector:
    """
    一个节点，用于从5个固定的prompt文件和一个自定义prompt中组合文本，输出为逗号分隔的字符串。
    """
    def __init__(self):
        # 确保 prompts 文件夹存在
        if not os.path.exists(PROMPTS_DIR):
            os.makedirs(PROMPTS_DIR)

    @classmethod
    def INPUT_TYPES(cls):
        # 获取 prompts 文件夹中的所有 txt 文件，去掉 .txt 扩展名
        prompt_files = [f[:-4] for f in os.listdir(PROMPTS_DIR) if f.endswith('.txt')] if os.path.exists(PROMPTS_DIR) else []
        options = ["None"] + prompt_files if prompt_files else ["None"]
        
        # 定义5个固定的 prompt 选择器和1个自定义 prompt 输入框
        inputs = {
            "required": {
                "prompt_1": (options, {"default": "None"}),
                "prompt_2": (options, {"default": "None"}),
                "prompt_3": (options, {"default": "None"}),
                "prompt_4": (options, {"default": "None"}),
                "prompt_5": (options, {"default": "None"}),
                "custom_prompt": ("STRING", {"multiline": True, "default": ""}),  # 自定义输入框，显示在最下方
            }
        }
        return inputs

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("combined_text",)
    FUNCTION = "select_prompts"
    CATEGORY = "💀Prompt Selector"

    def select_prompts(self, prompt_1, prompt_2, prompt_3, prompt_4, prompt_5, custom_prompt):
        # 读取文件内容的辅助函数
        def read_prompt(filename):
            if filename == "None":
                return ""  # 选择 None 时返回空字符串
            file_path = os.path.join(PROMPTS_DIR, f"{filename}.txt")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            except Exception as e:
                return f"Error reading file: {str(e)}"

        # 读取5个 prompt 选择器的内容
        prompts = [
            read_prompt(prompt_1),
            read_prompt(prompt_2),
            read_prompt(prompt_3),
            read_prompt(prompt_4),
            read_prompt(prompt_5)
        ]

        # 添加自定义 prompt（如果不为空）
        if custom_prompt.strip():
            prompts.append(custom_prompt.strip())

        # 过滤掉空字符串并用 ", " 连接
        combined_text = ", ".join(p for p in prompts if p)
        return (combined_text,)

# 节点映射
NODE_CLASS_MAPPINGS = {
    "PromptSelector": PromptSelector
}

# 节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptSelector": "💀Prompt Selector"
}

print("PromptSelector node loaded")