import faust
import asyncio


class CurrentAccountCDC(faust.Record):
    payload: dict


app = faust.App('soa_app', broker='kafka://kafka:9092')
topic = app.topic('current_currentaccount', value_type=CurrentAccountCDC)


@app.agent(topic)
async def hello(messages):
    async for message in messages:
        
        # fake a long-running computation
        # delegated to another machine (I/O idling)
        await asyncio.sleep(5)

        print(message.payload)


# @app.timer(interval=5.0)
# async def example_sender():
#     await hello.send(
#         value=Test(msg='Hello World!'),
#     )


if __name__ == '__main__':
    app.main()
