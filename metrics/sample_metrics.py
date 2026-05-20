from metrics.base import BaseMetric, register_metric
import pandas as pd

@register_metric(priority=1)
class AvgCardNumDetails(BaseMetric):
    name = "平均持卡量细化指标"
    category = "sample"

    def calculate(self, ctx):
        _min = ctx.data["sample"]["avg_card_count"].min()
        _min_dt = ctx.data["sample"].loc[ctx.data["sample"]["avg_card_count"].idxmin(), "backtrack_dt"]
        _max = ctx.data["sample"]["avg_card_count"].max()
        _max_dt = ctx.data["sample"].loc[ctx.data["sample"]["avg_card_count"].idxmax(), "backtrack_dt"]
        diff = _max - _min
        growth_rate = diff / _min

        ctx.metric[self.name] = [_min, _min_dt, _max, _max_dt, diff, growth_rate]

@register_metric(priority=1)
class AvgEffCardNumDetails(BaseMetric):
    name = "平均有效持卡量细化指标"
    category = "sample"

    def calculate(self, ctx):
        _min = ctx.data["sample"]["avg_eff_card_count"].min()
        _min_dt = ctx.data["sample"].loc[ctx.data["sample"]["avg_eff_card_count"].idxmin(), "backtrack_dt"]
        _max = ctx.data["sample"]["avg_eff_card_count"].max()
        _max_dt = ctx.data["sample"].loc[ctx.data["sample"]["avg_eff_card_count"].idxmax(), "backtrack_dt"]
        diff = _max - _min
        growth_rate = diff / _min

        ctx.metric[self.name] = [_min, _min_dt, _max, _max_dt, diff, growth_rate]

@register_metric(priority=2, depend=["样本分区"])
class CardMatchRateDetails(BaseMetric):
    name = "人卡查得率细化指标"
    category = "sample"

    def calculate(self, ctx):
        _min = ctx.cache["样本分区"]["sample_match_card_rate"].min()
        _max = ctx.cache["样本分区"]["sample_match_card_rate"].max()
        _min_dt = ctx.cache["样本分区"].loc[ctx.cache["样本分区"]["sample_match_card_rate"].idxmin(), "backtrack_dt"]
        _max_dt = ctx.cache["样本分区"].loc[ctx.cache["样本分区"]["sample_match_card_rate"].idxmax(), "backtrack_dt"]
        diff = _max - _min
        growth_rate = diff / _min

        ctx.metric[self.name] = [_min, _min_dt, _max, _max_dt, diff, growth_rate]

@register_metric(priority=1)
class CardLossDetails(BaseMetric):
    name = "渠道卡至有效卡损失细化指标"
    category = "sample"

    def calculate(self, ctx):
        ctx.data["sample"]["card_loss"] = ctx.data["sample"]["avg_card_count"] - ctx.data["sample"]["avg_eff_card_count"]
        _min = ctx.data["sample"]["card_loss"].min()
        _max = ctx.data["sample"]["card_loss"].max()
        _min_dt = ctx.data["sample"].loc[ctx.data["sample"]["card_loss"].idxmin(), "backtrack_dt"]
        _max_dt = ctx.data["sample"].loc[ctx.data["sample"]["card_loss"].idxmax(), "backtrack_dt"]
        diff = _max - _min
        growth_rate = diff / _min

        ctx.metric[self.name] = [_min, _min_dt, _max, _max_dt, diff, growth_rate]

@register_metric(priority=2, depend=["样本分区"])
class CardProdLossRateDetails(BaseMetric):
    name = "人卡查得至产品查得损失细化指标"
    category = "sample"

    def calculate(self, ctx):
        _min = ctx.cache["样本分区"]["card_prod_loss_rate"].min()
        _max = ctx.cache["样本分区"]["card_prod_loss_rate"].max()
        _min_dt = ctx.cache["样本分区"].loc[ctx.cache["样本分区"]["card_prod_loss_rate"].idxmin(), "backtrack_dt"]
        _max_dt = ctx.cache["样本分区"].loc[ctx.cache["样本分区"]["card_prod_loss_rate"].idxmax(), "backtrack_dt"]
        diff = _max - _min
        growth_rate = diff / _min

        ctx.metric[self.name] = [_min, _min_dt, _max, _max_dt, diff, growth_rate]

@register_metric(priority=2, depend=["样本分区"])
class CardMatchRateLowNum(BaseMetric):
    name = "人卡查得率偏低分区数"
    category = "sample"

    def calculate(self, ctx):
        val = (ctx.cache["样本分区"]["sample_match_card_rate"] < 0.9).sum()
        ctx.metric[self.name] = val

