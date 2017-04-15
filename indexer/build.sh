rm -rf build/*
cp __init__.py core.py connection.py settings.py models.py build/
pip install elasticsearch_dsl boto3 aws_requests_auth -t build/
cd build
zip -r core.zip *
chmod u=rwx,go=r core.zip
cd ..