import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox

# ✅ exe 배포를 위한 패키지 목록
required_packages = {
    "moviepy": "moviepy",
    "whisper": "git+https://github.com/openai/whisper.git",
    "torch": "torch"
}

def install_missing_packages(log_callback):
    """필요한 패키지가 없을 경우 자동 설치"""
    for module_name, pip_name in required_packages.items():
        try:
            __import__(module_name)
            log_callback(f"✅ {module_name} 설치됨")
        except ImportError:
            log_callback(f"📦 {module_name} 설치 중...")
            try:
                if pip_name.startswith("git+"):
                    subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
                else:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", pip_name])
                log_callback(f"✅ {module_name} 설치 완료")
            except Exception as e:
                log_callback(f"❌ {module_name} 설치 실패: {str(e)}")

class ExeReadyTranscriberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📼 MP4 일괄 텍스트 변환기 (exe 배포용)")
        self.root.geometry("500x420")

        # 설치 로그 영역
        self.install_label = tk.Label(root, text="🔍 필수 패키지 확인 중...")
        self.install_label.pack(pady=5)
        self.install_log = tk.Text(root, height=6, width=60)
        self.install_log.pack()

        # 폴더 선택 UI
        self.folder_label = tk.Label(root, text="MP4 폴더 선택:")
        self.folder_label.pack(pady=5)
        self.folder_path_var = tk.StringVar()
        self.folder_entry = tk.Entry(root, textvariable=self.folder_path_var, width=50)
        self.folder_entry.pack()
        self.browse_btn = tk.Button(root, text="찾아보기", command=self.browse_folder)
        self.browse_btn.pack()

        # 모델 선택 UI
        tk.Label(root, text="Whisper 모델 선택:").pack(pady=5)
        self.model_var = tk.StringVar(value="base")
        self.model_combo = Combobox(root, textvariable=self.model_var)
        self.model_combo['values'] = ("base", "small", "medium", "large-v3")
        self.model_combo.pack()

        # 변환 버튼
        self.start_btn = tk.Button(root, text="🟢 변환 시작", command=self.start_processing, state=tk.DISABLED)
        self.start_btn.pack(pady=10)

        # 변환 로그 영역
        self.log_text = tk.Text(root, height=10, width=60)
        self.log_text.pack()

        # 설치 확인 (exe에서도 작동하게끔)
        threading.Thread(target=self.install_packages_and_enable_ui).start()

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path_var.set(folder)

    def install_log_msg(self, msg):
        self.install_log.insert(tk.END, msg + "\n")
        self.install_log.see(tk.END)
        self.root.update_idletasks()

    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def install_packages_and_enable_ui(self):
        install_missing_packages(self.install_log_msg)
        self.install_label.config(text="✅ 설치 완료! 변환을 시작할 수 있습니다.")
        self.start_btn.config(state=tk.NORMAL)

    def start_processing(self):
        folder_path = self.folder_path_var.get()
        model_size = self.model_var.get()
        threading.Thread(target=self.process_folder, args=(folder_path, model_size)).start()

    def process_folder(self, folder_path, model_size):
        import whisper
        from moviepy import VideoFileClip

        if not os.path.isdir(folder_path):
            self.log("❌ 유효한 폴더를 선택하세요.")
            return

        files = [f for f in os.listdir(folder_path) if f.endswith(".mp4")]
        if not files:
            self.log("❌ MP4 파일이 없습니다.")
            return

        self.log(f"📂 총 {len(files)}개 MP4 파일 변환 시작...")
        model = whisper.load_model(model_size)

        for filename in files:
            try:
                full_path = os.path.join(folder_path, filename)
                self.log(f"▶ 처리 중: {filename}")

                base, _ = os.path.splitext(full_path)
                wav_path = base + ".wav"

                video = VideoFileClip(full_path)
                video.audio.write_audiofile(wav_path)

                result = model.transcribe(wav_path, language="Korean")
                transcription = result["text"]

                txt_path = base + "_transcription.txt"
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(transcription)

                self.log(f"✅ 저장 완료: {os.path.basename(txt_path)}")

            except Exception as e:
                self.log(f"⚠️ 오류 발생: {str(e)}")

        self.log("\n🎉 모든 파일 처리 완료!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExeReadyTranscriberApp(root)
    root.mainloop()
