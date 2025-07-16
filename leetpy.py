import subprocess
import sys
import time

def install_package(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

try:
    import requests
except ImportError:
    print("requests module is not installed. Installing...")
    install_package("requests")
    import requests

try:
    from tkinterweb import HtmlFrame
except ImportError:
    print("tkinterweb module is not installed. Installing...")
    install_package("tkinterweb")
    from tkinterweb import HtmlFrame

import tkinter as tk
from tkinterweb import HtmlFrame
import random
import threading


open_windows = 0
lock = threading.Lock()
class Problem:
    def __init__(self, problem_id, title, difficulty, description):
        self.problem_id = problem_id
        self.title = title
        self.difficulty = difficulty
        self.description = description

    


    def show(self):
        def run_gui():
            global open_windows
            with lock:
                open_windows += 1

            root = tk.Tk()
            root.title(f"{self.title} ({self.difficulty})")
            root.geometry("900x700")

            html_frame = HtmlFrame(root, messages_enabled=False)
            html_frame.load_html(f"<h1>{self.title} ({self.difficulty})</h1>{self.description}")
            html_frame.pack(fill="both", expand=True)

            def on_close():
                global open_windows
                with lock:
                    open_windows -= 1
                root.destroy()

            root.protocol("WM_DELETE_WINDOW", on_close)
            root.mainloop()

        threading.Thread(target=run_gui).start()


def get_problem(problem_id=None):
    """
    Fetches the problem details from LeetCode given a problem ID or name.
    If no ID is provided, fetches a random free problem.
    """
    import random
    url = "https://leetcode.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    if problem_id is None:
        # Step 1: Fetch a batch of problems
        query_batch = """
        query problemsetQuestionListV2($limit: Int, $skip: Int, $filters: QuestionFilterInput) {
          problemsetQuestionListV2(categorySlug: "", limit: $limit, skip: $skip, filters: $filters) {
            questions {
              titleSlug
              paidOnly
            }
          }
        }
        """
        

        response = requests.post(url, json={"query": query_batch}, headers=headers)
        try:
            questions = response.json()["data"]["problemsetQuestionListV2"]["questions"]
            free_questions = [q for q in questions if not q["paidOnly"]]
            if not free_questions:
                print("no free problems available.")
                return None
            problem_id = random.choice(free_questions)["titleSlug"]
        except KeyError:
            print("failed (random).")
            print("Response:", response.json())
            return None

    # Step 2: Fetch full problem details
    query_detail = """
    query getQuestionDetail($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionId
        title
        content
        difficulty
      }
    }
    """
    response = requests.post(url, json={"query": query_detail, "variables": {"titleSlug": problem_id}}, headers=headers)
    try:
        q = response.json()["data"]["question"]
        return Problem(q["questionId"], q["title"], q["difficulty"], q["content"])
    except KeyError:
        print("failed.")
        print("Response:", response.json())
        return None



def get_daily_problem():
    """
    Fetches the daily LeetCode problem.
    """
    url = "https://leetcode.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    query = """
    query questionOfToday {
      activeDailyCodingChallengeQuestion {
        question {
          questionId
          title
          titleSlug
          content
          difficulty
        }
      }
    }
    """

    response = requests.post(url, json={"query": query}, headers=headers)
    data = response.json()

    if "data" in data and data["data"]["activeDailyCodingChallengeQuestion"]:
        q = data["data"]["activeDailyCodingChallengeQuestion"]["question"]
        return Problem(q["questionId"], q["title"], q["difficulty"], q["content"])
    else:
        print("failed (daily).")
        return None

def solve(problem):
    """
    Placeholder for solution fetching logic.
    """
    return f"# Solution for {problem.title} (ID: {problem.problem_id})\n\n# TODO: Implement solution fetching."

def submit_problem(problem, solution):
    """
    Placeholder for solution submission logic.
    """
    print(f"Submitting solution for {problem.title} (ID: {problem.problem_id})")
    print("Solution content:")
    print(solution)
    return True  # Simulate successful submission


def wait_for_all_windows_to_close():
    """Blocks until all Tkinter windows are closed."""
    while True:
        with lock:
            if open_windows == 0:
                break
        time.sleep(0.5)
