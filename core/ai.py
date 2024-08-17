import os
from groq import AsyncGroq

groq = AsyncGroq(api_key=os.environ["GROQ_API_KEY"])