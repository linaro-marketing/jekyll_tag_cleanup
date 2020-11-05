---
author: lee.jones
category: blog
date: '2019-09-26 01:00:00'
image: /assets/images/content/porting-linux-featured-image.jpg
layout: post
tags:
- Arm
- Linux
- Open Source
- Collaborative Engineering
- AArch64
- Porting
title: Porting Linux to AArch64 Laptops
---

As the AArch64 Laptops collaboration between Linaro and Arm is wrapping up, we felt it would be helpful to summarise the project and take a quick victory lap.

Since late last year, on and off, we have been trying to find specification compliant methods of booting Linux distributions on a series of laptops based on various Qualcomm Snapdragon System-on-Chips (SoC). These laptops left the factory running a bespoke version of Windows 10 called Windows on Snapdragon. Our brief was to try and "fix" them to run mainline Linux as well.

The beginning of the project saw us gather together a bunch of laptops based on the Snapdragon 835. Which, in no particular (okay, maybe alphabetical) order were; ASUS NovaGo TP370QL, HP Envy x2 and Lenovo Mixx 630. The laptops implement UEFI support so we disabled Secure Boot, inserted a bootable SD card containing Grub for AArch64 and ... nothing. No error message. Not a sausage! Just a black screen. Thankfully, after a long period of head scratching some bright soul discovered that a bug in the firmware requires the bootable binary, Grub in this case, to be compiled 4k aligned for the firmware to take any notice of it. What we saw (or were not seeing) was UEFI Boot Services rejecting Grub as a viable binary.

Now in the possession of a working bootloader we were able to take advantage of the upstreaming effort undertaken by the Linaro Qualcomm Landing Team and Qualcomm themselves to boot into a Linux initramfs. This was a real turning point and marked the transition from a skunk-works task into a worthy and notable project in its own right.

Once we knew it was possible to boot Linux on these devices, the project ramped up and a public repository was created on GitHub called AArch64-Laptops (https://github.com/aarch64-laptops/build). Here we provided a build system for creating pre-built images based on Ubuntu. We also provided documentation describing how to disable Secure Boot on each device, how to build images and get them booted via the SD card. After the project had matured, the GitHub project was used store HOWTOs on the GPU and WiFi stacks and some troubleshooting information for good measure. A community was cultivated surrounding the project. Users submitted bugs & questions and discussed technical topics on the IRC channel (aarch64-laptops @ Freenode) and mailing list (https://lists.linaro.org/mailman/listinfo/aarch64-laptops).

News of the project spread fast, mainly due to the exposure provided by various popular online technical journals and blogs; Liliputing ([https://liliputing.com/2019/02/now-you-can-run-linux-on-some-arm-laptops-designed-for-windows-10-on-arm.html](https://liliputing.com/2019/02/now-you-can-run-linux-on-some-arm-laptops-designed-for-windows-10-on-arm.html)), Phoronix ([https://www.phoronix.com/scan.php?page=news_item&px=Linux-On-The-Win-Arm-Laptops](https://www.phoronix.com/scan.php?page=news_item&px=Linux-On-The-Win-Arm-Laptops)), Foss Bytes ([https://fossbytes.com/linux-on-windows-10-arm-laptops-project/](https://fossbytes.com/linux-on-windows-10-arm-laptops-project/)) and Tech Republic ([https://www.techrepublic.com/article/open-source-project-aims-to-make-ubuntu-usable-on-arm-powered-windows-laptops/](https://www.techrepublic.com/article/open-source-project-aims-to-make-ubuntu-usable-on-arm-powered-windows-laptops/)), to name but a few. It is likely that many of the current owners bought their hardware on the back of the apparent early successes of the project.

The project subsequently spent quite a bit of time enabling features; Graphics, USB, core Wireless support, UFS (on-board storage), etc and fixing bugs; SD card detect line inversion, touchpad, keyboard, graphics, MMU (efi=novamap [thank you Ard Biesheuvel) and adding documentation whenever necessary. Once we were able to boot into an Ubuntu Desktop, an automatic Docker/Libvirt based (Libvirt virtual machine inside a Docker container) building infrastructure was built to create new images as they became more featureful and more stable. We utilised the power of PPAs (Personal Package Archives) to keep the user's kernel up-do-date with the latest features and Canonical were kind enough to allow us to distribute test images on Linaro's Release site ([http://releases.linaro.org/aarch64-laptops](http://releases.linaro.org/aarch64-laptops)).

After a very productive and engaging meeting with representatives from; Linaro, Arm and Qualcomm at Connect BKK19, the project began to focus more on the newly released Lenovo Yoga C630, which featured an upgraded Snapdragon 850. Fortunately, Bjorn Andersson from the Linaro Qualcomm Landing Team had been in possession of one of these for a while and was last seen running a bespoke version of Arch Linux. Qualcomm was kind enough to permit Jeff Hugo and Bjorn to contribute towards the project in their spare time. Both were a great help to the project and continue to be active in the community to this day.

An attempt was made to reach out to some of the more well known companies offering Linux distributions, with varying degrees of success. Dimitri John Ledkov from Canonical was particularly helpful, volunteering his own time and technical prowess to create an intuitive installer, based on our kernel images and bootloader, which allows users to install Ubuntu onto UFS (on-board storage). He has also been actively upstreaming kernel patches which did not make Linux v5.3 (the expected kernel release for Eoan 19.10) into the Ubuntu kernel.

Some distributions refused point-blank to support these laptops using Device Tree (the primary and most featureful method of booting these devices), whether they were upstream or not. So we investigated other methods of booting off-the-shelf distro installers. Leif Lindholm and myself worked on a DTBLoader EFI module which offered up a previously saved, known working DTB in the case where one was not present (i.e. when booting distro installers lacking DTBs). Leif was a great help in this endeavour. The other option available to us was to enable ACPI. A potentially daunting task with a great many people expecting a booting solution to be many engineering-months of effort and with some expecting the task to be impossible without direct assistance from Qualcomm and/or Microsoft. Despite the expected difficulties, from Linux v5.4 it will be possible to boot to a Ubuntu Desktop utilising ACPI alone. It's not as featureful as the DT solution, not by a long shot, but it should help users to at least install a Linux Distro and switch over to booting with DT for subsequent boots.

One thing worth mentioning, before everyone goes out and purchases one of these devices (since they are a great platform to develop ARM-on-ARM and the like), there is still a little niggle with the on-board WiFi. It has been seen working, but it has a habit of restarting the machine. Particularly when running a GUI (X and Wayland). This is something Bjorn is currently working on and trying to understand. He’s been lobbying for information, but to no avail, yet! Once WiFi is up and running, this will be an outstanding little laptop. A few of us have mentioned switching to it as our daily driver (since it even has a really nice keyboard, which is unusual).

Apologies if you have contributed to this project and you have not been mentioned. There were so many very helpful people who took time out of their own lives to be a part of this project, it would be difficult to name everyone involved.

In closing, this project has been a great success. We've come a long way since the beginning and have developed a very usable platform, whether you are a core developer or more of a web surfer. To have a laptop of this calibre running ARMv8 and Linux on my desk is a delight. Hopefully we can fix the niggles and you will see them popping up on ARM and Linaro engineer's laps sometime soon.