import re
from metagpt.actions import Action
from metagpt.llm import LLM
from metagpt.actions import Action
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger
import json
from metagpt.roles import Searcher
from metagpt.tools import SearchEngineType

class GetMemes(Action):

  PROMPT_TEMPLATE = """
  我的目标：
  通过对提供的数据进行分析，发掘适合印在 T 恤上的梗，允许搭配 emoji，并以 Markdown 格式输出，约 5-10 个。
  从最近的网络潮流中提取有趣的梗（Meme），并以中文文字形式输出，主要从中文互联网中搜索。
  
  输入数据：
  ```
  {instruction}
  ```

  输出格式：
  - **\#热梗文字**: 解释
    - 小红书商品文案
  - **\#热梗文字**：解释
    - 小红书商品文案
  """

  def __init__(self, name="GetMemes", context=None, llm=None):
    super().__init__(name, context, llm)

  async def run(self, instruction: str):

    prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

    resp = await self._aask(prompt)

    return resp


class SearchMemes(Action):
  PROMPT_TEMPLATE = """
  我的目标：
  通过对提供的搜索数据进行分析，发掘适合印在 T 恤上的梗，允许搭配 emoji，并以 Markdown 格式输出，约 5-10 个。
  从最近的网络潮流中提取有趣的梗（Meme），并以中文文字形式输出，主要从中文互联网中搜索。

  输出格式：
  - **\#热梗文字**: 解释
    - 小红书商品文案
  - **\#热梗文字**：解释
    - 小红书商品文案
  """

  def __init__(self, name="SearchMemes", context=None, llm=None):
    super().__init__(name, context, llm)

  async def run(self, instruction: str):
    search_resp = await Searcher(
      name=self.name,
      profile=self.profile,
      engine=SearchEngineType.SERPAPI_GOOGLE,
      goal=self.PROMPT_TEMPLATE,
    ).run(instruction)

    return search_resp
  

class MemeAnalyzer(Role):
  def __init__(
    self,
    name: str = "耿文文",
    profile: str = "Meme Analyzer",
    **kwargs,
  ):
    super().__init__(name, profile, **kwargs)
    self._init_actions([GetMemes, SearchMemes])

  async def _act(self) -> Message:
    logger.info(f"{self._setting}: ready to {self._rc.todo}")
    todo = self._rc.todo # todo will be SimpleWriteCode()

    msg = self.get_memories(k=1)[0] # find the most recent k messages

    resp = await todo.run(msg.content)
    msg = Message(content=resp, role=self.profile, cause_by=type(todo))

    return msg