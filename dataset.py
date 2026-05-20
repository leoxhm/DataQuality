import os
import pandas as pd
from config import Config
from logger import TaskLogger, log

class QCDataset(object):

    def __init__(self, ctx, logger):
        self.ctx = ctx
        self.log = logger
        self.base_path = ctx.config.path
        self.files = {
            "fields": ctx.config.qc_files[0],
            "product": ctx.config.qc_files[1],
            "sample": ctx.config.qc_files[2]
        }

    def load(self):

        self.log.major_step(1, "Loading Dataset")

        for i, (k, f) in enumerate(self.files.items(), 1):

            try:
                self.log.minor_step(1, i, "Loading {}".format(k))
                path = os.path.join(self.base_path, f)
                self.ctx.data[k] = pd.read_csv(path)

                self.log.info(
                    "{} shape={}".format(
                        k,
                        self.ctx.data[k].shape
                    )
                )

            except Exception as e:
                self.log.error(
                    "LOAD {}".format(k),
                    str(e)
                )

                raise