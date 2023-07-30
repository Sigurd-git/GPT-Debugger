import tkinter as tk
from tkinter import ttk
import openai
import re
import os
# 从环境变量中读取你的OpenAI API密钥
# Read your OpenAI API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

# 从环境变量中读取OpenAI API的base url, 如果你使用的是OpenAI的服务器，可以不用设置
# Read the base url of the OpenAI API from the environment variable. If you are using OpenAI's server, you can skip this step
openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com")
def get_text_color(bg_color):
    # Define a mapping of background colors to text colors
    color_map = {
        'white': 'black',
        'black': 'white',
        # Add more color pairs if needed
    }
    return color_map.get(bg_color, 'black')  # Default to 'black' if bg_color is not in the map

class GPTDebugger(tk.Tk):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        # Set the window title
        self.title('GPT Debugger')

        # 设置默认的temperature和model
        # Set default temperature and model
        self.temperature = tk.DoubleVar(value=0.8)
        self.model = tk.StringVar(value='gpt-4')

        # # 设置窗口的背景颜色
        # # Set the background color of the window
        # self.configure(background='light gray')

        # 创建窗口部件
        # Create the window widgets
        self.create_widgets()

    def create_widgets(self):
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)
        # 创建System Prompt输入框
        # Create the System Prompt input field
        ttk.Label(self, text='System Prompt:').grid(row=0, column=0, sticky='w')
        self.system_prompt = tk.Entry(self, width=50)
        self.system_prompt.grid(row=0, column=1, sticky='we')

        # 创建User Prompt输入框
        # Create the User Prompt input field
        ttk.Label(self, text='User Prompt:').grid(row=1, column=0, sticky='w')
        self.user_prompt = tk.Entry(self, width=50)
        self.user_prompt.grid(row=1, column=1, sticky='we')

        # 创建Feedback输入框
        # Create the Feedback input field
        ttk.Label(self, text='Feedback:').grid(row=2, column=0, sticky='w')
        self.feedback = tk.Entry(self, width=50)
        self.feedback.grid(row=2, column=1, sticky='we')

        # 创建Temperature输入框
        # Create the Temperature input field
        ttk.Label(self, text='Temperature:').grid(row=3, column=0, sticky='nwes')
        tk.Entry(self, textvariable=self.temperature).grid(row=3, column=1, sticky='nwes')

        # 创建Model选择菜单
        # Create the Model selection menu
        ttk.Label(self, text='Model:').grid(row=4, column=0, sticky='nwes')
        tk.OptionMenu(self, self.model, 'gpt-3.5-turbo', 'gpt-4').grid(row=4, column=1, sticky='nwes')

        # 创建Submit按钮，点击时调用get_gpt_output方法
        # Create the Submit button, which calls the get_gpt_output method when clicked
        tk.Button(self, text='Submit', command=self.get_gpt_output).grid(row=8, column=0, sticky='nwes')

        # 创建Adjust System Prompt按钮，点击时调用adjust_system_prompt方法
        # Create the Adjust System Prompt button, which calls the adjust_system_prompt method when clicked
        tk.Button(self, text='Adjust System Prompt', command=self.adjust_system_prompt).grid(row=8, column=1, sticky='nwes')

        # 创建用于显示GPT输出的文本框
        # Create the text box for displaying GPT output with a scrollbar

        self.output_prompt = tk.Text(self, height=10, width=50)
        scrollbar = tk.Scrollbar(self, command=self.output_prompt.yview)
        self.output_prompt.configure(yscrollcommand=scrollbar.set)
        self.output_prompt.grid(row=5, column=0, rowspan=3, sticky='nsew')
        scrollbar.grid(row=5, column=2, rowspan=3, sticky='ns')

        # 创建3个用于显示new_system_prompt的文本框
        # Create the text box for displaying new_system_prompt
        self.new_system_prompts = [tk.Text(self,height=2) for _ in range(3)]
        for i in range(3):
            self.new_system_prompts[i].grid(row=5+i, column=1, sticky='nwes')
            self.new_system_prompts[i].bind("<Double-Button-1>", self.handle_double_click)

    def handle_double_click(self, event):
        # Get the text from the clicked Text widget
        text = event.widget.get("1.0", tk.END).strip()

        # Insert the text into the system_prompt Entry widget
        self.system_prompt.delete(0, tk.END)
        self.system_prompt.insert(0, text)



    def get_gpt_output_(self,system,user,temperature=0.5,n=1):
        # 调用OpenAI API，获取GPT的输出
        # Call the OpenAI API to get GPT output
        chat = openai.ChatCompletion.create(
            model=self.model.get(),
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            temperature=temperature,
            n=n,
        )
        result = [chat['choices'][i]['message']['content'] for i in range(n)]
        return result
    
    def get_gpt_output(self):
        # 调用OpenAI API，获取GPT的输出
        # Call the OpenAI API to get GPT output
        result = self.get_gpt_output_(self.system_prompt.get(),self.user_prompt.get(),0)[0]

        # 清除原有的输出
        # Clear the original output
        self.output_prompt.delete('1.0', tk.END)

        # 显示GPT的输出
        # Display the GPT output
        self.output_prompt.insert(tk.END, result)
    def adjust_system_prompt(self):
        # 使用用户的反馈产生新的System Prompt
        # Use the user's feedback to generate the new System Prompt
        feedback = self.feedback.get()

        # 获取output_prompt
        # Get the output_prompt
        reply = self.output_prompt.get('1.0', tk.END)

        # 获取user_prompt
        # Get the user_prompt
        user = self.user_prompt.get()

        # 获取system_prompt
        # Get the system_prompt
        system = self.system_prompt.get()

        adjust_system = '''I will provide you the system prompt, user prompt, chatgpt's response, and any identified shortcomings in the response in the format: <system>Whatever</system>; <user>Whatever</user>; <reply>Whatever</reply>; <feedback>Whatever</feedback>. Help me improve the system prompt to enhance chatgpt's performance. You can also generate some examples in system prompt for clarification. The output should be in the format: <system>Whatever</system>.Only the system prompt is required.'''

        adjust_user = '''<system>{}</system>; <user>{}</user>; <reply>{}</reply>; <feedback>{}</feedback>.'''.format(system, user, reply, feedback)

        new_system = self.get_gpt_output_(adjust_system, adjust_user, self.temperature.get(),n=3)
        # 删除<system>和</system>
        # Remove <system> and </system> 
        new_system = [re.sub('<system>', '', system) for system in new_system]
        new_system = [re.sub('</system>', '', system) for system in new_system]
        # Clear the original System Prompts
        for output in self.new_system_prompts:
            output.delete('1.0', tk.END)

        # Display the new System Prompts
        for output, system_prompt in zip(self.new_system_prompts, new_system):
            output.insert(tk.END, system_prompt)


if __name__ == '__main__':
    debugger = GPTDebugger()
    debugger.mainloop()


