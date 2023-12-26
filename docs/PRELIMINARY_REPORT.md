# Final Project
## Preliminary Report


## Introduction

This project preliminary report introduces a new software aimed to provide a self-hosted camera surveillance solution for home users. The idea of this project is based on a provided “Camera Surveillance System” template. The motivation behind this project is to devise a surveillance system that will be as efficient and convenient as the commercial cloud services but provide the security and privacy of the local self-hosted solutions.

Currently, my smart home setup consists of a few security cameras, including XIAOMI MI home security camera for indoor monitoring and an Arlo Video Doorbell for outdoor surveillance. These cameras are integrated with proprietary subscription-based cloud services, offering the convenience of remote access to live view and recordings through mobile applications from anywhere in the world.

They also provide a set of most common features such as motion detection to detect particular events of interest and distinguish it from the background noise. And push notifications to alert users about these events when they are away from home. These features are implemented using computer vision algorithms that are able to detect and recognize objects in the video stream. A user can configure the system to have different sensitivity levels, or to detect only particular objects, such as people, cars, or animals.

Despite their utility, these commercial surveillance solutions exhibit significant drawbacks. Firstly, the pricing model is usually based on the number of cameras and the number of days of video storage. The cost of these services can escalate quickly, especially with an increased number of cameras and extended video storage requirements. Secondly, and more crucially, the processing of a live stream and storage of recordings on private clouds, often in unknown jurisdiction, raises serious privacy concerns. A number of leaks and hacks of these cloud services have been reported in the past and some of the vendors have been even accused of spying on their customers. Moreover, IoT devices are known to be vulnerable to cyber attacks due to the short support life cycle and the lack of security updates.

In light of these challenges, an alternative solution that can be installed on a local server with connected cameras and storage is proposed. There is an abundance of free open source software that can be used to build camera surveillance systems using a local storage, such as Kerberos, Motion, Shinobi, ZoneMinder, and many others. Even entire operating systems MotionEyeOS is dedicated to this single purpose. However, these systems usually rely on web interfaces and lack the user-friendly aspect of mobile apps. Additionally, their setup often requires technical expertise, as evidenced by the common recommendation to use Docker or Docker Compose for installation, making them less accessible to the average user.

This project aims to bridge the gap between the user-friendly nature of commercial cloud services and the security and cost-effectiveness of local storage solutions. The proposed system will be a free, open-source software, suitable for operation on home servers or Raspberry Pi devices. It will offer standard features such as recording, live video streaming, motion detection, AI-based object identification and event-based notifications.

The distinguishing feature of this project is its ease of installation and use, especially for non-technical users. The system is envisaged to be deployable as a single binary file or a pip package, compatible with any Unix system, and will not necessitate the use of advanced software like Docker.

A significant innovation will be the development of a user-friendly mobile application, providing convenient access to live video feeds and recordings. This contrasts with the reliance on web interfaces in existing open-source solutions and is particularly advantageous for users needing remote access via smartphones. Thus, this project represents a significant step forward in home surveillance technology, addressing both the functional and security concerns prevalent in current systems.





## Design

## Feature Prototype

## References

