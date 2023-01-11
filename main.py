import os
from typing import List
from uuid import uuid4
import json

with open("journal.txt") as journal_handle:
    journal_lines: List[str] = journal_handle.readlines()
    journal_lines = [journal_line.strip('\n') for journal_line in journal_lines]

collections = dict()

for line_no, journal_line in enumerate(journal_lines):
    tokens = journal_line.split(';')
    command = tokens[0]
    trailing = tokens[1:]

    if command not in ['C', 'P']:
        print(f"Invalid Command at line {line_no}")
        print(f"Cancelling update; fix journal before continuing.")
        exit(2)

    if command == "C":
        if '#' == trailing[-1][0]:
            label = trailing[-1][1:]
            trailing.pop(-1)
        else:
            label = str(uuid4())
            if ";" == trailing[-1][-1]:
                journal_line += f"#{label}"
            else:
                journal_line += f";#{label}"
            journal_lines[line_no] = journal_line
        collections[label] = list()

    elif command == "P":
        try:
            push_to: str = trailing[0]
            try:
                to_push: dict = json.loads(trailing[1])
                try:
                    doc_id = to_push['doc_id']
                except KeyError:
                    if '#' == trailing[-1][0]:
                        doc_id = trailing[-1][1:]
                        trailing.pop(-1)
                    else:
                        doc_id = str(uuid4())
                        if ";" == trailing[-1][-1]:
                            journal_line += f"#{doc_id}"
                        else:
                            journal_line += f";#{doc_id}"
                        journal_lines[line_no] = journal_line
                    to_push['doc_id'] = doc_id

                collections[push_to].append(to_push)

            except json.JSONDecodeError as e:
                print(e.msg)
                print(e.args)
                print(f"Invalid JSON at line {line_no}")
                print(f"Cancelling update; fix journal before continuing.")
                exit(2)
            except IndexError:
                print(f"Missing JSON at line {line_no}")
                print(f"Cancelling update; fix journal before continuing.")
                exit(2)
            except KeyError:
                print(f"Invalid Collection at line {line_no}")
                print(f"Cancelling update; fix journal before continuing.")
                exit(2)
        except IndexError:
            print(f"Missing Collection Label at line {line_no}")
            print(f"Cancelling update; fix journal before continuing.")
            exit(2)

os.remove('./journal.txt')
print(journal_lines)
with open('./journal.txt', 'w') as journal_handle:
    journal_lines = [journal_line + "\n" for journal_line in journal_lines]
    journal_handle.writelines(journal_lines)
print("Written Amended Journal.")