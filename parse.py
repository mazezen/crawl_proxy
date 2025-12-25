import yaml

def parse() -> str:
    
    with open('.github/workflows/cron.yml', 'r') as file:
        workflow_data = yaml.safe_load(file)

        return workflow_data.get('env')