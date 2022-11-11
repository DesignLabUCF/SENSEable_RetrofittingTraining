set fileName=Logs\HomeTest.log
pushd D:\UnrealProjects\Retrofitting\Data
python RetrofittingParser.py %fileName%
python RetrofittingPlotter.py %fileName%

