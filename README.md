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
    $ python -m wackywango.client upload-sample -h '127.0.0.1' -p 8000 'tests/small_sample.mind.gz'
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
    $ python -m wackywango.server run-server -h '0.0.0.0' -p 8000 'rabbitmq://127.0.0.1:5672/'
    ```

- `parsers`
    
    The parser module loads predefined parsers into the system that listen to the queue, and parse the relevant information. 
    
    ```sh
    $ python -m wackywango.parsers run-parser 'color_image' 'rabbitmq://127.0.0.1:5672/'
    ```


- `saver`
    
    The saver saves the results from the parser into postgres db. 
    
    ```sh
    $ python -m wackywango.saver run-saver  'postgresql://127.0.0.1:5432' 'rabbitmq://127.0.0.1:5672/'
    ```

- `api`
    
    api provides some useful functionality to get the data saved in the db. [Full API below](#API). 
 
    ```sh
    $ python -m wackywango.saver run-saver  'postgresql://127.0.0.1:5432' 'rabbitmq://127.0.0.1:5672/'
    ```

## API
   
API server supports the following API:
* `GET /users`

    Returns the list of all the supported users, including their IDs and names only.


* `GET /users/user-id`

    Returns the specified user's details: ID, name, birthday and gender.

* `GET /users/user-id/snapshots`

    Returns the list of the specified user's snapshot IDs and datetimes only.|


* `GET /users/user-id/snapshots/snapshot-id`

    Returns the specified snapshot's details: ID, datetime, and the available results' names only (e.g. pose).


* `GET /users/user-id/snapshots/snapshot-id/result-name`

    Returns the specified snapshot's result as a json. The result has some data url for binary data in case of binary data
    
   


## CLI

The `wackywango` package also provides a command-line interface service, each corresponding to an API:

```sh
$ python -m wackywango.cli get-users
…
$ python -m wackywango.cli get-user 1
…
$ python -m wackywango.cli get-snapshots 1
…
$ python -m wackywango.cli get-snapshot 1 2
…
$ python -m wackywango.cli get-result 1 2 'pose'
```

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).


Do note that each command's options should be passed to *that* command, so for
example the `-q` and `-t` options should be passed to `wackywango.cli`, not `get-users` or
`get-user` etc...

```sh
$ python -m wackywango.cli get-users -q # this doesn't work
ERROR: no such option: -q
$ python -m wackywango.cli -q get-users # this does work
```

## Parsers

There are 4 built in parsers:
* `pose`:

    Parses a snapshot's pose, and output in a json format the translation and rotation
  
* `feelings`:

    Parses a snapshot's feelings, and output in a json format the feelings: hunger, hapiness etc...
    
* `color_image`:
    
    Parses a snapshot's color image, saves the color image as jpg to the designated location, and output a json with it's location
    
* `depath_image`:
    
    parses a snapshot's depth image, save the depth image as a heatmap to the designated location, and output a json. 
    
### Write you own parsers 

You can write your own parsers, that's super easy:
1. Go to `parsers/my_parsers`
2. A new parser is either a function that starts with parse_ and with an additional field `parser_type` that tell which parser type it accepts Or an Class called Something*Parser*. If you're using a Class please provide a parse method in the Class 
3. The function get's a context and a snapshot decoded from proto. 
4. The parser should return the value that the parser wants publish. 

#### The `context` class:
The context class provide the following functionality:
* `save(data)`:

    If you data support the `save` method, use this in order to save it to a designated location
    
* `get_save_path()`:

    If you data doesn't support `save`, use this method to get where you'll need to save your data, and save it manually. 

* `set_result(result)`:

    In case you want to have better logic for the result you're provided, you can override the default result, and write your own. 
        
        
Your new parser will be automatically collected. Note that if you created a new type of parser, you should add it to the parsers type the server knows in the config located at `config/cofig.ini`



