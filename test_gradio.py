from gradio_client import Client
client = Client("Nymbo/Virtual-Try-On")
print(client.view_api(return_format="dict"))
