## Like-My-GF
This is an auto-robot to like my girlfriend's post on Instagram.

#### Why This?
My girlfriend always complains that I don't care about what she's doing, I don't like her post on Instagram / Wechat / Weibo... and I don't comment on her posts, bla bla bla.

Being a programmer, I don't really have much ~~interest~~ time to review every social network. So I build this. Although now she knows that I'm using this to like her post. But she's pretty happy about it (don't ask me why) and never complained again. So I'm very happy with this tool.

#### Requires
* httplib2
* simplejson
* [python-instagram](https://github.com/Instagram/python-instagram)

All of these can be installed from pip install

#### Configurations
* Copy the config.ini to config, fill in your Instagram API info
* Setup Target name and path etc...
* Test run, first time run will like about 20 (Instagram's max paginate num of posts), so be aware that the target might think you are crazy.
* Setup the cron, I'm running it every 2 min.

#### To do
1. Setup email alert everytime robot found a new post, include the photo in the email.
2. Support more social media. Weibo, Wechat, Facebook...(This gonna be endless)
3. Maybe if anyone else want to use this, I can setup a web api and allow others to register their target. I can setup an engine to do it.
