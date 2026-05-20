from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

METRIC_REGISTRY = {}

def register_metric(priority=100, depend=None):

    def decorator(cls):
        cls.priority = priority
        cls.depend = depend or []
        METRIC_REGISTRY[cls.name] = cls

        return cls

    return decorator

class BaseMetric:
    name = None
    category = None

    def __init__(self, logger=None):
        self.log = logger

    def calculate(self, ctx):
        raise NotImplementedError

    def run(self, ctx):
        try:
            result = self.calculate(ctx)
            ctx.metric[self.name] = result
            if self.log:
                self.log.info(f"{self.name} success")

        except Exception as e:
            if self.log:
                self.log.error(
                    f"{self.name} 计算失败: {str(e)}",
                    exc_info=True
                )
            ctx.metric[self.name] = 0

class MetricScheduler:

    def __init__(self, logger=None, max_workers=4):

        self.log = logger
        self.max_workers = max_workers

    def run(self, ctx):

        # 1. priority 分组
        priority_groups = defaultdict(list)

        for metric_cls in METRIC_REGISTRY.values():
            priority_groups[metric_cls.priority].append(metric_cls)

        # 2. 按 priority 顺序执行
        for priority in sorted(priority_groups.keys()):

            metric_classes = priority_groups[priority]

            if self.log:
                self.log.info(f"Running priority={priority}")

            # 3. 同 priority 并行
            with ThreadPoolExecutor(
                max_workers=self.max_workers
            ) as executor:

                futures = []

                for metric_cls in metric_classes:

                    # depend check
                    missing_dep = [
                        dep
                        for dep in metric_cls.depend
                        if dep not in ctx.metric
                    ]

                    if missing_dep:

                        if self.log:
                            self.log.error(
                                f"{metric_cls.name} 缺少依赖: {missing_dep}"
                            )

                        continue

                    metric = metric_cls(logger=self.log)

                    futures.append(
                        executor.submit(metric.run, ctx)
                    )

                for future in as_completed(futures):
                    future.result()