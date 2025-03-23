# coding=utf8
import argparse
import grpc

import yandex.cloud.ai.foundation_models.v1.text_common_pb2 as pb
import yandex.cloud.ai.foundation_models.v1.text_generation.text_generation_service_pb2_grpc as service_pb_grpc
import yandex.cloud.ai.foundation_models.v1.text_generation.text_generation_service_pb2 as service_pb

def run(iam_token, folder_id, user_text):
    cred = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel('llm.api.cloud.yandex.net:443', cred)
    stub = service_pb_grpc.TextGenerationServiceStub(channel)

    request = service_pb.CompletionRequest(
        model_uri=f"gpt://{folder_id}/yandexgpt/rc",
        completion_options=pb.CompletionOptions(
            max_tokens={"value": 2000}, 
            temperature={"value": 0.2}
        ),
    )
    message_system = request.messages.add()
    message_system.role = "system"
    message_system.text = "prompt"

    message_user = request.messages.add()
    message_user.role = "user"
    message_user.text = user_text

    it = stub.Completion(request, metadata=(
        ('authorization', f'Bearer {iam_token}'),
    ))
    for response in it:
        for alternative in response.alternatives:
            print (alternative.message.text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--iam_token", required=True, help="IAM token")
    parser.add_argument("--folder_id", required=True, help="Folder id")
    parser.add_argument("--user_text", required=True, help="User text")
    args = parser.parse_args()
    run(args.iam_token, args.folder_id, args.user_text)
