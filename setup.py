from setuptools import setup
import mq_client

setup(
    name='Message Queue Client',
    version=mq_client.VERSION,
    url='https://github.com/deginner/mq-client',
    py_modules=['mq_client', 'mq_listener', 'mq_publisher'],
    author='deginner',
    author_email='support@deginner.com',
    description='A simple pika client implementation based on the examples.',
    install_requires=['amqp', 'pika', 'tornado'],
    entry_points = """
    [console_scripts]
    mqlisten = mq_listener:run
    mqpublish = mq_publisher:run
    """
)
