import os
import asyncio
from metaapi_cloud_sdk import MetaApi
from metaapi_cloud_sdk import CopyFactory
from datetime import datetime

# your MetaApi API token
token = os.getenv('TOKEN') or '<put in your token here>'
# your master MetaApi account id
# master account must have PROVIDER value in copyFactoryRoles
master_account_id = os.getenv('MASTER_ACCOUNT_ID') or '<put in your masterAccountId here>'

# The strategy will publish all signals to the telegram channel, including external signals and
# signals generated by MT terminal. For this code example we use external signals, however you can
# publish MT signals as well.
# Please refer to https://metaapi.cloud/docs/copyfactory/features/telegram/publish/ for details.
# Telegram bot token
bot_token = os.getenv('TELEGRAM_BOT_TOKEN') or '<put in your bot_token here>'
# Telegram chat id
chat_id = os.getenv('TELEGRAM_CHAT_ID') or '<put in your chat_id here>'


async def telegram_example():
    api = MetaApi(token)
    copyfactory = CopyFactory(token)

    try:
        master_metaapi_account = await api.metatrader_account_api.get_account(master_account_id)
        if (
            (master_metaapi_account is None)
            or master_metaapi_account.copy_factory_roles is None
            or 'PROVIDER' not in master_metaapi_account.copy_factory_roles
        ):
            raise Exception(
                'Please specify PROVIDER copyFactoryRoles value in your MetaApi '
                'account in order to use it in CopyFactory API'
            )

        configuration_api = copyfactory.configuration_api
        strategies = await configuration_api.get_strategies_with_infinite_scroll_pagination()
        strategy = next((s for s in strategies if s['accountId'] == master_metaapi_account.id), None)
        if strategy:
            strategy_id = strategy['_id']
        else:
            strategy_id = await configuration_api.generate_strategy_id()
            strategy_id = strategy_id['id']

        # create a strategy
        await configuration_api.update_strategy(
            strategy_id,
            {
                'name': 'Test strategy',
                'description': 'Some useful description about your strategy',
                'accountId': master_metaapi_account.id,
                'telegram': {'publishing': {'token': bot_token, 'chatId': chat_id, 'template': '${description}'}},
            },
        )

        # send external signal
        trading_api = copyfactory.trading_api
        signal_client = await trading_api.get_signal_client(master_metaapi_account.id)
        signal_id = signal_client.generate_signal_id()
        await signal_client.update_external_signal(
            strategy_id=strategy_id,
            signal_id=signal_id,
            signal={'symbol': 'EURUSD', 'type': 'POSITION_TYPE_BUY', 'time': datetime.now(), 'volume': 0.01},
        )

        await asyncio.sleep(5)

        # remove external signal
        await signal_client.remove_external_signal(
            strategy_id=strategy_id, signal_id=signal_id, signal={'time': datetime.now()}
        )
    except Exception as err:
        print(api.format_error(err))


asyncio.run(telegram_example())
