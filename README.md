# ShapeMix ATAC

Reference-based deconvolution of ATAC counts using peak accessibility and fragment-length distributions. The model combines a negative-binomial likelihood for total peak counts, a conditional multinomial likelihood for fragment-length bins, and a Gamma prior on effective abundance. Fixed reference signatures are fitted with multi-restart MAP optimization in PyTorch.

## Installation

Requires Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
python examples/toy_fit.py
pytest
```

For library use without the test dependencies, run `pip install .`. AnnData support is available through `pip install ".[anndata]"`. CUDA execution requires a compatible PyTorch installation and GPU.

## Inputs and API

Import from `shapemix_atac`. The core accepts prepared count arrays; fragment alignment and peak calling are upstream steps.

- `estimate_reference_signatures_from_array`: reference counts shaped **cells × peaks × bins**, cell labels, unique barcodes, and explicit ordered cell types and peak IDs. Estimates accessibility, bin probabilities, and cross-fitted dispersion.
- `estimate_reference_signatures_from_layers`: the same estimation from an ordered sequence of sparse or dense cells × peaks matrices.
- `estimate_reference_signatures`: AnnData convenience wrapper.
- `fit_shapemix_map`: spatial counts shaped **spots × peaks × bins**, or ordered sparse bin layers, plus `signatures=reference_signatures`; alternatively provide `A` (types × peaks), `omega` (types × peaks × bins), and `phi_ref` directly. Supply `outer_split_seed` and `inner_mixture_seed` explicitly.

Reference and spatial peak/bin axes must match in order. Counts must be finite nonnegative integers. Default fragment bins are <100 bp, 100–249 bp, and ≥250 bp, named short, mono, and long. Supply matching custom axes when using different bins.

The returned `MAPFitResult` includes spot × cell-type `proportions`, effective `abundance`, and optimization diagnostics. Effective abundance absorbs exposure and should not be interpreted as calibrated cell counts. Inspect convergence diagnostics before interpreting results.

`ShapeMixConfig()` provides the model-version-1 defaults. Set `use_shape=False` for the count-only ablation, or `device="cuda:0"` for CUDA. Optimizer overrides are supported; `validate_protocol_v1()` checks whether settings match the frozen default protocol. The toy example uses shortened optimization for demonstration.

## About this code

This repository contains the model code and numerical tests from the ShapeMix work in deconvATAC. It runs on its own; you do not need to install deconvATAC. Data preparation and the full benchmark pipeline are not included.

The implementation is still research code. The default settings match the original experiments, but a new dataset may need different optimizer settings. There is no license file yet.
