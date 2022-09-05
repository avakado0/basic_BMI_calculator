import logging
from pprint import pprint as pp
from modules.exceptions import InvalidJSONContent

class InfoLogger:
    def __init(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(process)d-%(levelname)s-%(message)s',
                            exc_info=True)
    def log(self, text):
        logging.info(text)
class WarningLogger:
    def __init__(self):
        logging.basicConfig(level=logging.WARNING,
                            format='%(process)d-%(levelname)s-%(message)s',
                            #exc_info=True
                            )
    def log(self, text):
        logging.warning(text)
    def fix_value(self, value_name):
        self.log(f"""Fix the value of {value_name} or remove the values 
                                                    belonging to that person""")

class ErrorLogger(InvalidJSONContent):
    def __init__(self):
        logging.basicConfig(level=logging.CRITICAL,
                            format='%(process)d-%(levelname)s-%(message)s',
                            exc_info=True)  
        self.warn = WarningLogger()      

    def log(self, text):
        logging.critical(text)

    def stop_and_warn(self, text):
        raise(InvalidJSONContent(text))
    def invalidBMI_warning(self):
        self.stop_and_warn(" Error : Wrong BMI format.")
    def zeroBMI_warning(self):
        self.stop_and_warn(" Error : A BMI with 0 value spotted. Check the input file content.")
    def invalid_input_for_BMI(self):
        self.stop_and_warn(" Error : W")
    def zeroBMI_input_warning(self, value_name):
        self.warn.fix_value(value_name)
        self.stop_and_warn(f""" Error : - BMI couldn't be calculated. 
                                       - {value_name} value for a person in input file
                                       is 0""")
        
                                


class Logger(InfoLogger, WarningLogger,ErrorLogger):
    def __init__(self):
        self.info = InfoLogger()
        self.warning = WarningLogger()
        self.error_ = ErrorLogger()
    def info(self, text):
        return self.info.log(text)
    def warning(self, text):
        return self.warning(text)
    def error(self, text):
        output_text = f"""---ERROR---  
                     ~~~
                                                            ~~~
                        {text}    ~~~
                                                        ~~~
                                                    ~~~
                             ~~~~~~~~~~~~~~~~~~~~~~~~"""
        return self.error_.log(output_text)

    def stopwarn(self, text):
        self.error_.stop_and_warn(text)