@register_metric(priority=1)
class SampleNum(BaseMetric):
    name = "样本量"
    category = "sample"

    def calculate(self, ctx):
        count = ctx.data["sample"].loc[ctx.data["sample"]["backtrack_dt"] == "000001", "sample_count"].iloc[0]
        ctx.metric[self.name] = count

@register_metric(priority=2, depend=["样本量"])
class SampleMatchCardNum(BaseMetric):
    name = "查得卡样本量"
    category = "sample"

    def calculate(self, ctx):
        count = ctx.metric["样本量"] - ctx.data["sample"].loc[ctx.data["sample"]["backtrack_dt"] == "000001", "bucket_0_cnt"].iloc[0]
        ctx.metric[self.name] = count

@register_metric(priority=1)
class SampleMatchProdNum(BaseMetric):
    name = "查得产品样本量"
    category = "sample"

    def calculate(self, ctx):
        count = ctx.data["fields"].loc[ctx.data["fields"]["column"] == "sample", "non_null_count"].iloc[0]
        ctx.metric[self.name] = count

@register_metric(priority=1)
class AvgCardNum(BaseMetric):
    name = "主键平均持卡数"
    category = "sample"

    def calculate(self, ctx):
        count = ctx.data["sample"].loc[ctx.data["sample"]["backtrack_dt"] == "000001", "avg_card_count"].iloc[0]
        ctx.metric[self.name] = count

@register_metric(priority=1)
class AvgEffCardNum(BaseMetric):
    name = "主键平均有效持卡数"
    category = "sample"

    def calculate(self, ctx):
        count = ctx.data["sample"].loc[ctx.data["sample"]["backtrack_dt"] == "000001", "avg_eff_card_count"].iloc[0]
        ctx.metric[self.name] = count

@register_metric(priority=1)
class MaxCardNum(BaseMetric):
    name = "主键最大持卡数"
    category = "sample"

    def calculate(self, ctx):
        count = ctx.data["sample"].loc[ctx.data["sample"]["backtrack_dt"] == "000001", "max_card_count"].iloc[0]
        ctx.metric[self.name] = count

@register_metric(priority=2, depend=["样本分区"])
class SampleNumTop5(BaseMetric):
    name = "样本数量top5"
    category = "sample"

    def calculate(self, ctx):

        sample_partition_df = pd.merge(
            ctx.data["sample"][
                ["backtrack_dt", "sample_count", "bucket_0_cnt"]
            ],
            ctx.data["prod"],
            how="left",
            on="backtrack_dt"
        )

        sample_partition_df["sample_match_card_count"] = (sample_partition_df["sample_count"] - sample_partition_df["bucket_0_cnt"])
        sample_partition_df["sample_match_prod_count"] = (sample_partition_df["non_empty_count"] / sample_partition_df["sample_count"])
        ctx.cache["样本分区"] = sample_partition_df
        top5_df = ctx.cache["样本分区"][
            [
                "backtrack_dt",
                "sample_count",
                "sample_match_card_count",
                "non_empty_count",
                "sample_match_prod_rate"
            ]
        ].sort_values("sample_count", ascending=False).head(5)

        return top5_df

@register_metric(priority=2, depend=["样本分区"])
class SampleNumLast5(BaseMetric):
    name = "样本数量last5"
    category = "sample"

    def calculate(self, ctx):
        last5_df = ctx.cache["样本分区"][
            [
                "backtrack_dt",
                "sample_count",
                "sample_match_card_count",
                "non_empty_count",
                "sample_match_prod_rate"
            ]
        ].sort_values("sample_count", ascending=True).head(5)

        return last5_df

@register_metric(priority=2, depend=["样本分区"])
class ProdNumTop5(BaseMetric):
    name = "产品查得top5"
    category = "sample"

    def calculate(self, ctx):
        last5_df = ctx.cache["样本分区"][
            [
                "backtrack_dt",
                "sample_count",
                "sample_match_card_count",
                "non_empty_count",
                "sample_match_prod_rate"
            ]
        ].sort_values("non_empty_count", ascending=False).head(5)

        return last5_df

@register_metric(priority=2, depend=["样本分区"])
class ProdNumLast5(BaseMetric):
    name = "产品查得last5"
    category = "sample"

    def calculate(self, ctx):
        last5_df = ctx.cache["样本分区"][
            [
                "backtrack_dt",
                "sample_count",
                "sample_match_card_count",
                "non_empty_count",
                "sample_match_prod_rate"
            ]
        ].sort_values("non_empty_count", ascending=True).head(5)

        return last5_df
