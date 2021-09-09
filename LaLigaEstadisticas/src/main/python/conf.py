import yaml

with open('config/config.yaml') as f:

    data = yaml.load(f, Loader=yaml.FullLoader)
    print(data)
    print(type(data))
