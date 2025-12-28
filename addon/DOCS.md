# Home Assistant Add-on: My Python Add-on

## About

This is a Python-based Home Assistant add-on template. Replace this description with details about your add-on's functionality.

## Installation

1. Navigate to the Supervisor panel in your Home Assistant frontend
2. Click on "Add-on Store"
3. Add this repository URL
4. Find "My Python Add-on" in the add-on store
5. Click "Install"

## Configuration

The add-on can be configured through the following options:

### Option: `log_level`

The `log_level` option controls the level of log output by the add-on.

```yaml
log_level: info
```

Possible values:
- `trace`: Show every detail, like all called internal functions
- `debug`: Shows detailed debug information
- `info`: Normal (usually) interesting events
- `warning`: Exceptional occurrences that are not errors
- `error`: Runtime errors that don't require immediate action
- `fatal`: Something went terribly wrong. Add-on becomes unusable

**Note**: Debug and trace logs may include sensitive information!

## Usage

After installation and configuration:

1. Start the add-on
2. Check the logs for any errors
3. Access the add-on through the Home Assistant interface (if applicable)

## Support

Got questions?

You could open an issue on GitHub:
https://github.com/YOUR-USERNAME/YOUR-REPO/issues

## Authors & Contributors

This add-on was created by YOUR NAME.

## License

Apache License 2.0 - See [LICENSE](https://github.com/YOUR-USERNAME/YOUR-REPO/blob/main/LICENSE) for details.
