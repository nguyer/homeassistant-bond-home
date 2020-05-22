# Bond Home Integration for Home Assistant

Uses the [bond-home Python library](https://github.com/nguyer/bond-home) (note, still very much a work in progress. PRs welcome :)

## Setup instructions

Copy the contents of the `bond` directory from this repo into a directory at `<YOUR_CONFIG_DIR>/custom_components/bond` under your Home Assistant install.

Add the following to your `configuration.yml`:

```yaml
bond:
  host: YOUR_BOND_HUB_IP
  token: YOUR_BOND_TOKEN
```

For details on how to get the Bond Hub's IP address, please see http://docs-local.appbond.com/#section/Getting-Started/Finding-the-Bond-IP

For details on getting a token, please see http://docs-local.appbond.com/#section/Getting-Started/Getting-the-Bond-Token

> **Note**: This is still in the very early stages of development. PRs welcome :)
