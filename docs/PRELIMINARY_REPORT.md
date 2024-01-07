# Final Project Preliminary Report


# Introduction

This report introduces a new software aimed to provide an on-premise camera surveillance solution for home users. The idea of this project is based on a provided “Camera Surveillance System” template. The motivation behind this project is to devise a surveillance system that will be as efficient and convenient as the commercial cloud services but provide the security and privacy of the local self-hosted solutions.

A number of commercial cloud services, such as Nest, Arlo, and others, offer convenient solutions for home surveillance systems. They provide a rich set of features such as motion detection to detect particular events of interest and distinguish it from the background noise or changes in lighting conditions. Recognize the nature of the moving object whether it is a person or a pet.  And push notifications to alert users about these events when they are away from home. These features are implemented using computer vision algorithms that are able to detect and recognize objects in the video stream. A user can configure the system to have different sensitivity levels, or to detect only particular objects, such as people, cars, or animals.

Despite their utility, these commercial surveillance solutions exhibit significant drawbacks. Firstly, the pricing model is usually based on the number of cameras and the number of days of video storage. The cost of these services can escalate quickly, especially with an increased number of cameras and extended video storage requirements. Secondly, and more crucially, the processing of a live stream and storage of recordings on private clouds, often in unknown jurisdiction, raises serious privacy concerns. A number of leaks and hacks of these cloud services have been reported in the past and some of the vendors have been even accused of spying on their customers. Moreover, IoT devices are known to be vulnerable to cyber attacks due to the short support life cycle and the lack of security updates.

In light of these challenges, an alternative solution that can be installed on a local server with connected cameras and storage is proposed. There is an abundance of free open source software that can be used to build camera surveillance systems using a local storage, such as Kerberos, Motion, Shinobi, ZoneMinder, and many others. Even entire operating systems MotionEyeOS is dedicated to this single purpose.

However, most of these solutions do not provide the same set of features as the commercial counterparts, such as motion detection, object recognition, and event-based notifications. Some of them require fine-tuning of the parameters, such as the sensitivity of the motion detection algorithm, which can be challenging for non-technical users and not very reliable. Most of them do not provide state-of-the-art AI-based object recognition, or require the additional installation of third-party AI models. It often results in a suboptimal user experience, with a lot of false positives or missed events and continuous tweaking of the parameters.

Most of the free solutions rely on web interfaces and lack the user-friendly aspect of mobile apps. Additionally, their setup often requires technical expertise, as evidenced by the common recommendation to use Docker or Docker Compose for installation, making them less accessible to the average user.

This project aims to bridge the gap between the user-friendly nature of commercial cloud services and the security and cost-effectiveness of local storage solutions. The proposed system will be a free, open-source software, suitable for operation on home servers or Raspberry Pi devices. It will offer standard features such as recording, live video streaming, motion detection, AI-based object identification and event-based notifications.

The distinguishing feature of this project is its ease of installation and use, especially for non-technical users. The system is envisaged to be deployable as a single binary file or a pip package, compatible with any Unix system, and will not necessitate the use of advanced software like Docker.

A significant innovation will be the development of a user-friendly mobile application, providing convenient access to live video feeds and recordings. This contrasts with the reliance on web interfaces in existing open-source solutions and is particularly advantageous for users needing remote access via smartphones. Thus, this project represents a significant step forward in home surveillance technology, addressing both the functional and security concerns prevalent in current systems.

# Literatures Review

During the preliminary research, it was found that there are three aspects of this project that require a review of the literature to gain a better understanding of the problem and to identify the most suitable solutions. Firstly, the project will involve the development and adaptation of computer vision algorithms to detect and recognize objects in the video stream. Motion detection is a challenging problem in computer vision, because it requires the system to distinguish between the events of interest and the background noise, changing lighting conditions, and other factors. There are a number of approaches that can be used to solve this problem. All these algorithms have their pros and cons, and the choice of the most suitable one requires a review of the literature.

Secondly, the project will require the development of an object recognition module to recognize objects in the video stream. This module will be used to distinguish between different types of moving objects, such as people, cars, animals, etc. There are a number of pre-trained deep learning models that can be used for this purpose. The choice of the most suitable model requires a review of the literature.

