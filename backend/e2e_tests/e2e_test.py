import os
import subprocess
import time
import unittest
from typing import Optional

from backend.domains.activities.schemas import CreateActivityRequest, ScoreType
from backend.client.client import Client
import backend.db

from sqlmodel import SQLModel
import requests

# Ensure we use a test DB
db_file = "wodcraft_e2e.db"
os.environ["DATABASE_TYPE"] = "sqlite"
os.environ["SQLITE_FILENAME"] = db_file


class TestActivityServiceE2E(unittest.TestCase):
    port = "7777"
    client: Optional[Client] = None

    @classmethod
    def run_server(cls, timeout=60):
        try:
            response = requests.get(f"http://localhost:{cls.port}/healthz")
            if response.status_code == 200:
                return
        except requests.exceptions.ConnectionError:
            pass

        cls.server_process = subprocess.Popen([
            "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", cls.port])

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"http://localhost:{cls.port}/healthz")
                if response.status_code == 200:
                    return True
            except requests.exceptions.ConnectionError:
                time.sleep(1)
        raise RuntimeError("Server did not start in time")

    @classmethod
    def setUpClass(cls):
        # Delete the DB file if exists
        if os.path.exists(db_file):
            os.remove(db_file)
        # # Create the database + tables
        # backend.db.init_db()
        # SQLModel.metadata.create_all(backend.db.engine)

        # Start the WODCraft server in a separate process, unless it's already running
        cls.client = Client(base_url=f"http://localhost:{cls.port}")
        cls.run_server()
        print("Server started")

    @classmethod
    def tearDownClass(cls):
        """ """
        # Don't stop the WODCraft server, so it can be reused when iterating on the tests
        # cls.server_process.terminate()
        # cls.server_process.wait()

        # Don't delete the DB file
        # if os.path.exists(db_file):
        #     os.remove(db_file)

    def test_add_activity(self):
        new_activity = CreateActivityRequest(
            name="Pull-ups",
            description="Max reps pull-ups",
            score_type=ScoreType.REPS
        )
        response = self.client.add_activity(new_activity)
        self.assertEqual(response["name"], new_activity.name)
        self.assertEqual(response["description"], new_activity.description)
        self.assertEqual(response["score_type"], new_activity.score_type)

        # Get the activities
        activities = self.client.get_activities()
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]["name"], new_activity["name"])


if __name__ == "__main__":
    unittest.main()
