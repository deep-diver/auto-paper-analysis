import pandas as pd
import datasets
from datasets import Dataset
from huggingface_hub import create_repo
from huggingface_hub.utils import HfHubHTTPError

def push_to_hf_hub(
	qnas, repo_id, token, append=True
):
	exist = False
	df = pd.DataFrame([qnas])
	ds = Dataset.from_pandas(df)
	ds = ds.cast_column("target_date", datasets.features.Value("timestamp[s]"))
    
	try:
		create_repo(repo_id, repo_type="dataset", token=token)
	except HfHubHTTPError as e:
		exist = True
    
	if exist and append:
		existing_ds = datasets.load_dataset(repo_id)
		ds = datasets.concatenate_datasets([existing_ds['train'], ds])
    
	ds.push_to_hub(repo_id, token=token)