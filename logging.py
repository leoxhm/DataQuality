import logging
import time
import sys

class TaskLogger(object):
    def __init__(self, name="DataTask", total_steps=4):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.total_steps = total_steps
        self.start_time = time.time()
        self.step_start_time = time.time()
        # 新增：专门用于记录小步骤的开始时间
        self.minor_start_time = time.time()

        if not self.logger.handlers:
            fmt = logging.Formatter('[%(asctime)s] %(message)s', '%H:%M:%S')
            sh = logging.StreamHandler(sys.stdout)
            sh.setFormatter(fmt)
            self.logger.addHandler(sh)

    def _to_str(self, msg):
        if isinstance(msg, unicode):
            return msg.encode('utf-8')
        return str(msg)

    def major_step(self, step_num, title):
        now = time.time()
        duration_msg = ""
        if step_num > 1:
            duration = now - self.step_start_time
            duration_msg = " (Last step took %.2fs)" % duration

        self.step_start_time = now
        # 重置 major_step 时，同时也重置 minor_start_time
        self.minor_start_time = now

        title = self._to_str(title).upper()
        divider = "=" * 60
        msg = "\n{0}\n[STEP {1}/{2}] >>> {3}{4}\n{0}".format(
            divider, step_num, self.total_steps, title, duration_msg
        )
        self.logger.info(msg)

    def minor_step(self, major_num, minor_num, msg):
        """
        小步骤：增加与上一个小步骤之间的耗时统计
        """
        now = time.time()
        # 如果不是该大步下的第一个小步，打印耗时
        duration_msg = ""
        if minor_num > 1:
            duration = now - self.minor_start_time
            duration_msg = " [%.2fs]" % duration

        self.minor_start_time = now
        msg = self._to_str(msg)
        # 将耗时显示在消息的前面或后面，这里建议放在中间，视觉更平衡
        self.logger.info("  |-- [{0}.{1}]{2} {3}...".format(major_num, minor_num, duration_msg, msg))

    def info(self, msg):
        """普通信息：增加进一步缩进"""
        msg = self._to_str(msg)
        self.logger.info("      > {0}".format(msg))

    def warn(self, msg):
        """警告：醒目但不破坏结构"""
        msg = self._to_str(msg)
        self.logger.warning("  [!] WARNING: {0}".format(msg))

    def error(self, action, err_msg):
        action = self._to_str(action).upper()
        err_msg = self._to_str(err_msg)
        total_duration = time.time() - self.start_time

        divider = "!" * 60
        # 将 total_duration 也放进 format 列表里
        msg = (u"\n{0}\n[ERROR] AT: {1}\nREASON: {2}\n"
               u"Total Runtime: {3:.2f}s\n{0}").format(
            divider, action, err_msg, total_duration
        )
        self.logger.error(self._to_str(msg))

log = TaskLogger(total_steps=9)