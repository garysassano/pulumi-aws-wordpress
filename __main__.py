import pulumi
from pulumi_random import RandomPassword
from components.frontend import WebService, WebServiceArgs
from components.backend import Db, DbArgs
from components.network import Vpc, VpcArgs

# Configuration
config = pulumi.Config()
service_name = config.get("service_name") or "wp-example"
container_image = config.get("container_image") or "wordpress:latest"
db_name = config.get("db_name") or "lampdb"
db_user = config.get("db_user") or "admin"

# Database password
db_password = config.get_secret("db_password")
if not db_password:
    password = RandomPassword(
        "db_password",
        length=16,
        special=True,
        override_special="_%@",
    )
    db_password = password.result

# Network setup
network = Vpc(f"{service_name}-net", VpcArgs())
subnet_ids = [subnet.id for subnet in network.subnets]

# Backend database
be = Db(
    f"{service_name}-be",
    DbArgs(
        db_name=db_name,
        db_user=db_user,
        db_password=db_password,
        subnet_ids=subnet_ids,
        security_group_ids=[network.rds_security_group.id],
        # publicly_accessible=True,  # Uncomment this to override for testing
    ),
)

# Frontend web service
fe = WebService(
    f"{service_name}-fe",
    WebServiceArgs(
        db_host=be.db.address,
        db_port="3306",
        db_name=be.db.name,
        db_user=be.db.username,
        db_password=be.db.password,
        vpc_id=network.vpc.id,
        subnet_ids=subnet_ids,
        security_group_ids=[network.fe_security_group.id],
        container_image=container_image,
    ),
)

# Exports
pulumi.export("Web Service URL", pulumi.Output.concat("http://", fe.alb.dns_name))
pulumi.export("ECS Cluster Name", fe.cluster.name)
pulumi.export("DB Endpoint", be.db.address)
pulumi.export("DB User Name", be.db.username)
pulumi.export("DB Password", be.db.password)
