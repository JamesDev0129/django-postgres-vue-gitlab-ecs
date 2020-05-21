from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_elasticloadbalancingv2 as elbv2,
    aws_sqs as sqs,
)


class CeleryDefaultWorkerService(core.Construct):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(
            scope, id, **kwargs,
        )

        # self.celery_default_worker_task = ecs.FargateTaskDefinition(
        #     self, "DefaultCeleryWorkerTask"
        # )

        # self.celery_default_worker_task.add_container(
        #     "DefaultCeleryWorkerContaienr",
        #     image=scope.image,
        #     logging=ecs.LogDrivers.aws_logs(
        #         stream_prefix="CeleryDefaultWorker"
        #     ),
        #     environment=scope.variables.regular_variables,
        #     secrets=scope.variables.secret_variables,
        #     command=[
        #         'celery',
        #         'worker',
        #         '-A',
        #         'backend.celery_app:app',
        #         '-l',
        #         'info',
        #     ],
        # )

        # self.celery_default_worker_service = ecs.FargateService(
        #     self,
        #     "DefaultCeleryWorkerService",
        #     task_definition=self.celery_default_worker_task,
        #     assign_public_ip=True,
        #     cluster=scope.ecs.cluster,
        #     security_group=ec2.SecurityGroup.from_security_group_id(
        #         self,
        #         "CeleryDefaultWorkerSG",
        #         security_group_id=scope.vpc.vpc_default_security_group,
        #     ),
        # )

        self.default_celery_worker_queue = sqs.Queue(
            self, "DefaultCeleryWorkerQueue", queue_name="default"
        )

        self.celery_default_worker_service = ecs_patterns.QueueProcessingFargateService(
            self,
            "CeleryDefaultWorkerService",
            image=scope.image,
            queue=self.default_celery_worker_queue,
            environment=scope.variables.regular_variables,
            secrets=scope.variables.secret_variables,
            command=[
                'celery',
                'worker',
                '-A',
                'backend.celery_app:app',
                '-l',
                'info',
            ],
            family="celery-default-worker",
            log_driver=ecs.LogDrivers.aws_logs(
                stream_prefix="CeleryDefaultWorker"
            ),
            vpc=scope.vpc,
            desired_task_count=1,
        )
