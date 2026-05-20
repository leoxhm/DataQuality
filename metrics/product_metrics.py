from metrics.base import BaseMetric, register_metric
import pandas as pd

@register_metric(priority=1)
class SamplePartitionIndex(BaseMetric):
    name = "样本分区"
    category = "prod"

    def calculate(self, ctx):
        sample_partition_df = pd.merge(
            ctx.data["sample"][
                ["backtrack_dt", "sample_count", "bucket_0_cnt"]
            ],
            ctx.data["product"],
            how="left",
            on="backtrack_dt"
        )

        sample_partition_df["sample_match_card_count"] = (
                    sample_partition_df["sample_count"] - sample_partition_df["bucket_0_cnt"]) #样本人卡查得数
        sample_partition_df["sample_match_card_rate"] = (
                    sample_partition_df["sample_match_card_count"] / sample_partition_df["sample_count"]) #人卡查得率
        sample_partition_df["sample_match_prod_rate"] = (
                    sample_partition_df["non_empty_count"] / sample_partition_df["sample_count"]) #产品查得率
        sample_partition_df["card_prod_loss_rate"] = (
                sample_partition_df["sample_match_card_rate"] - sample_partition_df["sample_match_prod_rate"])  #人卡查得至产品查得损失
        ctx.cache[self.name] = sample_partition_df

@register_metric(priority=2, depend=["样本分区"])
class ProdMatchRateDetails(BaseMetric):
    name = "产品查得率细化指标"
    category = "prod"

    def calculate(self, ctx):
        _min = ctx.cache["样本分区"]["sample_match_prod_rate"].min()
        _max = ctx.cache["样本分区"]["sample_match_prod_rate"].max()
        _min_dt =  ctx.cache["样本分区"].loc[ ctx.cache["样本分区"]["sample_match_prod_rate"].idxmin(), "backtrack_dt"]
        _max_dt = ctx.cache["样本分区"].loc[ctx.cache["样本分区"]["sample_match_prod_rate"].idxmax(), "backtrack_dt"]
        diff = _max - _min
        growth_rate = diff / _min

        ctx.metric[self.name] = [_min, _min_dt, _max, _max_dt, diff, growth_rate]
