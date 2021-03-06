# coding: utf-8
from datetime import datetime

from .log_record import LogRecord


class SmsLogRecord(LogRecord):
    """
    Notes
    -----
    SMS is only used for legacy systems in NWPC.
    So SMS log record is not maintained.
    """
    def __init__(self):
        LogRecord.__init__(self)

    def parse(self, line: str):
        self.log_record = line

        if not self.log_record.startswith("# "):
            """some line don't start with '# '

                exit

            just ignore it.
            """
            return

        start_pos = 2
        end_pos = line.find(":")
        self.log_type = line[start_pos:end_pos]

        start_pos = end_pos + 2
        end_pos = line.find("]", start_pos)
        if end_pos == -1:
            """some line is not like what we suppose it to be. Such as:

                # MSG:[02:50:38 22.10.2013] login:User nwp_sp@16239 with password from cma20n03
                readlists
                # MSG:[02:50:48 22.10.2013] logout:User nwp_sp@16239

            So we should check if the line starts with '#[...]'. If not, we don't parse it and just return.
            """
            return
        record_time_string = line[start_pos:end_pos]
        date_time = datetime.strptime(record_time_string, "%H:%M:%S %d.%m.%Y")
        self.date = date_time.date()
        self.time = date_time.time()

        start_pos = end_pos + 2
        end_pos = line.find(":", start_pos)
        if end_pos == -1:
            """
            some line is not like what we suppose it to be. Such as:

                # WAR:[21:05:13 25.9.2013] SCRIPT-NAME will return NULL, script is [/cma/g1/nwp_sp/SMSOUT/env_grib_v20/T639_ENV/gmf/12/upload/upload_003.sms]

            We need to check end_pos.
            """
            return
        self.command = line[start_pos:end_pos]

        if self.command in (
            "submitted",
            "active",
            "queued",
            "complete",
            "aborted",
            "suspend",
        ):
            start_pos = end_pos + 1
            end_pos = line.find(" ", start_pos)
            if end_pos == -1:
                self.node_path = line[start_pos:].strip()
            else:
                self.node_path = line[start_pos:end_pos]
                self.additional_information = line[end_pos + 1 :]

        elif self.command == "alter":
            start_pos = end_pos + 1
            pos = line.find(" [", start_pos)
            if pos != -1:
                self.node_path = line[start_pos:pos]
                start_pos = pos + 2
                end_pos = line.find("] ", start_pos)
                if end_pos != -1:
                    self.additional_information = line[start_pos:end_pos]

        elif self.command == "meter":
            if self.log_type != "ERR":
                start_pos = end_pos + 1
                end_pos = line.find(" ", start_pos)
                self.node_path = line[start_pos:end_pos]
                start_pos = end_pos + 4
                self.additional_information = line[start_pos:]
            else:
                start_pos = end_pos + 1
                if line[start_pos] == "/":
                    # ERR:[12:52:00 19.5.2014] meter:/gmf_gsi_v1r5/T639/06/dasrefresh:WaitingMins: 55 out of range [0 - 40]
                    end_pos = line.find(" ", start_pos)
                    if end_pos != -1 and line[end_pos - 1] == ":":
                        self.node_path = line[start_pos : end_pos - 1]
                        self.additional_information = line[end_pos + 1 :]
                else:
                    # ERR:[03:41:58 10.7.2014] meter:WaitingMins for /grapes_meso_v4_0/cold/00/pre_data/obs_get/aob_get:the node was not found:
                    pass

        elif self.command in ["begin", "autorepeat date"]:
            start_pos = end_pos + 1
            end_pos = line.find(" ", start_pos)
            self.node_path = line[start_pos:end_pos]

        elif self.command == "force" or self.command == "force(recursively)":
            start_pos = end_pos + 1
            end_pos = line.find(" ", start_pos)
            self.node_path = line[start_pos:end_pos]
            if line[end_pos : end_pos + 4] == " to ":
                start_pos = end_pos + 4
                end_pos = line.find(" ", start_pos)
                self.additional_information = line[start_pos:end_pos]

        elif self.command == "delete":
            start_pos = end_pos + 1
            end_pos = line.find(" ", start_pos)
            self.node_path = line[start_pos:end_pos]
            start_pos = end_pos + 1
            end_pos = line.find(" ", start_pos)
            self.additional_information = line[start_pos:end_pos]

        elif self.command in ["set", "clear"]:
            start_pos = end_pos + 1
            end_pos = line.find(":", start_pos)
            if end_pos != -1:
                self.node_path = line[start_pos:end_pos]
                self.additional_information = line[end_pos + 1 :]

        # WAR:[23:37:08 16.8.2015] requeue:/gmf_grapes_v1423/grapes_global/12/post/postp_084 from aborted
        # MSG:[23:37:08 16.8.2015] requeue:user nwp@5986333:/gmf_grapes_v1423/grapes_global/12/post/postp_084
        elif self.command == "requeue":
            start_pos = end_pos + 1
            if self.log_type == "WAR":
                end_pos = line.find(" ", start_pos)
                if end_pos != -1:
                    self.node_path = line[start_pos:end_pos]
                    start_pos = end_pos + 1
                    self.additional_information = line[start_pos:]
            elif self.log_type == "MSG":
                end_pos = line.find(":", start_pos)
                if end_pos != -1:
                    self.additional_information = line[start_pos:end_pos]
                    start_pos = end_pos + 1
                    self.node_path = line[start_pos:]