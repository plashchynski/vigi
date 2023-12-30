# Final Project
## Preliminary Report


## Introduction

This project preliminary report introduces a new software aimed to provide a self-hosted camera surveillance solution for home users. The idea of this project is based on a provided “Camera Surveillance System” template. The motivation behind this project is to devise a surveillance system that will be as efficient and convenient as the commercial cloud services but provide the security and privacy of the local self-hosted solutions.

Currently, my smart home setup consists of a few security cameras, including XIAOMI MI home security camera for indoor monitoring and an Arlo Video Doorbell for outdoor surveillance. These cameras are integrated with proprietary subscription-based cloud services, offering the convenience of remote access to live view and recordings through mobile applications from anywhere in the world.

They also provide a set of most common features such as motion detection to detect particular events of interest and distinguish it from the background noise. Recognize the nature of the moving object whether it is a person or a pet.  And push notifications to alert users about these events when they are away from home. These features are implemented using computer vision algorithms that are able to detect and recognize objects in the video stream. A user can configure the system to have different sensitivity levels, or to detect only particular objects, such as people, cars, or animals.

Despite their utility, these commercial surveillance solutions exhibit significant drawbacks. Firstly, the pricing model is usually based on the number of cameras and the number of days of video storage. The cost of these services can escalate quickly, especially with an increased number of cameras and extended video storage requirements. Secondly, and more crucially, the processing of a live stream and storage of recordings on private clouds, often in unknown jurisdiction, raises serious privacy concerns. A number of leaks and hacks of these cloud services have been reported in the past and some of the vendors have been even accused of spying on their customers. Moreover, IoT devices are known to be vulnerable to cyber attacks due to the short support life cycle and the lack of security updates.

In light of these challenges, an alternative solution that can be installed on a local server with connected cameras and storage is proposed. There is an abundance of free open source software that can be used to build camera surveillance systems using a local storage, such as Kerberos, Motion, Shinobi, ZoneMinder, and many others. Even entire operating systems MotionEyeOS is dedicated to this single purpose. However, these systems usually rely on web interfaces and lack the user-friendly aspect of mobile apps. Additionally, their setup often requires technical expertise, as evidenced by the common recommendation to use Docker or Docker Compose for installation, making them less accessible to the average user.

This project aims to bridge the gap between the user-friendly nature of commercial cloud services and the security and cost-effectiveness of local storage solutions. The proposed system will be a free, open-source software, suitable for operation on home servers or Raspberry Pi devices. It will offer standard features such as recording, live video streaming, motion detection, AI-based object identification and event-based notifications.

The distinguishing feature of this project is its ease of installation and use, especially for non-technical users. The system is envisaged to be deployable as a single binary file or a pip package, compatible with any Unix system, and will not necessitate the use of advanced software like Docker.

A significant innovation will be the development of a user-friendly mobile application, providing convenient access to live video feeds and recordings. This contrasts with the reliance on web interfaces in existing open-source solutions and is particularly advantageous for users needing remote access via smartphones. Thus, this project represents a significant step forward in home surveillance technology, addressing both the functional and security concerns prevalent in current systems.


## Literature Review

During the preliminary research, it was found that there are three aspects of this project that require a review of the literature to gain a better understanding of the problem and to identify the most suitable solutions. Firstly, the project will involve the development and adaptation of computer vision algorithms to detect and recognize objects in the video stream. Motion detection is a challenging problem in computer vision, because it requires the system to distinguish between the events of interest and the background noise, changing lighting conditions, and other factors. The most common approach to this problem is to use background subtraction algorithms, which are able to detect the moving objects by comparing the current frame with the background model. However, these algorithms are not robust to the changes in lighting conditions and are not able to distinguish between the objects of interest and the background noise.

A more advanced approach is to use deep learning algorithms to detect and recognize objects in the video stream. These algorithms are able to learn from the data and are able to distinguish between the objects of interest and the background noise. However, these algorithms are computationally expensive and require a lot of training data. Selecting a suitable approach for this project requires reviewing the literature and existing solutions.

Secondly, the project will require the development of a streaming server to provide live video feeds and recordings to the user. As for motion detection, many approaches have been proposed to solve this problem. There is a standard protocol for streaming video over the network, called RTSP (Real-Time Streaming Protocol). This protocol is supported by most of the modern IP cameras and is widely used in the industry. Another widely adopted protocol is ONVIF (Open Network Video Interface Forum) designed specifically for surveillance cameras. Besides them, there are a number of other protocols, such as RTMP (Real-Time Messaging Protocol), HLS (HTTP Live Streaming), and others. All these approaches have their pros and cons, and the choice of the most suitable one requires a review of the literature.