Finally, the project will require the development of a streaming server to provide live video feeds and recordings to the user. As for motion detection, many approaches have been proposed to solve this problem. There is a standard protocol for streaming video over the network, called RTSP (Real-Time Streaming Protocol). This protocol is supported by most of the modern IP cameras and is widely used in the industry. Another widely adopted protocol is ONVIF (Open Network Video Interface Forum) designed specifically for surveillance cameras. Besides them, there are a number of other protocols, such as RTMP (Real-Time Messaging Protocol), HLS (HTTP Live Streaming), and others. All these approaches have their pros and cons, and the choice of the most suitable one requires a review of the literature.

## Comparative Analysis of Moving Object Detection Algorithms [1]

This article presents a comprehensive study on motion detection algorithms most commonly used in video surveillance systems with stationary cameras. The primary goal of these algorithms is to distinguish moving pixels (foreground) from the environment (background), a crucial step for detecting events of interest. The challenge is to make these algorithms sensitive enough to notice moving objects while also being strong against background noise like changes in light, shadows, camera vibrations, and sensor noise.

The paper discusses traditional computer vision algorithms that rely on pixel-wise comparison and do not use deep learning: frame/temporal differencing (FD), simple adaptive background subtraction (BS), Mixture of Gaussian Model (MoG), and approximate median filter. These methods have been around for decades but are still widely used in video surveillance for being simple, efficient, and reliable. Some of the post-processing techniques are also discussed, such as thresholding and morphological operations. These techniques are used to improve the quality of the output and to reduce the number of false positives.

The authors provide a detailed description of each algorithm, including the mathematical foundations and block diagrams. They also created a basic GUI application to visually compare the output of these algorithms on various video clips. This comparison helps to assess how well each algorithm distinguishes moving objects and handles noise.

Figure 1: Comparison of different motion detection algorithms output [1]

Unfortunately, the authors do not provide any quantitative evaluation of the algorithms, which would be useful to compare their performance. Also, the code for the GUI application nor for the algorithms themselves is not provided, which makes it difficult to reproduce the results. Some popular background subtraction algorithms, such as KNN (K-nearest neighbors), CouNT, and ViBe, are not discussed in this paper, as well as optical flow based approaches. Anyways, this paper provides a good overview of the motion detection algorithm landscape, their mathematical foundations, and can be used as a starting point for further research.


## BSUV-Net 2.0: Spatio-Temporal Data Augmentations for Video-Agnostic Supervised Background Subtraction [9]

In recent years, deep learning-based methods have emerged as alternatives to traditional background subtraction methods in computer vision, particularly for motion detection. A prominent approach is Supervised Background Subtraction, where a deep learning model learns to separate background from foreground in video clips. The paper proposed BSUV-Net 2.0, a recent advancement in this field, as for 2023 considered a state-of-the-art model in this field.

BSUV-Net 2.0 builds on the original BSUV-Net architecture from 2019, which was based on the well-known U-Net architecture widely used in semantic segmentation. The new version uses spatio-temporal data augmentations to enhance its performance. The spatial augmentations help the model adapt to different camera angles and lighting conditions, while the temporal augmentations improve its handling of varying motion patterns, noise, and vibrations. These augmentations aim to improve the model's generalization capabilities and reduce overfitting.

The authors report that BSUV-Net 2.0 surpasses both its predecessor and other state-of-the-art models in performance on the CDNet 2014 dataset. The paper provides a thorough explanation of the model's design, training process, and source codes, alongside detailed evaluation results.

While the deep learning approach to motion detection is promising and worth considering, it may not be suitable for this project for a number of reasons. Firstly, it is more computationally intensive, which may not be suitable for inexpensive hardware like Raspberry Pi devices. Secondly, the pre-trained models are not freely available, so it would require training from scratch on a large dataset, which may not be feasible for this project. Thirdly, the model's performance is highly dependent on the training dataset, which may not be representative of the real-world scenarios. Finally, the model's performance is difficult to evaluate, as it requires a large dataset of video clips with and without motion, which is not publicly available.

## MotionPlus, a software motion detector [7]

MotionPlus is a new version of Motion, a GNU-licensed software package that for a long time was considered a de-facto standard to build camera surveillance systems on Linux. It was included in most of Linux distributions and was widely used in the industry. MotionPlus is a fork of the original Motion project, intended to modernize it, add new features, and improve its performance.

