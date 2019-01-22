'''
Rules to follow:
 - Teachers with only periods in {1, 2, 3, 4} are part-time on blue days, so all classes will have
   allowed periods of 1, 2, 3, 4. Same for {5, 6 ,7} and red days.
 - Semester courses that end up in the same period will be seen as constrained to be in the same period
 - Semester courses that are sem 1 will be seen as constrained to be in sem 1. Same for sem 2.
 - Homerooms will be ignored.
 - Room will be included as a constraint
 - Arabic key MUST be used to create list
    - Arabics are teamed 

 - Teaming:
    - team_1: Sections teamed to have same students and different periods
    - team_2: Sections teamed to have different students and same period
        - Orchestra
        - team_period
    - team_3: Sections teamed to have the same students and same period, provided that students have requested class
        - Arabics
        - team_period_students
'''