# laphw-python-client

A CLI tool for accessing Linux laptop hardware fixes from the [laphw](https://github.com/laphw/laphw) repository.

## Installation

```bash
# Install from PyPI (when published)
pip install laphw

# Or install from source
pip install git+https://github.com/laphw/laphw-python-client.git
```

## Usage

### Search for fixes

```bash
# Search for audio fixes
laphw search "audio"

# Search with filters
laphw search "wifi" --dist ubuntu --hw dell
```

### Show specific fix

```bash
laphw show ubuntu/dell/xps-13-9370/audio.md
```

### List available fixes

```bash
# List all fixes
laphw list

# Filter by distribution
laphw list --dist ubuntu

# Filter by hardware vendor
laphw list --hw dell
```

### Other commands

```bash
# Show version
laphw version

# Show help
laphw --help
```

## Features

- **Fast search** - Find hardware fixes quickly
- **Rich output** - Beautiful terminal formatting
- **Multiple filters** - Filter by distribution, hardware, tags, difficulty
- **Offline capable** - Works with local cache (planned)
- **Cross-platform** - Works on Linux, macOS, Windows

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.
