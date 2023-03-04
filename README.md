# pulumi-aws-wordpress

Pulumi project that deploys WordPress to AWS using ECS Fargate with RDS backend.

## Resources Deployed

```console
     Type                                 Name                                 Plan       
 +   pulumi:pulumi:Stack                  pulumi-aws-wordpress-dev             create     
 +   ├─ custom:resource:VPC               wp-example-net                       create     
 +   │  ├─ aws:ec2:Vpc                    wp-example-net-vpc                   create     
 +   │  ├─ aws:ec2:InternetGateway        wp-example-net-igw                   create     
 +   │  ├─ aws:ec2:Subnet                 wp-example-net-subnet-eu-central-1a  create     
 +   │  ├─ aws:ec2:SecurityGroup          wp-example-net-rds-sg                create     
 +   │  ├─ aws:ec2:SecurityGroup          wp-example-net-fe-sg                 create     
 +   │  ├─ aws:ec2:Subnet                 wp-example-net-subnet-eu-central-1b  create     
 +   │  ├─ aws:ec2:RouteTable             wp-example-net-rt                    create     
 +   │  ├─ aws:ec2:RouteTableAssociation  vpc-route-table-assoc-eu-central-1a  create     
 +   │  └─ aws:ec2:RouteTableAssociation  vpc-route-table-assoc-eu-central-1b  create     
 +   ├─ random:index:RandomPassword       db_password                          create     
 +   ├─ custom:resource:Frontend          wp-example-fe                        create     
 +   │  ├─ aws:ecs:Cluster                wp-example-fe-ecs                    create     
 +   │  ├─ aws:iam:Role                   wp-example-fe-task-role              create     
 +   │  ├─ aws:lb:TargetGroup             wp-example-fe-app-tg                 create     
 +   │  ├─ aws:iam:RolePolicyAttachment   wp-example-fe-task-policy            create     
 +   │  ├─ aws:lb:LoadBalancer            wp-example-fe-alb                    create     
 +   │  ├─ aws:lb:Listener                wp-example-fe-listener               create     
 +   │  ├─ aws:ecs:TaskDefinition         wp-example-fe-app-task               create     
 +   │  └─ aws:ecs:Service                wp-example-fe-app-svc                create     
 +   └─ custom:resource:Backend           wp-example-be                        create     
 +      ├─ aws:rds:SubnetGroup            wp-example-be-sng                    create     
 +      └─ aws:rds:Instance               wp-example-be-rds                    create     
 ```
