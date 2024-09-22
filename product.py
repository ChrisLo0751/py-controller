import asyncio

# 定义一个简单的自定义对象
class Item:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Item(name={self.name})"

async def producer(queue):
    for i in range(5):
        item = Item(name=f"Item-{i}")  # 创建自定义对象
        await queue.put(item)  # 将对象放入队列
        print(f'生产者: 生产 {item}')
        await asyncio.sleep(1)

async def consumer(queue):
    while True:
        item = await queue.get()  # 从队列中获取对象
        if item is None:  # 用于停止消费者
            break
        print(f'消费者: 消费 {item}')
        queue.task_done()

async def main():
    queue = asyncio.Queue()
    # 创建生产者和消费者任务
    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(consumer(queue))

    await producer_task  # 等待生产者完成
    await queue.join()    # 等待队列中的所有任务完成

    # 停止消费者
    await queue.put(None)  # 向队列中放入停止信号
    await consumer_task

asyncio.run(main())
