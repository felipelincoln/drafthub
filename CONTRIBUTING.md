# How to contribute
We're really happy you're interested in contributing :heart_eyes:.  
Please consider first discussing the changes you wanna make via issue before
making a pull request.

# Development environment setup
1. Clone this repo and [get docker :whale2::package:](https://docs.docker.com/get-docker/)
2. Start docker: `docker-compose up --build`
3. Make your changes! :sunglasses:

# Pull request process
1. Ensure all new dependencies are installed via `pipenv install <package>`
2. Write documentation if needed. We follow the [google style](http://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
3. Perform full check by running `docker-compose exec web python check.py`
4. Make a pull request!


That's all! :tada:

