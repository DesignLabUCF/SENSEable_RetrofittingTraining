set subject=33
set logName=01-26-2023_16-30-41_AUTO
set fileName=Subjects\%subject%\%logName%
env\Scripts\python RetrofittingParser.py %fileName%
::env\Scripts\python RetrofittingPlotter.py %fileName%

