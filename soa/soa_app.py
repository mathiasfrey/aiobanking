import faust
import asyncio
import random

class AccountProcessed(faust.Record):
    account: str
    balance: int
    modeloutput: float 

# a bit of a weird deserialization hapening here...
class CurrentAccountAfter(faust.Record):
    id: int
    account: str
    balance: int

class CurrentAccountPayload(faust.Record):
    after: CurrentAccountAfter

class CurrentAccountCDC(faust.Record):
    payload: CurrentAccountPayload


app = faust.App('soa_app', broker='kafka://kafka:9092', topic_partitions=1)
topic = app.topic('current_currentaccount', value_type=CurrentAccountCDC)
destination_topic = app.topic('account_processed', value_type=CurrentAccountCDC)


balance_stats = app.Table('balance_stats', default=int)

@app.agent(topic, sink=[destination_topic])
async def hello(messages):
    async for message in messages:
        
        # fake a long-running computation
        # delegated to another machine (I/O idling)
        await asyncio.sleep(3)
        

        try:
            
            account = message.payload.after.account
            balance = message.payload.after.balance

            # this is just an example that we can
            # store in-memory
            balance_stats[account] =  balance
            print('Saved to evolving fact table')
            print(balance_stats[account])

        except:
            # this was a delete event, there's no after
            print('Encountered a delete')
            raise
        yield AccountProcessed(account=account, balance=balance, modeloutput=random.random())

# @app.timer(interval=5.0)
# async def example_sender():
#     await hello.send(
#         value=Test(msg='Hello World!'),
#     )


if __name__ == '__main__':
    app.main()
