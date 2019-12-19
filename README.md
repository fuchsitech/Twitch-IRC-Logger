<h1 align="center">Twitch IRC Logger</h1>

<div align="center">
    A configurable <code>Python 3</code> bot which logs chat messages on twitch channels that are manually set.Forked from disabledtech/Twitch-IRC-Logger
</div>

<br/>

<div align="center">
  <a href="http://badges.mit-license.org">
    <img src="http://img.shields.io/:license-mit-blue.svg?style=flat-square)"
      alt="MIT Licence" />
  </a>
</div>

## Table of Contents
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Example](#example)
- [ToDo](#TODO)



---

## Prerequisites

<br/>

- Python 3.5 or newer.

- <a href="https://pypi.org/project/requests/" target="_blank">Requests</a> is used to get data on the most popular streamers online right now.
```
pip install requests
```

---
## Usage

<br/>

Fill out the settings in ```config.ini``` and then run ```run_bot.py```. Log files will be saved in the same directory as the script in a directory called ```logs```

### Config.ini Settings

<table>
    <tr>
        <td><b>Parameter</b></td>
        <td><b>Description</b></td>
    </tr>
    <tr>
        <td><strong>username</strong></td>
        <td>What the bot will call itself when joining the IRC server. Do not use the same name as a popular streamer, it <b>will</b> cause issues.</td>
    </tr>
    <tr>
        <td><strong>token</strong></td>
        <td>The Twitch IRC requires an OAuth token for authentication. See <a href="https://twitchapps.com/tmi/" target="_blank">here</a> to get your own token.</td>
    </tr>
    <tr>
        <td><strong>client_id</strong></td>
        <td>The Twitch API requires a ClientID for API access which we use to get a list of currently popular streamers. See the <a href="https://dev.twitch.tv/docs/v5" target="_blank">Twitch API docs</a> to get your own client ID</td>
    </tr>
    <tr>
        <td><strong>channel_limit</strong></td>
        <td>The number of IRC channels to join. Ex. If set to 20 the bot will join and log the 20 channels with the most viewers. <i>Max</i>: 100</td>
    </tr>
</table>
<br/>

---

## Example config.ini

This will join the top *10* streamers with the name *john_logger_bot999*.

`config.ini`


`username   = john_logger_bot999` <br/>
`token      = oauth:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` <br/>
`client_id  = xxxxxxxxxxxxxxxxxxxxxxxxxxx` <br/>
`channel_limit = 10` <br/>

---

## TODO

- Create individual file for each channel logged
- Access Meta Information about streams
- Parse Logged Messages to useful format
- Upload Messages and Meta Information to PostgreSQL Database

---

## License

MIT License

Copyright (c) 2019 disabledtech

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

