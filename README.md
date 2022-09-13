# Bearbot 3.0 - Finding Dips and making Tendies

<img src="static/bearbot_big_hero.png" alt="Bearbot Logo" width="200"/>

## Installation
Pretty straight forward to get started.
```python3
mkdir data
pip install -r requirements.txt
python3 dl.py
```
This will then pull prices for Symbols in `symbols.lst`, calculate the biggest consecutive loss over the last 365 days and the save it to `data/YYYY-MM-DD_SYMBOL.json`. The JSON Files are more like of a "state" keeping mechanism (because this was originally running in AWS Batch with Spot EC2), where the can terminate your instance. The way I built it, it should be fault tolerant for these kind of interruptions, on restart it would just keep going.
### Adding & Removing Symbols
If you want to add or remove symbols you just edit the `symbols.lst`.

## Infrastructure 
Before I refactored Bearbot, it was running on a t4g.small in ca-central-1 (0,0184 USD/hour,2vCPU, 2 GiB RAM) and built with Django an SQLite. That`s about $14 a month. I chose their Gravitron instances, because I love their performance and evironmental impact, that is also why I host my compute in Canada 🇨🇦,
[the ca-centra-1 zone is apparently being powered 99.5% by Hydropower](http://news.hydroquebec.com/en/press-releases/960/green-electricity-attracts-amazon-web-services-to-montreal/). I am just assuming by that fact alone that it must be one of their most sustainable zones (sadly aws does not supply that sort of data per zone).


You see the simplicity of this App. Would you pay $14 a month for it? Nope. I was looking for a cheaper way and started refactoring for AWS Batch + S3. I figured I cloud use some Spot EC2 for compute, run my script and save to S3 where I also planned on hosting. It worked so far as well, hence `dl.py` was built for interruptabillity.

I then thought, wait a minute GitHub is carbon neutral as well, and I could do this with GitHub Pages and GitHub Actions for absolutely free. Here we are.
