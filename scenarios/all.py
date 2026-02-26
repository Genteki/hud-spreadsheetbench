"""SpreadsheetBench HUD Environment"""

import logging
import sys
import os
from hud import Environment
import pandas as pd
from evaluate.eval_all import eval_all
from .prompts import PROMPT

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="[%(levelname)s] %(name)s | %(message)s",
    force=True,
)


env = Environment("spreadsheetbench")

max_turn_num = 100


def get_spreadsheet_content(input_file, num_rows=5):
    """Generate spreadsheet content preview"""
    excel_file = pd.ExcelFile(input_file)
    sheet_names = excel_file.sheet_names
    excel_data = {}

    for sheet_name in sheet_names:
        df = excel_file.parse(sheet_name)
        rows_to_show = num_rows if len(df) > num_rows else len(df)
        excel_data[sheet_name] = df.head(rows_to_show).to_string()

    final_str = ""
    for sheet_name, sheet_str in excel_data.items():
        final_str += f"Sheet Name: {sheet_name}\n"
        final_str += sheet_str + "\n"
        final_str += "-" * 50 + "\n"

    return final_str


def register_spreadsheetbench_all(env: Environment):
    @env.scenario("spreadsheetbench")
    async def spreadsheetbench(
        id: str,
        instruction: str,
        spreadsheet_path: str,
        instruction_type: str,
        answer_position: str,
    ):
        dataset_path = "all_data_912"
        spreadsheet_content = get_spreadsheet_content(os.path.join(dataset_path, spreadsheet_path, f"1_{id}_input.xlsx"))
        output_path = os.path.join(
            dataset_path, spreadsheet_path, f"1_{id}_output.xlsx"
        )
        
        prompt = PROMPT.format(instruction=instruction, spreadsheet_path=spreadsheet_path, spreadsheet_content=spreadsheet_content, instruction_type=instruction_type, answer_position=answer_position, output_path=output_path, max_turn_num=max_turn_num)
        yield prompt
        result = eval_all(id, answer_position, dataset_path)
        yield result

__all__ = ["register_spreadsheetbench_all"]
