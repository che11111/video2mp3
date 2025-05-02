import tkinter as tk
from tkinter import filedialog, messagebox
import video_to_mp3
import threading
import os
import sys

class VideoToMP3Converter:
    def __init__(self, root):
        self.root = root
        self.root.title("video2mp3")
        self.root.geometry("500x300")
        
        # 设置窗口图标和任务栏图标
        try:
            if os.name == 'nt':
                icon_path = os.path.join(os.path.dirname(__file__), "video2mp3.ico")
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
            else:
                icon_path = os.path.join(os.path.dirname(__file__), "video2mp3.icns")
                if os.path.exists(icon_path):
                    img = tk.PhotoImage(file=icon_path)
                    self.root.tk.call('wm', 'iconphoto', self.root._w, img)
        except Exception as e:
            print(f"加载图标失败: {e}")
        
        # 视频文件选择
        self.video_path = tk.StringVar()
        tk.Label(root, text="视频文件:").pack(pady=5)
        tk.Entry(root, textvariable=self.video_path, width=50).pack(pady=5)
        tk.Button(root, text="选择视频文件", command=self.select_video).pack(pady=5)
        
        # 输出目录选择
        self.output_dir = tk.StringVar()
        tk.Label(root, text="输出目录:").pack(pady=5)
        tk.Entry(root, textvariable=self.output_dir, width=50).pack(pady=5)
        tk.Button(root, text="选择输出目录", command=self.select_output_dir).pack(pady=5)
        
        # 按钮框架
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)
        
        # 转换按钮
        self.convert_btn = tk.Button(button_frame, text="开始转换", command=self.start_conversion)
        self.convert_btn.pack(side=tk.LEFT, padx=10)
        
        # 重置按钮
        self.reset_btn = tk.Button(button_frame, text="重置", command=self.reset_fields)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        # 打开目录按钮
        self.open_dir_btn = tk.Button(button_frame, text="打开输出目录", command=self.open_output_dir)
        self.open_dir_btn.pack(side=tk.LEFT)
        
        # 状态标签
        self.status = tk.StringVar()
        self.status.set("准备就绪")
        tk.Label(root, textvariable=self.status).pack(pady=5)
    
    def select_video(self):
        file_path = filedialog.askopenfilename(
            title="选择视频文件",
            filetypes=[("视频文件", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv")]
        )
        if file_path:
            self.video_path.set(file_path)
            self.status.set("已选择视频文件")
    
    def select_output_dir(self):
        dir_path = filedialog.askdirectory(title="选择输出目录")
        if dir_path:
            self.output_dir.set(dir_path)
            self.status.set("已选择输出目录")
    
    def start_conversion(self):
        video_path = self.video_path.get()
        if not video_path:
            messagebox.showerror("错误", "请先选择视频文件")
            return
            
        output_dir = self.output_dir.get() or os.path.dirname(video_path)
        
        self.convert_btn.config(state=tk.DISABLED)
        self.status.set("转换中...")
        
        # 在新线程中执行转换
        threading.Thread(
            target=self.convert_video,
            args=(video_path, output_dir),
            daemon=True
        ).start()
    
    def convert_video(self, video_path, output_dir):
        try:
            output_path = video_to_mp3.convert_video_to_mp3(video_path, output_dir)
            self.root.after(0, lambda: self.on_conversion_success(output_path))
        except Exception as e:
            self.root.after(0, lambda: self.on_conversion_error(str(e)))
    
    def on_conversion_success(self, output_path):
        self.convert_btn.config(state=tk.NORMAL)
        self.status.set("转换完成!")
        messagebox.showinfo("成功", f"MP3文件已保存到:\n{output_path}")
    
    def on_conversion_error(self, error_msg):
        self.convert_btn.config(state=tk.NORMAL)
        self.status.set("转换失败")
        messagebox.showerror("错误", error_msg)
        
    def reset_fields(self):
        """重置所有输入字段"""
        self.video_path.set("")
        self.output_dir.set("")
        self.status.set("已重置")
        
    def open_output_dir(self):
        """打开输出目录"""
        output_dir = self.output_dir.get()
        if not output_dir:
            messagebox.showwarning("提示", "请先选择输出目录")
            return
            
        try:
            if os.name == 'nt':  # Windows
                os.startfile(output_dir)
            elif os.name == 'posix':  # macOS/Linux
                os.system(f'open "{output_dir}"' if sys.platform == 'darwin' else f'xdg-open "{output_dir}"')
            self.status.set(f"已打开目录: {output_dir}")
        except Exception as e:
            messagebox.showerror("错误", f"无法打开目录:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoToMP3Converter(root)
    root.mainloop()
