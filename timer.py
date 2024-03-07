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
        if not self.running:
            self.running = True
            self.stop_event.clear()
            while not self.stop_event.is_set():
                print(f"Timer running: {self.time} seconds")
                self.time -= 1
                await asyncio.sleep(1)

    def stop_timer(self):
        self.stop_event.set()
        self.running = False
        return self.time

async def timer_loop(timer):
    task = asyncio.create_task(timer.start_timer())

    # Let the timer run for a few seconds for demonstration
    await asyncio.sleep(5)

    time_left = timer.stop_timer()
    await task  # Ensure the timer task completes

async def main():
    timer = Timer(30)
    await timer_loop(timer)
    await timer_loop(timer)

if __name__ == "__main__":
    asyncio.run(main())

