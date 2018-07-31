import os
import sys

Base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,Base_path)


from core.getGYAS import getGYAS_run
from core.ExcelGYAS import ExcelGYAS_run

if __name__ == "__main__":
    getGYAS_run()
    ExcelGYAS_run()