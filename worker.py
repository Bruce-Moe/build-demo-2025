import asyncio
import random
import time

class ExternalService:
    """Simulates an external service with connect/disconnect and task processing."""
    async def connect(self):
        print("Service: Connecting...")
        await asyncio.sleep(0.1) # Simulate connection time
        print("Service: Connected.")
        return object() # Simulate a connection object

    async def disconnect(self, connection):
        if connection:
            print("Service: Disconnecting...")
            await asyncio.sleep(0.05) # Simulate disconnection time
            print("Service: Disconnected.")

    async def process_data(self, connection, data):
        if not connection:
            raise ConnectionError("Service connection is not active.")
        print(f"Service: Processing data '{data}'...")
        # Simulate processing time and potential failure
        if random.random() < 0.3: # 30% chance of failure
            print(f"Service: Processing failed for '{data}'.")
            raise RuntimeError(f"Failed to process data: {data}")
        await asyncio.sleep(0.2)
        print(f"Service: Finished processing '{data}'.")
        return f"processed_{data}"

class Worker:
    def __init__(self):
        self._service = ExternalService()
        self._connection = None
        self._is_processing = False # State flag: is the worker busy?
        self._active_task = None # Track the current processing task

    async def _acquire_service(self):
        if self._connection is None:
            self._connection = await self._service.connect()

    async def _release_service(self):
        if self._connection:
            await self._service.disconnect(self._connection)
            self._connection = None
            # Bug: The _is_processing flag is not consistently reset
            # when a task fails and releases the connection.

    async def process_task(self, task_id, data):
        if self._is_processing:
            print(f"Worker: Warning: Worker is already processing task {self._active_task}. Skipping task {task_id}.")
            return None # Worker is busy, ignore new task

        self._is_processing = True # Mark worker as busy
        self._active_task = task_id # Track active task
        print(f"Worker: Starting task {task_id} for data '{data}'.")

        try:
            await self._acquire_service()
            result = await self._service.process_data(self._connection, data)
            print(f"Worker: Task {task_id} completed successfully.")
            return result
        except Exception as e:
            print(f"Worker: Task {task_id} failed with error: {e}")
            # Bug: If an error occurs here, _is_processing is not reset to False.
            # The finally block releases the connection, but the state is wrong.
            raise e # Re-raise the exception to signal failure
        finally:
            # This ensures the connection is released, BUT the state _is_processing might be wrong
            await self._release_service()
            # Bug: _active_task is also not reset on failure
            # self._active_task = None # This line is missing in the buggy code on failure path


# Simulate running the worker with multiple tasks
async def run_worker_buggy():
    worker = Worker()
    tasks = [
        ("task_1", "data_A"),
        ("task_2", "data_B"),
        ("task_3", "data_C"),
        ("task_4", "data_D"),
        ("task_5", "data_E"),
    ]

    # Run tasks concurrently
    await asyncio.gather(*(worker.process_task(id, data) for id, data in tasks), return_exceptions=True)

    print("\n--- Simulation Finished ---")
    print(f"Worker state after tasks: _is_processing={worker._is_processing}, _active_task={worker._active_task}, _connection is None={worker._connection is None}")

    # If any task failed, _is_processing will likely still be True, even though no task is running.
    # This prevents future tasks from being processed ("Worker is already processing...")


# To run this buggy example and observe the symptom:
# asyncio.run(run_worker_buggy())