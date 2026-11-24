---
title: "ChemVertMixParameters"
slug: "chemvertmixparameters"
domains: ["gaschem"]
component_types: ["model"]
subdomains: ["chem_transport"]
domain: "gaschem"
subdomain: "chem_transport"
component_type: "model"
esm_version: "1.1.0"
esm_path: "components/gaschem/chem_transport/vertmix_parameters.esm"
description: "Constants of WRF-Chem's vertical mixing of chemical species (chem/dry_dep_driver.F and chem/module_vertmx_wrf.F, WRF v4.8.0)."
tags: ["gaschem", "chem_transport", "model"]
---

## Description

Constants of WRF-Chem's vertical mixing of chemical species (chem/dry_dep_driver.F and chem/module_vertmx_wrf.F, WRF v4.8.0).

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `k_floor` | `m^2/s` | `1e-06` | Floor WRF applies to the exchange coefficient before mixing chem, ekmfull(k) = max(1.e-6, exch_h(k)) (chem/dry_dep_driver.F:709-712). |

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "variables": {
    "k_floor": {
      "type": "parameter",
      "units": "m^2/s",
      "default": 1e-06,
      "description": "Floor WRF applies to the exchange coefficient before mixing chem, ekmfull(k) = max(1.e-6, exch_h(k)) (chem/dry_dep_driver.F:709-712)."
    }
  },
  "equations": []
}
```

</details>
