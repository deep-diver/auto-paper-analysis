# Auto Paper Analysis

This project automatically generate Questions and Answers on a given arXiv ids. For now, the CLI tool only supports to grasp arXiv ids from [Hugging Face 🤗 Daily Papers](https://huggingface.co/papers). However, it will be generally support a single arXiv id or list of arXiv ids shortly.

You can see the generated QA dataset from [chansung/auto-paper-qa2](https://huggingface.co/datasets/chansung/auto-paper-qa2) repository. Also, you can see how these dataset could be used with [PaperQA](https://huggingface.co/spaces/chansung/paper_qa) space application.

## Instruction

If you want to do prompt engineering, modify the [prompts.toml](https://github.com/deep-diver/auto-paper-analysis/tree/main/app/constants/prompts.toml) file. There are two prompts to play with.

To generate QAs of arXiv papers on a specific date, run:

```shell
export GEMINI_API_KEY=<YOUR-GEMINI-API>
export HF_ACCESS_TOKEN=<YOUR-HF-ACCESS-TOKEN>

python app.py --target-date $current_date \
    --gemini-api $GEMINI_API_KEY \
    --hf-token $HF_ACCESS_TOKEN \
    --hf-repo-id $hf_repo_id
```

If you want to generate QAs of arXiv papers on the range of date, run:

```shell
export GEMINI_API_KEY=<YOUR-GEMINI-API>
export HF_ACCESS_TOKEN=<YOUR-HF-ACCESS-TOKEN>
export HF_DATASET_REPO_ID=<YOUR-HF-DATASET-REPO-ID>

./date_iterator.sh "2024-03-01" "2024-03-03" $HF_DATASET_REPO_ID
```