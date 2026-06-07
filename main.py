import sys

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.pipeline.training_pipeline import TrainingPipeline


def main() -> None:
    try:
        training_pipeline = TrainingPipeline()
        artifact = training_pipeline.run_pipeline()
        logging.info("Training pipeline finished: %s", artifact)
        print(artifact)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    main()
