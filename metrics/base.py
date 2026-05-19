
METRIC_REGISTRY = {}

def register_metric(cls):
    METRIC_REGISTRY[cls.name] = cls
    return cls

class BaseMetric:

    name = None
    category = None

    def calculate(self, ctx):
        raise NotImplementedError

    def run(self, ctx):
        try:
            self.calculate(ctx)

        except Exception as e:
            self.log.error(
                f"{self.name} 计算失败: {str(e)}",
                exc_info=True
            )
            ctx.metric[self.name] = 0