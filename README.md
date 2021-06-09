# Veides SDK for Python

[![Build Status](https://travis-ci.org/Veides/veides-sdk-python.svg?branch=master)](https://travis-ci.org/Veides/veides-sdk-python)
[![Coverage Status](https://coveralls.io/repos/github/Veides/veides-sdk-python/badge.svg?branch=master)](https://coveralls.io/github/Veides/veides-sdk-python?branch=master)
[![Latest version](https://img.shields.io/pypi/v/veides-sdk.svg)](https://pypi.org/project/veides-sdk)
[![Python versions](https://img.shields.io/pypi/pyversions/veides-sdk.svg)](https://pypi.org/project/veides-sdk)

This repository contains Python modules for Veides SDK. It allows Python developers to easily connect and interact with Veides platform.

**Jump to**:

* [Installation](#Installation)
* [Samples](#Samples)
* [Features](#Features)

## Installation

### Using pip

```bash
pip3 install veides-sdk
```

### From source

```bash
git clone https://github.com/Veides/veides-sdk-python.git
python3 -m pip install ./veides-sdk-python
```

## Samples

[Samples README](https://github.com/Veides/veides-sdk-python/blob/master/samples)

## Features

### Veides Stream Hub Client

- **SSL/TLS**: By default, this library uses encrypted connection
- **Auto Reconnection**: Client support automatic reconnect to Veides Stream Hub in case of a network issue

### Veides API Client

- **Methods operations**: Use your application to invoke methods on agent
