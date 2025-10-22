from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

@dataclass
class School:

    school_id: UUID
    school_name: str
    level: str | None = None
    province: str | None = None
    city: str | None = None
    subdistrict: str | None = None
    created_at: datetime = datetime.utcnow()

    @staticmethod
    def create(school_name: str, level: str = None, province: str = None,
               city: str = None, subdistrict: str = None) -> "School":

        return School(
            school_id=uuid4(),
            school_name=school_name,
            level=level,
            province=province,
            city=city,
            subdistrict=subdistrict
        )
