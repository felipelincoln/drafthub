# How to contribute
We're really happy you're interested in contributing :heart_eyes:.
Please consider first discussing the changes you wanna make via issue before
making a pull request.

# Pull request process
1. Ensure all new dependencies are installed via `pipenv install <package>`.
2. Write documentation if needed. Follow this conventions:
  [PEP 257](https://www.python.org/dev/peps/pep-0257/#what-is-a-docstring).
  You may also want to see this
  [good stuff](https://realpython.com/documenting-python-code/).
3. If you introduced a new `.py` file or an entire django app you have to
  create the documentation pages. To do this you have to run
  `python check.py doc` inside your container.
4. And finally make sure everything is building. Run `python check.py` inside
  your container.

**Examples of steps 3 and 4**:  
Running commands inside a running container

```
docker-compose up --build -d
docker-compose exec web python check.py
docker-compose exec web python check.py test
docker-compose exec web python check.py coverage
docker-compose exec web python check.py lint
docker-compose exec web python check.py doc
docker-compose down
```

Running commands inside a not running container
(new dependencies won't persist).

```
docker-compose run web python check.py
docker-compose run web python check.py test
docker-compose run web python check.py coverage
docker-compose run web python check.py lint
docker-compose run web python check.py doc
```

That's all! :tada:

