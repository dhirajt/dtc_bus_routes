#!/bin/sh

cd ../../

echo 'Dump started ...'

python manage.py dumpdata rost.Stage --indent 4 > rost/fixtures/stage.json
python manage.py dumpdata rost.Route --indent 4 > rost/fixtures/route.json
python manage.py dumpdata rost.StageSeq --indent 4 > rost/fixtures/stageseq.json

echo 'Dump complete, fixtures are in rost/fixtures.'

