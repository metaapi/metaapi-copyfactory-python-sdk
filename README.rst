CopyFactory trade copying API for Python (a member of `metaapi.cloud <https://metaapi.cloud>`_ project)
#######################################################################################################

CopyFactory is a powerful trade copying API which makes developing forex
trade copying applications as easy as writing few lines of code.

CopyFactory API is a member of MetaApi project (`https://metaapi.cloud <https://metaapi.cloud>`_),
a powerful cloud forex trading API which supports both MetaTrader 4 and MetaTrader 5 platforms.

MetaApi is a paid service, however we may offer a free tier access in some cases.

The `MetaApi pricing <https://metaapi.cloud/#pricing>`_ was developed with the intent to make your charges less or equal to what you would have to pay
for hosting your own infrastructure. This is possible because over time we managed to heavily optimize
our MetaTrader infrastructure. And with MetaApi you can save significantly on application development and
maintenance costs and time thanks to high-quality API, open-source SDKs and convenience of a cloud service.

This SDK requires a 3.8+ version of Python to run.

Why do we offer CopyFactory API trade copying API
=================================================

We found that developing reliable and flexible trade copier is a task
which requires lots of effort, because developers have to solve a series
of complex technical tasks to create a product.

We decided to share our product as it allows developers to start with a
powerful solution in almost no time, saving on development and
infrastructure maintenance costs.

Frequently asked questions (FAQ)
================================

FAQ is located here: `https://metaapi.cloud/docs/copyfactory/faq/ <http://metaapi.cloud/docs/copyfactory/faq/>`_

CopyFactory copytrading API features
====================================

Features supported:

- low latency trade copying API
- reliable trade copying API
- suitable for large-scale deployments
- suitable for large number of subscribers
- connect arbitrary number of strategy providers and subscribers
- subscribe accounts to multiple strategies at once
- select arbitrary copy ratio for each subscription
- configure symbol mapping between strategy providers and subscribers
- apply advanced risk filters on strategy provider side
- override risk filters on subscriber side
- provide multiple strategies from a single account based on magic or symbol filters
- supports manual trading on subscriber accounts while copying trades
- synchronize subscriber account with strategy providers
- monitor trading history
- calculate trade copying commissions for account managers
- support portfolio strategies as trading signal source, i.e. the strategies which include signals of several other strategies (also known as combos on some platforms)

Please note that trade copying to MT5 netting accounts is not supported in the current API version

Please check Features section of the `https://metaapi.cloud/docs/copyfactory/ <https://metaapi.cloud/docs/copyfactory/>`_
documentation for detailed description of all settings you can make.

REST API documentation
======================

CopyFactory SDK is built on top of CopyFactory REST API.

CopyFactory REST API docs are available at `https://metaapi.cloud/docs/copyfactory/ <https://metaapi.cloud/docs/copyfactory/>`_

Code examples
=============

We published some code examples in our github repository, namely:

- Python: `https://github.com/metaapi/metaapi-copyfactory-python-sdk/tree/master/examples <https://github.com/metaapi/metaapi-copyfactory-python-sdk/tree/master/examples>`_

Installation
============

.. code-block:: bash

    pip install metaapi-cloud-sdk

Retrieving API token
====================

Please visit `https://app.metaapi.cloud/token <https://app.metaapi.cloud/token>`_ web UI to obtain your API token.

Configuring trade copying
=========================

In order to configure trade copying you need to:

- add MetaApi MetaTrader accounts with CopyFactory as application field value (see above)
- create CopyFactory provider and subscriber accounts and connect them to MetaApi accounts via connectionId field
- create a strategy being copied
- subscribe subscriber CopyFactory accounts to the strategy

