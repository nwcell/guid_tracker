# Guid Tracker
This is an API for storing data by GUID.  It stores the data in a relational DB (configureable) and uses redis as a cache.

I chose to go with a new framework, [FastAPI](https://fastapi.tiangolo.com) (which builds off of [Starlette](https://www.starlette.io)), which is a fully asyncronous framework that leverages python's new typehints for generating Swagger documentation.

![Generated docs](docs/swagger.png?raw=true "Logo Title Text 1")

## Run
First, you'll want to clone the repo.  The codebase is using pipenv, so go install w/ pipenv.  In pipenv, we're using a custom command `serve`.

Once the server is running, you should be able to load [http://127.0.0.1:8000](http://127.0.0.1:8000).  This will display the swagger docs for the endpoint.

```bash
# Clone the repo & go into it.
git clone https://github.com/nwcell/ir_talent.git
cd ir_talent

# We're using pipenv, so install using that.
pipenv install

# Copy the .env.dist to .env, the dev server will grab envs from here
# You'll want to update the .env to point to your redis instance & db
cp .env.dist .env

# Run things and navigate to http://127.0.0.1:8000 for the API specs.
pipenv run serve
```

## Test
To run tests, you'll need to
```
pipenv install -d
pipenv run test
```
