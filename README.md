# Instagram Watchdog
A python script that can watch public instagram profiles for new posts and sends notifications to a telegram channel. Uses the official Bot API by Telegram and the official API by Instagram!

## WARNING
**\[10.12.2018\] Since Instagram deprecated their public API this repository will not be maintained anymore. Programs/Scripts or parts of them will not work properly anymore! USE AT OWN RISK!**

## Features:
- Watch instagram profiles for new posts (private and public profiles)
- Retrieve new posts from instagram profiles (only public profiles)
- Watch instagram profiles for new profile pictures (private and public profiles)
- Send reminders to check stories page (stories will only be shown if profile is public)

## Usage:

set script entries at bottom accordingly:

```python
	user_ids = []

	IB = InstaBot("instabot.synconf", "channel", "api_token")

	IB.instaBot(user_ids, 0, 21)
```

- user_ids: a list of user ids of profiles you want to observe e. g. [25025320](https://instagram.com/instagram). User IDs can be retrieved with [OSINT](https://inteltechniques.com/menu.html).
- InstaBot: set channel and api_token according to your Telegram. E. g. "@channelname" or "channel-id". The parameter api_token has to be a valid token for a Telegram Bot you own! [More](https://core.telegram.org/)
- Method instaBot takes three arguments: user_ids (see above), rtime and stime.
  - rtime is the time (in seconds) for how long the script should run (if 0 the script will run forever). The default is ~1h.
  - stime is the time (hour) when story notifications should be sent. The default is 21 (21:00).

## The Future of this Project

Instagram Watchdog (or InstaBot) was incorporated into [InstaPython - A small python package to access and deal with Instagram data!](https://github.com/t0xic-m/instapython) and will be updated and further developed there!

## License

[MIT License](https://github.com/t0xic-m/instagram_watchdog/blob/master/LICENSE.md)

## Contact

- Website: [Web](https://t0xic-m.github.io/web)
- Website: [GitHub](https://t0xic-m.github.io)
- Contact: [Mail](mailto:micha.birklbauer@gmail.com)
