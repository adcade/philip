# Philip

*Philippides is the messenger who delivered the news of victory from Marathon to Athens.*

Philip is a small tool for deploying applications to [Marathon](https://mesosphere.github.io/marathon/) and, of course, deliver the news of success from Marathon to the user.

Currently it only supports tags for docker applications, groups with tags are not supported (if you don't need to update tag then it doesn't matter).

## Install

Directly from GitHub:

``` bash
$ pip install git+https://github.com/adcade/philip.git@0.1.0
```

Or, build from the sources:

```bash
$ python setup.py install
```

## Configuration

By default, Philip reads from:
`~/.config/philip/config.yml` or `~/.config/philip/config.json`
but you can choose a specific configuration file by `philip -c config.json app.json` please reference to CLI help (`philip -h`)

``` yaml
stage:
    url: STAGE_MARATHON_URL
    username: YOUR_USERNAME
    password: YOUR_PASSWORD
prod:
    url: PROD_MARATHON_URL
    username: YOUR_USERNAME
    password: YOUR_PASSWORD
whatever:
    url: WHATEVER_MARATHON_URL
    username: YOUR_USERNAME
    password: YOUR_PASSWORD
```

## Marathon artifact/group extension

- First, like the configuration, you are allowed to use either json or yaml,
- Second, you can add profiles that can override the default content of the artifact/group configuration. The extended format is under the format like below:

``` yaml
# your regular artifact/group config
# ...
setting1:
  setting1_2: 'being overwritten'
# end of the config
profiles:
  some_profile:
    setting1:
      setting1_2: 'overwrites'
    setting2: 'additions'
    # the config to override the regular ones
    # end of the overriding conf
  # other profiles ...
```

A more detailed sample:

``` yaml
id: python
instances: 1
cpus: 0.1
mem: 64.0
args: ["python", "-m", "http.server", "8000"]
container:
  type: DOCKER
  docker:
    image: python:3.4.3
    network: BRIDGE
profiles:
  stage:
    container:
      docker:
        portMappings:
          -
            containerPort: 8000
            servicePort: 10000
  prod:
    container:
      docker:
        portMappings:
          -
            containerPort: 8001
            servicePort: 10001
```

When you specify your profile as stage (`philip apps create -p stage -m app.yml`), you got a final config like below:

``` yaml
id: ./python-8001-10001
instances: 1
cpus: 0.1
mem: 64.0
args: ["python", "-m", "http.server", "8001"]
container:
  type: DOCKER
  docker:
    image: python:3.4.3
    network: BRIDGE
    portMappings:
      -
        containerPort: 8001
        servicePort: 10001
```

## CLI

The CLI is organized the same way as [Marathon REST API](https://mesosphere.github.io/marathon/docs/rest-api.html):

```bash
$ philip -h
usage: philip [-h] {apps,tasks,groups,deployments,server,events} ...

positional arguments:
  {apps,tasks,groups,deployments,server,events}
                        sub-command help
    apps                api for apps
    tasks               api for tasks
    groups              api for groups
    deployments         api for deployments
    server              api for servers
    events              api for events

optional arguments:
  -h, --help            show this help message and exit
```

And you can also do:

```bash
$ philip apps create -h
usage: philip apps create [-h] [-p PROFILE] [-c CONFIGFILE] [--dry-run]
                          [-m MESSAGE] [-t TAG]

optional arguments:
  -h, --help            show this help message and exit
  -p PROFILE, --profile PROFILE
                        profile to run
  -c CONFIGFILE, --configfile CONFIGFILE
                        Config for Philip, by default locates at
                        ~/.config/philip/config.json
  --dry-run             dry run this command without really execute
  -m MESSAGE, --message MESSAGE
                        the message file Philip delivery to marathon
  -t TAG, --tag TAG     the tag of the application
```

So if you want to create a new application on Marathon using Philip, you would do:

```bash
$ philip apps create -m my-app.yaml -p stage -t 0.1.0
```

This will deploy `my-app.yaml` with the docker image tagged as 0.1.0, use the profile `stage` with it's `url`, `username`, `password` and overwrite the marathon artifact/group with the corresponding `profiles` section, please see `Marathon artifact/group extension`.

**Note: by default `stage` is being used as your profile, `Philipfile` as the message file, and use the image tag specified in the file message.**
