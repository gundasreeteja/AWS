from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_lambda as lambda_,
    aws_lambda_event_sources as lambda_event_sources
)


class SqsLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Creating SQS Queue
        queue = sqs.Queue(
            self, "Sqs-Lambda-Queue",
            visibility_timeout=Duration.seconds(300),
        )

        # Creating Lambda Function
        sqs_lambda = lambda_.Function(self, "SQS-Lambda",
                                      handler = 'lambda_handler.handler',
                                      runtime=lambda_.Runtime.PYTHON_3_12,
                                      code=lambda_.Code.from_asset('lambda')
                                      )

        # Creating Event Source
        sqs_event_source = lambda_event_sources.SqsEventSource(queue)

        # Add SQS Event Source to Lambda
        sqs_lambda.add_event_source(sqs_event_source)

        # topic = sns.Topic(
        #     self, "SqsLambdaTopic"
        # )

        # topic.add_subscription(subs.SqsSubscription(queue))
