
<h1 align=center>
  
  **grepenv** 🔎
  
</h1>

<h3 align=center>

  greps your env

</h3>


<div align=center>

  [![PyPI version](https://badge.fury.io/py/grepenv.svg)](https://badge.fury.io/py/grepenv)
  [![Coverage Status](https://coveralls.io/repos/github/mdLafrance/grepenv/badge.svg?branch=main)](https://coveralls.io/github/mdLafrance/grepenv?branch=main)
  [![Pipeline](https://github.com/mdLafrance/grepenv/actions/workflows/pipeline.yaml/badge.svg)](https://github.com/mdLafrance/grepenv/actions/workflows/pipeline.yaml)
  
</div>

## About
A little tool to search through your environment.  

I made `grepenv` to simplify the process of calling various combinations of `env | grep | sort`, and replicating my aliases for this across machines.

## Installation
`grepenv` can be installed using pip, but [pipx]([pipx](https://github.com/pypa/pipx)) is recommended:
```bash
pipx install grepenv
```
This installs the `grepenv` shell script:
```bash
grepenv --help 
ge --help # The short alias 'ge' is also available
```
## Usage
`grepenv` takes a regex pattern, and matches it against currently available environment variables. 
Calling `grepenv --example` will show some example usage.

```bash
$ grepenv xdg # Will find any key or value that contains the letters xdg (lower or upper case).
```

``` bash
$ grepenv "_api_(key|token)_" --keys # finds any environment variable with this regex pattern, matching only on keys.
GITHUB_API_TOKEN=abc_NlNhalNDL78NAhdKhNAk78bdf7f
OPENAI_API_KEY=123_abcdefghijklmno
```

```bash
$ grepenv --find-key gitlab # Search for an environment variable with the name gitlab, and output it's value.
123_abcdefghijklmnop
# GITLAB_API_TOKEN=123_abcdefghijklmnop
```

```bash
$ grepenv perl --path # Search for the pattern "perl", but only in the PATH
/usr/bin/site_perl
/usr/bin/vendor_perl
/usr/bin/core_perl
```
