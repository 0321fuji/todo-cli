import argparse
import json
from pathlib import Path


# TODOデータを保存するファイルです。
TODO_FILE = Path(__file__).with_name("todos.json")


def load_todos():
    # 保存ファイルがまだない場合は、空のリストを返します。
    if not TODO_FILE.exists():
        return []

    # JSONファイルを読み込んで、Pythonのリストに変換します。
    with TODO_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_todos(todos):
    # PythonのリストをJSONとして保存します。
    with TODO_FILE.open("w", encoding="utf-8") as file:
        json.dump(todos, file, ensure_ascii=False, indent=2)


def add_todo(task_name):
    todos = load_todos()

    # 1件分のTODOデータを辞書として追加します。
    todos.append(
        {
            "task": task_name,
            "done": False,
        }
    )

    save_todos(todos)
    print(f'追加しました: "{task_name}"')


def list_todos():
    todos = load_todos()

    if not todos:
        print("TODOはまだありません。")
        return

    print("未完了:")
    has_undone = False
    for index, todo in enumerate(todos, start=1):
        if not todo["done"]:
            print(f"  {index}. {todo['task']}")
            has_undone = True

    if not has_undone:
        print("  なし")

    print("\n完了:")
    has_done = False
    for index, todo in enumerate(todos, start=1):
        if todo["done"]:
            print(f"  {index}. {todo['task']}")
            has_done = True

    if not has_done:
        print("  なし")


def mark_done(todo_number):
    todos = load_todos()

    if not todos:
        print("TODOがないため、完了にできません。")
        return

    # ユーザーは1番から数えるので、配列用に0番始まりへ変換します。
    index = todo_number - 1

    if index < 0 or index >= len(todos):
        print("その番号のTODOは存在しません。")
        return

    if todos[index]["done"]:
        print(f'すでに完了しています: "{todos[index]["task"]}"')
        return

    todos[index]["done"] = True
    save_todos(todos)
    print(f'完了にしました: "{todos[index]["task"]}"')


def create_parser():
    # コマンドライン引数の設定をここでまとめて行います。
    parser = argparse.ArgumentParser(description="シンプルなTODO管理CLIツール")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="新しいTODOを追加します")
    add_parser.add_argument("task_name", help='追加するタスク名 例: add "買い物をする"')

    subparsers.add_parser("list", help="TODO一覧を表示します")

    done_parser = subparsers.add_parser("done", help="指定した番号のTODOを完了にします")
    done_parser.add_argument("number", type=int, help="完了にするTODOの番号")

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "add":
        add_todo(args.task_name)
    elif args.command == "list":
        list_todos()
    elif args.command == "done":
        mark_done(args.number)


if __name__ == "__main__":
    main()