Finally, the project will require the development of a mobile application to provide a user-friendly interface for the system. There are a number of existing solutions that can be used as a reference for this project. In this section, related works in each of these areas will be reviewed. The review will focus on the most recent and relevant works, with a particular emphasis on open-source solutions. Both scientific papers and existing software solutions will be considered.

### Comparative Analysis of Moving Object Detection Algorithms

This article presents a comprehensive study on motion detection algorithms most commonly used in video surveillance systems with stationary cameras. The primary goal of these algorithms is to distinguish moving pixels (foreground) from the environment (background), a crucial step for detecting events of interest. The challenge is to make these algorithms sensitive enough to notice moving objects while also being strong against background noise like changes in light, shadows, camera vibrations, and sensor noise.

The paper discusses traditional computer vision algorithms that rely on pixel-wise comparison and do not use deep learning: frame/temporal differencing (FD), simple adaptive background subtraction (BS), Mixture of Gaussian Model (MoG), and approximate median filter. These methods have been around for decades but are still widely used in video surveillance for being simple, efficient, and reliable. Some of the post-processing techniques are also discussed, such as thresholding and morphological operations. These techniques are used to improve the quality of the output and to reduce the number of false positives.

The authors provide a detailed description of each algorithm, including the mathematical foundations and block diagrams. They also created a basic GUI application to visually compare the output of these algorithms on various video clips. This comparison helps to assess how well each algorithm distinguishes moving objects and handles noise.

Unfortunately, the authors do not provide any quantitative evaluation of the algorithms, which would be useful to compare their performance. Also, the code for the GUI application nor for the algorithms themselves is not provided, which makes it difficult to reproduce the results. Some popular background subtraction algorithms, such as KNN (K-nearest neighbours), CouNT, and ViBe, are not discussed in this paper, as well as optical flow based approaches. Anyways, this paper provides a good overview of the motion detection algorithm landscape, their mathematical foundations, and can be used as a starting point for further research.


### BSUV-Net 2.0: Spatio-Temporal Data Augmentations for Video-Agnostic Supervised Background Subtraction

As an alternative to traditional background subtraction computer vision algorithms for motion detection discussed in the previous paper, a number of Deep learning-based approaches have been proposed in recent years. The approach called Supervised Background Subtraction, is based on the idea of using a deep learning model to learn the background model from the data. The model is trained on a dataset of video clips with the background and foreground masks. The model is then able to distinguish between the objects of interest and the background noise. The motion detection is performed by detecting the foreground objects in the video stream.

The paper describes a recent advancement in this field, called BSUV-Net 2.0, which is currently considered a state-of-the-art model for background subtraction. It is based on the BSUV-Net architecture proposed by the same authors in 2019. The first version of the model was based on a famous U-Net architecture, which is widely used in semantic segmentation tasks. The new version introduces spatio-temporal data augmentations to improve the performance of the first version. Spatial augmentations are used to improve the model's ability to generalize to different camera angles and lighting conditions. Temporal augmentations are used to improve the model's ability to generalize to different motion patterns, noise, and vibrations. Both types of augmentations are aimed to improve the model's generalization ability and to reduce overfitting.

Authors claim that the new version of the model outperforms the previous version and other state-of-the-art models on the CDNet 2014 dataset. The paper provides a detailed description of the model architecture and the training process, source codes for the model implementation, as well as the detailed results of the evaluation on the CDNet 2014 dataset. The model can be used as a motion detection module in the proposed surveillance system. However, the model is relatively computationally expensive in comparison to the traditional computer vision algorithms mentioned earlier. Also, the pre-trained model is not available, so it would require training from scratch on a large dataset, which may not be feasible for this project. However, this is a promising approach that can be considered in the future.
 
It is also worth mentioning that new models based on Transformer architecture called Vision Transformer are emergent and currently outperform the traditional CNN-based models in many computer vision tasks, including background subtraction. However, these models are not yet widely adopted and may not be mature enough for this project.


### DETRs Beat YOLOs on Real-time Object Detection

In surveillance systems, recognizing objects that cause motion is crucial. In indoor settings, false alarms often occur due to pets, insects, or other moving objects, but the key interest is in identifying people as potential intruders. Real-time object detection models can help in accurately labeling moving objects.

