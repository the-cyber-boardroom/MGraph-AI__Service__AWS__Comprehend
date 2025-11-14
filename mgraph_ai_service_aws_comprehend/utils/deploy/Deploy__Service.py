from osbot_fast_api_serverless.deploy.Deploy__Serverless__Fast_API import Deploy__Serverless__Fast_API
from mgraph_ai_service_aws_comprehend.config                       import SERVICE_NAME, LAMBDA_DEPENDENCIES__AWS__COMPREHEND
from mgraph_ai_service_aws_comprehend.fast_api.lambda_handler      import run


class Deploy__Service(Deploy__Serverless__Fast_API):

    def deploy_lambda(self):
        with super().deploy_lambda() as _:
            # Add any service-specific environment variables here
            # Example: _.set_env_variable('AWS_REGION', 'us-east-1')
            return _

    def handler(self):
        return run

    def lambda_dependencies(self):
        return LAMBDA_DEPENDENCIES__AWS__COMPREHEND

    def lambda_name(self):
        return SERVICE_NAME
