from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate

import helpers.document_helper as doc_helper

region_name = "us-west-2"
model_id = "anthropic.claude-3-sonnet-20240229-v1:0"


def get_llm(max_tokens=4096, temperature=0.9, top_k=250, top_p=1):
    model_kwargs = {
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_k": top_k,
        "top_p": top_p,
        "stop_sequences": ["\n\nHuman"],
    }
    return ChatBedrock(
        region_name=region_name,
        model_id=model_id,
        streaming=True,
        # callbacks=[StreamingStdOutCallbackHandler()],
        model_kwargs=model_kwargs
    )


def invoke_llm(prompt):
    # prompt = "당신은 영어를 한국어로 번역하는 전문 번역가입니다. I love programming."
    messages = [
        HumanMessage(
            content=prompt
        )
    ]
    llm = get_llm()
    result = llm.invoke(messages)
    return result.content


def summarize_using_stuff(filepath, question, max_tokens,
                          temperature, top_p, top_k, prompt):
    # Define prompt
    prompt_template = prompt

    prompt_template = PromptTemplate.from_template(prompt_template)

    # Define LLM chain
    llm = get_llm(max_tokens=max_tokens, temperature=temperature, top_p=top_p, top_k=top_k)
    llm_chain = LLMChain(llm=llm, prompt=prompt_template)

    # Define StuffDocumentsChain
    try:
        stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="contents")
        docs = doc_helper.get_docs(filepath=filepath)
        result = stuff_chain.invoke({"input_documents": docs})
        return result["output_text"]
    except:
        messages = [
            HumanMessage(
                content=prompt
            )
        ]
        result = llm.invoke(messages).content
        return result
