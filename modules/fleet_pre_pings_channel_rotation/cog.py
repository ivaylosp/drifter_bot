"""Cog for channel rotation"""

import os
import datetime
import discord
import logging
import json
import mysql.connector
from mysql.connector import Error
from discord.ext import commands, tasks

GUILD_ID = int(os.getenv('GUILD_ID'))
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_PORT = int(os.getenv('DATABASE_PORT'))

# Channel settings
CHANNEL_ROTATION = os.getenv('CHANNEL_ROTATION')
MODULE_NAME = 'fleet_pre_pings_channel_rotation'
CHANNEL_NAME = 'fleet-pre-pings'
WEBHOOK_NAME = '#fleet-pre-pings'
TIMES = []

try:
    utc = datetime.timezone.utc
    data = json.loads(CHANNEL_ROTATION)
    logger = logging.getLogger('discord')

    for rotation_settings in data:
        if rotation_settings['module'] == MODULE_NAME:
            logger.info('Loading module settings %s', MODULE_NAME)
            for time_settings in rotation_settings['times']:
                logger.info('Loading module time settings %s', time_settings)
                TIMES.append(datetime.time(hour=time_settings['hour'], minute=time_settings['minute'], second=time_settings['second'], tzinfo=utc))
except json.JSONDecodeError as e:
    logger.info('Invalid JSON format: %s', e)

class FleetPrePingsRotation(commands.Cog, name="Fleet pre pings channel rotation"):
    """Starts a channel rotation"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger('discord')
        self.guild = bot.get_guild(GUILD_ID)
        self.connection = None
        self.settings = None

        if self.guild is None:
            self.logger.warning('Guild not found!')
            self.cog_unload()

        self.db_connect()
        if self.connection is None:
            self.logger.warning('Aborting due to MySQL issue')
            self.cog_unload()
        self.db_disconnect()
        self.my_task.start()

    def cog_unload(self):
        """Stop rotation"""
        self.my_task.cancel()

    @tasks.loop(time=TIMES)
    async def my_task(self):
        """Start rotation"""
        existing_channel = discord.utils.get(self.guild.channels, name=CHANNEL_NAME)
        channel_overwrites = {}
        channel_category = None
        channel_topic = None
        channel_position = 0
        channel_slowmode_delay = 0
        channel_nsfw = False

        if existing_channel:
            self.logger.info('Deleting channel: %s', existing_channel.name)
            await existing_channel.delete()
            channel_overwrites = existing_channel.overwrites
            channel_category = existing_channel.category
            channel_topic = existing_channel.topic
            channel_position = existing_channel.position
            channel_slowmode_delay = existing_channel.slowmode_delay
            channel_nsfw = existing_channel.nsfw

        channel = await self.guild.create_text_channel(
            name=CHANNEL_NAME,
            topic=channel_topic,
            position=channel_position,
            category=channel_category,
            overwrites=channel_overwrites,
            slowmode_delay=channel_slowmode_delay,
            nsfw=channel_nsfw
        )

        if channel is None:
            self.logger.info('Channel failed to create')
            return

        webhook = await channel.create_webhook(name=WEBHOOK_NAME)

        if webhook is None:
            self.logger.info('Webhook failed to create')
            return

        self.logger.info('Webhook URL: %s', webhook.url)

        await self.update_webhook(WEBHOOK_NAME, webhook.url)

    async def update_webhook(self, webhook_name: str, webhook_url: str):
        '''Updating database with latest webhook'''

        if webhook_name == '':
            return
        
        try:
            self.db_connect()

            if self.connection.is_connected():
                cursor = self.connection.cursor()

                # Prepare update query
                sql_update_query = ("""
                    UPDATE fleetpings_webhook
                    SET url = %s
                    WHERE name = %s
                """)
                data = (webhook_url, webhook_name)

                # Execute and commit
                cursor.execute(sql_update_query, data)
                self.connection.commit()

                self.logger.info('Webhook updated successfully. Rows affected: %s', cursor.rowcount)
        except Error as error:
            self.logger.error('MySQL Error: %s', error)
        finally:
            self.db_disconnect

    def db_connect(self):
        try:
            # Connect to MySQL
            self.connection = mysql.connector.connect(
                host=DATABASE_HOST,
                database=DATABASE_NAME,
                user=DATABASE_USERNAME,
                password=DATABASE_PASSWORD,
                port=DATABASE_PORT
            )
        except Error as error:
            self.logger.error('Error while connecting to MySQL: %s', error)

    def db_disconnect(self):
        if self.connection is not None:
            if self.connection.is_connected():
                self.connection.close()
                self.logger.info('MySQL connection closed.')

async def setup(bot: commands.Bot):
    await bot.add_cog(FleetPrePingsRotation(bot))
