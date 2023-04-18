import pytest
import torch
from transformers import AutoModelForCausalLM


@pytest.mark.parametrize(
    "model_name, base_model, dataset, training_logs",
    [
        (
                "h2ogpt-oasst1-256-20b",
                "[GPT NeoX 20B](https://huggingface.co/EleutherAI/gpt-neox-20b)",
                "h2oai/openassistant_oasst1",
                "https://huggingface.co/h2oai/h2ogpt-oasst1-256-20b/blob/main/gpt-neox-20b.openassistant_oasst1.json.1_epochs.5fc91911bc2bfaaf3b6c2de577c4b0ae45a07a4a.18.zip",
        ),
        (
                "h2ogpt-oasst1-512-12b",
                "EleutherAI/pythia-12b",
                "h2oai/openassistant_oasst1",
                "https://huggingface.co/h2oai/h2ogpt-oasst1-512-12b/blob/main/pythia-12b.openassistant_oasst1.json.1_epochs.d45a9d34d34534e076cc6797614b322bd0efb11c.15.zip",
        ),
        (
                "h2ogpt-oig-oasst1-256-12b",
                "EleutherAI/pythia-12b-deduped",
                "h2oai/h2ogpt-oig-oasst1-instruct-cleaned-v1",
                "https://huggingface.co/h2oai/h2ogpt-oig-oasst1-256-12b/blob/main/pythia-12b-deduped.h2ogpt-oig-oasst1-instruct-cleaned-v1.json.1_epochs.5fc91911bc2bfaaf3b6c2de577c4b0ae45a07a4a.17.zip",
        ),
        (
                "h2ogpt-oig-oasst1-256-6.9b",
                "EleutherAI/pythia-6.9b",
                "h2oai/h2ogpt-oig-oasst1-instruct-cleaned-v1",
                "https://huggingface.co/h2oai/h2ogpt-oig-oasst1-256-6.9b/blob/main/pythia-6.9b.h2ogpt-oig-oasst1-instruct-cleaned-v1.json.1_epochs.5fc91911bc2bfaaf3b6c2de577c4b0ae45a07a4a.9.zip",
        ),
    ],
)
def test_create_model_cards(model_name, base_model, dataset, training_logs):
    model_size = model_name.split("-")[-1].upper()
    assert "B" == model_size[-1]
    assert int(model_size[-2]) >= 0
    model = AutoModelForCausalLM.from_pretrained("h2oai/%s" % model_name,
                                                 local_files_only=False,
                                                 torch_dtype=torch.float16,
                                                 device_map="auto")
    model_arch = str(model)
    model_config = str(model.config)
    with open("README-template.md", "r") as f:
        content = f.read()
        assert "<<MODEL_NAME>>" in content
        content = content.replace("<<MODEL_NAME>>", model_name)

        assert "<<MODEL_SIZE>>" in content
        content = content.replace("<<MODEL_SIZE>>", model_size[:-1])

        assert "<<BASE_MODEL>>" in content
        content = content.replace("<<BASE_MODEL>>", f"[{base_model}](https://huggingface.co/{base_model})")

        assert "<<DATASET>>" in content
        content = content.replace("<<DATASET>>", f"[{dataset}](https://huggingface.co/{dataset})")

        assert "<<MODEL_ARCH>>" in content
        content = content.replace("<<MODEL_ARCH>>", model_arch)

        assert "<<MODEL_CONFIG>>" in content
        content = content.replace("<<MODEL_CONFIG>>", model_config)

        assert "<<TRAINING_LOGS>>" in content
        content = content.replace("<<TRAINING_LOGS>>", training_logs)

        assert "<<" not in content
        assert ">>" not in content

    import os
    os.makedirs(model_name, exist_ok=True)
    with open(os.path.join(model_name, "README.md"), "w") as f:
        f.write(content)
