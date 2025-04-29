import logging
import os

def setup_logger(name: str, log_dir="logs"):
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, f"{name}.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 중복 핸들러 방지
    if not logger.handlers:
        file_handler = logging.FileHandler(log_path, mode='a', encoding='utf-8')  # ★ UTF-8 인코딩 + append 모드
        formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
