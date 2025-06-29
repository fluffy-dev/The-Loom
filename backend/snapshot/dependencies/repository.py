from fastapi import Depends
from typing import Annotated

from backend.snapshot.repositories.snapshot import SnapshotRepository

ISnapshotRepository = Annotated[SnapshotRepository, Depends()]