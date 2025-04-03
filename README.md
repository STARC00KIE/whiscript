# Whiscript 🎧📄  
Whiscript는 MP4 동영상의 음성을 추출하여, OpenAI Whisper를 이용해 텍스트(.txt)로 자동 변환해주는 GUI 앱입니다.

---

## 📖 소개  
Whiscript는 누구나 쉽게 사용할 수 있는 **Whisper 기반 음성 → 텍스트 변환기**입니다.  
Python이 설치되어 있지 않아도 `.exe` 버전으로 실행 가능하며, 번역, 강의 정리, 회의록 자동화에 활용할 수 있습니다.

---

## 🎯 주요 기능
- ✅ MP4 → WAV → TXT 자동 변환
- ✅ Whisper 모델 선택 (`base`, `small`, `medium`, `large-v3`)
- ✅ GUI 제공 – 클릭 몇 번으로 쉽게 사용 가능
- ✅ 라이브러리 자동 설치
- ✅ 변환 진행 로그 출력
- ✅ .exe 빌드 지원

---

## 🚀 사용 방법
1. 프로그램 실행
2. MP4 폴더 선택
3. Whisper 모델 선택
4. [🟢 변환 시작] 클릭
5. 결과는 동일한 폴더에 `.txt`로 저장됩니다

---

## ⚙️ 설치 방법 (Python)
```bash
pip install moviepy
pip install git+https://github.com/openai/whisper.git
```
또는 exe 파일을 사용하세요 (배포 링크 추가 예정)

---

## 🧱 기술 스택
- Python 3.x
- Tkinter
- MoviePy
- Whisper (OpenAI)
- PyInstaller

---

## 📦 향후 기능
- .srt 자막 생성 기능
- 다국어 자동 감지
- 자동 번역 기능 (Korean → English)

---

## 📄 라이선스
MIT License  
Whisper는 [OpenAI Whisper](https://github.com/openai/whisper)를 기반으로 합니다.

