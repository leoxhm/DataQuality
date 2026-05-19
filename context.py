from config import Config

class QCContext:
    def __init__(self, config: Config):
        self.config = config
        self.data = {}      # dataset 输出
        self.metric = {}    # metric 结果
        self.cache = {}     # 中间缓存