from dataclasses import dataclass
from math import isfinite

from scripts.Engine_search import Search
from scripts.planner import Planner
from scripts.evidence.fetcher import ResearchTask, collect
from scripts.stripper import strip
from scripts.evidence.collector import Collected


@dataclass
class EvidenceData:
    task_id: str
    toVerify: str
    url: str
    title: str
    passage: str
    score: float
    side: str


@dataclass
class EvidenceBundle:
    task_id: str
    toVerify: str
    supporting: list[EvidenceData]
    opposing: list[EvidenceData]
    task: ResearchTask | None = None


class Evidence:
    def __init__(self, querry: str):
        self.querry = querry
        self.resScore = []
        self.resSearch = []

    def ranState(self) -> list[EvidenceBundle]:
        tasks = collect(
            search=Search,
            planner=Planner,
            query=self.querry,
        ).searcher()

        self.resScore = []
        self.resSearch = []
        return [self.research_task(task) for task in tasks]

    def research_task(self, task: ResearchTask) -> EvidenceBundle:
        """Fetch fresh evidence for an existing planned claim."""
        sides = {}

        for side, plan in (
            ("supporting", task.supporting_evidence_plan),
            ("opposing", task.opposing_evidence_plan),
        ):
            urls = []
            seen = set()
            for query in plan.search_queries or task.keyword:
                for result in Search(query, 5).ddg() or []:
                    url = result.get("href")
                    if url and url not in seen:
                        seen.add(url)
                        urls.append(url)

            documents = []
            document_urls = []
            for url in urls:
                passage = strip(link=url)
                if passage:
                    document_urls.append(url)
                    documents.append(passage)

            sides[side] = []
            if not documents:
                continue

            query = " ".join(plan.retrieval_hints) or task.claim_to_verify
            scores = Collected(doc=documents, query=query).find()
            numeric_scores = [float(score) for score in scores]
            self.resSearch.extend(documents)
            self.resScore.extend(numeric_scores)

            ranked_indexes = sorted(
                range(len(documents)),
                key=lambda index: (
                    numeric_scores[index]
                    if isfinite(numeric_scores[index])
                    else float("-inf")
                ),
                reverse=True,
            )

            for index in ranked_indexes[:5]:
                score = numeric_scores[index]
                if not isfinite(score):
                    continue
                sides[side].append(EvidenceData(
                    task_id=task.id,
                    toVerify=task.claim_to_verify,
                    url=document_urls[index],
                    title=task.objective,
                    passage=documents[index],
                    score=score,
                    side=side,
                ))

        return EvidenceBundle(
            task_id=task.id,
            toVerify=task.claim_to_verify,
            supporting=sides["supporting"],
            opposing=sides["opposing"],
            task=task,
        )
