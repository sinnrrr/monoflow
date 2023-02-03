import asyncio
import os
import sys
import time
from datetime import datetime as dt

import aiofiles
import aiofiles.os
import aiohttp
from aiocsv import AsyncWriter  # pyright: ignore

from monoflow.config import (
    EXPORT_FILE_NAME,
    MONOBANK_API_FETCH_TIMEOUT,
    MONOBANK_API_TOKEN,
    Account,
    accounts,
)
from monoflow.utils import Entry, create_date, date_to_time

# client_info = requests.get(
#     "https://api.monobank.ua/personal/client-info",
#     headers={"X-Token": MONOBANK_API_TOKEN},
# ).json()


async def parse_account(
    account: Account,
    from_: int,
    to_: int = date_to_time(dt.now()),
) -> list[Entry]:
    auth_headers = {"X-Token": MONOBANK_API_TOKEN}
    async with aiohttp.ClientSession(headers=auth_headers) as session:
        async with session.get(
            f"https://api.monobank.ua/personal/statement/{account.id}/{from_}/{to_}"
        ) as response:
            bank_extract = await response.json()

            balances_extract = []
            for entry in bank_extract:
                balances_extract.append(Entry(account, entry))

            return balances_extract


async def main():
    if len(sys.argv) < 2:
        print("Please provide `from` time")
        exit(1)

    from_, to_ = int(sys.argv[1]), int(time.time())
    if len(sys.argv) > 2:
        to_ = int(sys.argv[2])

    _, from_time, from_str = create_date(from_)
    _, to_time, to_str = create_date(to_)

    print(f"🕐 Time range was set up from {from_str} to {to_str}")
    print()

    for account in accounts:
        # if i != 0:
        #     print(f"\n⏳ Waiting {MONOBANK_API_FETCH_TIMEOUT} seconds timeout\n")
        #     await asyncio.sleep(MONOBANK_API_FETCH_TIMEOUT)

        print(f"✨ Parsing {account.name} account")
        account_extract = await parse_account(account, from_time, to_time)
        export_location = f"out/{from_time}_{EXPORT_FILE_NAME}"

        await aiofiles.os.makedirs(os.path.dirname(export_location), exist_ok=True)
        async with aiofiles.open(
            export_location,
            mode="a",
            encoding="utf-8",
            newline="",
        ) as f:
            writer = AsyncWriter(f)
            for entry in account_extract:
                await writer.writerow(
                    [
                        entry.time,
                        entry.amount,
                        entry.currency,
                        entry.from_name,
                        entry.to_name,
                        entry.description,
                    ]
                )
        print(f"✅ Written {len(account_extract)} data records")
        print()


asyncio.run(main())
