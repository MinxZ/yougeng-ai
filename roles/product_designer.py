import re
from metagpt.actions import Action
from metagpt.llm import LLM
from metagpt.actions import Action
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger
import json

from data.text_on_img import text_on_img

class GetProductImage(Action):

    PROMPT_TEMPLATE = """
    我的目标：
    - 利用热门梗的数据，整理并输出一个字符串数组，每个字符串以 # 开头。
    - 从整理的梗中选择最符合印刷的梗，确保选取的梗具有一些差异性。
    - 返回至多 3 个你认为最适合印刷的梗。

    输入数据：
    ```
    {instruction}
    ```

    输出格式：
    ```json
    ["#topic1", "#topic2"]
    ```
    """

    def __init__(self, name="GetProductImage", context=None, llm=None):
        super().__init__(name, context, llm)

    async def run(self, instruction: str):

        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        resp = await self._aask(prompt)

        topic_list = self.parse_list(resp)

        img_list = self.text_to_img(topic_list)
        
        return img_list
    
    @staticmethod
    def text_to_imgurl(topic_list):
        image_path_list = []
        for topic in topic_list:
            image_path_list.append(text_on_img(topic))
        
        return image_path_list
    
    @staticmethod
    def parse_list(rsp):
        pattern = r'```json(.*)```'
        match = re.search(pattern, rsp, re.DOTALL)
        text = match.group(1) if match else rsp
        arr = json.loads(text)
        return arr


# TODO
class SearchMemes(Action):
    pass
    

class ProductDesigner(Role):
    def __init__(
        self,
        name: str = "耿涂涂",
        profile: str = "梗图设计师",
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