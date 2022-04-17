import logging


# Basic logging config info
log_format = "%(asctime)s - %(name)s.%(filename)s - %(levelname)s - %(message)s"
level = logging.INFO

# Create logger for stock trading model (stm)
default_logger_name = "chatbot"
logger = logging.getLogger(default_logger_name)
logger.setLevel(level)

# Create console handler to print all loggers
console = logging.StreamHandler()
console.setLevel(level)
console.setFormatter(logging.Formatter(log_format))

# Add console handler and disable logging from root handler
logger.propagate = False
logger.addHandler(console)
