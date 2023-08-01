import kopf
import kubernetes.client
import logging, os

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define the handler function for the operator
@kopf.on.create('quachson.me', 'v1', 'myresources')
def create_handler(body, **kwargs):
    logging.info(f"Creating object: {body}")
    replica = body['replica']
    api_instance = kubernetes.client.AppsV1Api()
    namespace = kwargs['namespace']
    logging.info(f"Namespace: f{namespace}")
    deployment_body = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": "my-deployment",
            "namespace": namespace
        },
        "spec": {
            "replicas": replica,
            "selector": {
                "matchLabels": {
                    "app": "my-app"
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": "my-app"
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": "my-container",
                            "image": "karthequian/helloworld:latest",
                            "ports": [
                                {
                                    "containerPort": 80
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }
    api_response = api_instance.create_namespaced_deployment(
        namespace=namespace, body=deployment_body)
    logging.info(f"Deployment created: {api_response}")
  
# @kopf.on.update('quachson.me', 'v1', 'myresources')
# def update_fn(body, **kwargs):
#     logging.info(f"Updating object")
#     deployment_name = "my-deployment"
#     api_instance = kubernetes.client.AppsV1Api()
#     api_instance.read_namespaced_deployment(name=deployment_name, namespace=kwargs['namespace'])

@kopf.on.delete('quachson.me', 'v1', 'myresources')
def delete_fn(body, **kwargs):
    logging.info(f"Deleting object: {body}")

# Run the operator
if __name__ == '__main__':
    kopf.run(default_registry=None)