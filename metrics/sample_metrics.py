from metrics.base import BaseMetric, register_metric

@register_metric
class SampleNumMetric(BaseMetric):
    name = "样本量"
    category = "sample"

    def calculate(self, ctx):
        count = ctx.data["sample"].loc[ctx.data["sample"]["backtrack"] == "000001", "sample_count"].iloc[0]
        ctx.metric["样本量"] = count