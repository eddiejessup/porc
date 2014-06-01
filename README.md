## Introduction

API docs for Porc using [Slate](https://github.com/tripit/slate), a [Middleman](http://middlemanapp.com/) template designed for such things. Based on [Orchestrate's API docs](https://github.com/orchestrate-io/apidocs).

## Usage

Building Porc's docs will require Python and Ruby. Once you've installed both of those, run this:

```
bundle install
python docs
bundle exec middleman server
```

Now Porc's documentation will be available at <http://localhost:4567>.

To publish push updates to the documtation live, run `rake publish`. To do that, your GitHub account will need write permissions to the repository.

## Editing

See `README-slate.md` at the root of this project.