It is a command-line Unix daemon that can be configured via a configuration file and provides a web interface to view the live video stream and access the recordings. It supports any Linux-compatible camera and can be configured to use multiple cameras. The original Motion project uses a simple frame differencing approach to detect motion in the video stream. MotionPlus provides a secondary method motion detection method, in addition to the original frame differencing method. The secondary method could be Haar cascades, HOG (Histogram of Oriented Gradients), and Deep Neural Networks. This shift to modern computer vision algorithms makes MotionPlus more accurate and reliable in detecting motion than the original Motion.

The MotionPlus project provides an important insight into the features that are expected from a modern camera surveillance system. It also provides a time-proved implementation of motion detection algorithms that can be used as a reference for this project. However, the original Motion approach to motion detection is quite simplistic and relies on the user to fine-tune the parameters to achieve the desired results. For example, the configuration file has a parameter called "threshold" that is a minimum number of changed pixels to consider it as motion. This parameter is difficult to guess and it is quite camera and scene dependent.

As a conclusion of a review of the literature on motion detection approaches, it can be said that while we have a number of approaches existing for decades, there is no single approach that is considered to be the perfect solution. Each approach has its significant limitations and requires fine-tuning of the parameters to achieve the desired results in a particular scenario. This is a challenging ongoing research problem in computer vision and is yet another manifestation of Moravec's paradox, which states that a seemingly trivial task for humans, such as recognizing a moving object, is a challenging problem for computers.

## DETRs Beat YOLOs on Real-time Object Detection [2]
In surveillance systems, recognizing objects that cause motion is crucial. In indoor settings, false alarms often occur due to pets, insects, or other moving objects, but the key interest is in identifying people as potential intruders. Real-time object detection models can help in accurately labeling moving objects.

Deep learning models are currently leading in object recognition, surpassing traditional computer vision approaches in accuracy and even inference speed. In the recent decade, a lot of deep learning models have been proposed for object detection and recognition. These models compete in accuracy and speed on public image datasets, like COCO [3] and ImageNet [4]. Until recently, YOLO [5] was regarded as the state-of-the-art model for real-time object detection due to its speed and accuracy.

However, in recent years, new models were proposed. One notable is DETR (DEtection TRansformer) [6] based on the Transformer architecture, initially used in Natural Language Processing (NLP) but gained popularity in computer vision as well. This particular paper proposes an optimized version of DETR, called RT-DETR (Real-Time DETR), which reportedly outperform recent YOLO versions in both speed and accuracy. According to the provided in the paper comparison, RT-DETR-L, the smallest version of RT-DETR with 32 million parameters, performs 1.6 times faster than YOLOv8-L with 43 million parameters, while maintaining similar or slightly greater accuracy on the COCO dataset.

Figure 1: Performance comparison between RT-DETR and YOLO [2]

The paper details the model's architecture, training process, provides source codes, and evaluation results on the COCO dataset. It all suggests that RT-DETR can be used for object recognition in surveillance systems, instead of the popular YOLO model. However, it's noted that this model faces challenges, especially in training and optimizing for small objects. These issues are expected to be resolved in future developments. Given our project's constraints for deployment on local servers or Raspberry Pi devices, a model's computational complexity is crucial. Thus, different existing models should be evaluated for their performance on small devices and the final choice will be made based on the evaluation results.

## Video Streaming Protocols: 6 Preferred Formats for Professional Broadcasting [10]

The article provides a comprehensive overview of the most common and widely adopted video streaming protocols, including RTSP, RTMP, HLS, WebRTC, and others. It explains the differences and relationships between streaming protocols, video codecs (vodecs), and container formats. It gives a detailed description of each protocol, including the history, the technical details, and the use cases. It also discusses the pros and cons of each protocol and provides recommendations on which one to use in different scenarios.

Based on this overview, WebRTC seems to be the most promising protocol for this project. It is a modern protocol that is supported by most of the modern browsers and mobile devices. It also offers near real-time streaming with low latency, which is crucial for surveillance systems. However, the focus of the article is primarily on professional broadcasting, not surveillance systems. Most arguments are based on broadcasting needs.

Also, the article does not provide information on software or hardware compatibility for each protocol. For instance, it's unclear which protocols are supported by Apple devices. Additionally, the article overlooks the security features of these protocols, a critical factor for surveillance systems. While the article is useful as a high-level overview of the video streaming protocols landscape, it does not offer enough detail for deciding on a protocol for this project. A more thorough study of each protocol's specifications is necessary.

