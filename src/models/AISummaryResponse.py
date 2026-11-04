from typing import List

from pydantic import RootModel

from models.AISummary import AISummary

AISummaryResponse = RootModel[List[AISummary] | None]