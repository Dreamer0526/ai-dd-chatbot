# import random
# from functools import partial
#
# from django.http import HttpResponse
# from transformers import GPT2LMHeadModel
# from transformers import GPT2Tokenizer
#
# from chatbot.utils.logger import logger
# import chatbot.utils.wechat_integration as wi
#
#
# def generate_answer(prompt, model, tokenizer, **kwargs):
#     model = model.eval()
#     input_ids = tokenizer.encode(prompt + tokenizer.eos_token, return_tensors="pt")
#     history_ids = model.generate(input_ids, **kwargs)
#
#     output_list = []
#     for output in history_ids:
#         output_list.append(
#             tokenizer.decode(output[input_ids.shape[-1] :], skip_special_tokens=True)
#         )
#
#     return output_list
#
#
# tokenizer = GPT2Tokenizer.from_pretrained("microsoft/DialoGPT-medium")
# model = GPT2LMHeadModel.from_pretrained("microsoft/DialoGPT-medium")
#
# generator_registry = [
#     {
#         "id": x,
#         "open_id": None,
#         "callable": partial(generate_answer, model=model, tokenizer=tokenizer),
#     }
#     for x in range(10)
# ]
#
#
# def find_generator(user_open_id):
#     for generator in generator_registry:
#         if user_open_id == generator["open_id"]:
#             return generator
#
#     for generator in generator_registry:
#         if generator["open_id"] is None:
#             generator["open_id"] = user_open_id
#             return generator
#
#     return None
#
#
# def index(request):
#     if request.method == "GET":
#         return wi.check_signature(request)
#
#     if request.method == "POST":
#         # parse user info and message received
#         user_open_id = request.GET["openid"]
#         msg_recv = wi.parse_msg_recv(request)
#         logger.info(f"Message received from user {user_open_id}: {msg_recv}")
#
#         # find generator
#         generator = find_generator(user_open_id)
#         logger.info(f"Generator {generator['id']} used for user {user_open_id}")
#
#         # prepare answer
#         output_list = generator["callable"](
#             msg_recv,
#             num_beams=5,
#             early_stopping=True,
#             no_repeat_ngram_size=2,
#             num_return_sequences=5,
#         )
#         logger.info(
#             f"All answers prepared for user {user_open_id}: {'; '.join(output_list)}"
#         )
#
#         answer_idx = random.randint(0, len(output_list) - 1)
#         answer = "\n".join(output_list)
#         logger.info(f"Answer selected for user {user_open_id}: {answer}")
#
#         # return answer to user
#         response = wi.gen_response(
#             to_user_open_id=user_open_id,
#             from_user_open_id="gh_74ccc0ad896d",  # PMXbot003
#             content=answer,
#         )
#         return HttpResponse(response, content_type="application/xml")