## ZoneMinder, an open source CCTV software [6]

Another open-source surveillance software that is worth mentioning is ZoneMinder. It is one of the most feature-rich solutions available on the market, used primarily in professional settings, but can also run on a home server. It provides a web interface, as well as Android and iOS apps. It can utilize virtually any number of cameras of any type, including infrared cameras. There is an impressive list of features, including advanced AI powered detection, cloud and local storage, and many others. It is a mature project with a large community and a number of commercial partners.

As for MotionPlus, ZoneMinder and other open-source solutions have tendencies to accumulate complexity over time. As a general-purpose, fit-for-all solution, it comes with a lot of features that are not relevant to the home users, targeting primarily enterprise customers. Also, some of the features are available only in the paid version. The installation and configuration process is quite complex and requires advanced technical skills. It is not very suitable for non-technical users.



# Design

##  Domain and Users

The domain of this project is “Camera Surveillance System,” specifically, a software component that enables home users to install and configure an on-premise camera surveillance system. The project will not involve the development of hardware components, such as cameras or sensors, as the software will be compatible with any cameras connected to the system and available through the standard API. The solution should be a viable alternative to commercial cloud services, offering the same or nearly the same set of features as the commercial counterparts.

The target users of this project are home users who want to avoid using cloud services for their surveillance systems whether due to cost or privacy concerns. The users of this project are expected to have basic technical skills and be able to install and configure the system on their own. The users are not expected to have advanced technical skills, such as Docker or Kubernetes, to deal with complex deployment scenarios.

## Features

There is an abundance of free open source software that can be used to build camera surveillance systems using a local storage, such as Kerberos, Motion, Shinobi, ZoneMinder, and many others. Many of these solutions are quite mature and offer a wide range of features that are not feasible to implement in this project. Many of them are even more advanced than the commercial solutions as the latter often focus on the specific features that are most demanded by the users, while the open-source solutions tend to be a general-purpose and sometimes end up being overwhelmingly complex.

Instead of trying to compete with the existing feature-rich solutions, this project will focus on the most common features that are expected from a modern camera surveillance system and will try to implement them in the most user-friendly way inspired by the commercial solutions. After reviewing the existing solutions, the following features are considered to be the most important and will be implemented in this project:

Ability to connect multiple cameras to the system
Provide live video streaming to the user
Detect motion in the video stream and distinguish it from the background noise
Log the events when motion is detected and store the video clips
Send notifications to the user when motion is detected
Provide access to the recordings to the user

Some of the existing solutions also provide AI-based object recognition, such as people, cars, animals, etc. and allow the user to configure the system to detect only particular objects. This feature reduces the number of false positives when pets or insects are detected as moving objects. Only a few of the existing free open source solutions provide such a feature while most of the commercial cloud services do. This feature is expected to be implemented in this project and is considered as a distinguishing feature.

Another distinguishing feature of this project is the development of a mobile application to provide a user-friendly interface for the system. Most of the existing open-source solutions rely on web interfaces and do not provide mobile applications.

It is worth noting that the cloud-based surveillance systems offer a number of features that are not feasible to implement in an on-premise environment. The most notable is that cloud storage can not be stolen or destroyed by an intruder along with the recordings. Another notable feature is the ability to seamlessly access the live video feeds and recordings from anywhere in the world. These features are not feasible to implement in an on-premise environment, so despite the efforts to make the system as user-friendly as possible, there is still a trade-off between the security and privacy of the self-hosted solution and the convenience of the cloud-based solution.


## Structure of the project

Figure 2: High-level architectural overview of the project

The overall architecture of the project is shown in Figure 2. For the ease of deployment, the backend component of the system is designed as a single monolithic application, which encapsulates all the modules of the system. Since our target users are not expected to have advanced technical skills to deal with complex deployment scenarios, such as Docker or Kubernetes, this approach is considered to be the most suitable for this project. The system consists of the following modules:

### Agent

The agent is a central component of the system that runs on a local server with connected cameras. It provides a REST API for the mobile application to access the live video feeds and recordings. It also provides a web console, which can be accessed from a web browser. The agent comprises three modules: a HTTP server, a streaming module, and a motion detection module. From a user's perspective, the agent is the one software package that needs to be installed on a local server, configured, and run. When the agent is started, it starts all the internal modules and provides access to the system through the integrated HTTP server. Thus, the internal complexity of the system is hidden from the user, but from the developer's perspective, the system is modular and each module can be developed and tested independently.

