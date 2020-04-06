![build status](https://travis-ci.com/eran-tau/wacky-wango.svg?branch=master)
[![codecov](https://codecov.io/gh/eran-tau/wacky-wango/branch/master/graph/badge.svg)](https://codecov.io/gh/eran-tau/wacky-wango)

# Wacky Wango

Final Advanced Computer Design mind reading project. See [full documentation](https://wacky-wango.readthedocs.io/en/latest/). (Not implemented yet)

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:eran-tau/wacky-wango.git
    ...
    $ cd wacky-wango/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [wackywango] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:

    ```sh
    $ pytest tests/
    ...
    ```
    
4. Depending on your local setup, you might need to install docker and some other stuff:

    ```sh
    $ sudo apt-get install postgresql
    $ sudo apt-get install python-psycopg2
    $ sudo apt-get install libpq-dev
    ```
    
## Usage

1. The easiest way to see that everything is working is to use the run-pipeline which will run everything on docker:

    ```sh
    $ sudo ./run-pipeline.sh
    ...
    ```


2. You'll need to upload some data into the system. The repo provides a very small sample you can use or download a real sample file from [here](https://storage.googleapis.com/advanced-system-design/sample.mind.gz) 
To uploaded the sample (Either the one provided or the one you downloaded), use:


    ```sh
    $ python -m wackywango.client upload-sample -h '127.0.0.1' -p 8000 'sample/small_sample.mind.gz'
    ```

3. Once done, just go to: http://127.0.0.1:8080/ and enjoy

## Detailed Usage


The `wackywango` packages provides the following modules:

- `client`
    
    The client is used to upload sample data to the server. Example:
    
    ```sh
    $ python -m wackywango.client upload-sample -h '127.0.0.1' -p 8000 'sample/small_sample.mind.gz'
    ```

- `server`

    The server is used to get the data, and populate it to a rabbitmq with the relevant parsed data.     
    
    ```sh
    $ python -m wackywango.server run-server -h '0.0.0.0' -p 8000 'rabbitmq://rabbitmq-server:5672/'
    ```

- `parsers`
    
    The parser module loads predefined parsers into the system that listen to the queue, and parse the relevant information. 
    
    ```sh
    $ python -m wackywango.parsers run-parser 'color_image' 'rabbitmq://rabbitmq-server:5672/'
    ```


- `saver`
    
    The saver saves the results from the parser into postgres db. 
    
    ```sh
    $ python -m wackywango.saver run-saver  'postgresql://postgres-server:5432' 'rabbitmq://rabbitmq-server:5672/'
    ```

- `api`
    
    api provides some useful functionality to get the data saved in the db. [Full API below](#API). 
 
    ```sh
    $ python -m wackywango.saver run-saver  'postgresql://postgres-server:5432' 'rabbitmq://rabbitmq-server:5672/'
    ```

## API
   

The `foobar` package also provides a command-line interface:

```sh
$ python -m foobar
foobar, version 0.1.0
```

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

The CLI provides the `foo` command, with the `run`, `add` and `inc`
subcommands:

```sh
$ python -m foobar foo run
foo
$ python -m foobar foo inc 1
2
$ python -m foobar foo add 1 2
3
```

The CLI further provides the `bar` command, with the `run` and `error`
subcommands.

Curiously enough, `bar`'s `run` subcommand accepts the `-o` or `--output`
option to write its output to a file rather than the standard output, and the
`-u` or `--uppercase` option to do so in uppercase letters.

```sh
$ python -m foobar bar run
bar
$ python -m foobar bar run -u
BAR
$ python -m foobar bar run -o output.txt
$ cat output.txt
BAR
```

Do note that each command's options should be passed to *that* command, so for
example the `-q` and `-t` options should be passed to `foobar`, not `foo` or
`bar`.

```sh
$ python -m foobar bar run -q # this doesn't work
ERROR: no such option: -q
$ python -m foobar -q bar run # this does work
```

To showcase these options, consider `bar`'s `error` subcommand, which raises an
exception:

```sh
$ python -m foobar bar error
ERROR: something went terribly wrong :[
$ python -m foobar -q bar error # suppress output
$ python -m foobar -t bar error # show full traceback
ERROR: something went terribly wrong :[
Traceback (most recent call last):
    ...
RuntimeError: something went terrible wrong :[
```