.. code-block:: python

    from metaapi_cloud_sdk import MetaApi, CopyFactory

    token = '...'
    metaapi = MetaApi(token=token)
    copy_factory = CopyFactory(token=token)

    # retrieve MetaApi MetaTrader accounts with CopyFactory as application field value
    # provider account must have PROVIDER value in copyFactoryRoles
    provider_metaapi_account = await metaapi.metatrader_account_api.get_account(account_id='providerMetaapiAccountId')
    if (provider_metaapi_account is None) or provider_metaapi_account.copy_factory_roles is None or 'PROVIDER' not \
            in provider_metaapi_account.copy_factory_roles:
        raise Exception('Please specify PROVIDER copyFactoryRoles value in your MetaApi '
                        'account in order to use it in CopyFactory API')
    # subscriber account must have SUBSCRIBER value in copyFactoryRoles
    subscriber_metaapi_account = await metaapi.metatrader_account_api.get_account(account_id='subscriberMetaapiAccountId')
    if (subscriber_metaapi_account is None) or subscriber_metaapi_account.copy_factory_roles is None or 'SUBSCRIBER' not \
            in subscriber_metaapi_account.copy_factory_roles:
        raise Exception('Please specify SUBSCRIBER copyFactoryRoles value in your MetaApi '
                        'account in order to use it in CopyFactory API')

    configuration_api = copy_factory.configuration_api

    # create a strategy being copied
    strategy_id = await configuration_api.generate_strategy_id()
    await configuration_api.update_strategy(id=strategy_id['id'], strategy={
        'name': 'Test strategy',
        'description': 'Some useful description about your strategy',
        'accountId': provider_metaapi_account.id,
        'maxTradeRisk': 0.1,
        'stopOutRisk': {
            'value': 0.4,
            'startTime': '2020-08-24T00:00:00.000Z'
        },
        'timeSettings': {
            'lifetimeInHours': 192,
            'openingIntervalInMinutes': 5
        }
    })

    # subscribe subscriber CopyFactory accounts to the strategy
    await configuration_api.update_subscriber(subscriber_metaapi_account.id, {
        'name': 'Demo account',
        'subscriptions': [
            {
                'strategyId': strategy_id['id'],
                'multiplier': 1
            }
        ]
    })


See in-code documentation for full definition of possible configuration options.

Retrieving paginated lists
==========================

There are two groups of methods to retrieve paginated lists:

- with pagination in infinite scroll style
- with pagination in a classic style which allows you to calculate page count

They are applied to following entities:

- strategies: ``get_strategies_with_infinite_scroll_pagination`` and ``get_strategies_with_classic_pagination``
- provider portfolios: ``get_portfolio_strategies_with_infinite_scroll_pagination`` and ``get_portfolio_strategies_with_classic_pagination``
- subscribers: ``get_subscribers_with_infinite_scroll_pagination`` and ``get_subscribers_with_classic_pagination``

Example of retrieving strategies with pagination in infinite scroll style:

.. code-block:: python

    # paginate strategies, see in-code documentation for full list of filter options available.
    strategies = await api.metatrader_account_api.get_strategies_with_infinite_scroll_pagination(
        {'limit': 10, 'offset': 0}
    )

    # get strategies without filter (returns 1000 strategies max)
    strategies = await api.metatrader_account_api.get_strategies_with_infinite_scroll_pagination()
    strategy = None

    for s in strategies:
        if s['_id'] == 'strategyId':
            strategy = s
            break

Example of retrieving strategies with pagination in classic style:

.. code-block:: python

    # paginate strategies, see in-code documentation for full list of filter options available.
    strategies = await api.metatrader_account_api.get_strategies_with_classic_pagination({'limit': 10, 'offset': 0})
    strategy = None

    for s in strategies:
        if s['_id'] == 'strategyId':
            strategy = s
            break
    # number of all strategies matching filter without pagination options
    print(strategies['count'])

    # get strategies without filter (returns 1000 strategies max)
    strategies = await api.metatrader_account_api.get_strategies_with_classic_pagination()

Retrieving trade copying history
================================

CopyFactory allows you to monitor transactions conducted on trading accounts in real time.

Retrieving trading history on provider side
-------------------------------------------

.. code-block:: python

    history_api = copy_factory.history_api

    # retrieve trading history, please note that this method support pagination and limits number of records
    print(await history_api.get_provided_transactions(time_from=datetime.fromisoformat('2020-08-01'),
        time_till=datetime.fromisoformat('2020-09-01')))


Retrieving trading history on subscriber side
---------------------------------------------

