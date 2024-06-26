from langchain_openai import ChatOpenAI
import base64

llm = ChatOpenAI(
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key="API KEY",  # if you prefer to pass api key in directly instaed of using env vars
)

print(llm.invoke("say hello to david"))

def load_image(inputs: dict) -> dict:
    """Load image from file and encode it as base64."""
    image_path = inputs["image_path"]
  
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    image_base64 = encode_image(image_path)
    return {"image": image_base64}

from langchain.chains import TransformChain
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain import globals
from langchain_core.runnables import chain

load_image_chain = TransformChain(
    input_variables=["image_path"],
    output_variables=["image"],
    transform=load_image
)

# Set verbose
globals.set_debug(True)

@chain
def image_model(inputs: dict) -> str | list[str] | dict:
 """Invoke model with image and prompt."""
 model = ChatOpenAI(temperature=0.5, max_tokens=1024, model="gpt-4o",api_key="API KEY")
 msg = model.invoke(
             [HumanMessage(
             content=[
             {"type": "text", "text": inputs["prompt"]},
             {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{inputs['image']}"}},
             ])]
             )
 return msg.content


def get_image_information(image_path: str) -> dict:
   vision_prompt = """
   Describe the image you see
   """
   vision_chain = load_image_chain | image_model 
   return vision_chain.invoke({'image_path': f'{image_path}', 
                               'prompt': vision_prompt})

get_image_information("/my_frames/timestamp_0.00.jpg")