### Streaming module

The streaming module is a module of the agent responsible for providing live video feeds to the user via the integrated HTTP server. This module runs as a separate process that directly interacts with the cameras using FFmpeg library. It takes the video stream from the camera and converts it to the HLS format, which is then served to the user via the HTTP server. The HLS format is chosen because it is supported by most of the modern web browsers and mobile devices. It also provides adaptive bitrate streaming, which is crucial for providing a smooth video playback on mobile devices with limited bandwidth.

### Motion detection module

The motion detection module is responsible for detecting motion in the video stream. This module also runs as a separate process that directly interacts with the cameras using OpenCV library. In contrast to the streaming module that serves the video as a continuous stream, the motion detection module processes the video stream as a sequence of discrete frames. When the motion is detected, the module sends a notification to the Push Notification Service, which then sends a push notification to the user's mobile device. The module also stores the video clip with the detected motion in the storage and metadata about the event in the SQLite database, so the user can access it later via the HTTP server.

The motion detection module will also be responsible for object recognition. It will use a pre-trained deep learning model to recognize objects in the video stream. The records will be tagged accordingly, so the user can filter the events by the type of the object. Also, the user will be able to configure the system to send notifications only for particular objects, such as people.

### Database

The SQLite database was chosen as a storage solution for the metadata because it is lightweight and does not require a separate database server to be installed. It is also widely supported making it easy to integrate with other components of the system. The video clips are stored in the file system, which is also a lightweight solution and does not require any configuration except for the path to the storage directory.

### HTTP Server

The HTTP server module is responsible for providing access to the system via the HTTP web console and serves REST API for the mobile application. It also serves the video streams from the streaming module and the video recordings from the storage. The web console will provide a user-friendly interface for the system, where the user can view the live video feeds, and access the recordings.
Mobile application

The mobile application will provide the same functionality as the web console, but in a more mobile-friendly way. It will provide convenient access to live video feeds and recordings. It will also provide push notifications when motion is detected.

# Work Plan

Agile methodology will be used for the development of this project. The work will be divided into a number of sprints, each lasting two weeks. By the end of each sprint, a deliverable piece of software will be produced. This approach will allow for a more flexible development process and will make it easier to adapt to the changing requirements, less subject to the risks of unforeseen circumstances. For example, if a particular feature turns out to be more complex than expected, it can be omitted or simplified without affecting the rest of the project. Even by the end of the first sprint, a working version of the system will be ready to use, albeit with limited functionality.

The work will be divided into the following sprints:
Sprint #
Tasks (Backlog)
1
Setup the development environment, create a prototype of a basic HTTP server that streams a video from a camera:
Setup the development environment
Create a basic HTTP server using the FastAPI framework
Implement a basic streaming module using the FFmpeg library
Create a HTML page that displays a video stream from the connected camera


2
Implement a prototype of the motion detection module:
Connect to a camera using the OpenCV library.
Implement a basic motion detection algorithm that detects motion in the video stream
Save video recording with the detected motion to the disk
3
Implement a first version of the web console:
Implement a basic web console using the FastAPI framework that provides access to the live video feeds.
Implement a basic web console that provides access to the video recordings.
4
Implement a first version of the mobile application:
Implement a basic mobile application that provides access to the live video feeds.
Implement provides access to the video recordings.
5
Implement the object recognition module:
Implement a basic object recognition module using a pre-trained deep learning model that recognizes objects in the video stream and labels the video recordings accordingly.
Implement a push notification service that sends push notifications to the user's mobile device when motion is detected with the type of the object.
6
Implement a support for multiple cameras
Implement support for multiple cameras for the streaming module.
Implement support for multiple cameras for the motion detection module.
Implement support for multiple cameras for the web console.
Implement support for multiple cameras for the mobile application.
7
Polish the web console and the mobile application
Implement a user-friendly interface for the web console
Implement a user-friendly interface for the mobile application
8
Documentation and testing
Write documentation
Perform evaluation and testing


 
# Evaluation Plan

