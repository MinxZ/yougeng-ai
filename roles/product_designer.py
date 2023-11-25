import re
from metagpt.actions import Action
from metagpt.llm import LLM
from metagpt.actions import Action
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger
import json

class GetProductImage(Action):

    PROMPT_TEMPLATE = """
    我的目标：
    基于热梗的数据，整理出一个列表，用字符串数组输出，以 # 开头
    
    输入数据：
    ```
    {instruction}
    ```

    输出格式：
    ["#topic1", "#topic2"]
    """

    def __init__(self, name="GetProductImage", context=None, llm=None):
        super().__init__(name, context, llm)

    async def run(self, instruction: str):

        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        resp = await self._aask(prompt)

        return resp


# TODO
class SearchMemes(Action):
    pass
    

class ProductDesigner(Role):
    def __init__(
        self,
        name: str = "耿涂涂",
        profile: str = "产品设计师",
        **kwargs,
    ):
        super().__init__(name, profile, **kwargs)
        self._init_actions([GetProductImage])

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        todo = self._rc.todo # todo will be SimpleWriteCode()

        msg = self.get_memories(k=1)[0] # find the most recent k messages

        resp = await todo.run(msg.content)
        msg = Message(content=resp, role=self.profile, cause_by=type(todo))

        return msg