As today in the landscape of object recognition a deep learning approach is the most effective, beating the traditional computer vision algorithms in terms of accuracy. A number of deep learning models have been proposed in the recent years. These models were competing in accuracy and speed on public image recognition datasets, such as COCO and ImageNet. In this competition a YOLO model (Redmon J., et al. 2015) has been shown to be the most accurate and the fastest, considered as a state-of-the-art and first choice model for real-time object detection.

However, a number of new model were proposed after that. The most promising one called DETR (DEtection TRansformer) has been proposed by Carion N. et al. [2020], which was based on the Transformer architecture, originally developed for Natural Language Processing (NLP) tasks, but seek popularity in the computer vision field as well. In the considered paper, the authors proposed an optimized version of DETR model, called RT-DETR (Real-Time DETR), which reportedly outperformed recent versions of YOLO in terms of both accuracy and speed. According to the paper, RT-DETR-L, the smallest version of RT-DETR with 32 million parameters, is 1.6 times faster than YOLOv8-L with 43 million parameters, while achieving the same accuracy on the COCO dataset.

The paper provides a detailed description of the model architecture and the training process, source codes for the model implementation, as well as the detailed results of the evaluation on the COCO dataset. The model can be used as a object recognition module in the proposed surveillance system. But despite being promising, this model may not be mature enough. Authors specifically mentioned that "This new design for detectors also comes with new challenges, in particular regarding training, optimization and performances on small objects. Current detectors required several years of improvements to cope with similar issues, and we expect future work to successfully address them for DETR." Another important consideration is since our project is aimed to be deployed on a local server or a Raspberry Pi device, the computational complexity of the model is a more important factor than the accuracy. Probably, a more lightweight model specifically designed for embedded devices would be a better choice.

Deep learning models are currently leading in object recognition, surpassing traditional computer vision approaches in accuracy and even inference speed. However, they are computationally expensive and require a lot of training data. Selecting a suitable approach for this project requires reviewing the literature and existing solutions. In the recent years, a number of deep learning models have been proposed for object recognition. The most promising one called DETR (DEtection TRansformer) has been proposed by Carion N. et al. [2020], which was based on the Transformer architecture, originally developed for Natural Language Processing (NLP) tasks, but seek popularity in the computer vision field as well. In the considered paper, the authors proposed an optimized version of DETR model, called RT-DETR (Real-Time DETR), which reportedly outperformed recent versions of YOLO in terms of both accuracy and speed. According to the paper, RT-DETR-L, the smallest version of RT-DETR with 32 million parameters, is 1.6 times faster than YOLOv8-L with 43 million parameters, while achieving the same accuracy on the COCO dataset.

### Video Streaming Protocols: 6 Preferred Formats for Professional Broadcasting

In surveillance systems, recognizing objects that cause motion is crucial. In indoor settings, false alarms often occur due to pets, insects, or other moving objects, but the key interest is in identifying people as potential intruders. Real-time object detection models can help in accurately labeling moving objects.

Deep learning models are currently leading in object recognition, surpassing traditional computer vision approaches in accuracy and even inference speed. In the recent decade, a lot of deep learning models have been proposed for object detection and recognition. These models compete in accuracy and speed on public image datasets, like COCO [3] and ImageNet [4]. Until recently, YOLO [5] was regarded as the state-of-the-art model for real-time object detection due to its speed and accuracy.

However, in recent years, new models were proposed. One notable is DETR (DEtection TRansformer) [6] based on the Transformer architecture, initially used in Natural Language Processing (NLP) but gained popularity in computer vision as well. This particular paper proposes an optimized version of DETR, called RT-DETR (Real-Time DETR), which reportedly outperform recent YOLO versions in both speed and accuracy. According to the provided in the paper comparison, RT-DETR-L, the smallest version of RT-DETR with 32 million parameters, performs 1.6 times faster than YOLOv8-L with 43 million parameters, while maintaining similar or slightly greater accuracy on the COCO dataset.

Figure 1: Performance comparison between RT-DETR and YOLO [2]

The paper details the model's architecture, training process, provides source codes, and evaluation results on the COCO dataset. It all suggests that RT-DETR can be used for object recognition in surveillance systems, instead of the popular YOLO model. However, it's noted that this model faces challenges, especially in training and optimizing for small objects. These issues are expected to be resolved in future developments. Given our project's constraints for deployment on local servers or Raspberry Pi devices, a model's computational complexity is crucial. Therefore, a lightweight model specifically designed for mobile and embedded devices might be a more suitable choice.


