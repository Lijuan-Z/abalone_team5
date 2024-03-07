import asyncio
import time


class Timer:
    def __init__(self, start_time):
        self.start_time = start_time
        self.time = start_time
        self.running = False
        self.stop_event = asyncio.Event()

    def set_time(self, new_time):
        self.time = new_time

    def set_starting_time(self, start_time):
        self.start_time = start_time

    def reset_timer(self):
        self.time = self.start_time

    async def start_timer(self):
        self.task = asyncio.create_task(self.run_timer())

    async def run_timer(self):
        if not self.running:
            self.running = True
            self.stop_event.clear()
            while not self.stop_event.is_set():
                print(f"Timer running: {self.time} seconds")
                self.time -= 1
                await asyncio.sleep(1)

    async def stop_timer(self):
        self.stop_event.set()
        self.running = False
        await self.task

async def main():
    timer = Timer(30)
    await timer.start_timer()
    await asyncio.sleep(5)
    await timer.stop_timer()
    await timer.start_timer()
    await asyncio.sleep(5)
    await timer.stop_timer()

if __name__ == "__main__":
    asyncio.run(main())

