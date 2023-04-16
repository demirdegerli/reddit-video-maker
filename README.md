# Reddit Video Maker

Reddit Video Maker gets a random or user entered post then gets it's comments and makes a video from these comments.

https://user-images.githubusercontent.com/67432156/179314072-11e87099-8845-42be-bb9b-9f13dc391145.mp4

**Note: Please use the latest commit if you're not testing something. This tool has not specific versions.**

## Get started

### Clone the repository
```sh
git clone https://github.com/demirdegerli/reddit-video-maker.git
cd ./reddit-video-maker
```

### Install packages
```sh
pip3 install -r requirements.txt
```

### Install ImageMagick
Go to the [ImageMagick download page](https://imagemagick.org/script/download.php) and install the right one.

**This is required for converting texts to image.**

### Install FFmpeg
Install the right one from the [FFmpeg download page](https://ffmpeg.org/download.html).

There are tons of guides explaining how to install FFmpeg on Internet. Follow one of these.

_Note: Windows users may need to add FFmpeg to the path._

### Get Reddit credentials
- Go to the [Reddit Apps Panel](https://www.reddit.com/prefs/apps/).
- Click `create app...` or if you already created an app use it's credentials or click `create another app...`.
- Select `script` and fill other form sections.
- Click `create app`.
- Get client id from under the app name and client secret from `secret` section.

Run the script and follow it
```sh
python3 main.py
```

Enjoy!