## Design

### Project Overview

The project is aimed to provide a self-hosted camera surveillance solution for home users. The idea of this project is based on a provided “Camera Surveillance System” template. The motivation behind this project is to devise a surveillance system that will be as efficient and convenient as the commercial cloud services but provide the cost-efficiency, security and privacy of the local self-hosted solutions.

The inspiration for this project comes from my existing home setup, that includes XIAOMI MI home security camera for indoor monitoring and an Arlo Video Doorbell for outdoor surveillance. These cameras are integrated with proprietary subscription-based cloud services. While these devices offer remote access, motion detection, AI-based object recognition, and event-based notifications through proprietary cloud services, they also come with significant limitations in terms of cost and privacy.

The existing free open source software solutions for camera surveillance systems, such as Kerberos, Motion, Shinobi, ZoneMinder, and others, are not user-friendly and often require technical expertise to install and use. This project aims to bridge the gap between the user-friendly nature of commercial cloud services and the security and cost-effectiveness of local storage solutions. The proposed system will be a free, open-source software, suitable for operation on home servers or Raspberry Pi devices. It will offer standard features such as recording, live video streaming, motion detection, AI-based object identification and event-based notifications.

The main distinguishing feature of this project is accompanying mobile application, providing convenient access to live video feeds and recordings. This contrasts with the reliance on web interfaces in existing open-source solutions.

### Domain and Users

The domain of this project is "Home Surveillance Systems," specifically focusing on self-hosted, user-friendly camera surveillance solutions for home users. The target users of this project are home users who are privacy-conscious and want to avoid using cloud services for their surveillance systems. The users of this project are expected to have basic technical skills and be able to install and configure the system on their own. The users are expected to have a home server or a Raspberry Pi device to run the system. The users are expected to have a smartphone to use the mobile application.

### Features

From the preliminary research of the existing solutions, it was found that the following features are common in existing surveillance systems and are expected to be implemented in this project:

* Ability to connect multiple cameras to the system
* Provide live video streaming to the user
* Detect motion in the video stream
* Record and store video clips when motion is detected
* Send notifications to the user when motion is detected
* Provide access to the recordings to the user

Some of the existing solutions also provide AI-based object recognition, such as people, cars, animals, etc. and allow the user to configure the system to detect only particular objects. This feature reduces the number of false positives when pets or insects are detected as moving objects. Only a few of the existing free open source solutions provide such a feature while most of the commercial cloud services do. This feature is expected to be implemented in this project and is considered as a distinguishing feature.

Another distinguishing feature of this project is the development of a mobile application to provide a user-friendly interface for the system. Most of the existing open-source solutions rely on web interfaces and do not provide mobile applications. This is a significant drawback, especially for users needing remote access via smartphones. The mobile application is expected to provide convenient access to live video feeds and recordings.

### Structure of the project

The overall architecture of the project is shown in Figure 2. For the ease of deployment, the project is designed as a single monolithic application, which encapsulates all the components of the system. Since our target users are not expected to have advanced technical skills to deal with complex deployment scenarios, such as Docker or Docker Compose, this approach is considered to be the most suitable for this project.

The central package of the system is an agent, which comprises three modules: a HTTP server, a streaming module, and a motion detection module. From a user's perspective, the agent is the only component of the system that needs to be installed and configured. When the agent is started, it starts all the internal modules and provides access to the system through the HTTP interface. So the internal complexity of the system is hidden from the user, but from the developer's perspective, the system is modular and each module can be developed and tested independently.

We streamings module is responsible for providing live video feeds to the user via the HTTP server module. This module runs as a separate process that directly interacts with the cameras using FFmpeg library. It takes the video stream from the camera and converts it to the HLS format, which is then served to the user via the HTTP server. The HLS format is chosen because it is supported by most of the modern web browsers and mobile devices. It also provides adaptive bitrate streaming, which is crucial for providing a smooth video playback on mobile devices with limited bandwidth.

The motion detection module is responsible for detecting motion in the video stream. This module also runs as a separate process that directly interacts with the cameras using OpenCV library. In contrast to the streaming module that serves the video as a continuous stream, the motion detection module processes the video stream as a sequence of discrete frames. When the motion is detected, the module sends a notification to the Push Notification Service, which then sends a push notification to the user's mobile device. The module also stores the video clip with the detected motion in the storage and metadata about the event in the SQLite database, so the user can access it later via the HTTP server.

