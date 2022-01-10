# SplitWise-Costs
Compute the cost of each individual from a SplitWise exported csv

## Operating Assumption
*Only 1 person has paid in each expanse line, this person is identifiable by a positive cost in the expanse line*

*Only 1 currency is used in the csv*; this assumption could be lifted but I'm not bothering for now

*The first float of each line is the total cost of the line (we can't rely on column labels because the csv is translated to user language)*
