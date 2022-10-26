from typing import List, Any
from datetime import datetime


class CompletedBy:
    id: int
    first_name: str
    last_name: str
    avatar: None
    email: str
    initials: str

    def __init__(self, id: int) -> None:
        self.id = id
        self.first_name = ""
        self.last_name = ""
        self.avatar = None
        self.email = "bparikh@andrew.cmu.edu"
        self.initials = "bp"


class Value:
    start: int
    end: int
    text: str
    labels: List[str]

    def __init__(self, start: int, end: int, text: str, labels: List[str]) -> None:
        self.start = start
        self.end = end
        self.text = text
        self.labels = labels


class Result:
    value: Value
    id: str
    from_name: str
    to_name: str
    type: str
    origin: str

    def __init__(self, value: Value, id: str) -> None:
        self.value = value
        self.id = id
        self.from_name = "label"
        self.to_name = "text"
        self.type = "labels"
        self.origin = "manual"


class Annotation:
    id: int
    created_username: str
    created_ago: str
    completed_by: CompletedBy
    result: List[Result]
    was_cancelled: bool
    ground_truth: bool
    created_at: datetime
    updated_at: datetime
    lead_time: float
    task: int
    parent_prediction: None
    parent_annotation: None

    def __init__(self, id: int, completed_by: CompletedBy, result: List[Result]) -> None:
        self.id = id
        self.created_username = " bparikh@andrew.cmu.edu, " + str(id)
        self.created_ago = "1 minute"
        self.completed_by = completed_by
        self.result = result
        self.was_cancelled = False
        self.ground_truth = False
        self.created_at = "2022-10-20T05:43:33.793638Z"
        self.updated_at = "2022-10-20T05:43:33.793638Z"
        self.lead_time = 69.420
        self.task = id
        self.parent_prediction = None
        self.parent_annotation = None

class Data:
    text: str
    paperid: int

    def __init__(self, text: str, paperid: int) -> None:
        self.text = text
        self.paperid = paperid

class LabelStudio:
    id: int
    data: Data
    annotations: List[Annotation]
    predictions: List[Any]

    def __init__(self, id: int, data: Data, annotations: List[Annotation], predictions: List[Any]) -> None:
        self.id = id
        self.data = data
        self.annotations = annotations
        self.predictions = predictions