The SQLite database was chosen as a storage solution for the metadata because it is lightweight and does not require a separate database server to be installed. It is also widely supported making it easy to integrate with other components of the system. The video clips are stored in the file system, which is also a lightweight solution and does not require any configuration except for the path to the storage directory.

The motion detection module will also be responsible for object recognition. It will use a pre-trained deep learning model to recognize objects in the video stream. The records will be tagged accordingly, so the user can filter the events by the type of the object. Also, the user will be able to configure the system to send notifications only for particular objects, such as people.

The HTTP server module is responsible for providing access to the system via the HTTP web console and serves REST API for the mobile application. It also serves the video streams from the streaming module and the video recordings from the storage. The web console will provide a user-friendly interface for the system, where the user can view the live video feeds, and access the recordings.

The mobile application will provide the same functionality as the web console, but in a more mobile-friendly way. It will provide convenient access to live video feeds and recordings. It will also provide push notifications when motion is detected.

## Work Plan

Agile methodology will be used for the development of this project. The work will be divided into a number of sprints, each lasting two weeks. By the end of each sprint, a deliverable piece of software will be produced. This approach will allow for a more flexible development process and will make it easier to adapt to the changing requirements, less subject to the risks of unforeseen circumstances. For example, if a particular feature turns out to be more complex than expected, it can be omitted or simplified without affecting the rest of the project. Even by the end of the first sprint, a working version of the system will be ready to use, albeit with limited functionality.

The work will be divided into the following sprints:

1. Setup the development environment, create a prototype of basic HTTP server that streams a video from a camera
* Setup the development environment
* Create a basic HTTP server using the FastAPI framework
* Implement a basic streaming module using the FFmpeg library

2. Implement a prototype of the motion detection module
* Connect to a camera using the OpenCV library
* Implement a basic motion detection algorithm that detects motion in the video stream
* Save the video clips with the detected motion in the storage

3. Implement a version of the web console
* Implement a basic web console using the FastAPI framework that provides access to the live video feeds
* Implement a basic web console that provides access to the video recordings

4. Implement a version of the mobile application
* Implement a basic mobile application that provides access to the live video feeds
* Implement provides access to the video recordings

5. Implement the object recognition module
* Implement a basic object recognition module using a pre-trained deep learning model that recognizes objects in the video stream and labels the video recordings accordingly
* Implement a push notification service that sends push notifications to the user's mobile device when motion is detected with the type of the object

6. Implement a support for multiple cameras
* Implement a support for multiple cameras for the streaming module
* Implement a support for multiple cameras for the motion detection module
* Implement a support for multiple cameras for the web console
* Implement a support for multiple cameras for the mobile application

7. Polish the web console and the mobile application
* Implement a user-friendly interface for the web console
* Implement a user-friendly interface for the mobile application

8. Documentation and testing
* Write documentation
* Perform evaluation and testing

## Evaluation Plan

The evaluation of this project will be performed for each of the sprints. The first two sprints will be focused on the evaluation of feasibility of the project itself. The evaluation will be performed by implementing a prototype of the system that provides a core functionality: streaming a video from a camera and detecting motion in the video stream. The evaluation will be performed by testing the prototype on a single camera and assessing the performance of the system. The performance will be measured in terms of the frame rate, latency, CPU usage, and subjective user experience.

The next two sprints will be focused on the implementation of the web console and the mobile application. The evaluation will be performed by questioning the potential users about their experience with the system and their feedback on the user interface. The questions will include the following:
* How easy was it to install and configure the system? A scale from 1 to 5 and comments

1-5 and comments
* How easy was it to use the web console? 1-5 and comments
* How easy was it to use the mobile application? 1-5 and comments

The feedback will be used to improve the user interface and the user experience.

The methodology of TDD (Test Driven Development) in its relaxed form will be used for the development of this project. In its pure form, TDD requires writing tests before writing the code and then writing the code to pass the tests. The downside of this approach is that it requires a lot of context switching between writing tests and writing code, and overhead of writing tests for every single unit of code, which can be counterproductive. The relaxed form of TDD, on the other hand, emphasizes the importance of writing tests when it speeds up the development process. For example, it will be beneficial to write tests for the motion detection module to have a set of sample video clips with and without motion to efficiently test the module and not have to manually record the video clips every time.

