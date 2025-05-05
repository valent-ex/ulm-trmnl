from core.scheduler import start_scheduler
from dotenv import load_dotenv
import sys

load_dotenv()

sys.stdout.write("🟢 Starting ulm-trmnl...\n")
sys.stdout.flush()

if __name__ == "__main__":
    try:
        start_scheduler()
    except Exception as e:
        sys.stderr.write(f"❌ Exception on startup: {e}\n")
        sys.stderr.flush()