.. code-block:: python

    history_api = copy_factory.history_api

    # retrieve trading history, please note that this method support pagination and limits number of records
    print(await history_api.get_subscription_transactions(time_from=datetime.fromisoformat('2020-08-01'),
        time_till=datetime.fromisoformat('2020-09-01')))

Resynchronizing subscriber accounts to providers
================================================
There is a configurable time limit during which the trades can be opened. Sometimes trades can not open in time due to broker errors or trading session time discrepancy.
You can resynchronize a subscriber account to place such late trades. Please note that positions which were
closed manually on a subscriber account will also be reopened during resynchronization.

.. code-block:: python

    account_id = '...' # CopyFactory account id

    # resynchronize all strategies
    await copy_factory.trading_api.resynchronize(account_id=account_id)

    # resynchronize specific strategy
    await copy_factory.trading_api.resynchronize(account_id=account_id, strategy_ids=['ABCD'])

Sending external trading signals to a strategy
==============================================
You can submit external trading signals to your trading strategy.

.. code-block:: python

    trading_api = copy_factory.trading_api
    signal_id = trading_api.generate_signal_id()

    # get strategy signal client
    strategy_signal_client = await trading_api.get_strategy_signal_client(strategy_id)

    # add trading signal
    await strategy_signal_client.update_external_signal(signal_id=signal_id, signal={
        'symbol': 'EURUSD',
        'type': 'POSITION_TYPE_BUY',
        'time': datetime.now(),
        'volume': 0.01
    })

    # get external signals
    print(await strategy_signal_client.get_external_signals())

    # remove signal
    await strategy_signal_client.remove_external_signal(signal_id=signal_id, signal={
        'time': datetime.now()
    })

Retrieving trading signals
==========================

.. code-block:: python

    subscriber_id = '...' # CopyFactory subscriber id
    subscriber_signal_client = await trading_api.get_subscriber_signal_client(subscriber_id)

    # retrieve trading signals
    print(await subscriber_signal_client.get_trading_signals())

Managing stopouts
=================
A subscription to a strategy can be stopped if the strategy have exceeded allowed risk limit.

.. code-block:: python

    trading_api = copy_factory.trading_api
    account_id = '...' # CopyFactory account id
    strategy_id = '...' # CopyFactory strategy id

    # retrieve list of strategy stopouts
    print(await trading_api.get_stopouts(account_id=account_id))

    # reset a stopout so that subscription can continue
    await trading_api.reset_subscription_stopouts(account_id=account_id, strategy_id=strategy_id, reason='daily-equity')

Managing stopout listeners
==========================
You can subscribe to a stream of stopout events using the stopout listener.

.. code-block:: python

    from metaapi_cloud_sdk import StopoutListener

    trading_api = copy_factory.trading_api

    # create a custom class based on the StopoutListener
    class Listener(StopoutListener):

        # specify the function called on event arrival
        async def on_stopout(self, strategy_stopout_event):
            print('Strategy stopout event', strategy_stopout_event)

        # specify the function called on error event
        async def on_error(self, error):
            print('Error event', error)

    # add listener
    listener = Listener()
    listener_id = trading_api.add_stopout_listener(listener)

    # remove listener
    trading_api.remove_stopout_listener(listener_id)

Retrieving subscriber trading logs
==================================

.. code-block:: python

    trading_api = copy_factory.trading_api
    account_id = '...' # CopyFactory account id

    # retrieve subscriber trading log
    print(await trading_api.get_user_log(account_id))

    # retrieve paginated subscriber trading log by time range
    print(await trading_api.get_user_log(account_id, datetime.fromtimestamp(datetime.now().timestamp() - 24 * 60 * 60), None, 20, 10))

Log streaming
=============
You can subscribe to a stream of strategy or subscriber log events using the user log listener.

Strategy logs
-------------

.. code-block:: python

    from metaapi_cloud_sdk import UserLogListener

    trading_api = copy_factory.trading_api

    # create a custom class based on the UserLogListener
    class Listener(UserLogListener):

        # specify the function called on event arrival
        async def on_user_log(self, log_event):
            print('Strategy user log event', log_event)

        # specify the function called on error event
        async def on_error(self, error):
            print('Error event', error)

    # add listener
    listener = Listener()
    listener_id = trading_api.add_strategy_log_listener(listener, 'ABCD')

    # remove listener
    trading_api.remove_strategy_log_listener(listener_id)