The final evaluation will involve implementing an evaluation scenario with described steps and expected outcomes. The evaluation scenario will be performed by the developer and the potential users. The evaluation will be performed by testing the system on multiple cameras and assessing the overall performance and quality of the system.

## Feature Prototype

Two features of the system that are considered to be the most challenging and crucial for the project are the streaming module and the motion detection module. To reduce the risk of failure, these features should be implemented first at lest in their minimal form. The aim of this prototype is to assess the feasibility of the project and to identify the most suitable approaches for implementing these features.

The first prototype was implemented as an agent that provides a basic web console with a live video feed from a single camera and a basic motion detection functionality. The agent is implemented as a Flask application that runs on a local server with a connected camera. The agent uses the OpenCV library to connect to the camera and fetch the video stream as discrete frames. These frames are then processed by the motion detection module, which uses a simple background subtraction algorithm to detect motion in the video stream. When the motion is detected, the agent displays a bounding box around the moving object and saves the video clip of the event on the disk.

During the development of this prototype, it was found that the basic variant of live video streaming using the Flask application is to provide an endpoint that returns a continuous stream of frames as JPEG images. The client displays these images as a video. This approach is far simpler than using the streaming protocols, such as HLS, but has limitations in terms of network overhead and latency. But for the purpose of this prototype, it was found to be sufficient.

## References
[1] Hussien, H.M., Meko, S.F., Teshale, N.B. 2018. Comparative Analysis of Moving Object Detection Algorithms. Lecture Notes of the Institute for Computer Sciences, Social Informatics and Telecommunications Engineering, vol 244. Springer, Cham. Retrieved from https://doi.org/10.1007/978-3-319-95153-9_16.
[2] Wenyu Lv, Yian Zhao, Shangliang Xu, Jinman Wei, Guanzhong Wang, Cheng Cui, Yuning Du, Qingqing Dang, Yi Liu. 2023. DETRs Beat YOLOs on Real-time Object Detection. arXiv:2304.08069. Retrieved from https://arxiv.org/abs/2304.08069.
[3] Tsung-Yi Lin, Michael Maire, Serge Belongie, Lubomir Bourdev, Ross Girshick, James Hays, Pietro Perona, Deva Ramanan, C. Lawrence Zitnick, Piotr Dollár. 2014. Microsoft COCO: Common Objects in Context. arXiv:1405.0312. Retrieved from https://arxiv.org/abs/1405.0312.
[4] Olga Russakovsky, Jia Deng, Hao Su, Jonathan Krause, Sanjeev Satheesh, Sean Ma, Zhiheng Huang, Andrej Karpathy, Aditya Khosla, Michael Bernstein, Alexander C. Berg, Li Fei-Fei. 2014. ImageNet Large Scale Visual Recognition Challenge. arXiv:1409.0575. Retrieved from https://arxiv.org/abs/1409.0575.
[5] Joseph Redmon, Santosh Divvala, Ross Girshick, Ali Farhadi. 2015. You Only Look Once: Unified, Real-Time Object Detection. arXiv:1506.02640. Retrieved from https://arxiv.org/abs/1506.02640.
[6] Nicolas Carion, Francisco Massa, Gabriel Synnaeve, Nicolas Usunier, Alexander Kirillov, Sergey Zagoruyko. 2020. End-to-End Object Detection with Transformers. arXiv:2005.12872. Retrieved from https://arxiv.org/abs/2005.12872.
[7] Muzammal Naseer, Kanchana Ranasinghe, Salman Khan, Munawar Hayat, Fahad Shahbaz Khan, Ming-Hsuan Yang. 2021. Intriguing Properties of Vision Transformers. arXiv:2105.10497. Retrieved from https://arxiv.org/abs/2105.10497.
[8] M. Ozan Tezcan, Prakash Ishwar, Janusz Konrad. 2019. BSUV-Net: A Fully-Convolutional Neural Network for Background Subtraction of Unseen Videos. arXiv:1907.11371. Retrieved from https://arxiv.org/abs/1907.11371.
[9] M. Ozan Tezcan, Prakash Ishwar, Janusz Konrad. 2021. BSUV-Net 2.0: Spatio-Temporal Data Augmentations for Video-Agnostic Supervised Background Subtraction. arXiv:2101.09585. Retrieved from https://arxiv.org/abs/2101.09585.
[10] Max Wilbert. 2023. Video Streaming Protocols: 6 Preferred Formats for Professional Broadcasting. Retrieved from https://www.dacast.com/blog/video-streaming-protocol/.