The evaluation of this project will be performed for each of the sprints. The first two sprints will be focused on the evaluation of feasibility of the project itself. The evaluation will be performed by implementing a prototype of the system that provides a core functionality: streaming a video from a camera and detecting motion in the video stream. The evaluation will be performed by a developer, testing the prototype on a single camera and assessing the performance of the system.

The next two sprints will be focused on the implementation of the web console and the mobile application. The evaluation will be performed by questioning the potential users about their experience with the system. The questions will include the following:
How easy was it to install and configure the system? A scale from 1 to 5 and comments.
How easy was it to use the web console? 1-5 and comments
How easy was it to use the mobile application? 1-5 and comments
The feedback will be used to improve the user interface and the user experience.

The methodology of TDD (Test Driven Development) in its relaxed form will be used for the development of this project. In its pure form, TDD requires writing tests before writing the code and then writing the code to pass the tests. The downside of this approach is that it requires a lot of context switching between writing tests and writing code, and overhead of writing tests for every single unit of code, which can be counterproductive.The relaxed form of TDD, on the other hand, emphasizes the importance of writing tests when it speeds up the development process. For example, it will be beneficial to write tests for the motion detection module to have a set of sample video clips with and without motion to efficiently test the module and not have to manually record the video clips every time.

The final evaluation will involve implementing an evaluation scenario with described steps and expected outcomes. The evaluation scenario will be performed by the developer and the potential users. The evaluation will be performed by testing the system on multiple cameras and assessing the overall performance and quality of the system.

# Feature Prototype

Two features of the system that are considered to be the most challenging and crucial for the project are the streaming module and the motion detection module. To reduce the risk of failure, these features should be implemented first at least in their minimal form. The aim of this prototype is to assess the feasibility of the project and to identify the most suitable approaches for implementing these features.

The first prototype was implemented as an agent that provides a basic web console with a live video feed from a single camera and a basic motion detection functionality. The agent is implemented as a Flask application that runs on a local server with a connected camera. The agent uses the OpenCV library to connect to the camera and fetch the video stream as discrete frames. These frames are then processed by the motion detection module, which uses a simple background subtraction algorithm to detect motion in the video stream. When the motion is detected, the agent displays a bounding box around the moving object and saves the video clip of the event on the disk.

During the development of this prototype, it was found that the basic variant of live video streaming using the Flask application is to provide an endpoint that returns a continuous stream of frames as JPEG images. The client displays these images as a video. This approach is far simpler than using the streaming protocols, such as HLS, but has limitations in terms of network overhead and latency. But for the purpose of this prototype, it was found to be sufficient.

The prototype served as a playground for experimenting with different approaches to motion detection. One thing was found that not only the changes in lighting conditions and the background noise can cause false positives, but also the camera auto-focus feature. It is important to know such challenges in advance to have time to find a solution.

# References

[1] Hussien, H.M., Meko, S.F., Teshale, N.B. 2018. Comparative Analysis of Moving Object Detection Algorithms. Lecture Notes of the Institute for Computer Sciences, Social Informatics and Telecommunications Engineering, vol 244. Springer, Cham. Retrieved Jan 7, 2024 from https://doi.org/10.1007/978-3-319-95153-9_16.
[2] M. Ozan Tezcan, Prakash Ishwar, Janusz Konrad. 2021. BSUV-Net 2.0: Spatio-Temporal Data Augmentations for Video-Agnostic Supervised Background Subtraction. arXiv:2101.09585. Retrieved Jan 7, 2024 from https://arxiv.org/abs/2101.09585.
[3] MotionPlus developers. 2023. MotionPlus, a software motion detector. Retrieved Jan 7, 2024 from https://motion-project.github.io/.
[4] Wenyu Lv, Yian Zhao, Shangliang Xu, Jinman Wei, Guanzhong Wang, Cheng Cui, Yuning Du, Qingqing Dang, Yi Liu. 2023. DETRs Beat YOLOs on Real-time Object Detection. arXiv:2304.08069. Retrieved Jan 7, 2024 from https://arxiv.org/abs/2304.08069.
[5] Max Wilbert. 2023. Video Streaming Protocols: 6 Preferred Formats for Professional Broadcasting. Retrieved Jan 7, 2024 from https://www.dacast.com/blog/video-streaming-protocol/.
[6] ZoneMinder developers. 2023. ZoneMinder, an open source CCTV software. Retrieved Jan 7, 2024 from https://zoneminder.com/.
