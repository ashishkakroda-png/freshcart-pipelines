# Part C — Local model checks and run evidence checklist

The supplied Mage notebook uses `train_test_split(..., test_size=0.2, random_state=42)` and a `DecisionTreeClassifier(random_state=42)`. The repository's importable block modules mirror that classroom logic so pytest can test the transformer outside Mage.

A local dry check with scikit-learn gives the following results for the provided 150-row Iris dataset:

| max_depth | Test accuracy | `test_accuracy` (>= 0.80) | CSV created by Mage if test is enforced? |
|---:|---:|---|---|
| 1 | 0.667 | Fail | No |
| 2 | 0.933 | Pass | Yes |
| 3 | 0.967 | Pass | Yes |
| 4 | 0.933 | Pass | Yes |
| 5 | 0.933 | Pass | Yes |

These are local scikit-learn checks of the same split/model configuration, not a claim that Mage has been run. Run the Mage notebook to capture the required pipeline-run output and verify the table in your Mage version.

## Evaluation branch

The `metadata.yaml` in `iris_project/pipelines/iris_classifier/` branches `train_model` to both `save_results` and `evaluate_model`. `evaluate_model.py` prints a confusion matrix and returns accuracy, macro precision, macro recall and macro F1.

## Evidence still to capture from your own run

- `mage run iris_project iris_classifier --test` successful run.
- For each depth 1–5, delete `iris_predictions.csv`, run with `--runtime-vars`, and record whether the exporter ran.
- Mage UI screenshot showing `train_model` branching to `save_results` and `evaluate_model`.
- Confusion matrix and metrics table from the actual Mage run.
