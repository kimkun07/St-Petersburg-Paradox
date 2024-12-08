from PyInquirer import prompt


def _do_prompt(question: dict) -> str:
    questions = [{**question, "name": "QUESTION"}]
    answers = prompt(questions)
    return answers["QUESTION"]


def prompt_input(message: str, default: str):
    return _do_prompt({"type": "input", "message": message, "default": default})


def prompt_list(message: str, choices: list[str]):
    return _do_prompt(
        {
            "type": "list",
            "message": message,
            "choices": choices,
        }
    )
