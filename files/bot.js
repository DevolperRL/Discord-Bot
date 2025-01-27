const { Client, GatewayIntentBits } = require('discord.js');
const dotenv = require('dotenv');

// Load environment variables from .env file
dotenv.config();

// Get the bot token from environment variables
const TOKEN = process.env.BOT_TOKEN;

// Create a new Discord client
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
    ],
});

// Bot is ready
client.once('ready', () => {
    console.log(`Bot is online as ${client.user.tag}`);
});

// Message listener
client.on('messageCreate', (message) => {
    if (message.author.bot) return; // Ignore bot messages

    if (message.content === '!ping') {
        message.reply('Pong! 🏓');
    }
});

// Login the bot
client.login(TOKEN);
