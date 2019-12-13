# jiti
Not sure if I'm that lazy or jira's interface is that bad.

<img src="https://i.imgur.com/aOb1mZf.gif" alt="demo jiti" height="320px">

### Installation
Install it from pypi:
```
pip install --user jiti
```

Create config file:
```
touch ~/.jiti_settings
```

Example credentials file:
```
[credentials]
host=https://your-jira-address.atlassian.net
email=email
token=your api token
```

You can obtain your api token [here](https://id.atlassian.com/manage/api-tokens)


### Usage
You can log hours in two ways, just simply run ```jiti``` and it will prompt you for details:


or

```
jiti log --ticket OP-808 --time 10m --date 2019-09-01
```

Please note that __date is not mandatory__, leaving it empty will set logging date to present day.
