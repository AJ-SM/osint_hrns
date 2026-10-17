from scripts.Engine_search import Search
from scripts.planner import Planner
from scripts.stripper import strip
from dataclasses import dataclass, field

@dataclass
class EvidencePlan:
    objective: str
    search_queries: list[str]
    retrieval_hints: list[str]


@dataclass
class ResearchTask:
    id: str
    keyword: list[str]

    objective: str
    claim_to_verify: str
    claim_type: str
    priority: str

    parallelizable: bool

    preferred_sources: list[str]

    supporting_evidence_plan: EvidencePlan
    opposing_evidence_plan: EvidencePlan

    requires_independent_verification: bool
    requires_primary_source: bool

    dependencies: list[str] = field(default_factory=list)
## Get the seraching urls 

test_url = "https://www.scaler.com/topics/artificial-intelligence-boon-or-bane/"
class collect:
    def __init__(self,search,planner,query):
        self.query= query
        self.search=search
        self.planner=planner()
        self.href=[]
        self.rest=[]

    def searcher(self):
        self.data = self.planner.paln(query=str(self.query))
        self.tasks = self.data["research_tasks"]
        if not self.tasks:
            raise ValueError("Planner returned no research task")
        self.rest = []
        for elements in self.tasks:
            task = ResearchTask(
                id=elements["id"],
                keyword=elements["keyword"],
                objective=elements["objective"],
                claim_to_verify=elements["claim_to_verify"],
                claim_type=elements["claim_type"],
                priority=elements["priority"],
                parallelizable=elements["parallelizable"],
                preferred_sources=elements["preferred_sources"],

                supporting_evidence_plan=EvidencePlan(
                    **elements["supporting_evidence_plan"]
                ),

                opposing_evidence_plan=EvidencePlan(
                    **elements["opposing_evidence_plan"]
                ),

                requires_independent_verification=elements["requires_independent_verification"],
                requires_primary_source=elements["requires_primary_source"],
                dependencies=elements["dependencies"],
            )
            self.rest.append(task)


        primary = self.rest[0]
        primary.id = "task_001"
        primary.objective = self.query
        primary.claim_to_verify = self.query
        primary.dependencies = []
        for extra in self.rest[1:]:
            for name in ("keyword", "preferred_sources"):
                values = getattr(primary, name)
                values.extend(value for value in getattr(extra, name) if value not in values)
            for side in ("supporting_evidence_plan", "opposing_evidence_plan"):
                base_plan = getattr(primary, side)
                extra_plan = getattr(extra, side)
                for name in ("search_queries", "retrieval_hints"):
                    values = getattr(base_plan, name)
                    values.extend(value for value in getattr(extra_plan, name) if value not in values)
            primary.requires_independent_verification |= extra.requires_independent_verification
            primary.requires_primary_source |= extra.requires_primary_source
        return [primary]


class fetch:
    def __init__(self,links:list,strip:callable=strip):
        self.link = links
        self.results = []
        self.strip = strip
        
    
    def information(self):
        for planLink in self.link:
            self.results.append(str(self.strip(link=planLink)))
        return self.results
        



