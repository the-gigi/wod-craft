import os
import subprocess
import time
import unittest
from typing import Optional

from backend.domains.activities.schemas import CreateActivityRequest, ScoreType
from backend.client.client import Client

import requests

from backend.domains.users.schemas import CreateUserRequest, EmailStr

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

        # cls.server_process = subprocess.Popen([
        #     "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", cls.port])
        cmd = f"""
                    import os
                    import uvicorn
                    uvicorn.run("backend.main:app", host="0.0.0.0", port={cls.port}, reload=True)
        """
        # Remove leading spaces from each line
        cmd = "\n".join([line.strip() for line in cmd.split("\n")])

        cls.server_process = subprocess.Popen(["python", "-c", cmd], env=os.environ)

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
        #print("Server started")

    @classmethod
    def tearDownClass(cls):
        """ """
        # Don't stop the WODCraft server, so it can be reused when iterating on the tests
        cls.server_process.terminate()
        cls.server_process.wait()

        # Don't delete the DB file
        if os.path.exists(db_file):
            os.remove(db_file)

    def test_add_activity(self):
        new_activity = CreateActivityRequest(
            name="Pull-ups",
            description="Max reps pull-ups",
            score_type=ScoreType.REPS.value
        )
        activity = self.client.add_activity(new_activity)
        self.assertEqual(activity.name, new_activity.name)
        self.assertEqual(activity.description, new_activity.description)
        self.assertEqual(activity.score_type, new_activity.score_type)

        # Get the activities
        activities = self.client.get_activities()
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0].name, new_activity.name)

        # Get activity
        activity = self.client.get_activity(activity.id)
        self.assertEqual(activity.name, new_activity.name)

    def test_add_user(self):
        """ """
        new_user = CreateUserRequest(
            name="guy",
            email="guysayfan@gmail.com"
        )
        user = self.client.add_user(new_user)
        self.assertEqual(user.name, new_user.name)
        self.assertEqual(user.email, new_user.email)

        user = self.client.get_user(new_user.name)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, new_user.email)

if __name__ == "__main__":
    unittest.main()
