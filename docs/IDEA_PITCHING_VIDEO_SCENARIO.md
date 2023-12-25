Hi, my name is Dzmitry.
I'm passionate about computer vision and I'm pretty paranoid about my home security.

This is the reason why i've chosen a "Camera Surveillance System" template for my final project.

At my home, I use these little guys to monitor the situation inside.
And this doorbell camera outside.

Both of these surveillance systems come with subscription-based cloud services
that allow users to view the live video and recordings via convenient mobile apps.

They also detect motions and send push notifications to alert users about any events when they are away from home.

====

These and other similar commercial surveillance solutions worked well for me and other users.
But there are some drawbacks.

First, these services are paid and charge a monthly fee depending on the number of cameras and the number of days of video storage.
It could be quite expensive if you have many cameras and want to store the recordings for a long period of time.

====


Second, the recordings are stored in a private cloud in unknown jurisdiction. It's not clear who has access to the videos so it arises some privacy concerns.

====

Some of the vendors have been even accused of spying on their customers.

https://www.ftc.gov/news-events/news/press-releases/2023/05/ftc-says-ring-employees-illegally-surveilled-customers-failed-stop-hackers-taking-control-users


Moreover, IoT devices are known to be vulnerable to cyber attacks due to the short support life cycle and the lack of security updates.

https://threatpost.com/yi-iot-home-camera-riddled-with-code-execution-vulnerabilities/138741/
https://threatpost.com/arlo-zaps-high-severity-bugs/146216/


====


An alternative solution that addresses these concerns is to use a local storage to store the recording instead of the private cloud services.

===

There is an abundance of free open source software that can be used to build a camera surveillance systems using a local storage, such as Kerberos, Motion, Shinobi, ZoneMinder, and many others. Even entire operating systems such as MotionEyeOS dedicated to this single purpose.


But they mostly rely on the web interface and lack of convenience of the mobile apps. Also, they are not as easy to set up and require some technical skills. For example, many installation guides suggest to use Docker or Docker Compose to run the software. And this is not a trivial task to connect cameras to the Docker container. So, it's definitely not a plug-and-play solution, like it used to be with the commercial services.


===

So, the comparison of the local and cloud solutions looks like this. The commercial cloud services are easy to install and use, usually have convenient mobile apps, but they are paid and raise security and privacy concerns. The local storage solutions are usually free and open source, usually don't have security and privacy issues but they are not as easy to install and use, don't have convenient mobile apps, rely mainly on the web interface.

===

To address these issues, I propose to build a free and open source software that will combine the best of both worlds. Just like the mentioned projects, this pice of software will be free and open source  suitable to run on a home server or a Raspberry Pi with connected cameras and storage.

===

Just like the mentioned projects, this pice of software will provide a set of most common features such as recording, and live video streaming, motion detection, and push notifications about events.

===

But unlike the mentioned projects, it will be easy to install and use. The goal is to make it easy to install for non-technical users. Most likely, it will be a single binary file or a pip package that can be run on any Unix system. It will not require Docker or any other sophisticated software to run.

Another big difference is that it will have a convenient mobile app that will allow users to view the live video and recordings. It's much more convenient than using a web interface, especially when you are away from home and only have a smartphone with you.