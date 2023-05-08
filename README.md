# Infibot

This is the source code for infibot, a simple whatsapp webhook handler to run on AWS Lambda. More detailed instructions to deploy your own version will be added soon.

## Local Instructions

- To zip the package and upload to aws lambda: `rm ../code.zip && zip ../code.zip *.py `
- To test locally with test secrets: `export $(cat ../secrets-infibot | xargs) && python3 test.py`