from collections.abc import Iterable
from logging import Logger, StreamHandler, getLogger

from dotenv import load_dotenv
from telicent_lib import AutomaticAdapter, Record
from telicent_lib.config import Configurator
from telicent_lib.logging import CoreLoggerFactory
from telicent_lib.records import RecordUtils
from telicent_lib.sinks import KafkaSink

load_dotenv()
# Mapper Configuration
config = Configurator()
target_topic= config.get("TARGET_TOPIC", required=True,
                    description="Specifies the Kafka topic the mapper pushes its output to")
name = config.get("PRODUCER_NAME", required=True,
                    description="Specifies the name of the producer")
source_name=config.get("SOURCE_NAME", required=True,
                    description="Specifies the source that the data has originated from")
content_type=config.get("CONTENT_TYPE", required=True,
                    description="Specifies the content type of the payload source that the data has originated from")
default_security_label = "*"

logger = getLogger(__name__)

def create_records(data, source_filename) -> Iterable[Record]:
    record = Record(
        RecordUtils.to_headers(
            {
                "Security-Label": default_security_label,
                "Content-Type": content_type,
                "Data-Source": source_filename,
                "Data-Producer": name,
            }
        ),
        None,
        data.encode('utf-8')
    )
    logger.debug(record)
    return record

# def process_source(adapter) -> Record | list[Record] | None:
#     logger.info(f"loading {file_path}")
#     adapter.send(create_records(data, file_path))
#     logger.info(f"File {file_path} Uploaded")
#     # return None

if __name__ == "__main__":

    from adapter.data.config import data_files

    def process_files():
        try:
            for file_path in data_files:
                # Load ttl file
                with open('adapter/data/' + file_path) as f:
                    data = f.read()
                yield create_records(data, file_path)
                logger.info(f"File {file_path} Uploaded")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
        finally:
            logger.info("Adapter finished")

    logger = CoreLoggerFactory.get_logger(__name__)

    if isinstance(logger, Logger):
        logger.addHandler(StreamHandler())
    else:
        logger.logger.addHandler(StreamHandler())

    # Instantiate Sink for different topics
    sink = KafkaSink(target_topic)
    adapter = AutomaticAdapter(
        target=sink,
        name=name,
        adapter_function=process_files,
        source_name=source_name
    )
    adapter.run()
    logger.info("Adapter Created")
