import openai
try:
    _ = openai.OpenAI
    print("openai.OpenAI exists")
except AttributeError:
    print("openai.OpenAI does not exist")

try:
    from openai import OpenAI
    print("from openai import OpenAI works")
except ImportError:
    print("from openai import OpenAI fails")

try:
    from openai import AsyncOpenAI
    print("from openai import AsyncOpenAI works")
except ImportError:
    print("from openai import AsyncOpenAI fails")
