import sys

from scripts.evidence.extractor import Evidence


def main():
    query = " ".join(sys.argv[1:]).strip()
    if not query:
        try:
            query = input("Enter your target query: ").strip()
        except EOFError:
            query = ""
    if not query:
        print("Please enter a query or pass one as a command line argument.")
        return

    bundles = Evidence(querry=query).ranState()
    if not bundles:
        print("No research tasks found.")
        return

    for bundle in bundles:
        print(f"\n{bundle.task_id}: {bundle.toVerify}")
        for side, items in (
            ("Supporting", bundle.supporting),
            ("Opposing", bundle.opposing),
        ):
            print(f"{side} evidence:")
            if not items:
                print("  No readable search results.")
                continue
            for item in items:
                excerpt = item.passage[:300]
                if len(item.passage) > 300:
                    excerpt += "..."
                print(f"  Score: {item.score:.3f} | {item.url}")
                print(f"  {excerpt}")


if __name__ == "__main__":
    main()
