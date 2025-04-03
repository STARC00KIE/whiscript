import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
from moviepy import VideoFileClip
import whisper
import os

class BasicTranscriberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MP4 → Text 변환기")
        self.root.geometry("400x250")

        # 파일 선택
        self.file_label = tk.Label(root, text="MP4 파일 선택:")
        self.file_label.pack(pady=5)

        self.file_path_var = tk.StringVar()
        self.file_entry = tk.Entry(root, textvariable=self.file_path_var, width=50)
        self.file_entry.pack()

        self.browse_btn = tk.Button(root, text="찾아보기", command=self.browse_file)
        self.browse_btn.pack()

        # Whisper 모델 선택
        tk.Label(root, text="Whisper 모델 선택:").pack(pady=5)
        self.model_var = tk.StringVar(value="base")
        self.model_combo = Combobox(root, textvariable=self.model_var)
        self.model_combo['values'] = ("base", "small", "medium", "large-v3")
        self.model_combo.pack()

        # 변환 시작 버튼
        self.start_btn = tk.Button(root, text="변환 시작", command=self.start_processing)
        self.start_btn.pack(pady=10)

        # 로그 출력
        self.log_text = tk.Text(root, height=5, width=50)
        self.log_text.pack()

    def browse_file(self):
        file = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        if file:
            self.file_path_var.set(file)

    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def start_processing(self):
        mp4_path = self.file_path_var.get()
        model_size = self.model_var.get()

        if not os.path.isfile(mp4_path):
            messagebox.showerror("오류", "유효한 MP4 파일을 선택하세요.")
            return

        self.log(f"▶ 변환 시작: {mp4_path}")
        model = whisper.load_model(model_size)

        base, _ = os.path.splitext(mp4_path)
        wav_path = base + ".wav"

        # 오디오 추출
        video = VideoFileClip(mp4_path)
        video.audio.write_audiofile(wav_path, verbose=False, logger=None)

        # 텍스트 변환
        result = model.transcribe(wav_path, language="Korean")
        transcription = result["text"]

        # 저장
        txt_path = base + "_transcription.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(transcription)

        self.log(f"✅ 저장 완료: {txt_path}")

# 앱 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = BasicTranscriberApp(root)
    root.mainloop()