I've selected a "Camera Surveillance System" template of the "CM3065 Intelligent Signal Processing" course.

The reason why I've selected this template is that I'm interested in the field of computer vision and home security.

I personally have a few security cameras at home because I want to know what is happening at home when I'm not there.
These cameras come with a mobile app that allows me to view the live video from the cameras and also to view the recorded videos.
These videos are stored in the cloud provided by the camera manufacturer.
And these services worked well for me for many years. It is a really easy to use.

But these are some concerns about these services.
First, these service are paid and charge a monthly fee depending on the number of cameras and the number of days of video storage.
It could be quite expensive if you have many cameras and want to store the videos for a long time.

Second, the videos are stored in a private cloud in unknown jurisdiction. It's not clear who has access to the videos so it arises some privacy concerns.
For many users it could be a deal breaker if someone else can view the live video from inside of their home.
Moreover, some of these services has been hacked in the past and the videos were leaked to the public.

An alternative solution that addresses these concerns is to use a local storage to store the videos instead of the cloud.
There are free open source software that can be used to build a camera surveillance system with a local storage such as [Kerberos](https://doc.kerberos.io/).

While these software are pretty mature and have many features, they are not as easy to use as the commercial services.
They require some technical knowledge to setup and maintain. Additionally, these software usually have a web interface to view the videos which lacks the convenience of the mobile app.

So I want to build a camera surveillance system that addresses these problems by using the local storage to store the videos and I would like to accompany this system with a convenient mobile app to view the videos similar to the commercial services.