Subscriber logs
---------------

.. code-block:: python

    from metaapi_cloud_sdk import UserLogListener

    trading_api = copy_factory.trading_api

    # create a custom class based on the UserLogListener
    class Listener(UserLogListener):

        # specify the function called on event arrival
        async def on_user_log(self, log_event):
            print('Subscriber user log event', log_event)

        # specify the function called on error event
        async def on_error(self, error):
            print('Error event', error)

    # add listener
    listener = Listener()
    listener_id = trading_api.add_subscriber_log_listener(listener, 'accountId')

    # remove listener
    trading_api.remove_subscriber_log_listener(listener_id)

Transaction streaming
=====================
You can subscribe to a stream of strategy or subscriber transaction events using the transaction listener.

Strategy transactions
---------------------

.. code-block:: python

    from metaapi_cloud_sdk import TransactionListener

    history_api = copy_factory.history_api

    # create a custom class based on the TransactionListener
    class Listener(TransactionListener):

        # specify the function called on event arrival
        async def on_transaction(self, transaction_event):
            print('Strategy transaction event', transaction_event)

        # specify the function called on error event
        async def on_error(self, error):
            print('Error event', error)

    # add listener
    listener = Listener()
    listener_id = history_api.add_strategy_transaction_listener(listener, 'ABCD')

    # remove listener
    history_api.remove_strategy_transaction_listener(listener_id)

Subscriber transactions
-----------------------

.. code-block:: python

    from metaapi_cloud_sdk import TransactionListener

    history_api = copy_factory.history_api

    # create a custom class based on the TransactionListener
    class Listener(TransactionListener):

        # specify the function called on event arrival
        async def on_transaction(transaction_event):
            print('Subscriber transaction event', transaction_event)

        # specify the function called on error event
        async def on_error(self, error):
            print('Error event', error)

    # add listener
    listener = Listener()
    listener_id = history_api.add_strategy_transaction_listener(listener, 'ABCD')

    # remove listener
    history_api.remove_subscriber_transaction_listener(listener_id)

Webhooks
========

Webhooks can be created on specific strategies and their URLs can be provided to external systems to create external trading signals. The URL contains a secret webhook ID, so no extra authorization is required on a REST API invocation to a webhook.

.. code-block:: python

    strategy_id = '...'

    webhook = await copyfactory.configuration_api.create_webhook(strategy_id)
    url = webhook['url']

For example, if ``webhook.url`` is ``https://copyfactory-api-v1.london.agiliumtrade.ai/webhooks/yMLd8aviewgFfS4NBxZETkoVPbWAJ92t`` then a request can be sent to it to create an external signal:

.. code-block:: bash

    curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{
      "symbol": "EURUSD",
      "type": "POSITION_TYPE_BUY",
      "time": "2024-12-19T06:52:19.679Z",
      "volume": 0.1
    }' 'https://copyfactory-api-v1.london.agiliumtrade.ai/webhooks/yMLd8aviewgFfS4NBxZETkoVPbWAJ92t'


Related projects:
=================

See our website for the full list of APIs and features supported `https://metaapi.cloud/#features <https://metaapi.cloud/#features>`_

Some of the APIs you might decide to use together with this module:

1. MetaApi cloud forex trading API `https://metaapi.cloud/docs/client/ <https://metaapi.cloud/docs/client/>`_
2. MetaTrader account management API `https://metaapi.cloud/docs/provisioning/ <https://metaapi.cloud/docs/provisioning/>`_
3. MetaStats cloud forex trading statistics API `https://metaapi.cloud/docs/metastats/ <https://metaapi.cloud/docs/metastats/>`_
4. MetaApi MT manager API `https://metaapi.cloud/docs/manager/ <https://metaapi.cloud/docs/manager/>`_
5. MetaApi risk management API `https://metaapi.cloud/docs/risk-management/ <https://metaapi.cloud/docs/risk-management/>`_
