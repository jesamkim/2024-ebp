from services import bedrock_service


def generate_answer(question):
    result = bedrock_service.invoke_llm(question)
    return result


def generate_summary(filepath, question, max_tokens,
                     temperature, top_p, top_k, prompt):
    result = bedrock_service.summarize_using_stuff(filepath=filepath, question=question, max_tokens=max_tokens,
                                                   temperature=temperature, top_p=top_p, top_k=top_k, prompt=prompt)
    return result

#
# def generate_answer(question: str, max_tokens: int = 200, temperature: float = 0, top_p: float = 0.9,
#                     top_k: int = 250, model_id: str = 'anthropic.claude-v2'):
#     prompt = "".join([f"\n\nHuman: {question} ", "\n\nAssistant:"])
#
#     parameters = {
#         "prompt": prompt,
#         "max_tokens_to_sample": max_tokens,  # min:0, max:8,000, default:200
#         "stop_sequences": ["\n\nHuman:"],
#         "temperature": temperature,  # min:0, max:1, default:0.5
#         "top_p": top_p,  # min:0, max:1, default:1
#         "top_k": top_k  # min:0, max:500, default:250
#     }
#     response = bedrock_service.get_predict_from_bedrock_client(model_id=model_id,
#                                                                parameters=parameters)
#
#     response_body = json.loads(response.get("body").read())
#     return response_body.get("completion"), prompt
#
#
# def generate_answer_with_context(question: str, sentence: str, context: str,
#                                  max_tokens: int = 200, temperature: float = 0,
#                                  top_p: float = 0.9,
#                                  top_k: int = 250, model_id: str = 'anthropic.claude-v2'):
#
#     user_input = question
#     issue_sentence = sentence
#     issue_question = context
#
#     # prompt = "".join([f"\n\nHuman: {question} \n\n", f"<text>{context}<text>", "\n\nAssistant:"])
#     prompt = f"""
# Human: Here is a sentence, in <sentence></sentence> XML tags:
# Here is questions in <question></question> XML tags to clarify a sentence :
#
# <sentence>
# {issue_sentence}
# </sentence>
#
# <question>
# {issue_question}
# </question>
#
# {user_input}
# Please make answer relevant to <sentence> referring to the question in <question>;
# Please show me only new questions
#
# Assistant:"""
#
#     parameters = {
#         "prompt": prompt,
#         "max_tokens_to_sample": max_tokens,  # min:0, max:8,000, default:200
#         "stop_sequences": ["\n\nHuman:"],
#         "temperature": temperature,  # min:0, max:1, default:0.5
#         "top_p": top_p,  # min:0, max:1, default:1
#         "top_k": top_k  # min:0, max:500, default:250
#     }
#
#     response = bedrock_service.get_predict_from_bedrock_client(model_id=model_id,
#                                                                parameters=parameters)
#
#     response_body = json.loads(response.get("body").read())
#     return response_body.get("completion"), prompt
#
#
# def generate_stream_answer_with_context(question: str, context: str,
#                                         max_tokens: int = 200, temperature: float = 0,
#                                         top_p: float = 0.9,
#                                         top_k: int = 250, model_id: str = 'anthropic.claude-v2'):
#
#     user_input = question
#     issue_question = context
#     # prompt = "".join([f"\n\nHuman: {question} \n\n", context, "\n\nAssistant:"])
#     prompt = f"""
# Human: Here is a issue sentence, in <input></input> XML tags:
# Here is sample questions about sentences, in <text></text> XML tags:
#
# <input>
# {user_input}
# </input>
#
# <text>
# {issue_question}
# </text>
#
# Please make the answer in <input> referring to the sample in <text>; otherwise tell me you don't know it.
#
# Assistant:"""
#
#     parameters = {
#         "prompt": prompt,
#         "max_tokens_to_sample": int(max_tokens),  # min:0, max:8,000, default:200
#         "stop_sequences": ["\n\nHuman:"],
#         "temperature": float(temperature),  # min:0, max:1, default:0.5
#         "top_p": float(top_p),  # min:0, max:1, default:1
#         "top_k": int(top_k)  # min:0, max:500, default:250
#     }
#
#     print(parameters)
#
#     try:
#         response = bedrock_service.get_stream_from_bedrock_client(model_id=model_id,
#                                                                   parameters=parameters)
#         return response.get('body'), prompt
#     except botocore.exceptions.ClientError as error:
#         if error.response['Error']['Code'] == 'AccessDeniedException':
#             print(f"\x1b[41m{error.response['Error']['Message']}\
#                             \nTo troubeshoot this issue please refer to the following resources.\
#                              \nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\
#                              \nhttps://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")
#
#         else:
#             raise error
