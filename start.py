from datetime import datetime, timedelta
from sources.pipeline.suspilne_pipeline import SuspilnePipeline

if __name__ == "__main__":
    pipeline = SuspilnePipeline()
    yesterday = datetime.now() - timedelta(days=1)

    pipeline.execute(start=yesterday, end=datetime.now())
