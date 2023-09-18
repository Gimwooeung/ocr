# 기반 이미지 설정
FROM python:3.9.13

# 환경 변수 설정 (버퍼를 사용하지 않도록 설정)
ENV PYTHONUNBUFFERED 1

# 작업 디렉토리 생성 및 설정
WORKDIR /ocr

# 필요한 패키지 설치 및 pip 업그레이드
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# 프로젝트 코드를 도커 컨테이너에 복사
COPY . .

# 포트 8000을 사용하도록 명시
EXPOSE 8001

# 서버 실행 명령어
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]