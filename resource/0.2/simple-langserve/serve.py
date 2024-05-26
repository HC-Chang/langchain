#!/usr/bin/env python

from typing import List

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes

import asyncio
import nest_asyncio
nest_asyncio.apply()

import os



# 0. add api key
# 0.1 add api key from file

# api-path = 'YOUR-API-FILE-PATH'
# f = open(path, 'r')
# OPENAI_API_KEY=f.read()
# f.close()
# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# 0.2 add api key by typing yourself
# os.environ["OPENAI_API_KEY"] = getpass.getpass()


# 1. Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# 2. Create model
model = ChatOpenAI()

# 3. Create parser
parser = StrOutputParser()

# 4. Create chain
chain = prompt_template | model | parser


# 4. App definition
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

# 5. Adding chain route

add_routes(
    app,
    chain,
    path="/chain",
)

async def main():
    import uvicorn
    os.system("start http://localhost:8000/chain/playground")
    uvicorn.run(app, host="localhost", port=8000, loop="asyncio")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
