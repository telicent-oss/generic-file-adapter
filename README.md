# Generic File Adapter

## How to use with docker:
1. Create a directory called `data` at the same level as the `docker-compose.yml` and add the files you want to push to a given topic.
2. Add a file called `config.py` to this `data` directory which looks like this:
```python
data_files = [
    "file_1.ttl",
    "file_2.ttl",
    "file_etc.ttl"
]
```
3. Update the environment variables in the `docker-compose.yml` based on which topic you want to post the data too and the file (MIME) types being ingested. At this stage, this adapter can only be used for files of the same type.
4. Run command:
```
docker compose up
```