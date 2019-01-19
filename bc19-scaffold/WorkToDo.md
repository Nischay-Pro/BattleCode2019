
TODO - Do an all check of which function should check of len(a) != 0 or check for a != None
TODO - Check that tuple == tuple is not happening as bc19 cant handle that(sigh , convert tos tr first
TODO - Manage special cases like seed 30
TODO - Make combat units not step on mines by default
TODO - Production module should take k=note of map initial karb/initial fuel ratio
TODO - Since we can now store change in karbonite/fuel, use this for decision making
TODO - The enemies strategy can be read by using the step number of the enemy


New idea for production of pilgrims -
    Castles make one pilgrim per resource rich area (they have to divide zones somehow and allocate pilgrims) (see mapping.py) and send them off
    They also make pilgrims for all mines within convoy distance
    And for units outside of convoy radius, make churches who make pilgrims for all unoccupied mines in convoy radius