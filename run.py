from config import Config
from context import QCContext
from dataset import QCDataset

# 触发 metric 注册
import metrics

from metrics.base import MetricScheduler
from logger import TaskLogger


def main():

    # 1. logger
    log = TaskLogger("qc_task")

    # 2. config
    config = Config(
        uuid="test_001",
        path="./",
        data_file="",
        qc_files=[
            "multi_key_vars_qc1.csv",
            "multi_key_vars_qc2.csv",
            "idcard_qc_M-2-1.csv"
        ],
        name_user="test_user",
        name_domain="test_domain",
        name_cust="test_cust",
        bus_dt="20260520",
        backtrack="000001",
        dmd3t="demo",
        table_nm="test_table"
    )

    # 3. context
    ctx = QCContext(config)

    # 4. dataset load
    dataset = QCDataset(ctx, log)
    dataset.load()

    # 5. metric scheduler
    scheduler = MetricScheduler(
        logger=log,
        max_workers=4
    )

    scheduler.run(ctx)

    # 6. print result
    print("\n===== metric result =====")

    for k, v in ctx.metric.items():

        print("\n--------------------")
        print(f"{k}:")

        if hasattr(v, "shape"):
            print(v)
        else:
            print(v)


if __name__ == "__main__":
    main()