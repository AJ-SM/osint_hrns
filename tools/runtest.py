import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agents.court import Court
from scripts.evidence.extractor import Evidence


BLUE = "\033[34m"
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"


def print_court_event(event, trial_no, value):
    if event == "retrial":
        print(f"\n  Retrial {trial_no}", flush=True)
    elif event == "researching":
        print("  Researching again...", flush=True)
    elif event == "court":
        print(f"  Court trial {trial_no}...", flush=True)
    elif event == "supporter":
        print(f"{BLUE}  Supporter argument: {value}{RESET}", flush=True)
    elif event == "opposition":
        print(f"{RED}  Opposition argument: {value}{RESET}", flush=True)
    elif event == "ruling":
        print("  Ruling...", flush=True)
    elif event == "judge":
        print(f"{GREEN}  Judge verdict: {value.verdict}{RESET}", flush=True)
        print(f"{GREEN}  Judge reasoning: {value.reasoning}{RESET}", flush=True)
        if value.need_more_evidence and value.research_gap:
            print(f"{GREEN}  Research gap: {value.research_gap}{RESET}", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Research a claim and run court trials.")
    parser.add_argument("query", nargs="*", help="Claim or question to research")
    parser.add_argument("--trials", type=int, help="Number of court trials (at least 1)")
    args = parser.parse_args()

    query = " ".join(args.query).strip()
    if not query:
        try:
            query = input("Enter your target query: ").strip()
        except EOFError:
            query = ""
    if not query:
        print("Please enter a query or pass one as a command line argument.")
        return

    if args.trials is None:
        try:
            trial_text = input("Enter number of trials: ").strip()
            no_of_trials = int(trial_text)
        except (EOFError, ValueError):
            parser.error("enter a whole number of trials or pass --trials N")
    else:
        no_of_trials = args.trials
    if no_of_trials < 1:
        parser.error("number of trials must be at least 1")

    print("Researching...", flush=True)
    research = Evidence(querry=query)
    bundles = research.ranState()
    if not bundles:
        print("No research tasks found.")
        return

    court = Court()
    for bundle in bundles:
        print(f"\n{bundle.task_id}: {bundle.toVerify}")
        state = court.trial(
            bundle,
            no_of_trials,
            on_event=print_court_event,
            refresh_evidence=lambda current: research.research_task(current.task),
        )
        winning_side = {
            "SUPPORTED": "supporting",
            "CONTRADICTED": "opposing",
        }.get(state.final_verdict, "no clear winner")
        print(
            f"  Final verdict: {state.final_verdict}\n"
            f"  Winning side: {winning_side}\n"
            f"  Conclusion: {state.conclusion}\n"
            f"  Trials run: {len(state.trials)}/{no_of_trials}\n"
            f"  Trial summary: supported={state.support_wins}, "
            f"contradicted={state.opposition_wins}, other={state.equal_trials}"
        )


if __name__ == "__main__":
    main()
