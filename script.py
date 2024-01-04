import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

# Define your intents
intents = discord.Intents.default()
intents.messages = True  # Allow access to message-related events, including content
intents.message_content = True  # Enable message content intent

# Set up the Discord bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='search')
async def search_youtube(ctx, *, arguments):
    print(f"Received command: !search {arguments}")  # Add this line for debugging
    
    # Split the arguments into URL and keyword
    arguments = arguments.split()

    print(f"Parsed arguments: {arguments}")  # Add this line for debugging
    
    # Check if both URL and keyword are provided
    if len(arguments) != 2:
        await ctx.send("Invalid command format. Please provide a valid URL and keyword.")
        return

    url, keyword = arguments

    try:
        # Fetch the HTML content of the YouTube community page
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all posts on the page
        posts = soup.find_all('yt-formatted-string', class_='style-scope ytd-comment-renderer')

        # Filter posts that contain the specified keyword
        keyword_posts = [post.text for post in posts if keyword.lower() in post.text.lower()]

        # Print the found posts for debugging
        print(f"Found posts: {keyword_posts}")

        # Send the matching posts to the Discord channel
        if keyword_posts:
            await ctx.send(f"Posts containing '{keyword}':\n{{'\\n'.join(keyword_posts)}}")
        else:
            await ctx.send(f"No posts found containing '{keyword}'.")

    except Exception as e:
        print(f"Error: {e}")
        await ctx.send("An error occurred. Please try again later.")

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run('MTE5MjQ2MTkyNjEzMTg0NzIwOA.G_7ix6.m0-gaFHLstyvAEjczPOVg08KoHIHrMSWpkbXSY')