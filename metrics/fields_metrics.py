from metrics.base import BaseMetric, register_metric

@register_metric
class FieldNumMetric(BaseMetric):
    name = "字段数"
    category = "fields"

    def calculate(self, ctx):
        count = ctx.data["fields"].shape[0]
        ctx.metric[self.name] = count

@register_metric
class LossRateMetric(BaseMetric):
    name = "字段缺失率"
    category = "fields"

    def calculate(self, ctx):
        ctx.data["fields"]["loss_rate"] = ctx.data["non_null_count"] / ctx.metric["样本量"]

@register_metric
class LossRateOver50Proportion(BaseMetric):
    name = "字段缺失率高于50%占比"
    category = "fields"

    def calculate(self, ctx):
        count = (ctx.data["fields"]["loss_rate"] > 0.5).sum() / ctx.metric["样本量"]
        ctx.metric[self.name] = count

@register_metric
class LossRateOver80Proportion(BaseMetric):
    name = "字段缺失率高于80%占比"
    category = "fields"

    def calculate(self, ctx):
        count = (ctx.data["fields"]["loss_rate"] > 0.8).sum() / ctx.metric["样本量"]
        ctx.metric[self.name] = count

@register_metric
class LossRateOver99Proportion(BaseMetric):
    name = "字段缺失率高于99%占比"
    category = "fields"

    def calculate(self, ctx):
        count = (ctx.data["fields"]["loss_rate"] > 0.99).sum() / ctx.metric["样本量"]
        ctx.metric[self.name] = count

@register_metric
class FieldsNumNoDiffMetric(BaseMetric):
    name = "无差异字段数"
    category = "basic"

    def calculate(self, ctx):
        df = ctx.data["fields"]
        count = ((df["loss_rate"] < 1) & (df["min"] == df["max"])).sum()
        ctx.metric["self.name"] = count

