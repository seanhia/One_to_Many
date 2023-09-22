from orm_base import Base

class Section(Base):
    """A group of students that meet for instruction at a particular day and time, while still
    teaching the same subject. For example, Section 1 of CECS 323 meets on Mondays and Wednesdays
     at 3:30 whereas Section 2 meets at 12 noon."""
    __tablename__ = "sections"